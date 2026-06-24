const SURFACES = [
  { id: "left", label: "Left wall", temp: 28, kind: "wall" },
  { id: "right", label: "Right wall", temp: 38, kind: "wall" },
  { id: "front", label: "Front wall", temp: 29, kind: "wall" },
  { id: "back", label: "Back wall", temp: 36, kind: "wall" },
  { id: "floor", label: "Floor", temp: 33, kind: "floor" },
  { id: "ceiling", label: "Ceiling", temp: 27, kind: "ceiling" }
];

const state = {
  activePoint: "A",
  heatmap: [],
  lastA: null,
  lastB: null,
  minValue: 0,
  maxValue: 1
};

const $ = (id) => document.getElementById(id);

function cToK(c) {
  return Number(c) + 273.15;
}

function kToC(k) {
  return k - 273.15;
}

function clamp(value, min, max) {
  return Math.max(min, Math.min(max, value));
}

function formatTemp(value) {
  return `${value.toFixed(1)} deg C`;
}

function getRoom() {
  return {
    width: Number($("roomWidth").value),
    depth: Number($("roomDepth").value),
    height: Number($("roomHeight").value),
    airTemp: Number($("airTemp").value),
    radWeight: Number($("radWeight").value),
    rayCount: Number($("rayCount").value)
  };
}

function getSurfaces() {
  return SURFACES.map((surface) => ({
    ...surface,
    temp: Number($(`${surface.id}Temp`).value)
  }));
}

function getPoint(prefix, room) {
  return {
    x: clamp(Number($(`${prefix}x`).value), 0.05, room.width - 0.05),
    y: clamp(Number($(`${prefix}y`).value), 0.05, room.depth - 0.05),
    z: clamp(Number($(`${prefix}z`).value), 0.05, room.height - 0.05)
  };
}

function setPoint(prefix, point) {
  $(`${prefix}x`).value = point.x.toFixed(2);
  $(`${prefix}y`).value = point.y.toFixed(2);
  $(`${prefix}z`).value = point.z.toFixed(2);
}

function fibonacciDirections(count) {
  const directions = [];
  const golden = Math.PI * (3 - Math.sqrt(5));
  for (let i = 0; i < count; i += 1) {
    const y = 1 - (i / (count - 1)) * 2;
    const radius = Math.sqrt(Math.max(0, 1 - y * y));
    const theta = golden * i;
    directions.push({
      x: Math.cos(theta) * radius,
      y,
      z: Math.sin(theta) * radius
    });
  }
  return directions;
}

function firstSurfaceHit(point, direction, room) {
  const tests = [];
  if (direction.x < -1e-9) tests.push({ t: (0 - point.x) / direction.x, surface: "left" });
  if (direction.x > 1e-9) tests.push({ t: (room.width - point.x) / direction.x, surface: "right" });
  if (direction.y < -1e-9) tests.push({ t: (0 - point.y) / direction.y, surface: "front" });
  if (direction.y > 1e-9) tests.push({ t: (room.depth - point.y) / direction.y, surface: "back" });
  if (direction.z < -1e-9) tests.push({ t: (0 - point.z) / direction.z, surface: "floor" });
  if (direction.z > 1e-9) tests.push({ t: (room.height - point.z) / direction.z, surface: "ceiling" });

  let best = null;
  for (const test of tests) {
    if (test.t <= 0) continue;
    if (!best || test.t < best.t) best = test;
  }
  return best ? best.surface : null;
}

function estimateViewFactors(point, room, rayCount) {
  const counts = Object.fromEntries(SURFACES.map((surface) => [surface.id, 0]));
  const directions = fibonacciDirections(rayCount);
  for (const direction of directions) {
    const hit = firstSurfaceHit(point, direction, room);
    if (hit) counts[hit] += 1;
  }
  const total = directions.length;
  return Object.fromEntries(Object.entries(counts).map(([surface, count]) => [surface, count / total]));
}

function computePoint(point, room, surfaces) {
  const viewFactors = estimateViewFactors(point, room, room.rayCount);
  let weightedFourth = 0;
  for (const surface of surfaces) {
    weightedFourth += viewFactors[surface.id] * Math.pow(cToK(surface.temp), 4);
  }
  const tmrt = kToC(Math.pow(weightedFourth, 0.25));
  const top = (1 - room.radWeight) * room.airTemp + room.radWeight * tmrt;
  return { point, viewFactors, tmrt, top };
}

function computeReading(surface, fa, fb) {
  const hotter = surface.temp >= Math.max(Number($("airTemp").value), 30);
  const moreAtB = fb - fa > 0.04;
  const moreAtA = fa - fb > 0.04;
  if (moreAtB) return `B sees more ${hotter ? "warm" : "cool"} ${surface.kind}`;
  if (moreAtA) return `A sees more ${hotter ? "warm" : "cool"} ${surface.kind}`;
  return "similar exposure";
}

