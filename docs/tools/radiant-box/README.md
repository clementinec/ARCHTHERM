# A2 Radiant Box Tool

This static browser tool supports the A2 Radiant Exchange Card.

It asks students to compare two occupied positions inside a simple rectangular box. The air temperature is assumed well mixed, while the six surrounding surfaces can have different temperatures. The tool estimates what each body point "sees" radiantly and computes mean radiant temperature and operative temperature.

## Model

The tool estimates view factors by casting rays from a body point. Each ray hits the first room surface in its direction. The fraction of rays that hit a surface becomes that surface's approximate view factor.

The mean radiant temperature calculation is:

```text
T_mrt = (sum(F_i * T_i^4))^(1/4)
```

Temperatures are converted to Kelvin for the fourth-power calculation and converted back to deg C for display.

The operative temperature approximation is:

```text
T_op ~= (1 - w) * T_a + w * T_mrt
```

The default radiant weight `w = 0.5` is a teaching simplification for low air speed.

## A2 Use

Students should export:

- one heatmap PNG;
- one CSV table of surface temperatures, view factors, `T_mrt`, and `T_op`;
- one short A2 statement:

```text
Position B differs from Position A because the body sees more of ______,
whose surface temperature is ______. This changes T_mrt by ______ and
T_op by ______ under the stated assumptions.
```

## Limits

This is not a certification model. It assumes:

- rectangular geometry;
- uniform surface temperatures;
- point-like body location;
- no direct solar beam on the body;
- no body orientation weighting;
- no transient surface heat storage;
- no humidity, air speed, or clothing effect beyond the simple `T_op` weighting.

For a real project, students can treat this as a transparent proxy, then state which assumptions need Ladybug, Honeybee, EnergyPlus, thermal imaging, globe temperature, or a Grasshopper view-factor workflow.

## Grasshopper Translation

The same logic can become a GH pipeline:

1. Define room, courtyard, or facade surfaces.
2. Assign surface temperatures from measurement, simulation, or scenario assumptions.
3. Define occupant points at seated or standing height.
4. Cast rays or use a view-analysis component to estimate surface view fractions.
5. Compute `sum(F_i * T_i^4)` in Kelvin.
6. Convert to `T_mrt`, then compute a declared `T_op` approximation.
7. Export a table and a plan/section visualization.
