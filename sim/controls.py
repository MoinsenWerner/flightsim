from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Iterable, NamedTuple

from .platform import Platform


class DeviceType(Enum):
    KEYBOARD = "keyboard"
    MOUSE_BUTTON = "mouse_button"
    MOUSE_AXIS = "mouse_axis"
    GAMEPAD = "gamepad"
    TOUCH = "touch"
    GYRO = "gyro"


class InputSpec(NamedTuple):
    device: DeviceType
    code: str
    scale: float = 1.0


@dataclass
class ActionBinding:
    """Mapping between a logical action and one or more physical inputs."""

    action: str
    inputs: list[InputSpec] = field(default_factory=list)

    def add_input(self, spec: InputSpec) -> None:
        if spec not in self.inputs:
            self.inputs.append(spec)

    def remove_input(self, spec: InputSpec) -> None:
        self.inputs = [existing for existing in self.inputs if existing != spec]


@dataclass
class ControlProfile:
    """A platform-aware set of bindings for simulator actions."""

    name: str
    platform: Platform
    bindings: dict[str, ActionBinding] = field(default_factory=dict)

    def bind(self, action: str, spec: InputSpec) -> None:
        binding = self.bindings.setdefault(action, ActionBinding(action=action))
        binding.add_input(spec)

    def unbind(self, action: str, spec: InputSpec) -> None:
        if action in self.bindings:
            self.bindings[action].remove_input(spec)
            if not self.bindings[action].inputs:
                del self.bindings[action]

    def actions_for_device(self, device: DeviceType) -> Iterable[ActionBinding]:
        return (
            binding
            for binding in self.bindings.values()
            if any(spec.device == device for spec in binding.inputs)
        )


def default_desktop_profile() -> ControlProfile:
    profile = ControlProfile(name="desktop_default", platform=Platform.LINUX)
    profile.bind("pitch_up", InputSpec(device=DeviceType.MOUSE_AXIS, code="y-", scale=0.5))
    profile.bind("pitch_down", InputSpec(device=DeviceType.MOUSE_AXIS, code="y+", scale=0.5))
    profile.bind("roll_left", InputSpec(device=DeviceType.MOUSE_AXIS, code="x-", scale=0.5))
    profile.bind("roll_right", InputSpec(device=DeviceType.MOUSE_AXIS, code="x+", scale=0.5))
    profile.bind("throttle_increase", InputSpec(device=DeviceType.KEYBOARD, code="E"))
    profile.bind("throttle_decrease", InputSpec(device=DeviceType.KEYBOARD, code="Q"))
    profile.bind("toggle_ap", InputSpec(device=DeviceType.MOUSE_BUTTON, code="left"))
    profile.bind("toggle_atc_menu", InputSpec(device=DeviceType.KEYBOARD, code="F12"))
    return profile


def default_android_profile() -> ControlProfile:
    profile = ControlProfile(name="android_default", platform=Platform.ANDROID)
    profile.bind("pitch_up", InputSpec(device=DeviceType.GYRO, code="pitch_up", scale=1.0))
    profile.bind("pitch_down", InputSpec(device=DeviceType.GYRO, code="pitch_down", scale=1.0))
    profile.bind("roll_left", InputSpec(device=DeviceType.GYRO, code="roll_left", scale=1.0))
    profile.bind("roll_right", InputSpec(device=DeviceType.GYRO, code="roll_right", scale=1.0))
    profile.bind("toggle_ap", InputSpec(device=DeviceType.TOUCH, code="tap_ap_button"))
    profile.bind("toggle_atc_menu", InputSpec(device=DeviceType.TOUCH, code="tap_atc_button"))
    profile.bind("throttle_increase", InputSpec(device=DeviceType.TOUCH, code="swipe_up", scale=0.8))
    profile.bind("throttle_decrease", InputSpec(device=DeviceType.TOUCH, code="swipe_down", scale=0.8))
    return profile
