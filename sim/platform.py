from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class Platform(Enum):
    """Supported build targets."""

    LINUX = "linux"
    WINDOWS = "windows"
    ANDROID = "android"


@dataclass(frozen=True)
class PlatformCapabilities:
    """Features exposed on a target platform."""

    supports_mouse: bool
    supports_keyboard: bool
    supports_touch: bool
    supports_gyro: bool


PLATFORM_CAPABILITIES: dict[Platform, PlatformCapabilities] = {
    Platform.LINUX: PlatformCapabilities(
        supports_mouse=True,
        supports_keyboard=True,
        supports_touch=False,
        supports_gyro=False,
    ),
    Platform.WINDOWS: PlatformCapabilities(
        supports_mouse=True,
        supports_keyboard=True,
        supports_touch=False,
        supports_gyro=False,
    ),
    Platform.ANDROID: PlatformCapabilities(
        supports_mouse=False,
        supports_keyboard=False,
        supports_touch=True,
        supports_gyro=True,
    ),
}


def platform_supports(platform: Platform, *, gyro: bool = False, touch: bool = False) -> bool:
    """Check whether a platform offers required input channels."""

    capabilities = PLATFORM_CAPABILITIES[platform]
    if gyro and not capabilities.supports_gyro:
        return False
    if touch and not capabilities.supports_touch:
        return False
    return True
