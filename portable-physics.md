# Portable Physics For Architectural Thermal Reasoning

This file collects the small equations and physical ideas that should travel through the course.

The aim is not to turn the course into a thermodynamics problem set. The aim is to give students portable equations that produce maps, sections, time-series, thresholds, and design decisions.

## Core Rule

Every equation must answer:

> What does this change in the way I read or design the space?

## Spatial Air Field

Use in A1.

```text
ΔT = T_position B - T_position A
```

Architectural use:

- compare perimeter and core
- compare indoor and threshold condition
- compare shaded and exposed positions
- show whether one "room temperature" claim hides spatial difference

Humidity reminder:

```text
same T_air + different RH = different thermal stress and evaporation potential
```

Architectural use:

- distinguish hot-dry and hot-humid conditions
- show why air temperature alone is not enough in Hong Kong

## Radiant Exchange

Use in A2.

Simplified radiant heat exchange:

```text
q_rad ≈ h_r A (T_surface - T_body)
```

Conceptual use:

- warm surfaces add radiant load to the body
- cold surfaces increase radiant heat loss
- body position and orientation matter
- a surface can matter even when air temperature is unchanged

Mean radiant temperature:

```text
T_mrt = the uniform surrounding temperature that would produce the same radiant exchange
```

Operative temperature, simplified:

```text
T_op ≈ weighted combination of T_air and T_mrt
```

Architectural use:

- compare window seat and interior seat
- compare sun and shade
- explain why surface temperature and view exposure matter

## Conduction And Envelope

Use in A3/A4.

```text
q = U A ΔT
```

Architectural use:

- estimate heat flow through roof, wall, window, or slab
- compare insulation, glazing, and exposed envelope
- explain why area and temperature difference both matter

## Thermal Capacity And Build-Up

Use in A3.

```text
Q = m c ΔT
```

Architectural use:

- explain thermal mass
- explain why heavy materials heat and cool slowly
- explain delayed peak temperature
- distinguish quick surface heating from stored heat

Simple heat balance:

```text
C dT/dt = gains - losses
```

Architectural use:

- show build-up when gains exceed losses
- show night flushing as increased loss
- show shading as reduced gain
- connect temporal sequence to design action

## Accumulated Exposure

Use in A3/A4.

```text
degree-hours = ∫ max(T - T_threshold, 0) dt
```

Discrete student version:

```text
degree-hours ≈ Σ max(T_hour - T_threshold, 0)
```

Architectural use:

- count how long a condition remains beyond a threshold
- compare strategies by accumulated burden
- avoid relying only on maximum temperature

## Air Movement

Use in A4 and optional CFD-lite.

Conceptual relation:

```text
convective heat exchange increases when air speed increases
```

Architectural use:

- fans can change perceived heat without changing air temperature much
- cross ventilation depends on openings, pressure, path, and obstruction
- air movement can help heat removal or create drafts

Optional design cue:

```text
flow path matters as much as flow rate
```

## Fire Engineering Connection

Use as an optional conceptual bridge, not a core assessment.

Shared logic:

- heat release and heat accumulation
- smoke/heat layer stratification
- tenability thresholds
- exposure duration
- failure as threshold exceedance over time

Architectural use:

- show that thermal thinking is not just comfort
- connect heat, time, exposure, and safety
- reinforce the idea that failure can be temporal and cumulative

## CFD-Lite Connection

Optional extension if there is time.

Use CFD only for bounded questions:

- does air reach the occupied zone?
- does a fan or opening change the flow path?
- does a courtyard trap or flush air?
- does a partition block ventilation?

Do not assess CFD polish. Assess:

- boundary assumptions
- flow path interpretation
- design consequence
- uncertainty statement

