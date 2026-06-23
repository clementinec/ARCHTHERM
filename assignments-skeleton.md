# Assignments Skeleton

The assessment spine should be physically distinct and easy to grade:

1. **A1 Spatial Air Field**: air temperature, humidity, spatial sampling.
2. **A2 Radiant Exchange**: surface temperature, MRT, radiant flux, body perception.
3. **A3 Temporal Build-Up**: heat capacity, lag, accumulated exposure, thresholds.
4. **A4 Mechanism-Informed Thermal Design Intervention**: one bounded architectural action with roll-forward validation.

This makes the course less like a generic evidence-workflow course and more like a portable thermal-thinking course for architecture.

## Final Course Object: Mechanism-Informed Thermal Design Intervention

The final package answers:

> What thermal condition is uneven or risky, how do we know, what physical mechanism matters, what uncertainty remains, and what should the architect change?

The final package should be assembled from four accumulated artifacts:

1. **Spatial Air Field Map**: where air temperature and humidity vary.
2. **Radiant Exchange Card**: how surfaces, sun, and body position change heat exchange.
3. **Thermal Build-Up Plot**: how heat accumulates, lags, or exceeds a threshold over time.
4. **Design Action Memo**: one bounded architectural intervention, why it helps, what it does not solve, and what should be tested next.
5. **Roll-Forward Validation Note**: how the action behaves when the stress period, climate assumption, or evaluation window changes.

## Deliverable Philosophy

Students should feel they are building a thermal evidence deck:

| Stage | Artifact | Physical idea | Main question | Final package role |
|---|---|---|---|---|
| A1 | Spatial Air Field Map | air temperature, humidity, sampling uncertainty | Where is the air/humidity field different? | baseline condition and sampled field |
| A2 | Radiant Exchange Card | surface temperature, MRT, radiant flux, body exposure | Why are two similar air temperatures not the same thermal condition? | radiant mechanism and body perception |
| A3 | Temporal Build-Up Audit | heat capacity, lag, degree-hours, threshold exceedance | When does heat accumulate, persist, or fail to dissipate? | temporal failure and threshold evidence |
| A4 | Mechanism-Informed Thermal Design Intervention | bounded intervention, roll-forward validation, and defense | What should the architect change, and how robust is that action under future or shifted stress? | synthesis, future-proofing logic, and design action |

## Assignment 1: Spatial Air Field Map

Weeks 1-3, provisional weight 20%.

Students choose one real architectural condition:

- studio corner
- classroom perimeter
- corridor threshold
- atrium edge
- roof terrace
- courtyard
- bus stop
- library perimeter seat
- facade-adjacent desk
- shaded outdoor bench
- indoor/outdoor threshold

Core physical ideas:

- air temperature is spatially sampled, not universal
- humidity changes what air temperature means
- a measurement protocol shapes the claim
- spatial difference can be as important as absolute value

Portable equations/concepts:

```text
delta T:        ΔT = T_position B - T_position A
humidity note:  same T_air can imply different heat stress when RH differs
sampling:       claim strength depends on where, when, and how often we measure
```

Deliverables:

- one plan or section with 3-5 sampling points
- air temperature and relative humidity readings or curated sample data
- one spatial gradient map
- short field notes
- sensing protocol, including what was measured and what was not
- uncertainty table
- one thermal claim they can defend
- one thermal claim they cannot defend

Suggested format:

- one A3 board or two A4 pages
- small data table or CSV appendix
- optional 60-second explanation from the board

Assessment clarity:

- Are the locations clear?
- Are `Ta` and RH values recorded or credibly inferred?
- Is the spatial difference visible?
- Is the uncertainty honestly stated?
- Does the claim stay within the evidence?

Core lesson:

> A thermal condition is not a number. It is a sampled air/humidity field.

## Assignment 2: Radiant Exchange Card

Weeks 4-6, provisional weight 20%.

Students isolate radiant difference from air-temperature difference.

Prompt:

> Find or construct two positions where air temperature alone does not explain the thermal experience.

Good cases:

