from __future__ import annotations

from dataclasses import dataclass

from .platform import Platform, platform_supports


@dataclass(frozen=True)
class RenderingDetail:
    airports: str = "high"
    world: str = "medium"
    dynamic_lighting: bool = True


@dataclass(frozen=True)
class SimulationConfig:
    """Top-level simulator configuration."""

    platform: Platform
    rendering: RenderingDetail = RenderingDetail()
    enable_atc: bool = True
    enable_touch_ui: bool = False
    enable_gyro_controls: bool = False

    def validate(self) -> None:
        if self.enable_touch_ui and not platform_supports(self.platform, touch=True):
            raise ValueError("Touch UI requested on a platform without touch support")
        if self.enable_gyro_controls and not platform_supports(self.platform, gyro=True):
            raise ValueError("Gyro requested on a platform without gyro support")


def default_config(platform: Platform) -> SimulationConfig:
    touch = platform == Platform.ANDROID
    gyro = platform == Platform.ANDROID
    config = SimulationConfig(
        platform=platform,
        enable_touch_ui=touch,
        enable_gyro_controls=gyro,
    )
    config.validate()
    return config
