import * as THREE from 'three';
import { RoundedBoxGeometry } from './vendor/RoundedBoxGeometry.js';

const COLOR_BODY = 0x156358;
const COLOR_BODY_DARK = 0x0B4A42;
const COLOR_LID = 0x0E7C6E;
const COLOR_WHEEL = 0x1B2422;
const COLOR_FOAM = 0xF3FBF8;
const COLOR_WATER = 0x8FE9DC;

function makeRadialTexture(innerColor, outerColor, size = 128) {
  const canvas = document.createElement('canvas');
  canvas.width = canvas.height = size;
  const ctx = canvas.getContext('2d');
  const grad = ctx.createRadialGradient(size / 2, size / 2, 0, size / 2, size / 2, size / 2);
  grad.addColorStop(0, innerColor);
  grad.addColorStop(1, outerColor);
  ctx.fillStyle = grad;
  ctx.fillRect(0, 0, size, size);
  const tex = new THREE.CanvasTexture(canvas);
  tex.colorSpace = THREE.SRGBColorSpace;
  return tex;
}

/* alphaMap in three.js reads texture luminance, not the alpha channel — so masks
   must be painted in white/grey on a black-transparent canvas; the actual hue is
   supplied separately via material.color. */
function makeBlobTexture({ size = 512, blobs = 34, minR = 10, maxR = 34, minA = 0.35, maxA = 0.85, stretchMin = 1, stretchMax = 1, speckle = 0 }) {
  const canvas = document.createElement('canvas');
  canvas.width = canvas.height = size;
  const ctx = canvas.getContext('2d');
  ctx.clearRect(0, 0, size, size);
  for (let i = 0; i < blobs; i++) {
    const x = Math.random() * size;
    const y = Math.random() * size;
    const r = minR + Math.random() * (maxR - minR);
    const stretch = stretchMin + Math.random() * (stretchMax - stretchMin);
    const alpha = minA + Math.random() * (maxA - minA);
    const grad = ctx.createRadialGradient(x, y, 0, x, y, r);
    grad.addColorStop(0, `rgba(255,255,255,${alpha})`);
    grad.addColorStop(0.6, `rgba(255,255,255,${alpha * 0.55})`);
    grad.addColorStop(1, 'rgba(255,255,255,0)');
    ctx.fillStyle = grad;
    ctx.save();
    ctx.translate(x, y);
    ctx.rotate(Math.random() * Math.PI);
    ctx.scale(stretch, 1);
    ctx.beginPath();
    ctx.arc(0, 0, r, 0, Math.PI * 2);
    ctx.fill();
    ctx.restore();
  }
  for (let i = 0; i < speckle; i++) {
    ctx.fillStyle = `rgba(255,255,255,${0.25 + Math.random() * 0.35})`;
    ctx.beginPath();
    ctx.arc(Math.random() * size, Math.random() * size, 1 + Math.random() * 2.5, 0, Math.PI * 2);
    ctx.fill();
  }
  return new THREE.CanvasTexture(canvas);
}

function makeDirtTexture() {
  return makeBlobTexture({ blobs: 34, minR: 10, maxR: 34, minA: 0.3, maxA: 0.65, stretchMin: 1.4, stretchMax: 3.6, speckle: 90 });
}