- window seat versus interior seat
- shaded bench versus sunlit bench
- glass facade perimeter versus deeper plan
- exposed concrete courtyard versus vegetated edge
- roof terrace sun patch versus shaded threshold
- atrium edge with high radiant exposure
- cold wall or cold window asymmetry

Core physical ideas:

- surfaces exchange radiant heat with the body
- solar radiation and longwave exchange can dominate perception
- MRT is not the same as air temperature
- body orientation and view exposure matter
- heat flux can be drawn architecturally

Portable equations/concepts:

```text
radiant exchange idea:  q_rad ≈ h_r A (T_surface - T_body)
MRT proxy:              T_mrt represents surrounding radiant field
operative temperature:  T_op combines air and radiant effects
```

Deliverables:

- radiant plan or section comparing two positions
- surface temperature or radiant/MRT proxy evidence
- air temperature comparison showing why air alone is insufficient
- body position/orientation diagram
- one heat-flux or radiant-exchange sketch
- one architectural implication

Suggested format:

- one Radiant Exchange Card
- one section/plan
- one supporting table or plot

Assessment clarity:

- Are the compared positions specific?
- Is the radiant difference visible?
- Does the student distinguish air, surface, and radiant conditions?
- Is MRT or radiant proxy method stated?
- Does the design implication follow from the radiant evidence?

Core lesson:

> Same air temperature does not mean same thermal condition.

## Assignment 3: Temporal Build-Up Audit

Weeks 7-9, provisional weight 25%.

Students examine how heat accumulates, lags, exceeds thresholds, or fails to dissipate over time.

Prompt:

> Show when a thermal condition becomes problematic, not just where.

Good cases:

- afternoon perimeter overheating
- roof-exposed room after several hot days
- courtyard surface heat build-up
- night cooling failure
- winter morning warm-up
- heatwave tail hours
- outdoor shade that works only at certain hours
- fan or ventilation schedule that changes exposure

Core physical ideas:

- thermal capacity stores heat
- materials and air volumes create lag
- peak risk may occur after peak sun
- cumulative exposure can matter more than one maximum value
- thresholds can be integrated over time

Portable equations/concepts:

```text
stored heat:       Q = m c ΔT
conduction loss:   q = U A ΔT
heat balance:      C dT/dt = gains - losses
degree-hours:      ∫ max(T - T_threshold, 0) dt
```

Deliverables:

- one time-series or sequence strip
- one threshold line or target
- one degree-hour / exceedance / accumulated exposure calculation
- explanation of the build-up or lag mechanism
- one failure statement
- one candidate design action

Suggested format:

- one Temporal Build-Up Card
- one time-series plot
- one short calculation note
- one annotated section or sequence strip

Assessment clarity:

- Is the time period explicit?
- Is the threshold explicit?
- Is accumulation or lag visible?
- Does the student use at least one portable equation/concept correctly?
- Does the candidate action respond to the temporal mechanism?

Core lesson:

> Thermal failure often comes from accumulation, duration, and lag, not a single peak value.

## Assignment 4: Mechanism-Informed Thermal Design Intervention

Weeks 9-12, provisional weight 35%.

Prompt:

> Given one thermally consequential architectural condition, propose and defend one bounded design action using spatial air evidence, radiant exchange evidence, temporal build-up evidence, and a roll-forward validation note.

The final project should not ask students to redesign an entire building or run a decade-by-decade climate retrofit study. However, students must explicitly acknowledge how climate stress, weather-window choice, and model limits affect the proposed action. Climate stress-testing, fire-engineering analogies, CFD, or EnergyPlus can appear as optional evidence layers, but the assessed object is one defensible design action.

## Final Project Routes

Students choose one route.

| Route | Best for | Final output |
|---|---|---|
| **Room / Interior Condition** | classrooms, studios, offices, housing, libraries | one plan/section intervention for a specific occupied position |
| **Facade / Envelope Edge** | window seats, perimeter zones, roof-exposed rooms, atria | one envelope/shade/material/control action |
| **Outdoor / Threshold Microclimate** | courtyards, walkways, bus stops, terraces, plazas | one shade/surface/program/exposure action |
| **Operational / Air-Movement Choice** | mixed-mode spaces, fans, schedules, adaptive setpoints | one control, ventilation, or use-pattern recommendation tied to space |

