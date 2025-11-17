from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Iterable


class AircraftType(Enum):
    A380 = "Airbus A380"
    B747 = "Boeing 747"
    GENERIC = "Generic"


class PanelSection(Enum):
    OVERHEAD = "overhead"
    MAIN = "main"
    CENTER = "center"
    PEDESTAL = "pedestal"


@dataclass(frozen=True)
class ControlDescriptor:
    """Metadata for an interactive cockpit control."""

    control_id: str
    label: str
    section: PanelSection
    control_type: str
    detents: tuple[str, ...] | None = None
    guarded: bool = False


@dataclass(frozen=True)
class AircraftSystems:
    avionics: tuple[str, ...]
    navigation: tuple[str, ...]
    autoflight: tuple[str, ...]
    electrical: tuple[str, ...]
    hydraulics: tuple[str, ...]
    fuel: tuple[str, ...]
    environmental: tuple[str, ...]
    warnings: tuple[str, ...]


@dataclass
class Aircraft:
    """Data definition for a supported aircraft."""

    name: str
    type: AircraftType
    cockpit_controls: list[ControlDescriptor] = field(default_factory=list)
    systems: AircraftSystems | None = None

    def add_control(self, control: ControlDescriptor) -> None:
        self.cockpit_controls.append(control)

    def controls_in_section(self, section: PanelSection) -> Iterable[ControlDescriptor]:
        return (control for control in self.cockpit_controls if control.section == section)


def predefined_aircraft() -> list[Aircraft]:
    """Bootstrap default aircraft with rich cockpit definitions."""

    a380 = Aircraft(
        name="Airbus A380",
        type=AircraftType.A380,
        systems=AircraftSystems(
            avionics=("FMGC", "EFIS", "RADIO"),
            navigation=("IRS", "GNSS", "ILS", "VOR"),
            autoflight=("Autopilot", "Autothrust", "Flight Director"),
            electrical=("IDG", "APU GEN", "EXT PWR"),
            hydraulics=("Green", "Blue", "Yellow"),
            fuel=("Inner", "Outer", "Trim", "Center", "Transfer"),
            environmental=("Packs", "Bleed", "Pressurization"),
            warnings=("ECAM", "GPWS", "TCAS"),
        ),
    )
    a380.add_control(
        ControlDescriptor(
            control_id="ap_master",
            label="AP1",
            section=PanelSection.MAIN,
            control_type="push_button",
        )
    )
    a380.add_control(
        ControlDescriptor(
            control_id="efis_range",
            label="ND Range",
            section=PanelSection.MAIN,
            control_type="rotary",
            detents=("10", "20", "40", "80", "160", "320"),
        )
    )
    a380.add_control(
        ControlDescriptor(
            control_id="battery_master",
            label="BAT",
            section=PanelSection.OVERHEAD,
            control_type="toggle",
            guarded=True,
        )
    )

    b747 = Aircraft(
        name="Boeing 747",
        type=AircraftType.B747,
        systems=AircraftSystems(
            avionics=("FMC", "EFIS", "RADIO"),
            navigation=("IRS", "GNSS", "ILS", "VOR"),
            autoflight=("Autopilot", "Autothrottle", "Flight Director"),
            electrical=("IDG", "APU GEN", "EXT PWR"),
            hydraulics=("Sys1", "Sys2", "Sys3", "Sys4"),
            fuel=("Main1", "Main2", "Main3", "Main4", "Center", "Stab"),
            environmental=("Packs", "Bleed", "Pressurization"),
            warnings=("EICAS", "GPWS", "TCAS"),
        ),
    )
    b747.add_control(
        ControlDescriptor(
            control_id="yaw_damper",
            label="Yaw Damper",
            section=PanelSection.OVERHEAD,
            control_type="toggle",
        )
    )
    b747.add_control(
        ControlDescriptor(
            control_id="flt_dir_left",
            label="FD L",
            section=PanelSection.MAIN,
            control_type="toggle",
        )
    )
    b747.add_control(
        ControlDescriptor(
            control_id="autobrake",
            label="Autobrake",
            section=PanelSection.CENTER,
            control_type="rotary",
            detents=("RTO", "OFF", "1", "2", "3", "4"),
        )
    )

    return [a380, b747]