function makeSparkleTexture(size = 128) {
  const canvas = document.createElement('canvas');
  canvas.width = canvas.height = size;
  const ctx = canvas.getContext('2d');
  const c = size / 2;
  ctx.translate(c, c);

  const glow = ctx.createRadialGradient(0, 0, 0, 0, 0, c);
  glow.addColorStop(0, 'rgba(255,250,230,0.9)');
  glow.addColorStop(0.4, 'rgba(255,201,60,0.45)');
  glow.addColorStop(1, 'rgba(255,201,60,0)');
  ctx.fillStyle = glow;
  ctx.beginPath();
  ctx.arc(0, 0, c, 0, Math.PI * 2);
  ctx.fill();

  function starPath(outerR, innerR) {
    ctx.beginPath();
    for (let i = 0; i < 8; i++) {
      const r = i % 2 === 0 ? outerR : innerR;
      const a = (i / 8) * Math.PI * 2;
      const px = Math.sin(a) * r;
      const py = -Math.cos(a) * r;
      if (i === 0) ctx.moveTo(px, py); else ctx.lineTo(px, py);
    }
    ctx.closePath();
  }

  starPath(c * 0.82, c * 0.16);
  const starGrad = ctx.createRadialGradient(0, 0, 0, 0, 0, c * 0.82);
  starGrad.addColorStop(0, 'rgba(255,255,255,1)');
  starGrad.addColorStop(0.5, 'rgba(255,222,140,0.95)');
  starGrad.addColorStop(1, 'rgba(255,201,60,0)');
  ctx.fillStyle = starGrad;
  ctx.fill();

  const tex = new THREE.CanvasTexture(canvas);
  return tex;
}

function clamp(v, min, max) { return Math.max(min, Math.min(max, v)); }
function smoothstep(edge0, edge1, x) {
  const t = clamp((x - edge0) / (edge1 - edge0), 0, 1);
  return t * t * (3 - 2 * t);
}
function triangle(x, start, peak, end) {
  if (x <= start || x >= end) return 0;
  if (x <= peak) return (x - start) / (peak - start);
  return 1 - (x - peak) / (end - peak);
}

export function supportsWebGL() {
  try {
    const canvas = document.createElement('canvas');
    return !!(window.WebGLRenderingContext &&
      (canvas.getContext('webgl2') || canvas.getContext('webgl')));
  } catch (e) {
    return false;
  }
}

