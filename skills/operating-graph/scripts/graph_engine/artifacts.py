"""Artifact provenance registration, integrity checks, and activation eligibility."""

from __future__ import annotations

from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import tempfile
from typing import Iterable, List, Optional, Sequence, Tuple

from .constants import EventType
from .events import EventStore
from .models import Artifact, Evidence


class ArtifactError(RuntimeError):
    """Base class for artifact contract failures."""


class UnsafeArtifactPathError(ArtifactError):
    """Raised when an artifact path escapes its declared ownership boundary."""


class ArtifactIntegrityError(ArtifactError):
    """Raised when registered bytes no longer match their digest."""


class ArtifactUnavailableError(ArtifactError):
    """Raised when an artifact is inactive or missing."""


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")


def resolve_artifact_path(run_directory: Path, node_id: str, relative_path: str) -> Path:
    """Resolve a declared artifact only within `artifacts/<node-id>/`."""
    if not isinstance(relative_path, str) or not relative_path:
        raise UnsafeArtifactPathError("artifact path must be a non-empty relative path")
    if any(ord(character) < 32 or ord(character) == 127 for character in relative_path):
        raise UnsafeArtifactPathError("artifact path contains control characters")
    if "\\" in relative_path:
        raise UnsafeArtifactPathError("artifact path must use POSIX separators")
    relative = PurePosixPath(relative_path)
    if relative.is_absolute() or ".." in relative.parts:
        raise UnsafeArtifactPathError("artifact path escapes the run directory")
    expected_prefix = ("artifacts", node_id)
    if len(relative.parts) < 3 or relative.parts[:2] != expected_prefix:
        raise UnsafeArtifactPathError(
            f"artifact path is outside node {node_id!r} ownership"
        )
    root = Path(run_directory).resolve()
    owner_root = (root / "artifacts" / node_id).resolve()
    candidate = (root / Path(*relative.parts)).resolve()
    try:
        candidate.relative_to(root)
        candidate.relative_to(owner_root)
    except ValueError as error:
        raise UnsafeArtifactPathError("artifact path escapes its ownership boundary") from error
    return candidate


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _atomic_replace(path: Path, content: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary_path: Optional[Path] = None
    try:
        with tempfile.NamedTemporaryFile(dir=path.parent, prefix=f".{path.name}.", delete=False) as handle:
            temporary_path = Path(handle.name)
            handle.write(content)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary_path, path)
        temporary_path = None
    finally:
        if temporary_path is not None:
            temporary_path.unlink(missing_ok=True)


