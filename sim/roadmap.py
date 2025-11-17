"""Programmatic access to the README Next Steps roadmap.

These entries mirror the "Next Steps" section in the root README so
upstream tools can reason about upcoming milestones directly from code.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import List


@dataclass(frozen=True)
class NextStep:
    """Represents a planned milestone pulled from the README."""

    summary: str
    focus_area: str
    detail: str


def _build_next_steps() -> List[NextStep]:
    return [
        NextStep(
            summary="Implement data-driven aircraft definitions",
            focus_area="aircraft",
            detail=(
                "Use the Aircraft dataclass backbone to load panel layout, "
                "systems, and control bindings from external definitions."
            ),
        ),
        NextStep(
            summary="Flesh out system simulation services",
            focus_area="systems",
            detail=(
                "Model avionics, autoflight, electrical, hydraulic, fuel, "
                "and warning behaviors and wire them to control events."
            ),
        ),
        NextStep(
            summary="Integrate rendering and input engine",
            focus_area="platform",
            detail=(
                "Attach a rendering/input runtime (e.g., Godot/Unreal/Unity) "
                "behind the platform adapters to drive visuals and controls."
            ),
        ),
        NextStep(
            summary="Add persistence for profiles and avionics state",
            focus_area="persistence",
            detail=(
                "Store control profiles and per-aircraft avionics snapshots "
                "so sessions can restore bindings and system configurations."
            ),
        ),
    ]


def get_next_steps() -> List[NextStep]:
    """Return the roadmap entries mirrored from the README."""

    return list(_build_next_steps())
