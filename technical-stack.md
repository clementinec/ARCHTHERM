# Technical Stack And Starter-Kit Direction

Keep the stack bounded. Do not let tool installation become the course.

## Required

- spreadsheet or Python notebook for plotting
- provided EnergyPlus/OpenStudio files
- provided CSV outputs as fallback
- simple comfort calculations
- portable thermodynamics/building-physics calculations
- roll-forward validation note using changed stress/window assumptions
- environmental sensing protocol
- air temperature, humidity, surface temperature, and radiant/MRT proxy where available
- plan/section drawing
- time-series and distribution plots

## Optional

- Ladybug/Honeybee
- ClimateStudio
- pythermalcomfort
- Rhino/Grasshopper
- custom EnergyPlus/OpenStudio parametric runs
- thermal imaging
- sensors
- SMART-style radiant sensing module, exact hardware/specification to confirm
- globe thermometer or equivalent MRT proxy
- infrared thermometer or thermal camera
- wearable or occupant survey data
- CFD-lite exercise for bounded air-movement questions
- fire-engineering analogy module for heat/smoke accumulation and tenability thresholds
- multi-window weather validation for distinction-level work

## What EnergyPlus Should Do

Use it for three things only.

### 1. Produce Hourly Exposure States

Examples:

- air temperature
- mean radiant temperature
- operative temperature
- humidity
- loads
- solar gains
- zone outputs

### 2. Support Stress Testing

Examples:

- weather files
- schedules
- envelope assumptions
- service states
- climate scenarios
- stress-window length

### 3. Support Bounded Action Testing

Run a bounded action ladder, find which action first reaches a target, and report censored rows honestly.

Do not teach EnergyPlus as a full professional workflow. Teach it as a thermal evidence generator.

## First Course Kit To Build

1. One canonical shoebox model: south-facing perimeter room with roof, window, and shade options.
2. One residential exposure-cell model: reference/middle-floor, roof-exposed, lightweight/vulnerable envelope.
3. One indoor/outdoor sensing exercise: air temperature, surface temperature, radiant/MRT proxy, and position metadata.
4. One outdoor microclimate-lite exercise: sun/shade/material/sky-view comparison, even if simplified.
5. Five notebooks:
   - map spatial Ta/RH fields from sensor or sample data
   - translate globe/SMART/surface readings into MRT or radiant-flux interpretation
   - plot hourly thermal states and degree-hours
   - compare air temperature, MRT, and operative temperature
   - run comfort/adaptive/tail-hour checks
   - conduct bounded action-ladder testing
   - compare one action across different stress windows or weather files
6. Five templates:
   - sensing protocol and field note sheet
   - portable equation sheet
   - roll-forward validation note
   - uncertainty statement
   - failure audit
   - final thermal design action package
7. One sample final project:
   - found/censored action outcomes
   - architectural translation
   - defensible uncertainty statement

## Reproducibility Standard

Every supported route should have:

- one runnable starter artifact
- sample input data
- checked output
- setup notes
- known assumptions
- uncertainty/failure notes
- a path back to architectural representation
