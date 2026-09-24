from pathlib import Path


def create_artifact(source: Path, output: Path) -> None:
    text = source.read_text(encoding="utf-8")
    temporary = output.with_suffix(output.suffix + ".tmp")
    temporary.write_text(text, encoding="utf-8")
    temporary.replace(output)
