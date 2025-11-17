# FlightSim Architecture Proposal

This document outlines a cockpit-centric flight simulator blueprint that targets Linux, Windows (installer packaging), and Android (APK packaging). The emphasis is on full cockpit interactivity, realistic systems, and flexible control input across mouse/keyboard, touch, and optional gyroscope support on Android.

## Core Tenets
- **Round-trip cockpit visibility:** Every supported aircraft exposes overhead, center pedestal, and main instrument panels within a 360° cockpit camera. Panels are spatially accurate to the aircraft layout.
- **Full switchability:** All cockpit controls (switches, knobs, potentiometers, annunciators, selectors, guards) are modeled as stateful components that feed downstream systems, mirroring real-world behavior.
- **System fidelity:** Aircraft definitions list avionics, navigation, autoflight, warning, electrical, hydraulic, fuel, pneumatic, environmental, and flight control systems. Each system can subscribe to cockpit component changes and simulation state.
- **Configurable controls:** A single action can be bound to multiple input sources, including mouse buttons/wheel, keyboard keys, gamepads, touch gestures, and mobile gyroscope channels for pitch/roll.
- **Platform packaging:** Core logic stays platform-agnostic; build scripts wrap the engine for Windows installers and Android APKs. Input adapters are swappable per platform.
- **Realistic world data:** Airport areas (runways, taxiways, gates, lighting) are prioritized for mesh and texture detail; broader terrain streams lower-detail data for performance.
- **Simulated ATC:** A radio subsystem exposes frequency management, audio routing, scripted/AI ATC behavior, and traffic/ground service interactions.

## Module Overview
- `sim/aircraft.py` — Data definitions for aircraft, cockpits, and systems; supports multiple widebody types such as the Airbus A380 and Boeing 747.
- `sim/controls.py` — Input/action abstraction with multi-binding support and per-platform adapters (mouse/keyboard, touch, gyroscope).
- `sim/config.py` — High-level simulation configuration (target platforms, rendering tiers, airport detail budgets) and factory helpers.
- `sim/platform.py` — Build target enumeration and platform capability flags to gate features at compile/runtime.

## Cockpit Interaction Model
1. **Camera:** A 6-DOF cockpit camera allows head movement and rotation to line up controls. VR head tracking hooks can be layered later without changing interaction contracts.
2. **Hit-testing:** Cockpit meshes expose colliders tagged with control IDs. Mouse/touch rays identify the control, then send the interaction event to the control system.
3. **Control states:** Each control tracks state (on/off, guarded, detent position, rotary value). State changes emit events consumed by systems (e.g., IRS alignment, fuel pump activation, autopilot mode changes).
4. **Feedback:** Control state drives annunciators, instrument updates, and aural warnings. Detents, latching switches, and rotary encoders are modeled via control metadata.

## Control Binding Strategy
- **Actions:** Canonical actions (e.g., `aileron_left`, `pitch_up`, `ap_toggle`, `com1_frequency_inc`) are declared centrally.
- **Bindings:** Each action can map to multiple inputs. Inputs describe device type, code, modifiers, and optional scaling curves (for analog axes like mouse wheel or gyro pitch).
- **Profiles:** Saveable profiles target different platforms (desktop, gamepad-heavy, Android touch/gyro). Loading a profile repopulates bindings without code changes.
- **Touch/Gyro:** On Android, a touch adapter maps gestures/tappable overlays to actions; a gyro adapter exposes pitch/roll channels for elevators/ailerons.

## Systems and Avionics
- **Electrical:** AC/DC buses, transformers, IDGs, APU generators, battery relays, and load shedding that gate avionics availability.
- **Hydraulics:** Engine/APU/elec pumps, accumulators, and pressure-driven surfaces (flaps, gear, brakes) tied to cockpit controls.
- **Fuel:** Tanks, crossfeed, pumps, and transfer logic that affect engine supply and weight/balance.
- **Flight controls:** Control laws per aircraft, fly-by-wire modes, envelope protection, trim, spoilers, and speedbrakes.
- **Avionics & navigation:** FMC/MCDU, IRS, GNSS, VOR/ILS, FMS lateral/vertical guidance, autoflight modes (LNAV/VNAV, managed/selected), TCAS, EGPWS.
- **Environment:** Weather layers, winds, turbulence, and icing feed sensor and aerodynamic models.

## World and Airport Detail
- **Data tiers:** Global terrain streams at medium detail. Airports allocate higher poly budgets, accurate markings, taxiway signs, PAPI/VASI, and gate layouts.
- **Lighting:** Dynamic runway/taxiway lighting with LOD transitions. Configurable day/night/low-visibility scenarios.

## Audio and ATC
- **Radio stack:** COM/NAV radios with frequency management and audio mixing. ATIS/ground/tower/center frequencies are scriptable.
- **ATC logic:** Phraseology-aware scripts for VFR/IFR flows, SID/STAR handling, traffic advisories, and pushback/ground service coordination.

## Build and Platform Notes
- **Linux:** Primary development target. Uses native window/input and full simulator feature set.
- **Windows:** Packaged via installer; uses the same rendering/input stack with Win32 device adapters.
- **Android:** Uses touch/gyro adapters and mobile-friendly UI overlays. Performance presets dial back mesh/texture sizes outside airports.

## Next Steps
- Implement data-driven aircraft definitions using the `Aircraft` dataclass as a backbone.
- Flesh out system simulation services and connect them to control state events.
- Integrate a rendering/input engine (e.g., Godot/Unreal/Unity or a custom renderer) behind the platform adapters.
- Add persistence for control profiles and per-aircraft avionics states.