function colorFor(value, min, max) {
  const t = max === min ? 0.5 : clamp((value - min) / (max - min), 0, 1);
  const stops = [
    [0.0, [45, 127, 175]],
    [0.5, [238, 240, 178]],
    [0.75, [231, 127, 54]],
    [1.0, [169, 50, 37]]
  ];
  for (let i = 0; i < stops.length - 1; i += 1) {
    const [t0, c0] = stops[i];
    const [t1, c1] = stops[i + 1];
    if (t >= t0 && t <= t1) {
      const f = (t - t0) / (t1 - t0);
      const rgb = c0.map((channel, idx) => Math.round(channel + f * (c1[idx] - channel)));
      return `rgb(${rgb[0]}, ${rgb[1]}, ${rgb[2]})`;
    }
  }
  return "rgb(169, 50, 37)";
}

function buildHeatmap(room, surfaces, metric, z) {
  const nx = 30;
  const ny = 20;
  const lowRayRoom = { ...room, rayCount: Math.min(room.rayCount, 360) };
  const values = [];
  let minValue = Infinity;
  let maxValue = -Infinity;
  for (let j = 0; j < ny; j += 1) {
    const row = [];
    for (let i = 0; i < nx; i += 1) {
      const point = {
        x: ((i + 0.5) / nx) * room.width,
        y: ((j + 0.5) / ny) * room.depth,
        z
      };
      const result = computePoint(point, lowRayRoom, surfaces);
      const value = result[metric];
      minValue = Math.min(minValue, value);
      maxValue = Math.max(maxValue, value);
      row.push(value);
    }
    values.push(row);
  }
  return { values, minValue, maxValue, nx, ny };
}

function drawMarker(ctx, point, room, canvas, label, color) {
  const x = (point.x / room.width) * canvas.width;
  const y = canvas.height - (point.y / room.depth) * canvas.height;
  ctx.save();
  ctx.fillStyle = color;
  ctx.strokeStyle = "#ffffff";
  ctx.lineWidth = 3;
  ctx.beginPath();
  ctx.arc(x, y, 11, 0, Math.PI * 2);
  ctx.fill();
  ctx.stroke();
  ctx.fillStyle = "#ffffff";
  ctx.font = "bold 13px sans-serif";
  ctx.textAlign = "center";
  ctx.textBaseline = "middle";
  ctx.fillText(label, x, y + 0.5);
  ctx.restore();
}

function drawHeatmap(room, aPoint, bPoint) {
  const canvas = $("heatmap");
  const ctx = canvas.getContext("2d");
  const metric = $("metric").value;
  const surfaces = getSurfaces();
  const z = (aPoint.z + bPoint.z) / 2;
  const heatmap = buildHeatmap(room, surfaces, metric, z);
  state.heatmap = heatmap.values;
  state.minValue = heatmap.minValue;
  state.maxValue = heatmap.maxValue;

  const cellW = canvas.width / heatmap.nx;
  const cellH = canvas.height / heatmap.ny;
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  for (let j = 0; j < heatmap.ny; j += 1) {
    for (let i = 0; i < heatmap.nx; i += 1) {
      const value = heatmap.values[j][i];
      ctx.fillStyle = colorFor(value, heatmap.minValue, heatmap.maxValue);
      ctx.fillRect(i * cellW, canvas.height - (j + 1) * cellH, cellW + 1, cellH + 1);
    }
  }

  ctx.strokeStyle = "rgba(29,36,40,0.55)";
  ctx.lineWidth = 3;
  ctx.strokeRect(1.5, 1.5, canvas.width - 3, canvas.height - 3);
  drawMarker(ctx, aPoint, room, canvas, "A", "#1c6f7a");
  drawMarker(ctx, bPoint, room, canvas, "B", "#b5442c");
  $("legendMin").textContent = formatTemp(heatmap.minValue);
  $("legendMax").textContent = formatTemp(heatmap.maxValue);
}