export function initBinScene(canvas) {
  const renderer = new THREE.WebGLRenderer({ canvas, antialias: true, alpha: true, powerPreference: 'high-performance' });
  renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 2));
  renderer.outputColorSpace = THREE.SRGBColorSpace;
  renderer.toneMapping = THREE.ACESFilmicToneMapping;
  renderer.toneMappingExposure = 1.15;

  const scene = new THREE.Scene();
  const camera = new THREE.PerspectiveCamera(26, 1, 0.1, 50);
  const camBase = new THREE.Vector3(0, 1.12, 5.4);
  camera.position.copy(camBase);
  camera.lookAt(0, 1.05, 0);

  scene.add(new THREE.HemisphereLight(0xEAF7F2, 0x0B4A42, 0.65));

  const key = new THREE.DirectionalLight(0xffffff, 1.55);
  key.position.set(2.4, 3.6, 2.8);
  scene.add(key);

  const fill = new THREE.DirectionalLight(0xBEEFE3, 0.4);
  fill.position.set(-3, 1.6, 1.2);
  scene.add(fill);

  const rim = new THREE.DirectionalLight(0xFFE8AE, 0.65);
  rim.position.set(-1.2, 2.6, -3.2);
  scene.add(rim);

  const popLight = new THREE.PointLight(0xFFFFFF, 0, 6);
  popLight.position.set(0.6, 1.8, 2.2);
  scene.add(popLight);

  /* ---------- Contact shadow (fake AO blob) ---------- */
  const shadowTex = makeRadialTexture('rgba(6,36,32,0.42)', 'rgba(6,36,32,0)');
  const shadowMesh = new THREE.Mesh(
    new THREE.PlaneGeometry(2.6, 1.5),
    new THREE.MeshBasicMaterial({ map: shadowTex, transparent: true, depthWrite: false })
  );
  shadowMesh.rotation.x = -Math.PI / 2;
  shadowMesh.position.y = 0.001;
  scene.add(shadowMesh);

  /* ---------- Bin group (rotates as a whole) ---------- */
  const binGroup = new THREE.Group();
  scene.add(binGroup);

  const bodyMat = new THREE.MeshPhysicalMaterial({
    color: COLOR_BODY, roughness: 0.38, metalness: 0.06,
    clearcoat: 0.55, clearcoatRoughness: 0.28
  });
  const bodyGeo = new RoundedBoxGeometry(1.0, 1.86, 0.82, 4, 0.085);
  const body = new THREE.Mesh(bodyGeo, bodyMat);
  body.position.y = 0.98;
  binGroup.add(body);

  // subtle vertical ridges
  for (const rx of [-0.28, 0, 0.28]) {
    const ridge = new THREE.Mesh(
      new THREE.BoxGeometry(0.05, 1.5, 0.02),
      new THREE.MeshStandardMaterial({ color: COLOR_BODY_DARK, roughness: 0.5, metalness: 0.04 })
    );
    ridge.position.set(rx, 0.98, 0.415);
    binGroup.add(ridge);
  }

  // dirt overlay shell
  const dirtTex = makeDirtTexture();
  const dirtMat = new THREE.MeshStandardMaterial({
    color: 0x6b5a42, alphaMap: dirtTex, transparent: true,
    roughness: 0.95, metalness: 0, depthWrite: false, polygonOffset: true, polygonOffsetFactor: -1
  });
  const dirtGeo = new RoundedBoxGeometry(1.012, 1.878, 0.832, 3, 0.086);
  const dirtMesh = new THREE.Mesh(dirtGeo, dirtMat);
  dirtMesh.position.y = 0.98;
  binGroup.add(dirtMesh);


  // wheels
  const wheelMat = new THREE.MeshStandardMaterial({ color: COLOR_WHEEL, roughness: 0.65, metalness: 0.1 });
  const wheelGeo = new THREE.CylinderGeometry(0.165, 0.165, 0.1, 20);
  for (const wx of [-0.32, 0.32]) {
    const wheel = new THREE.Mesh(wheelGeo, wheelMat);
    wheel.rotation.z = Math.PI / 2;
    wheel.position.set(wx, 0.165, -0.28);
    binGroup.add(wheel);
  }

  // lid on a hinge pivot at the back-top edge
  const lidPivot = new THREE.Group();
  lidPivot.position.set(0, 1.916, -0.39);
  binGroup.add(lidPivot);

  const lidMat = new THREE.MeshPhysicalMaterial({
    color: COLOR_LID, roughness: 0.32, metalness: 0.05,
    clearcoat: 0.7, clearcoatRoughness: 0.2
  });
  const lidGeo = new RoundedBoxGeometry(1.05, 0.1, 0.86, 3, 0.05);
  const lid = new THREE.Mesh(lidGeo, lidMat);
  lid.position.set(0, 0.05, 0.43);
  lidPivot.add(lid);

  const handle = new THREE.Mesh(
    new THREE.TorusGeometry(0.1, 0.018, 8, 20, Math.PI),
    new THREE.MeshStandardMaterial({ color: COLOR_BODY_DARK, roughness: 0.5, metalness: 0.15 })
  );
  handle.rotation.set(Math.PI / 2, 0, Math.PI);
  handle.position.set(0, 0.1, 0.2);
  lidPivot.add(handle);

  function randomFacePoint() {
    // 0 = front, 1 = right, 2 = left
    const face = Math.floor(Math.random() * 3);
    const y = 0.3 + Math.random() * 1.55;
    if (face === 0) return { x: (Math.random() - 0.5) * 0.86, y, z: 0.425 };
    if (face === 1) return { x: 0.515, y, z: (Math.random() - 0.5) * 0.7 };
    return { x: -0.515, y, z: (Math.random() - 0.5) * 0.7 };
  }

  /* ---------- Foam / lather bubbles (dense instanced clusters = coverage) ---------- */
  const FOAM_COUNT = 150;
  const foamGeo = new THREE.SphereGeometry(1, 8, 8);
  const foamMat = new THREE.MeshStandardMaterial({ color: COLOR_FOAM, roughness: 0.85, transparent: true });
  const foamMesh = new THREE.InstancedMesh(foamGeo, foamMat, FOAM_COUNT);
  foamMesh.instanceMatrix.setUsage(THREE.DynamicDrawUsage);

  const foamData = [];
  for (let i = 0; i < FOAM_COUNT; i++) {
    const p = randomFacePoint();
    const big = Math.random() < 0.22;
    foamData.push({
      pos: new THREE.Vector3(p.x * (1 + Math.random() * 0.05), p.y, p.z * (1 + Math.random() * 0.05)),
      scale: big ? 0.045 + Math.random() * 0.05 : 0.02 + Math.random() * 0.028,
      t0: Math.random() * 0.6,
      t1: 0.35 + Math.random() * 0.55
    });
  }
  binGroup.add(foamMesh);

  /* ---------- Water rinse streaks ---------- */
  const WATER_COUNT = 34;
  const waterGeo = new THREE.CapsuleGeometry(0.014, 0.16, 2, 6);
  const waterMat = new THREE.MeshStandardMaterial({ color: COLOR_WATER, roughness: 0.15, metalness: 0.1, transparent: true });
  const waterMesh = new THREE.InstancedMesh(waterGeo, waterMat, WATER_COUNT);
  waterMesh.instanceMatrix.setUsage(THREE.DynamicDrawUsage);
  const waterData = [];
  for (let i = 0; i < WATER_COUNT; i++) {
    const p = randomFacePoint();
    waterData.push({
      x: p.x,
      z: p.z * 1.02,
      yStart: 1.7 + Math.random() * 0.3,
      yEnd: 0.15 + Math.random() * 0.35,
      scale: 0.8 + Math.random() * 0.8,
      t0: Math.random() * 0.55,
      t1: 0.4 + Math.random() * 0.6
    });
  }
  binGroup.add(waterMesh);

  /* ---------- Sparkles ---------- */
  const sparkTex = makeSparkleTexture();
  const SPARK_COUNT = 6;
  const sparkles = [];
  for (let i = 0; i < SPARK_COUNT; i++) {
    const mat = new THREE.SpriteMaterial({ map: sparkTex, transparent: true, opacity: 0, depthWrite: false, blending: THREE.AdditiveBlending });
    const sprite = new THREE.Sprite(mat);
    const angle = (i / SPARK_COUNT) * Math.PI * 2;
    sprite.position.set(Math.sin(angle) * 0.62, 0.5 + Math.random() * 1.3, Math.cos(angle) * 0.5);
    sprite.scale.setScalar(0.16 + Math.random() * 0.1);
    binGroup.add(sprite);
    sparkles.push({ sprite, phase: Math.random() });
  }

  /* ---------- Pressure washer prop (fixed in world space) ---------- */
  const WASHER_BASE_Y = 1.32;
  const washerGroup = new THREE.Group();
  washerGroup.position.set(0.62, WASHER_BASE_Y, 1.05);
  washerGroup.rotation.set(-0.15, -0.55, 0.65);
  scene.add(washerGroup);

  const gunMat = new THREE.MeshStandardMaterial({ color: 0x1C2422, roughness: 0.45, metalness: 0.3, transparent: true });
  const accentMat = new THREE.MeshStandardMaterial({ color: 0x2DD4BF, roughness: 0.3, metalness: 0.2, transparent: true });

  const wand = new THREE.Mesh(new THREE.CylinderGeometry(0.028, 0.028, 0.85, 12), gunMat);
  wand.rotation.z = Math.PI / 2;
  wand.position.set(-0.35, 0, 0);
  washerGroup.add(wand);

  const nozzle = new THREE.Mesh(new THREE.ConeGeometry(0.04, 0.14, 12), gunMat);
  nozzle.rotation.z = Math.PI / 2;
  nozzle.position.set(-0.82, 0, 0);
  washerGroup.add(nozzle);

  const grip = new THREE.Mesh(new THREE.BoxGeometry(0.09, 0.2, 0.06), gunMat);
  grip.position.set(0.05, -0.15, 0);
  grip.rotation.z = 0.35;
  washerGroup.add(grip);

  const trigger = new THREE.Mesh(new THREE.BoxGeometry(0.1, 0.03, 0.05), accentMat);
  trigger.position.set(0.02, -0.02, 0);
  washerGroup.add(trigger);

  const washerMeshes = [wand, nozzle, grip, trigger];

  /* ---------- Choreography ---------- */
  const dummy = new THREE.Object3D();

  function updateFoam(progress) {
    const windowOn = triangle(progress, 0.06, 0.32, 0.58);
    for (let i = 0; i < FOAM_COUNT; i++) {
      const d = foamData[i];
      const local = smoothstep(d.t0 * 0.55 + 0.06, d.t0 * 0.55 + 0.06 + d.t1 * 0.3, progress) *
        (1 - smoothstep(0.5, 0.62, progress));
      const s = d.scale * local;
      dummy.position.copy(d.pos);
      dummy.scale.setScalar(Math.max(s, 0.0001));
      dummy.rotation.set(0, 0, 0);
      dummy.updateMatrix();
      foamMesh.setMatrixAt(i, dummy.matrix);
    }
    foamMesh.instanceMatrix.needsUpdate = true;
    foamMat.opacity = clamp(windowOn * 1.1, 0, 0.97);
  }

  function updateWater(progress) {
    const windowOn = triangle(progress, 0.5, 0.66, 0.86);
    for (let i = 0; i < WATER_COUNT; i++) {
      const d = waterData[i];
      const local = smoothstep(0.48 + d.t0 * 0.3, 0.48 + d.t0 * 0.3 + d.t1 * 0.3, progress);
      const y = THREE.MathUtils.lerp(d.yStart, d.yEnd, local);
      const fade = local * (1 - smoothstep(0.8, 0.9, progress));
      dummy.position.set(d.x, y, d.z);
      dummy.scale.set(1, d.scale * Math.max(fade, 0.0001), 1);
      dummy.rotation.set(0, 0, 0);
      dummy.updateMatrix();
      waterMesh.setMatrixAt(i, dummy.matrix);
    }
    waterMesh.instanceMatrix.needsUpdate = true;
    waterMat.opacity = clamp(windowOn * 0.9, 0, 0.85);
  }

  function updateWasher(progress) {
    const active = Math.max(triangle(progress, 0.02, 0.3, 0.6), triangle(progress, 0.46, 0.68, 0.9));
    const op = clamp(active * 1.2, 0, 1);
    washerMeshes.forEach((m) => { m.material.opacity = op; });
    washerGroup.visible = op > 0.01;
    washerGroup.position.y = WASHER_BASE_Y + Math.sin(progress * Math.PI * 2) * 0.02;
  }

  function updateSparkles(progress) {
    const base = smoothstep(0.82, 1, progress);
    sparkles.forEach(({ sprite, phase }) => {
      const twinkle = 0.6 + 0.4 * Math.sin((progress + phase) * Math.PI * 6);
      sprite.material.opacity = base * twinkle;
    });
  }

  function render(progress) {
    binGroup.rotation.y = THREE.MathUtils.degToRad(-26) + progress * THREE.MathUtils.degToRad(190);

    const lidOpen = smoothstep(0.8, 1, progress);
    lidPivot.rotation.x = -lidOpen * 1.9;

    dirtMat.opacity = clamp(1 - smoothstep(0.05, 0.42, progress) * 1.05, 0, 1);

    updateFoam(progress);
    updateWater(progress);
    updateWasher(progress);
    updateSparkles(progress);

    popLight.intensity = smoothstep(0.82, 1, progress) * 1.4;
    bodyMat.clearcoat = 0.55 + smoothstep(0.8, 1, progress) * 0.35;
    lidMat.clearcoat = 0.7 + smoothstep(0.8, 1, progress) * 0.25;

    camera.position.x = camBase.x;
    camera.position.y = camBase.y + progress * 0.06;
    camera.position.z = camBase.z - progress * 0.35;
    camera.lookAt(0, 1.05 + lidOpen * 0.05, 0);

    renderer.render(scene, camera);
  }

  function resize(width, height) {
    renderer.setSize(width, height, false);
    camera.aspect = width / height;
    camera.updateProjectionMatrix();
  }

  function dispose() {
    renderer.dispose();
    bodyGeo.dispose();
    dirtGeo.dispose();
    lidGeo.dispose();
    foamGeo.dispose();
    waterGeo.dispose();
  }

  return { render, resize, dispose };
}
