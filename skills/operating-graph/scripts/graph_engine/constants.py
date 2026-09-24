"""Closed value sets and shared constants for Operating Graph records."""

from __future__ import annotations

from enum import Enum
from typing import FrozenSet, Tuple


SCHEMA_VERSION = "1.0"


class NodeKind(str, Enum):
    AUTHORITY = "authority"
    CONTROLLER = "controller"
    WORKER = "worker"
    STATE = "state"
    EVALUATOR = "evaluator"
    DISTRIBUTOR = "distributor"
    SIGNAL = "signal"


class ExecutionMode(str, Enum):
    INLINE = "inline"
    SUBAGENT = "subagent"
    TOOL = "tool"
    HUMAN = "human"


class EdgeKind(str, Enum):
    GOAL = "goal"
    ASSIGN = "assign"
    READ = "read"
    WRITE = "write"
    VERIFY = "verify"
    APPROVE = "approve"
    PUBLISH = "publish"
    MEASURE = "measure"
    ESCALATE = "escalate"
    LEARN = "learn"


class Temporal(str, Enum):
    SAME_EPOCH = "same_epoch"
    NEXT_EPOCH = "next_epoch"


class ActivationMode(str, Enum):
    ALL = "all"
    ANY = "any"


class NodeStatus(str, Enum):
    PENDING = "pending"
    READY = "ready"
    RUNNING = "running"
    BLOCKED = "blocked"
    SUCCEEDED = "succeeded"
    FAILED = "failed"
    SKIPPED = "skipped"
    CANCELLED = "cancelled"


class RunStatus(str, Enum):
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class EventType(str, Enum):
    GRAPH_CREATED = "graph.created"
    GRAPH_VALIDATED = "graph.validated"
    RUN_STARTED = "run.started"
    NODE_READY = "node.ready"
    NODE_STARTED = "node.started"
    NODE_SUCCEEDED = "node.succeeded"
    NODE_FAILED = "node.failed"
    NODE_BLOCKED = "node.blocked"
    NODE_RETRIED = "node.retried"
    THREAD_DISPATCH_PREPARED = "thread.dispatch-prepared"
    THREAD_LAUNCHED = "thread.launched"
    THREAD_LAUNCH_FAILED = "thread.launch-failed"
    NODE_RETURN_INGESTED = "node.return-ingested"
    ARTIFACT_REGISTERED = "artifact.registered"
    ARTIFACT_INVALIDATED = "artifact.invalidated"
    APPROVAL_REQUESTED = "approval.requested"
    APPROVAL_GRANTED = "approval.granted"
    APPROVAL_DENIED = "approval.denied"
    SIGNAL_OBSERVED = "signal.observed"
    REWRITE_PROPOSED = "rewrite.proposed"
    REWRITE_APPROVED = "rewrite.approved"
    REWRITE_DENIED = "rewrite.denied"
    REWRITE_APPLIED = "rewrite.applied"
    VERIFICATION_STARTED = "verification.started"
    VERIFICATION_PASSED = "verification.passed"
    VERIFICATION_FAILED = "verification.failed"
    RUN_COMPLETED = "run.completed"
    RUN_FAILED = "run.failed"
    RUN_CANCELLED = "run.cancelled"


class Confidence(str, Enum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    UNKNOWN = "unknown"


class RiskLevel(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class ApprovalStatus(str, Enum):
    PENDING = "pending"
    GRANTED = "granted"
    DENIED = "denied"


class ApprovalSubjectType(str, Enum):
    REWRITE = "rewrite"
    EXTERNAL_ACTION = "external-action"
    ARTIFACT = "artifact"
    RESUME = "resume"


class RewriteOperationKind(str, Enum):
    ADD_NODE = "add_node"
    UPDATE_NODE = "update_node"
    DISABLE_NODE = "disable_node"
    ADD_EDGE = "add_edge"
    DISABLE_EDGE = "disable_edge"
    SET_PRIORITY = "set_priority"


class VerificationStatus(str, Enum):
    PASS = "pass"
    CONDITIONAL_PASS = "conditional-pass"
    FAIL = "fail"


NODE_STATUS_TRANSITIONS: FrozenSet[Tuple[NodeStatus, NodeStatus]] = frozenset(
    {
        (NodeStatus.PENDING, NodeStatus.READY),
        (NodeStatus.PENDING, NodeStatus.BLOCKED),
        (NodeStatus.PENDING, NodeStatus.SKIPPED),
        (NodeStatus.READY, NodeStatus.RUNNING),
        (NodeStatus.READY, NodeStatus.BLOCKED),
        (NodeStatus.RUNNING, NodeStatus.SUCCEEDED),
        (NodeStatus.RUNNING, NodeStatus.FAILED),
        (NodeStatus.RUNNING, NodeStatus.BLOCKED),
        (NodeStatus.FAILED, NodeStatus.READY),
        (NodeStatus.BLOCKED, NodeStatus.READY),
        (NodeStatus.PENDING, NodeStatus.CANCELLED),
        (NodeStatus.READY, NodeStatus.CANCELLED),
        (NodeStatus.BLOCKED, NodeStatus.CANCELLED),
    }
)