function updateOutputs() {
  const room = getRoom();
  const surfaces = getSurfaces();
  const pointA = getPoint("a", room);
  const pointB = getPoint("b", room);
  setPoint("a", pointA);
  setPoint("b", pointB);
  const resultA = computePoint(pointA, room, surfaces);
  const resultB = computePoint(pointB, room, surfaces);
  state.lastA = resultA;
  state.lastB = resultB;

  $("aTmrt").textContent = formatTemp(resultA.tmrt);
  $("aTop").textContent = formatTemp(resultA.top);
  $("bTmrt").textContent = formatTemp(resultB.tmrt);
  $("bTop").textContent = formatTemp(resultB.top);
  $("dTmrt").textContent = formatTemp(resultB.tmrt - resultA.tmrt);
  $("dTop").textContent = formatTemp(resultB.top - resultA.top);

  const tbody = $("viewTable").querySelector("tbody");
  tbody.innerHTML = "";
  for (const surface of surfaces) {
    const fa = resultA.viewFactors[surface.id];
    const fb = resultB.viewFactors[surface.id];
    const tr = document.createElement("tr");
    tr.innerHTML = `
      <td>${surface.label}</td>
      <td>${formatTemp(surface.temp)}</td>
      <td>${fa.toFixed(3)}</td>
      <td>${fb.toFixed(3)}</td>
      <td>${computeReading(surface, fa, fb)}</td>
    `;
    tbody.appendChild(tr);
  }
  drawHeatmap(room, pointA, pointB);
}

function createSurfaceControls() {
  const root = $("surfaceControls");
  for (const surface of SURFACES) {
    const wrap = document.createElement("div");
    wrap.className = "surface-control";
    wrap.innerHTML = `
      <label>${surface.label}
        <input id="${surface.id}Range" type="range" min="10" max="60" step="0.5" value="${surface.temp}">
      </label>
      <label>deg C
        <input id="${surface.id}Temp" type="number" min="10" max="60" step="0.5" value="${surface.temp}">
      </label>
    `;
    root.appendChild(wrap);
    const range = $(`${surface.id}Range`);
    const temp = $(`${surface.id}Temp`);
    range.addEventListener("input", () => {
      temp.value = range.value;
      updateOutputs();
    });
    temp.addEventListener("input", () => {
      range.value = temp.value;
      updateOutputs();
    });
  }
}

function csvRows() {
  const room = getRoom();
  const surfaces = getSurfaces();
  const rows = [
    ["Radiant Box Tool Export"],
    ["room_width_m", room.width],
    ["room_depth_m", room.depth],
    ["room_height_m", room.height],
    ["air_temp_c", room.airTemp],
    ["radiant_weight", room.radWeight],
    [],
    ["position", "x_m", "y_m", "z_m", "tmrt_c", "top_c"],
    ["A", state.lastA.point.x, state.lastA.point.y, state.lastA.point.z, state.lastA.tmrt, state.lastA.top],
    ["B", state.lastB.point.x, state.lastB.point.y, state.lastB.point.z, state.lastB.tmrt, state.lastB.top],
    [],
    ["surface", "temp_c", "view_factor_A", "view_factor_B"]
  ];
  for (const surface of surfaces) {
    rows.push([
      surface.label,
      surface.temp,
      state.lastA.viewFactors[surface.id],
      state.lastB.viewFactors[surface.id]
    ]);
  }
  return rows;
}

function downloadCsv() {
  const text = csvRows()
    .map((row) => row.map((value) => `"${String(value ?? "").replaceAll('"', '""')}"`).join(","))
    .join("\n");
  const blob = new Blob([text], { type: "text/csv" });
  const link = document.createElement("a");
  link.href = URL.createObjectURL(blob);
  link.download = "a2-radiant-box-export.csv";
  link.click();
  URL.revokeObjectURL(link.href);
}

function downloadPng() {
  const link = document.createElement("a");
  link.href = $("heatmap").toDataURL("image/png");
  link.download = "a2-radiant-box-heatmap.png";
  link.click();
}

function setActivePoint(point) {
  state.activePoint = point;
  $("placeA").classList.toggle("active", point === "A");
  $("placeB").classList.toggle("active", point === "B");
}

function handleCanvasClick(event) {
  const room = getRoom();
  const canvas = $("heatmap");
  const rect = canvas.getBoundingClientRect();
  const x = ((event.clientX - rect.left) / rect.width) * room.width;
  const y = (1 - (event.clientY - rect.top) / rect.height) * room.depth;
  const prefix = state.activePoint.toLowerCase();
  const z = Number($(`${prefix}z`).value);
  setPoint(prefix, { x, y, z });
  updateOutputs();
}

function bindInputs() {
  const inputIds = [
    "roomWidth", "roomDepth", "roomHeight", "airTemp", "radWeight", "rayCount",
    "ax", "ay", "az", "bx", "by", "bz", "metric"
  ];
  for (const id of inputIds) {
    $(id).addEventListener("input", updateOutputs);
  }
  $("placeA").addEventListener("click", () => setActivePoint("A"));
  $("placeB").addEventListener("click", () => setActivePoint("B"));
  $("heatmap").addEventListener("click", handleCanvasClick);
  $("downloadCsv").addEventListener("click", downloadCsv);
  $("downloadPng").addEventListener("click", downloadPng);
}

createSurfaceControls();
bindInputs();
updateOutputs();
