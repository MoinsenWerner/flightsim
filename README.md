# FlightSim

A modular flight simulator concept targeting Linux builds that can also be packaged for Windows and Android. The project documentation outlines a cockpit-first approach with fully interactive panels, configurable input bindings (mouse, keyboard, touch, and gyroscope), avionics system simulation, and realistic world rendering priorities.

## Goals
- Support multiple widebody and narrowbody airliners (e.g., Airbus A380, Boeing 747) with cockpit round-trip visibility and fully interactive overhead, center, and main panels.
- Provide system fidelity across avionics, navigation, autoflight, warning, electrical, hydraulic, fuel, and environmental systems.
- Allow complete control remapping, including multi-binding per function and touch/gyro options on Android.
- Deliver realistic air traffic control (ATC) radio simulations and dense airport detail relative to broader world rendering.
- Enable cross-platform build targets: native Linux development, Windows installers, and Android APK packaging.

See `docs/design.md` for the current architecture proposal and `sim/` for the initial scaffolding used to prototype control mappings and aircraft/system descriptions.

## Next Steps
- Implement data-driven aircraft definitions using the `Aircraft` dataclass as a backbone.
- Flesh out system simulation services and connect them to control state events.
- Integrate a rendering/input engine (e.g., Godot/Unreal/Unity or a custom renderer) behind the platform adapters.
- Add persistence for control profiles and per-aircraft avionics states.
