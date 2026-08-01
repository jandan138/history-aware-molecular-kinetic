import * as THREE from "three";
import { OrbitControls } from "three/addons/controls/OrbitControls.js";
import { EffectComposer } from "three/addons/postprocessing/EffectComposer.js";
import { OutputPass } from "three/addons/postprocessing/OutputPass.js";
import { RenderPass } from "three/addons/postprocessing/RenderPass.js";
import { UnrealBloomPass } from "three/addons/postprocessing/UnrealBloomPass.js";
import "./style.css";

const palette = {
  passive: new THREE.Color("#263040"),
  foreground: new THREE.Color("#d9e7e8"),
  target: new THREE.Color("#36d6ff"),
  edited: new THREE.Color("#ff5b6e"),
};

const stories = {
  "reveal-echo": ["E1 — A Frame Is Not a Future", "A visible frame is not a future.", "Matched resolved presents retain different hidden collision correlations and separate again in time."],
  "branch-collision": ["E3 — One Collision, Two Worlds", "Edit one collision.<br />Watch two worlds diverge.", "A one-degree edit to one addressable collision creates an exact counterfactual branch."],
  "choose-cause": ["E4 — Choose the Cause", "Point at the consequence.<br />Trace its past cause.", "A selected future stroke ranks historical collisions before exact previews steer the result."],
  "same-present-hero": ["E5 — Same Present, Chosen Future", "Same visible present.<br />Chosen physical future.", "Four of 256 particles exchange hidden velocity ownership while every visible position stays fixed at the pivot."],
};

const canvas = document.querySelector("#stage");
const renderer = new THREE.WebGLRenderer({ canvas, antialias: true, powerPreference: "high-performance" });
renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
renderer.setSize(window.innerWidth, window.innerHeight);
renderer.outputColorSpace = THREE.SRGBColorSpace;
renderer.toneMapping = THREE.ACESFilmicToneMapping;
renderer.toneMappingExposure = 1.4;

const scene = new THREE.Scene();
scene.background = new THREE.Color("#03050a");
scene.fog = new THREE.FogExp2("#03050a", 0.055);
const camera = new THREE.PerspectiveCamera(48, window.innerWidth / window.innerHeight, 0.01, 100);
camera.position.set(0, -7.6, 9.8);
const controls = new OrbitControls(camera, canvas);
controls.target.set(0, 0, 0);
controls.enableDamping = true;
controls.minDistance = 5;
controls.maxDistance = 16;

const composer = new EffectComposer(renderer);
composer.addPass(new RenderPass(scene, camera));
composer.addPass(new UnrealBloomPass(new THREE.Vector2(window.innerWidth, window.innerHeight), 0.55, 0.4, 0.82));
composer.addPass(new OutputPass());

scene.add(new THREE.HemisphereLight("#b9e9ff", "#03050a", 1.1));
scene.add(new THREE.AmbientLight("#d9e7e8", 4.5));
const cyanLight = new THREE.PointLight("#36d6ff", 26, 14, 2);
cyanLight.position.set(-4, -2, 5);
scene.add(cyanLight);
const coralLight = new THREE.PointLight("#ff5b6e", 18, 12, 2);
coralLight.position.set(4, 1, 4);
scene.add(coralLight);

const stage = new THREE.Group();
scene.add(stage);
const particleGeometry = new THREE.IcosahedronGeometry(1, 2);
const particleMaterial = new THREE.MeshPhysicalMaterial({
  color: "#ffffff",
  roughness: 0.24,
  metalness: 0.22,
  clearcoat: 0.45,
  clearcoatRoughness: 0.22,
  vertexColors: true,
});

let bundle = null;
let meshes = [];
let positions = null;
let roles = {};
let currentFrame = 50;
let playing = false;
let lastTick = performance.now();
const dummy = new THREE.Object3D();

function addLaboratory(offset) {
  const group = new THREE.Group();
  group.position.x = offset;
  const floor = new THREE.Mesh(
    new THREE.BoxGeometry(4.3, 2.3, 0.08),
    new THREE.MeshPhysicalMaterial({ color: "#0c101a", roughness: 0.17, metalness: 0.72, clearcoat: 0.5 }),
  );
  floor.position.z = -0.06;
  group.add(floor);
  const railMaterial = new THREE.MeshBasicMaterial({ color: "#36d6ff", toneMapped: false });
  for (const [x, y, sx, sy] of [[-2.1, 0, .025, 1.08], [2.1, 0, .025, 1.08], [0, -1.08, 2.1, .025], [0, 1.08, 2.1, .025]]) {
    const rail = new THREE.Mesh(new THREE.BoxGeometry(sx * 2, sy * 2, .035), railMaterial);
    rail.position.set(x, y, 0.01);
    group.add(rail);
  }
  stage.add(group);
}

function clearStage() {
  while (stage.children.length) stage.remove(stage.children[0]);
  meshes = [];
}

function readFloat32(buffer) {
  const view = new DataView(buffer);
  const values = new Float32Array(buffer.byteLength / 4);
  for (let index = 0; index < values.length; index += 1) values[index] = view.getFloat32(index * 4, true);
  return values;
}