## Design Action Ladder

Instead of a large retrofit grid, students test a small ladder or matrix.

Minimum ladder:

1. **Use / position action**: move body, schedule, program, refuge, activity, or control access.
2. **Spatial / surface action**: shade, material, surface exposure, vegetation, facade depth, or roof condition.
3. **Envelope / air movement / system action**: glazing, insulation, ventilation, fan, mixed-mode rule, setpoint, or control change.

Students may test more, but the required deliverable is a bounded comparison, not exhaustive optimization.

## Final Deliverables

1. **Condition Board**
   - condition photo/drawing
   - plan/section location
   - body position and time
   - key thermal claim

2. **Spatial Air Field Evidence**
   - `Ta + RH` map or transect
   - sampling points
   - uncertainty note

3. **Radiant Exchange Evidence**
   - surface/radiant/MRT proxy evidence
   - body orientation
   - air versus radiant distinction

4. **Temporal Build-Up Evidence**
   - time-series or sequence strip
   - threshold/exceedance/degree-hour logic
   - build-up or lag explanation

5. **Design Action Memo**
   - proposed action
   - before/after comparison
   - target or threshold
   - found/censored/unresolved conclusion, if applicable
   - what should be tested next

6. **Roll-Forward Validation Note**
   - one changed stress assumption: hotter period, different weather file, different time window, altered occupancy, or future climate slice
   - whether the design action is robust, weakened, censored, or unsupported under that change
   - one honest limitation the student owns
   - one future-proofing implication for design

7. **Reproducibility Capsule**
   - inputs and sources
   - calculation/simulation/notebook/workbook files, if used
   - checked output figure
   - rerun or inspection instructions
   - known limits

8. **Oral Defense**
   - 5 minutes
   - defend the claim, physics, uncertainty, roll-forward validation, design action, and limit of claim

## Meaningful Output Types

Students should choose outputs that make thermal consequence architecturally visible:

- spatial `Ta + RH` field map
- body-surface-air heat exchange sketch
- radiant plan or section
- MRT versus air temperature comparison
- thermal build-up time-series
- degree-hour or threshold exceedance plot
- roll-forward validation card
- sun/shade exposure card
- action ladder
- before/after section
- design action memo
- reproducibility capsule

## Optional Extensions

These may appear only when they support the bounded design action:

- CFD-lite comparison for air movement, plume, or ventilation path
- fire-engineering analogy: smoke/heat layer, tenability threshold, heat release as accumulated risk
- EnergyPlus/OpenStudio hourly states
- Ladybug/Honeybee solar/radiant exposure
- pythermalcomfort or simple comfort calculation
- thermal camera/sensor-based radiant atlas

## Distinction-Level Extension: Multi-Window Roll-Forward

Students who have the setup and time may go beyond the required validation note by rerunning the same action across multiple weather or time windows.

Examples:

- compare a typical week, hot week, and heatwave week
- compare current EPW and future/climate-adjusted EPW
- compare 3-day, 7-day, and 14-day stress windows
- compare dry-hot and humid-hot periods
- compare a baseline and shifted occupancy schedule
- compare two window/glazing assumptions while keeping the design action constant

This is comparable to cross-validation or segment-length sensitivity: the student asks whether the design conclusion survives when the evaluation window changes.

This should be treated as **distinction-level evidence**, not as a hidden requirement. It can improve the quality of the final argument when it is clearly documented, but it should not reward extra computation without better architectural judgment.

## Assessment Guardrails

- The final project is assembled from Assignments 1-3. It should not be restarted from scratch.
- The final target is one defensible design action, not comprehensive optimization.
- Each assignment has a distinct physical idea: spatial air, radiant exchange, temporal build-up, design action.
- A4 must include a roll-forward validation note: how the action is expected to behave under changed climate/stress assumptions.
- Tool difficulty does not automatically produce higher marks.
- A simple, inspectable thermal argument is stronger than an opaque advanced workflow.
- Censored or unresolved results are valid if the tested ladder, target, and remaining burden are clearly stated.
- Multi-window climate roll-forward, CFD, or fire-engineering analogies are optional distinction-level extensions unless they directly support the chosen design action.
