# Schedule Skeleton

Default assumption: 12 teaching weeks. The semester should tolerate holidays or short weeks by keeping the final two weeks clinic/jury oriented rather than introducing major new technical content.

## Semester Arc

| Week | Lens | Studio/lab output | Assignment alignment |
|---:|---|---|---|
| 1 | The average room does not exist | thermal claim autopsy | A1 launch |
| 2 | Body, surface, air, and radiant exchange | body-surface-air heat exchange sketch | A1 evidence setup |
| 3 | Environmental sensing and uncertainty | spatial Ta/RH field map | A1 due |
| 4 | Radiant environment and MRT | radiant plan/section + MRT logic | A2 launch |
| 5 | Radiant exchange and heat flux | radiant exchange card | A2 due |
| 6 | Thermal build-up, capacity, and integrals | sequence storyboard + threshold setup + pulse check | A3 launch |
| 7 | EnergyPlus as exposure-state generator | hourly state log + output variables | A3 development |
| 8 | Weather, indoor/outdoor stress tests, and future scenarios | degree-hour/failure-hour comparison | A3 development |
| 9 | Inverse questions: what does it take? | found/censored action ladder | A3 due / final project launch |
| 10 | Failure audit to design action | design action ladder + alternatives | final project development |
| 11 | Roll-forward validation, uncertainty, and defense | final board draft + validation/uncertainty statement | final project clinic |
| 12 | Thermal design jury | thermal design action package | final project due |

## Unit 1: Defaults, Evidence, And Thermal Fields

Purpose: kill the average-room myth and make students sample thermal fields instead of quoting one number.

### Week 1: The Average Room Does Not Exist

Key question: What does it mean to claim a space is thermally comfortable?

Topics:

- default body
- default room
- default weather
- default setpoint
- default comfort claim
- architectural consequences of averaging
- indoor and outdoor claims as equally situated

Studio/lab:

- Students bring one thermal claim from a studio project, precedent, campus space, or building they use.
- They identify the hidden defaults.

Output:

- thermal claim autopsy diagram

### Week 2: Body, Surface, Air, And Radiant Exchange

Key question: How does a body exchange heat with a building or microclimate?

Topics:

- conduction
- convection
- radiation
- evaporation
- metabolism
- clothing
- air temperature versus radiant temperature
- radiant flux as a body-environment exchange problem

Studio/lab:

- Draw one occupant in one architectural condition.
- Annotate body-surface-air heat-exchange pathways.
- Identify whether the dominant uncertainty is air, surface, radiation, activity, exposure, or duration.

Output:

- body-surface-air heat exchange sketch

### Week 3: Environmental Sensing And Uncertainty

Key question: What can a measurement actually prove?

Topics:

- sensor placement
- logging interval
- sampling bias
- missing variables
- surface temperature
- globe temperature and MRT approximation
- SMART-style radiant sensing module, if available
- subjective reports
- indoor/outdoor transects
- data quality

Studio/lab:

- Students design a measurement protocol.
- They collect or critique a short transect/time-series.
- If sensor hardware is available, students compare air temperature against radiant/surface signals in at least two positions.

Output:

- Assignment 1 spatial Ta/RH field map and sensing protocol

## Unit 2: Radiation, Heat Flux, And Model Limits

Purpose: build enough physics to make architecture consequential.

### Week 4: Radiant Environment And MRT

Key question: Why can two spaces with the same air temperature feel different?

Topics:

- mean radiant temperature
- operative temperature
- surface temperature
- solar radiation
- longwave radiation
- radiant asymmetry
- glass, pavement, exposed concrete, and vegetation
- shade as thermal architecture
- translating radiant flux into sensed heat and MRT

Studio/lab:

- Radiant section drawing.
- Compare sunlit and shaded occupant positions.
- Translate a globe/SMART/surface reading into a design interpretation.

Output:

- Assignment 2 radiant section or radiant plan

### Week 5: Radiant Exchange And Heat Flux

Key question: How does radiant exchange change what the body receives?

Topics:

- radiant heat flux
- body orientation
- surface area and view exposure
- glass, pavement, and facade materials
- sun/shade as heat-flux control
- operative temperature as air plus radiant interpretation
- comfort model limits