async function loadShot(shotId) {
  document.querySelector("#loading").classList.remove("hidden");
  const base = `/shots/${shotId}`;
  bundle = await fetch(`${base}/manifest.json`).then((response) => {
    if (!response.ok) throw new Error(`Missing staged E6 data for ${shotId}`);
    return response.json();
  });
  [positions, roles] = await Promise.all([
    fetch(`${base}/${bundle.arrays.positions.path}`).then((response) => response.arrayBuffer()).then(readFloat32),
    fetch(`${base}/${bundle.roles.path}`).then((response) => response.json()),
  ]);
  clearStage();
  const offsets = bundle.branches.length === 2 ? [-2.25, 2.25] : [0];
  for (let branch = 0; branch < bundle.branches.length; branch += 1) {
    addLaboratory(offsets[branch]);
    const mesh = new THREE.InstancedMesh(particleGeometry, particleMaterial, bundle.particles.count);
    mesh.instanceMatrix.setUsage(THREE.DynamicDrawUsage);
    mesh.userData = { branch, offset: offsets[branch] };
    mesh.frustumCulled = false;
    stage.add(mesh);
    meshes.push(mesh);
  }
  currentFrame = bundle.timeline.frame_count - 1;
  const slider = document.querySelector("#timeline");
  slider.max = String(currentFrame);
  slider.value = String(currentFrame);
  document.querySelector("#branch-left").textContent = bundle.branches[0].label;
  document.querySelector("#branch-right").textContent = bundle.branches[1].label;
  const [act, title, copy] = stories[shotId];
  document.querySelector("#act-label").textContent = act;
  document.querySelector("#story-title").innerHTML = title;
  document.querySelector("#story-copy").textContent = copy;
  document.querySelectorAll(".acts button").forEach((button) => button.classList.toggle("active", button.dataset.shot === shotId));
  updateMetrics(shotId);
  updateParticles();
  document.querySelector("#loading").classList.add("hidden");
}

function roleColor(particleId, passiveColor) {
  if ((roles.edited || []).includes(particleId)) return palette.edited;
  if ((roles.target || []).includes(particleId)) return palette.target;
  return passiveColor ? palette.foreground : palette.passive;
}

function updateParticles() {
  if (!bundle || !positions) return;
  const [, frameCount, particleCount] = bundle.arrays.shape;
  const radius = bundle.physics.particle_radius * 4.4;
  for (const mesh of meshes) {
    for (let particle = 0; particle < particleCount; particle += 1) {
      const base = ((mesh.userData.branch * frameCount + currentFrame) * particleCount + particle) * 3;
      dummy.position.set(mesh.userData.offset + positions[base] - 2, positions[base + 1] - 1, radius);
      const id = bundle.particles.ids[particle];
      const emphasis = (roles.target || []).includes(id) || (roles.edited || []).includes(id);
      dummy.scale.setScalar(radius * (emphasis ? 1.45 : 1));
      dummy.updateMatrix();
      mesh.setMatrixAt(particle, dummy.matrix);
      mesh.setColorAt(particle, roleColor(id, bundle.particles.passive_colors[particle]));
    }
    mesh.instanceMatrix.needsUpdate = true;
    if (mesh.instanceColor) mesh.instanceColor.needsUpdate = true;
  }
  const t = bundle.timeline.start_time + (bundle.timeline.end_time - bundle.timeline.start_time) * currentFrame / Math.max(1, frameCount - 1);
  document.querySelector("#time-value").textContent = t.toFixed(2);
  document.querySelector("#timeline").value = String(currentFrame);
}

function updateMetrics(shotId) {
  const definitions = {
    "reveal-echo": [["0.448", "mean echo gap"], ["2", "opposite futures"]],
    "branch-collision": [["1°", "one collision edit"], ["79 / 105", "events reused"], ["106 / 106", "pair agreement"]],
    "choose-cause": [["4.0×", "target selectivity"], ["79 / 103", "events reused"], ["12", "exact previews"]],
    "same-present-hero": [["4 / 256", "particles touched"], ["75%", "target reduction"], ["100%", "collateral retained"]],
  };
  document.querySelector("#metrics").innerHTML = definitions[shotId].map(([value, label]) => `<div class="metric"><strong>${value}</strong><span>${label}</span></div>`).join("");
}

document.querySelectorAll(".acts button").forEach((button) => button.addEventListener("click", () => loadShot(button.dataset.shot)));
document.querySelector("#timeline").addEventListener("input", (event) => { currentFrame = Number(event.target.value); playing = false; updateParticles(); });
document.querySelector("#play").addEventListener("click", () => { playing = !playing; document.querySelector("#play").textContent = playing ? "Ⅱ" : "▶"; });
document.querySelector("#reset-camera").addEventListener("click", () => { camera.position.set(0, -7.6, 9.8); controls.target.set(0, 0, 0); });

window.addEventListener("resize", () => {
  camera.aspect = window.innerWidth / window.innerHeight;
  camera.updateProjectionMatrix();
  renderer.setSize(window.innerWidth, window.innerHeight);
  composer.setSize(window.innerWidth, window.innerHeight);
});

function animate(now) {
  requestAnimationFrame(animate);
  if (playing && bundle && now - lastTick > 90) {
    currentFrame = (currentFrame + 1) % bundle.timeline.frame_count;
    updateParticles();
    lastTick = now;
  }
  controls.update();
  composer.render();
}

loadShot("same-present-hero").catch((error) => { document.querySelector("#loading").textContent = error.message; });
requestAnimationFrame(animate);
