"""E5 authoring: preserve the visible present and choose a future glyph."""

from .artifacts import summarize_e5, write_e5_result
from .experiment import run_molecular_time_machine_e5
from .models import (
    E5Metrics,
    FutureOutcomeMetrics,
    FutureTarget,
    MolecularTimeMachineE5Result,
    PivotReplayAudit,
    ResolvedPresentAudit,
    SurgeryPreview,
    VelocityOwnershipSurgery,
)
from .protocol import MolecularTimeMachineE5Protocol, load_e5_protocol
from .surgery import apply_velocity_ownership_surgery, enumerate_target_surgeries

__all__ = [
    "E5Metrics",
    "FutureOutcomeMetrics",
    "FutureTarget",
    "MolecularTimeMachineE5Protocol",
    "MolecularTimeMachineE5Result",
    "PivotReplayAudit",
    "ResolvedPresentAudit",
    "SurgeryPreview",
    "VelocityOwnershipSurgery",
    "apply_velocity_ownership_surgery",
    "enumerate_target_surgeries",
    "load_e5_protocol",
    "run_molecular_time_machine_e5",
    "summarize_e5",
    "write_e5_result",
]