Studio/lab:

- Students compare two positions with similar air temperature but different radiant exposure.
- Students translate a surface/radiant/MRT proxy into an architectural implication.

Output:

- Assignment 2 radiant exchange card

### Week 6: Thermal Build-Up, Capacity, And Integrals

Key question: When does heat accumulate, persist, or fail to dissipate?

Topics:

- thermal capacity
- thermal lag
- heat balance
- conduction through envelope
- degree-hours and accumulated exposure
- temporal thresholds
- comfort/protection models and what they erase
- default occupant versus vulnerable occupant

Studio/lab:

- Students choose a time period and threshold for A3.
- Students create a first time-series or sequence strip.

Output:

- Assignment 3 storyboard and threshold setup

### Week 6 Pulse Check

Anonymous 5-minute check:

1. Is the course matching what you expected from the DCP?
2. Which concept or tool route needs more support?
3. What is unclear about the assignments or final project?
4. What should be adjusted before the second half of semester?

Instructor summarizes one or two adjustments in Week 7.

## Unit 3: Stress-Testing, Failure, And Sufficiency

Purpose: make uncertainty operational and connect build-up to stress testing.

### Week 7: EnergyPlus As Exposure-State Generator

Key question: What should EnergyPlus be used for in this course?

Answer:

> Not truth. Not magic. Not a software credential. It is a way to generate structured hourly exposure states.

Topics:

- weather files
- zones
- constructions
- internal gains
- schedules
- output variables
- zone air temperature
- mean radiant temperature
- operative temperature
- humidity
- energy/load outputs
- response to Week 6 pulse check

Studio/lab:

- Run or inspect a provided shoebox/small-zone model.
- Export hourly outputs.
- Plot time series and distributions.

Output:

- simulation state log

### Week 8: Weather, Indoor/Outdoor Stress Tests, And Future Scenarios

Key question: What happens when the weather file, exposure, or boundary condition changes?

Topics:

- typical year versus extreme year
- heatwave year
- future weather
- outdoor exposure and surface temperature
- indoor response to outdoor stress
- climate scenario as stress test
- not pretending one weather file is the future

Studio/lab:

- Same model/condition, different weather file, design day, shade condition, or outdoor exposure.
- Compare failure hours.

Output:

- climate/exposure stress-test memo with degree-hours or failure hours

### Week 9: Inverse Questions: What Does It Take?

Key question: Instead of "how does this design perform?", ask "what intervention reaches the target?"

Topics:

- forward simulation
- inverse query
- target
- service state
- found query
- censored query
- action-space edge
- masked burden
- stopping rule

Studio/lab:

- Students run or inspect a small design action ladder.
- They identify the minimum successful action or censored outcome.

Output:

- found/censored action ladder

## Unit 4: Design Action, Defense, And Final Argument

Purpose: turn analysis into defensible architecture.

### Week 10: Failure Audit To Design Action

Key question: What must change architecturally?

Topics:

- compliance failure
- protection failure
- spatial failure
- temporal failure
- occupant failure
- model failure
- retrofit failure
- intervention classes
- translating evidence into section, facade, material, shade, program, or control

Studio/lab:

- Assignment 3 pin-up.
- Students convert one failure mode into a bounded design action ladder.

Output:

- design action ladder and alternatives matrix

### Week 11: Roll-Forward Validation, Uncertainty, And Defense

Key question: How do students defend a thermal action under changed climate or stress assumptions without overclaiming?

Topics:

- roll-forward validation
- future or shifted weather assumptions
- stress-window sensitivity
- uncertainty statement
- out-of-support conditions
- what the model does not include
- what was not measured
- what was averaged
- what remains unresolved
- how to present a censored result
- reproducibility capsule

Studio/lab:

- validate the same action against one changed stress assumption
- mock oral defense
- reproducibility check

Output:

- final board draft, roll-forward validation note, and uncertainty statement

### Week 12: Thermal Design Jury

Final presentation structure:

1. The condition.
2. The evidence.
3. The heterogeneity.
4. The failure mode.
5. The design action ladder.
6. The minimum found action or censored result.
7. The roll-forward validation note.
8. The architectural proposal.
9. The uncertainty statement.
10. What should be tested next.