class ArtifactRegistry:
    """Controller-owned append-only provenance registry for one run."""

    def __init__(
        self,
        run_directory: Path,
        run_id: str,
        event_store: EventStore,
    ) -> None:
        self.run_directory = Path(run_directory)
        self.run_id = run_id
        self.event_store = event_store
        self.path = self.run_directory / "artifacts.jsonl"

    def read_all(self) -> Tuple[Artifact, ...]:
        if not self.path.exists():
            return ()
        artifacts: List[Artifact] = []
        seen = set()
        for line_number, line in enumerate(self.path.read_text(encoding="utf-8").splitlines(), 1):
            try:
                artifact = Artifact.from_dict(json.loads(line))
            except (ValueError, TypeError, json.JSONDecodeError) as error:
                raise ArtifactIntegrityError(
                    f"invalid artifact registry record on line {line_number}: {error}"
                ) from error
            if artifact.run_id != self.run_id:
                raise ArtifactIntegrityError(
                    f"artifact {artifact.artifact_id!r} belongs to another run"
                )
            if artifact.artifact_id in seen:
                raise ArtifactIntegrityError(
                    f"duplicate artifact id {artifact.artifact_id!r}"
                )
            seen.add(artifact.artifact_id)
            artifacts.append(artifact)
        return tuple(artifacts)

    def register(
        self,
        *,
        artifact_id: str,
        node_id: str,
        graph_version: int,
        artifact_type: str,
        path: str,
        media_type: str,
        supersedes: Optional[str] = None,
        evidence: Optional[Sequence[Evidence]] = None,
        actor_node_id: str = "controller",
        timestamp: Optional[str] = None,
    ) -> Artifact:
        self.event_store.require_controller(actor_node_id)
        existing = self.read_all()
        if any(item.artifact_id == artifact_id for item in existing):
            raise ArtifactIntegrityError(f"duplicate artifact id {artifact_id!r}")
        if supersedes is not None:
            self.verify(supersedes)
        resolved = resolve_artifact_path(self.run_directory, node_id, path)
        if not resolved.is_file():
            raise ArtifactUnavailableError(f"artifact file {path!r} does not exist")
        artifact = Artifact(
            artifact_id=artifact_id,
            run_id=self.run_id,
            node_id=node_id,
            graph_version=graph_version,
            type=artifact_type,
            path=path,
            media_type=media_type,
            sha256=_sha256(resolved),
            created_at=timestamp or _utc_now(),
            supersedes=supersedes,
            evidence=list(evidence or ()),
        )
        self.event_store.append(
            EventType.ARTIFACT_REGISTERED,
            {"artifact": artifact.to_dict()},
            graph_version,
            actor_node_id=actor_node_id,
            timestamp=timestamp,
        )
        current = self.path.read_bytes() if self.path.exists() else b""
        record = (
            json.dumps(
                artifact.to_dict(),
                sort_keys=True,
                separators=(",", ":"),
                ensure_ascii=False,
                allow_nan=False,
            ).encode("utf-8")
            + b"\n"
        )
        _atomic_replace(self.path, current + record)
        return Artifact.from_dict(artifact.to_dict())

    def invalidate(
        self,
        artifact_id: str,
        *,
        reason: str,
        actor_node_id: str = "controller",
        timestamp: Optional[str] = None,
    ) -> None:
        self.event_store.require_controller(actor_node_id)
        artifact = self._get(artifact_id)
        if artifact_id in self._invalidated_ids():
            raise ArtifactUnavailableError(f"artifact {artifact_id!r} is already invalidated")
        self.event_store.append(
            EventType.ARTIFACT_INVALIDATED,
            {"artifactId": artifact_id, "reason": reason},
            artifact.graph_version,
            actor_node_id=actor_node_id,
            timestamp=timestamp,
        )

    def _get(self, artifact_id: str) -> Artifact:
        for artifact in self.read_all():
            if artifact.artifact_id == artifact_id:
                return artifact
        raise ArtifactUnavailableError(f"artifact {artifact_id!r} is not registered")

    def _invalidated_ids(self) -> set[str]:
        return {
            str(event.payload.get("artifactId"))
            for event in self.event_store.read_all()
            if event.type == EventType.ARTIFACT_INVALIDATED
            and event.payload.get("artifactId") is not None
        }

    def _superseded_ids(self) -> set[str]:
        return {
            artifact.supersedes
            for artifact in self.read_all()
            if artifact.supersedes is not None
        }

    def verify(self, artifact_id: str, *, require_active: bool = True) -> Artifact:
        artifact = self._get(artifact_id)
        if require_active and artifact_id in self._invalidated_ids():
            raise ArtifactUnavailableError(f"artifact {artifact_id!r} is invalidated")
        if require_active and artifact_id in self._superseded_ids():
            raise ArtifactUnavailableError(f"artifact {artifact_id!r} is superseded")
        resolved = resolve_artifact_path(
            self.run_directory, artifact.node_id, artifact.path
        )
        if not resolved.is_file():
            raise ArtifactUnavailableError(f"artifact file {artifact.path!r} is missing")
        if _sha256(resolved) != artifact.sha256:
            raise ArtifactIntegrityError(
                f"artifact {artifact_id!r} SHA-256 mismatch"
            )
        return Artifact.from_dict(artifact.to_dict())

    def active_artifacts(self, artifact_type: Optional[str] = None) -> Tuple[Artifact, ...]:
        active = []
        for artifact in self.read_all():
            if artifact_type is not None and artifact.type != artifact_type:
                continue
            try:
                active.append(self.verify(artifact.artifact_id))
            except ArtifactError:
                continue
        return tuple(active)

    def satisfies_activation(self, required_types: Iterable[str]) -> bool:
        return all(self.active_artifacts(artifact_type) for artifact_type in required_types)


__all__ = [
    "ArtifactError",
    "ArtifactIntegrityError",
    "ArtifactRegistry",
    "ArtifactUnavailableError",
    "UnsafeArtifactPathError",
    "resolve_artifact_path",
]
