// ================= 1. BIẾN TRẠNG THÁI CHUYẾN BAY =================
let originAirport = AIRPORTS[0];
let destAirport = AIRPORTS[2];
let selectedAircraft = "Airbus A321neo";
let currentDistance = 605;
let selectedDuration = 55;
let selectedSeat = "06A";
let selectedFocus = FOCUS_MODES[1];
let isBookingCollapsed = false;

let isFlying = false, strictModeEnabled = true, isPausedByViolation = false, violationCount = 0;
const MAX_VIOLATIONS = 3;
let alarmInterval = null, flightInterval = null;
window.audioCtx = null;
window.cabinNoiseNode = null;
let remainingSeconds = 55 * 60, totalFlightSeconds = 55 * 60;
let currentFlightProgress = 0;
let flightEtaString = "--:--";

let currentCamView = "map";
let currentEnvMode = "day";
let isShadeClosed = false;
let cabinMoodIdx = 0;
let isReadingLightOn = false;
let isTrayTableOpen = true;
let is2DMapActive = false;

// ================= 2. QUẢ ĐỊA CẦU 3D THREE.JS & BẢN ĐỒ VỆ TINH 2D LEAFLET =================
let scene, camera, renderer, earthGroup, earthMesh, routeArcLine;
const GLOBE_RADIUS = 100;
let globeCameraZ = 275, targetGlobeZ = 275;
let isDraggingGlobe = false, prevMouse = { x: 0, y: 0 }, targetRot = { x: 0.22, y: 3.4 }, lastTransitionTime = 0;

function createFallbackEarthCanvas() {
    const c = document.createElement('canvas');
    c.width = 1024; c.height = 512;
    const ctx = c.getContext('2d');
    const grad = ctx.createLinearGradient(0, 0, 0, 512);
    grad.addColorStop(0, '#0c4a6e'); grad.addColorStop(0.5, '#082f49'); grad.addColorStop(1, '#0c4a6e');
    ctx.fillStyle = grad; ctx.fillRect(0, 0, 1024, 512);
    return new THREE.CanvasTexture(c);
}

function latLngToVec3(lat, lng, radius = GLOBE_RADIUS) {
    const phi = (90 - lat) * (Math.PI / 180);
    const theta = (lng + 180) * (Math.PI / 180);
    return new THREE.Vector3(-radius * Math.sin(phi) * Math.cos(theta), radius * Math.cos(phi), radius * Math.sin(phi) * Math.sin(theta));
}

function initThreeGlobe() {
    try {
        if (typeof THREE === 'undefined') return;
        const canvas = document.getElementById('globe-canvas');
        if (!canvas) return;
        scene = new THREE.Scene();
        const w = window.innerWidth || 1200, h = Math.max(400, (window.innerHeight - 56) || 700);
        camera = new THREE.PerspectiveCamera(45, w / h, 1, 2000);
        camera.position.z = globeCameraZ;

        renderer = new THREE.WebGLRenderer({ canvas: canvas, antialias: true, alpha: true });
        renderer.setSize(w, h);
        renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 2));

        const starGeo = new THREE.BufferGeometry();
        const starCount = 2000;
        const starPos = new Float32Array(starCount * 3);
        const starColors = new Float32Array(starCount * 3);
        for (let i = 0; i < starCount * 3; i += 3) {
            const r = 450 + Math.random() * 850;
            const theta = Math.random() * Math.PI * 2;
            const phi = Math.acos(2 * Math.random() - 1);
            starPos[i] = r * Math.sin(phi) * Math.cos(theta);
            starPos[i+1] = r * Math.sin(phi) * Math.sin(theta);
            starPos[i+2] = r * Math.cos(phi);
            const tint = 0.75 + Math.random() * 0.25;
            starColors[i] = tint; starColors[i+1] = tint; starColors[i+2] = 1.0;
        }
        starGeo.setAttribute('position', new THREE.BufferAttribute(starPos, 3));
        starGeo.setAttribute('color', new THREE.BufferAttribute(starColors, 3));
        scene.add(new THREE.Points(starGeo, new THREE.PointsMaterial({ size: 2.2, vertexColors: true, transparent: true, opacity: 0.9 })));

        earthGroup = new THREE.Group();
        scene.add(earthGroup);

        const sphereGeo = new THREE.SphereGeometry(GLOBE_RADIUS, 64, 64);
        const earthMat = new THREE.MeshPhongMaterial({ map: createFallbackEarthCanvas(), shininess: 16, specular: new THREE.Color(0x1e3a8a) });
        earthMesh = new THREE.Mesh(sphereGeo, earthMat);
        earthGroup.add(earthMesh);

        const loader = new THREE.TextureLoader();
        loader.setCrossOrigin('anonymous');
        loader.load('https://unpkg.com/three-globe@2.31.0/example/img/earth-blue-marble.jpg', (tex) => {
            earthMat.map = tex; earthMat.needsUpdate = true;
        });

        earthGroup.add(new THREE.Mesh(
            new THREE.SphereGeometry(GLOBE_RADIUS * 1.035, 64, 64),
            new THREE.MeshBasicMaterial({ color: 0x38bdf8, transparent: true, opacity: 0.16, side: THREE.BackSide })
        ));

        scene.add(new THREE.AmbientLight(0xdbeafe, 0.85));
        const dirLight = new THREE.DirectionalLight(0xffffff, 0.95);
        dirLight.position.set(250, 180, 300);
        scene.add(dirLight);

        canvas.addEventListener('mousedown', (e) => { isDraggingGlobe = true; prevMouse = { x: e.clientX, y: e.clientY }; });
        window.addEventListener('mousemove', (e) => {
            if (!isDraggingGlobe) return;
            targetRot.y += (e.clientX - prevMouse.x) * 0.0055;
            targetRot.x = Math.max(-1.2, Math.min(1.2, targetRot.x + (e.clientY - prevMouse.y) * 0.0055));
            prevMouse = { x: e.clientX, y: e.clientY };
        });
        window.addEventListener('mouseup', () => { isDraggingGlobe = false; });

        canvas.addEventListener('wheel', (e) => {
            e.preventDefault();
            if (Date.now() - lastTransitionTime < 650) return;
            const step = Math.sign(e.deltaY) * Math.min(Math.abs(e.deltaY) * 0.15, 10);
            targetGlobeZ = Math.max(150, Math.min(430, targetGlobeZ + step));
            if (targetGlobeZ <= 165 && e.deltaY < 0) {
                targetGlobeZ = 190; globeCameraZ = 190; activate2DSatelliteMap();
            }
        }, { passive: false });

        window.addEventListener('resize', () => {
            const nw = window.innerWidth || 1200, nh = Math.max(400, (window.innerHeight - 56) || 700);
            if (camera && renderer) {
                camera.aspect = nw / nh; camera.updateProjectionMatrix();
                renderer.setSize(nw, nh);
            }
            if (map) map.invalidateSize(true);
        });

        animateThreeGlobe();
    } catch (err) {}
}

function update3DGlobeRouteArc() {
    if (!earthGroup || typeof THREE === 'undefined') return;
    if (routeArcLine) { earthGroup.remove(routeArcLine); routeArcLine.geometry.dispose(); }
    const startVec = latLngToVec3(originAirport.coords[0], originAirport.coords[1], GLOBE_RADIUS * 1.005);
    const endVec = latLngToVec3(destAirport.coords[0], destAirport.coords[1], GLOBE_RADIUS * 1.005);
    const midVec = startVec.clone().add(endVec).multiplyScalar(0.5);
    midVec.normalize().multiplyScalar(GLOBE_RADIUS + Math.max(12, startVec.distanceTo(endVec) * 0.28));

    const curve = new THREE.QuadraticBezierCurve3(startVec, midVec, endVec);
    routeArcLine = new THREE.Line(
        new THREE.BufferGeometry().setFromPoints(curve.getPoints(64)),
        new THREE.LineBasicMaterial({ color: 0x38bdf8, linewidth: 3 })
    );
    earthGroup.add(routeArcLine);

    const midLat = (originAirport.coords[0] + destAirport.coords[0]) / 2;
    const midLng = (originAirport.coords[1] + destAirport.coords[1]) / 2;
    targetRot.y = (midLng + 90) * (Math.PI / 180);
    targetRot.x = midLat * (Math.PI / 180) * 0.75;

    setTextIfExist('globe-origin-code', originAirport.code);
    setTextIfExist('globe-dest-code', destAirport.code);
    const gSvg = document.getElementById('globe-plane-svg');
    if (gSvg) gSvg.innerHTML = getAircraftSVG(selectedAircraft, calcBearingDeg(originAirport.coords, destAirport.coords));
}

function update3DPinOverlay(elId, lat, lng, lift = 1.02) {
    const el = document.getElementById(elId);
    if (!el || !earthGroup || !camera || is2DMapActive || currentCamView !== 'map') { if (el) el.classList.add('hidden'); return; }
    const worldVec = latLngToVec3(lat, lng, GLOBE_RADIUS * lift).applyMatrix4(earthGroup.matrixWorld);
    if (camera.position.clone().normalize().dot(worldVec.clone().normalize()) < 0.15) { el.classList.add('hidden'); return; }
    const projected = worldVec.clone().project(camera);
    el.style.left = `${(projected.x * 0.5 + 0.5) * window.innerWidth}px`;
    el.style.top = `${(-(projected.y * 0.5) + 0.5) * (window.innerHeight - 56) + 56}px`;
    el.classList.remove('hidden');
}

function animateThreeGlobe() {
    requestAnimationFrame(animateThreeGlobe);
    if (!earthGroup || !renderer || !camera) return;
    earthGroup.rotation.y += (targetRot.y - earthGroup.rotation.y) * 0.08;
    earthGroup.rotation.x += (targetRot.x - earthGroup.rotation.x) * 0.08;
    globeCameraZ += (targetGlobeZ - globeCameraZ) * 0.085;
    camera.position.z = globeCameraZ;
    renderer.render(scene, camera);

    update3DPinOverlay('globe-origin-pin', originAirport.coords[0], originAirport.coords[1], 1.02);
    update3DPinOverlay('globe-dest-pin', destAirport.coords[0], destAirport.coords[1], 1.02);
    if (isFlying) {
        const curLat = originAirport.coords[0] + (destAirport.coords[0] - originAirport.coords[0]) * currentFlightProgress;
        const curLng = originAirport.coords[1] + (destAirport.coords[1] - originAirport.coords[1]) * currentFlightProgress;
        update3DPinOverlay('globe-plane-pin', curLat, curLng, 1.05);
    } else {
        const pEl = document.getElementById('globe-plane-pin');
        if (pEl) pEl.classList.add('hidden');
    }
    if (typeof updateSquadron3DPins === 'function') updateSquadron3DPins();
}

let map = null;
try {
    if (typeof L !== 'undefined') {
        map = L.map('map', { zoomControl: false, minZoom: 3, maxZoom: 18, zoomSnap: 0.5, zoomDelta: 0.5, wheelPxPerZoomLevel: 120 }).setView([14.5, 107.5], 6);
        L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}', { maxZoom: 18 }).addTo(map);
        L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/Reference/World_Boundaries_and_Places/MapServer/tile/{z}/{y}/{x}', { maxZoom: 18 }).addTo(map);

        map.getContainer().addEventListener('wheel', (e) => {
            if (is2DMapActive && e.deltaY > 0 && map.getZoom() <= 4 && (Date.now() - lastTransitionTime > 650)) activate3DSpaceGlobe();
        }, { passive: true });
    }
} catch (err) {}

let routeLine = null, originMarker = null, destMarker = null, planeMarker = null;

function activate2DSatelliteMap() {
    lastTransitionTime = Date.now(); is2DMapActive = true;
    const t = I18N[currentLang];
    document.getElementById('globe-wrapper').classList.add('globe-hidden');
    document.getElementById('map-2d-wrapper').classList.add('active-2d');
    setTextIfExist('projection-mode-badge', "2D");
    setTextIfExist('quick-switch-proj-btn', t.btnGlobe3D || "🌍 Quả cầu 3D");
    const refresh2DMap = () => {
        if (!map) return;
        map.invalidateSize(true);
        if (isFlying && planeMarker) map.setView(planeMarker.getLatLng(), 7, { animate: false });
        else if (routeLine) map.fitBounds(routeLine.getBounds(), { padding: [90, 90], maxZoom: 7, animate: false });
    };
    refresh2DMap(); setTimeout(refresh2DMap, 100);
}

function activate3DSpaceGlobe() {
    lastTransitionTime = Date.now(); is2DMapActive = false; targetGlobeZ = 245; globeCameraZ = 190;
    const t = I18N[currentLang];
    document.getElementById('map-2d-wrapper').classList.remove('active-2d');
    document.getElementById('globe-wrapper').classList.remove('globe-hidden');
    setTextIfExist('projection-mode-badge', "3D");
    setTextIfExist('quick-switch-proj-btn', t.btnMap2D || "🛰️ Bản đồ 2D");
}

function toggleProjectionMode() { if (is2DMapActive) activate3DSpaceGlobe(); else activate2DSatelliteMap(); }
function zoomStepIn() { if (!is2DMapActive) { targetGlobeZ -= 30; if (targetGlobeZ <= 168) activate2DSatelliteMap(); } else if (map) map.zoomIn(1); }
function zoomStepOut() { if (is2DMapActive) { if (map && map.getZoom() <= 4.5) activate3DSpaceGlobe(); else if (map) map.zoomOut(1); } else targetGlobeZ = Math.min(430, targetGlobeZ + 30); }

// ================= 3. TÍNH GIỜ BAY & MÔ HÌNH MÁY BAY SVG =================
function getAircraftSpecs(aircraftType) {
    if (aircraftType.includes("787")) return { speedKmh: 910, altFt: "39,000 FT", taxiMins: 12 };
    if (aircraftType.includes("A350")) return { speedKmh: 905, altFt: "40,000 FT", taxiMins: 12 };
    if (aircraftType.includes("ATR")) return { speedKmh: 510, altFt: "22,000 FT", taxiMins: 8 };
    return { speedKmh: 840, altFt: "36,000 FT", taxiMins: 12 };
}

function calcDistanceKm(coord1, coord2) {
    const R = 6371;
    const dLat = (coord2[0] - coord1[0]) * Math.PI / 180;
    const dLon = (coord2[1] - coord1[1]) * Math.PI / 180;
    const a = Math.sin(dLat/2)**2 + Math.cos(coord1[0]*Math.PI/180) * Math.cos(coord2[0]*Math.PI/180) * Math.sin(dLon/2)**2;
    return Math.max(25, Math.round(R * 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a))));
}

function calcStudyDurationFromDistance(distKm, aircraftType) {
    const specs = getAircraftSpecs(aircraftType);
    return Math.max(10, Math.round((distKm / specs.speedKmh) * 60 + specs.taxiMins));
}

function formatDurationLabel(mins) {
    const t = I18N[currentLang] || I18N.vi;
    const uMin = t.unitMin || "phút";
    const uHr = t.unitHr || "giờ";
    if (mins < 60) return `${mins} ${uMin}`;
    const h = Math.floor(mins / 60), m = mins % 60;
    return m > 0 ? `${h}h ${m}m (${mins} ${uMin})` : `${h} ${uHr} (${mins} ${uMin})`;
}

function calcRealTimeETA(durationMins) {
    const eta = new Date(Date.now() + durationMins * 60000);
    return `${String(eta.getHours()).padStart(2,'0')}:${String(eta.getMinutes()).padStart(2,'0')}`;
}

function updateRealTimeClock() {
    const now = new Date();
    const hh = String(now.getHours()).padStart(2, '0');
    const mm = String(now.getMinutes()).padStart(2, '0');
    const ss = String(now.getSeconds()).padStart(2, '0');
    const t = I18N[currentLang];
    const dateStr = `${t.fullWeekdays[now.getDay()]}, ${String(now.getDate()).padStart(2,'0')}/${String(now.getMonth()+1).padStart(2,'0')}/${now.getFullYear()}`;

    setTextIfExist('realtime-clock', `${hh}:${mm}:${ss}`);
    setTextIfExist('realtime-date', dateStr);
    setTextIfExist('cockpit-real-clock', `${hh}:${mm}:${ss}`);
    setTextIfExist('cabin-real-clock', `${hh}:${mm}:${ss}`);

    if (!isFlying) {
        setTextIfExist('booking-realtime-eta', `${hh}:${mm} ➔ ${calcRealTimeETA(selectedDuration)}`);
    }
}
setInterval(updateRealTimeClock, 1000);

function syncEnvironmentWithRealTime() {
    const hour = new Date().getHours();
    if (hour >= 6 && hour < 16) setFlightEnvironment('day');
    else if (hour >= 16 && hour < 18) setFlightEnvironment('sunset');
    else setFlightEnvironment('night');
}

function getAircraftSVG(aircraftType, headingDeg = 0) {
    if (aircraftType.includes("787")) {
        return `<svg viewBox="0 0 100 100" style="transform: rotate(${headingDeg}deg);" class="w-full h-full drop-shadow-[0_6px_12px_rgba(0,0,0,0.85)]"><rect x="32" y="46" width="7" height="14" rx="3" fill="#eab308"/><rect x="61" y="46" width="7" height="14" rx="3" fill="#eab308"/><path d="M50 34 L94 62 L98 68 L88 67 L55 52 L45 52 L12 67 L2 68 L6 62 Z" fill="#f8fafc" stroke="#eab308" stroke-width="1.5"/><path d="M50 76 L72 90 L70 94 L53 86 L47 86 L30 94 L28 90 Z" fill="#eab308"/><path d="M50 6 C55 6 57 18 57 45 L55 86 L50 95 L45 86 L43 45 C43 18 45 6 50 6 Z" fill="#ffffff"/><path d="M46 14 Q50 10 54 14 Q50 16 46 14 Z" fill="#0284c7"/></svg>`;
    } else if (aircraftType.includes("A350")) {
        return `<svg viewBox="0 0 100 100" style="transform: rotate(${headingDeg}deg);" class="w-full h-full drop-shadow-[0_6px_12px_rgba(0,0,0,0.85)]"><rect x="31" y="45" width="7" height="14" rx="3" fill="#ec4899"/><rect x="62" y="45" width="7" height="14" rx="3" fill="#ec4899"/><path d="M50 35 L92 58 L96 66 L89 64 L56 51 L44 51 L11 64 L4 66 L8 58 Z" fill="#f1f5f9" stroke="#ec4899" stroke-width="1.5"/><path d="M50 76 L72 89 L70 93 L50 86 L30 93 L28 89 Z" fill="#ec4899"/><path d="M50 5 C55 5 57 18 57 46 L55 87 L50 96 L45 87 L43 46 C43 18 45 5 50 5 Z" fill="#ffffff"/><path d="M44 13 Q50 8 56 13 Q56 17 50 15 Q44 17 44 13 Z" fill="#0f172a"/></svg>`;
    } else if (aircraftType.includes("ATR")) {
        return `<svg viewBox="0 0 100 100" style="transform: rotate(${headingDeg}deg);" class="w-full h-full drop-shadow-[0_6px_12px_rgba(0,0,0,0.85)]"><rect x="8" y="40" width="84" height="11" rx="4" fill="#e2e8f0" stroke="#10b981" stroke-width="1.5"/><rect x="29" y="34" width="6" height="16" rx="2" fill="#10b981"/><rect x="65" y="34" width="6" height="16" rx="2" fill="#10b981"/><rect x="33" y="83" width="34" height="7" rx="3" fill="#10b981"/><path d="M50 10 C54 10 55 20 55 46 L54 85 L50 93 L46 85 L45 46 C45 20 46 10 50 10 Z" fill="#ffffff"/></svg>`;
    }
    return `<svg viewBox="0 0 100 100" style="transform: rotate(${headingDeg}deg);" class="w-full h-full drop-shadow-[0_6px_12px_rgba(0,0,0,0.85)]"><rect x="33" y="44" width="6" height="12" rx="2.5" fill="#06b6d4"/><rect x="61" y="44" width="6" height="12" rx="2.5" fill="#06b6d4"/><path d="M50 36 L90 56 L93 63 L87 61 L55 50 L45 50 L13 61 L7 63 L10 56 Z" fill="#f8fafc" stroke="#06b6d4" stroke-width="1.5"/><path d="M50 76 L70 88 L68 92 L50 85 L32 92 L30 88 Z" fill="#06b6d4"/><path d="M50 7 C54 7 56 18 56 46 L54 86 L50 95 L46 86 L44 46 C44 18 46 7 50 7 Z" fill="#ffffff"/><path d="M46 14 Q50 11 54 14 Z" fill="#0284c7"/></svg>`;
}

function calcBearingDeg(coord1, coord2) {
    const lat1 = coord1[0] * Math.PI / 180, lat2 = coord2[0] * Math.PI / 180;
    const dLon = (coord2[1] - coord1[1]) * Math.PI / 180;
    const y = Math.sin(dLon) * Math.cos(lat2);
    const x = Math.cos(lat1) * Math.sin(lat2) - Math.sin(lat1) * Math.cos(lat2) * Math.cos(dLon);
    return Math.round((Math.atan2(y, x) * 180 / Math.PI + 360) % 360);
}

function createAirportBadge(code, isDest) {
    const cls = isDest ? 'bg-yellow-400 text-black' : 'bg-cyan-400 text-black';
    return L.divIcon({
        className: 'badge-icon',
        html: `<div class="${cls} font-black text-[11px] px-2 py-0.5 rounded-md shadow-xl border border-black/40 flex items-center gap-1 whitespace-nowrap">✈️ ${code}</div>`,
        iconSize: [56, 24], iconAnchor: [28, 12]
    });
}

function createCustomAircraftMapIcon() {
    const svgHtml = getAircraftSVG(selectedAircraft, calcBearingDeg(originAirport.coords, destAirport.coords));
    return L.divIcon({
        className: 'custom-plane-leaflet-icon',
        html: `<div class="relative w-16 h-16 flex items-center justify-center"><div class="radar-ring absolute inset-1 rounded-full border-2 border-cyan-400/80"></div><div class="w-14 h-14 relative z-10">${svgHtml}</div></div>`,
        iconSize: [64, 64], iconAnchor: [32, 32]
    });
}

// ================= 4. GÓC NHÌN BUỒNG LÁI / CABIN / CỬA SỔ & MÔI TRƯỜNG BAY =================
function setCameraView(view) {
    currentCamView = view;
    ['map', 'cockpit', 'cabin', 'window'].forEach(v => {
        document.querySelectorAll('.cam-' + v).forEach(btn => {
            if (v === view) { btn.classList.add('bg-cyan-500', 'text-black', 'shadow'); btn.classList.remove('text-slate-300'); }
            else { btn.classList.remove('bg-cyan-500', 'text-black', 'shadow'); btn.classList.add('text-slate-300'); }
        });
    });
    document.getElementById('zoom-mode-controls').classList.toggle('hidden', view !== 'map');
    document.getElementById('view-cockpit').classList.toggle('hidden', view !== 'cockpit');
    document.getElementById('view-cockpit').classList.toggle('flex', view === 'cockpit');
    document.getElementById('view-cabin').classList.toggle('hidden', view !== 'cabin');
    document.getElementById('view-cabin').classList.toggle('flex', view === 'cabin');
    document.getElementById('view-window').classList.toggle('hidden', view !== 'window');
    document.getElementById('view-window').classList.toggle('flex', view === 'window');
    if (view === 'map' && is2DMapActive && map) setTimeout(() => map.invalidateSize(true), 60);
    updateCameraViewsData();
}

function setFlightEnvironment(mode) {
    currentEnvMode = mode;
    ['day', 'sunset', 'night', 'rain'].forEach(m => {
        document.querySelectorAll('.env-' + m).forEach(btn => {
            if (m === mode) { btn.classList.add('bg-amber-400', 'text-black', 'shadow'); btn.classList.remove('text-slate-300'); }
            else { btn.classList.remove('bg-amber-400', 'text-black', 'shadow'); btn.classList.add('text-slate-300'); }
        });
    });

    const mapEl = document.getElementById('map');
    if (mapEl) {
        mapEl.className = "";
        if (mode === 'night') mapEl.classList.add('map-night-filter');
        if (mode === 'sunset') mapEl.classList.add('map-sunset-filter');
        if (mode === 'rain') mapEl.classList.add('map-rain-filter');
    }

    const cSky = document.getElementById('cockpit-sky-bg');
    const wSky = document.getElementById('window-sky-container');
    const cbWin = document.getElementById('cabin-side-window');
    const cStars = document.getElementById('cockpit-stars');
    const wStars = document.getElementById('window-stars');
    const cRain = document.getElementById('cockpit-rain-layer');
    const wRain = document.getElementById('window-rain-layer');
    const celestial = document.getElementById('window-celestial');

    cRain.classList.toggle('hidden', mode !== 'rain');
    wRain.classList.toggle('hidden', mode !== 'rain');

    if (mode === 'day') {
        cSky.className = "absolute inset-0 bg-gradient-to-b from-sky-500 via-blue-400 to-sky-200 transition-all duration-700 overflow-hidden";
        wSky.style.background = "linear-gradient(180deg, #0284c7 0%, #38bdf8 55%, #bae6fd 100%)";
        if (cbWin) cbWin.style.background = "linear-gradient(180deg, #0284c7 0%, #38bdf8 60%, #bae6fd 100%)";
        cStars.style.opacity = "0"; wStars.style.opacity = "0";
        celestial.className = "absolute top-10 right-12 w-12 h-12 rounded-full bg-yellow-300 shadow-[0_0_50px_#fde047]";
    } else if (mode === 'sunset') {
        cSky.className = "absolute inset-0 bg-gradient-to-b from-[#1e1b4b] via-[#be185d] to-[#f97316] transition-all duration-700 overflow-hidden";
        wSky.style.background = "linear-gradient(180deg, #1e1b4b 0%, #9d174d 45%, #f97316 85%, #fde047 100%)";
        if (cbWin) cbWin.style.background = "linear-gradient(180deg, #1e1b4b 0%, #be185d 50%, #f97316 100%)";
        cStars.style.opacity = "0.35"; wStars.style.opacity = "0.35";
        celestial.className = "absolute top-24 right-12 w-14 h-14 rounded-full bg-orange-400 shadow-[0_0_60px_#fb923c]";
    } else if (mode === 'night') {
        cSky.className = "absolute inset-0 bg-gradient-to-b from-[#020617] via-[#090d1e] to-[#111827] transition-all duration-700 overflow-hidden";
        wSky.style.background = "linear-gradient(180deg, #02040a 0%, #070d1f 65%, #1e1b4b 100%)";
        if (cbWin) cbWin.style.background = "linear-gradient(180deg, #02040a 0%, #090d1e 100%)";
        cStars.style.opacity = "1"; wStars.style.opacity = "1";
        celestial.className = "absolute top-10 right-12 w-10 h-10 rounded-full bg-slate-100 shadow-[0_0_30px_#e2e8f0]";
    } else if (mode === 'rain') {
        cSky.className = "absolute inset-0 bg-gradient-to-b from-slate-950 via-slate-800 to-slate-900 transition-all duration-700 overflow-hidden";
        wSky.style.background = "linear-gradient(180deg, #090d16 0%, #1e293b 65%, #0f172a 100%)";
        if (cbWin) cbWin.style.background = "linear-gradient(180deg, #090d16 0%, #1e293b 100%)";
        cStars.style.opacity = "0.15"; wStars.style.opacity = "0.15";
        celestial.className = "hidden";
    }
}

function toggleWindowShade() {
    isShadeClosed = !isShadeClosed;
    document.getElementById('window-shade-panel').style.height = isShadeClosed ? "88%" : "0%";
}

function toggleReadingLight() {
    isReadingLightOn = !isReadingLightOn;
    document.getElementById('reading-light-beam').classList.toggle('hidden', !isReadingLightOn);
    const btn = document.getElementById('btn-reading-light');
    if (btn) {
        btn.className = isReadingLightOn
            ? "bg-yellow-400 text-black px-2.5 py-1 rounded-xl text-[11px] font-extrabold shadow"
            : "bg-slate-800 hover:bg-slate-700 border border-white/15 px-2.5 py-1 rounded-xl text-[11px] font-bold text-slate-200 transition";
    }
}

function toggleTrayTable() {
    isTrayTableOpen = !isTrayTableOpen;
    document.getElementById('cabin-tray-table-open').classList.toggle('hidden', !isTrayTableOpen);
}

function callFlightAttendant() {
    playCabinDingDong();
    if (typeof openFirstClassMenuPrompt === 'function') openFirstClassMenuPrompt();
    else alert(`🛎️ Tiếp viên trưởng: Chúc hành khách ${appState.members[currentMemberKey].name} (Ghế ${selectedSeat}) có chuyến bay học tập hiệu quả!`);
}

function cycleCabinMoodLight() {
    const moods = ["from-cyan-500/35 via-blue-500/15 to-transparent", "from-purple-500/35 via-pink-500/15 to-transparent", "from-amber-500/35 via-orange-500/15 to-transparent", "from-emerald-500/35 via-teal-500/15 to-transparent"];
    cabinMoodIdx = (cabinMoodIdx + 1) % moods.length;
    document.getElementById('cabin-ceiling-glow').className = `absolute top-0 inset-x-0 h-28 bg-gradient-to-b ${moods[cabinMoodIdx]} blur-xl pointer-events-none transition-all duration-700`;
}

function updateCameraViewsData() {
    const profile = appState.members[currentMemberKey];
    const brng = calcBearingDeg(originAirport.coords, destAirport.coords);
    const specs = getAircraftSpecs(selectedAircraft);

    setTextIfExist('hud-speed', `${specs.speedKmh} KM/H`);
    setTextIfExist('hud-heading', `${brng}°`);
    setTextIfExist('hud-alt', specs.altFt);
    setTextIfExist('hud-aircraft-name', selectedAircraft.toUpperCase());
    setTextIfExist('hud-route-code', `${originAirport.code} ➔ ${destAirport.code}`);
    const cpSvg = document.getElementById('cockpit-plane-svg-preview');
    if (cpSvg) cpSvg.innerHTML = getAircraftSVG(selectedAircraft, 0);
    setTextIfExist('cockpit-task-display', `${selectedFocus.icon} ${selectedFocus.label}`);

    setTextIfExist('cabin-seat-label', selectedSeat);
    setTextIfExist('cabin-window-seat-tag', selectedSeat);
    setTextIfExist('cabin-aircraft-label', selectedAircraft);
    setTextIfExist('cabin-route-label', `${originAirport.code} ➔ ${destAirport.code}`);
    setTextIfExist('cabin-task-title', `${selectedFocus.icon} ${selectedFocus.label}`);
    setTextIfExist('cabin-passenger-name', profile.name);
}

function switchPage(page) {
    const pageDash = document.getElementById('page-dashboard');
    const pageFlight = document.getElementById('page-flight');
    const btnDash = document.getElementById('nav-btn-dashboard');
    const btnFlight = document.getElementById('nav-btn-flight');

    if (page === 'flight') {
        pageDash.classList.remove('page-layer-visible'); pageDash.classList.add('page-layer-hidden');
        pageFlight.classList.remove('page-layer-hidden'); pageFlight.classList.add('page-layer-visible');
        btnFlight.className = "px-2.5 sm:px-3 py-1.5 rounded-lg text-xs font-extrabold bg-gradient-to-r from-blue-600 to-cyan-500 text-white shadow transition flex items-center gap-1.5";
        btnDash.className = "px-2.5 sm:px-3 py-1.5 rounded-lg text-xs font-extrabold text-slate-400 hover:text-white transition flex items-center gap-1.5";
        setTimeout(() => {
            const nw = window.innerWidth || 1200, nh = Math.max(400, (window.innerHeight - 56) || 700);
            if (camera && renderer) {
                camera.aspect = nw / nh; camera.updateProjectionMatrix();
                renderer.setSize(nw, nh);
            }
            if (map) map.invalidateSize(true);
            updateBookingUI();
        }, 80);
    } else {
        pageFlight.classList.remove('page-layer-visible'); pageFlight.classList.add('page-layer-hidden');
        pageDash.classList.remove('page-layer-hidden'); pageDash.classList.add('page-layer-visible');
        btnDash.className = "px-2.5 sm:px-3 py-1.5 rounded-lg text-xs font-extrabold bg-gradient-to-r from-blue-600 to-cyan-500 text-white shadow transition flex items-center gap-1.5";
        btnFlight.className = "px-2.5 sm:px-3 py-1.5 rounded-lg text-xs font-extrabold text-slate-400 hover:text-white transition flex items-center gap-1.5";
        renderCalendarGrid();
        renderDashboard();
    }
}

// ================= 5. ĐẶT VÉ, CHỌN GHẾ, VÉ BOARDING PASS & CẤT CÁNH =================
function toggleBookingCardSize() {
    const card = document.getElementById('screen-booking');
    const btn = document.getElementById('toggle-booking-btn');
    const t = I18N[currentLang];
    isBookingCollapsed = !isBookingCollapsed;
    if (isBookingCollapsed) { card.classList.add('translate-y-[130%]'); btn.innerText = t.btnExpand || "🔼 Mở bảng"; }
    else { card.classList.remove('translate-y-[130%]'); btn.innerText = t.btnCollapse || "🔽 Thu gọn bảng"; }
}

function initAirportDropdowns() {
    const oSel = document.getElementById('origin-select');
    const dSel = document.getElementById('dest-select');
    const qSel = document.getElementById('quick-task-dest');
    const t = I18N[currentLang] || I18N.vi;

    const prevOrigin = (oSel && oSel.value) ? oSel.value : originAirport.code;
    const prevDest = (dSel && dSel.value) ? dSel.value : destAirport.code;
    const prevQuick = (qSel && qSel.value) ? qSel.value : "DAD";

    const vnAirports = AIRPORTS.filter(a => a.group === 'VN');
    const intAirports = AIRPORTS.filter(a => a.group === 'INT');

    const buildOptions = (withTimeHint = false) => {
        let html = `<optgroup label="${t.vnGroup || '🇻🇳 Việt Nam (22)'}" class="bg-slate-900">`;
        vnAirports.forEach(a => {
            const dist = calcDistanceKm(originAirport.coords, a.coords);
            const mins = calcStudyDurationFromDistance(dist, "Airbus A321neo");
            html += `<option value="${a.code}">${a.code} - ${a.name} ${withTimeHint ? `(~${mins}p)` : ''}</option>`;
        });
        html += `</optgroup><optgroup label="${t.intGroup || '🌏 Quốc tế (12)'}" class="bg-slate-900">`;
        intAirports.forEach(a => {
            const dist = calcDistanceKm(originAirport.coords, a.coords);
            const mins = calcStudyDurationFromDistance(dist, "Airbus A321neo");
            html += `<option value="${a.code}">${a.code} - ${a.name} ${withTimeHint ? `(~${mins}p)` : ''}</option>`;
        });
        html += `</optgroup>`;
        return html;
    };

    if (oSel) { oSel.innerHTML = buildOptions(false); oSel.value = prevOrigin; }
    if (dSel) { dSel.innerHTML = buildOptions(false); dSel.value = prevDest; }
    if (qSel) { qSel.innerHTML = buildOptions(true); qSel.value = prevQuick; }
}

function onRouteChange() {
    const oSel = document.getElementById('origin-select');
    const dSel = document.getElementById('dest-select');
    if (!oSel || !dSel) return;
    if (oSel.value === dSel.value) {
        const alt = AIRPORTS.find(a => a.code !== oSel.value);
        if (alt) dSel.value = alt.code;
    }
    originAirport = AIRPORTS.find(a => a.code === oSel.value) || AIRPORTS[0];
    destAirport = AIRPORTS.find(a => a.code === dSel.value) || AIRPORTS[2];
    currentDistance = calcDistanceKm(originAirport.coords, destAirport.coords);
    selectedDuration = calcStudyDurationFromDistance(currentDistance, selectedAircraft);
    updateBookingUI();
    if (typeof updateDestinationLiveWeather === 'function') updateDestinationLiveWeather(destAirport.code);
}

function swapRoute() {
    const temp = originAirport; originAirport = destAirport; destAirport = temp;
    document.getElementById('origin-select').value = originAirport.code;
    document.getElementById('dest-select').value = destAirport.code;
    onRouteChange();
}

function updateAircraft() {
    selectedAircraft = document.getElementById('aircraft-select').value;
    selectedDuration = calcStudyDurationFromDistance(currentDistance, selectedAircraft);
    updateBookingUI();
    if (isFlying && planeMarker) planeMarker.setIcon(createCustomAircraftMapIcon());
}

function updateBookingUI() {
    const specs = getAircraftSpecs(selectedAircraft);
    const box = document.getElementById('booking-plane-svg-box');
    if (box) box.innerHTML = getAircraftSVG(selectedAircraft, 45);
    setTextIfExist('badge-origin', originAirport.code);
    setTextIfExist('badge-dest', destAirport.code);
    setTextIfExist('badge-dist', `${currentDistance} km`);
    setTextIfExist('banner-dest-title', `${originAirport.name.split(' (')[0]} ➔ ${destAirport.name}`);
    setTextIfExist('auto-calc-duration-text', formatDurationLabel(selectedDuration));
    setTextIfExist('auto-calc-speed-text', `(${currentDistance} km • ${specs.speedKmh} km/h)`);

    const now = new Date();
    setTextIfExist('booking-realtime-eta', `${String(now.getHours()).padStart(2,'0')}:${String(now.getMinutes()).padStart(2,'0')} ➔ ${calcRealTimeETA(selectedDuration)}`);

    if (map && typeof L !== 'undefined') {
        if (routeLine) map.removeLayer(routeLine);
        if (originMarker) map.removeLayer(originMarker);
        if (destMarker) map.removeLayer(destMarker);

        originMarker = L.marker(originAirport.coords, { icon: createAirportBadge(originAirport.code, false) }).addTo(map);
        destMarker = L.marker(destAirport.coords, { icon: createAirportBadge(destAirport.code, true) }).addTo(map);
        routeLine = L.polyline([originAirport.coords, destAirport.coords], { color: '#38bdf8', weight: 3.5, dashArray: '8, 8', opacity: 0.95 }).addTo(map);

        if (is2DMapActive) { map.invalidateSize(true); map.fitBounds(routeLine.getBounds(), { padding: [90, 90], maxZoom: 7 }); }
    }
    update3DGlobeRouteArc();
    updateCameraViewsData();
}

function startFocusFromTopTask() {
    const profile = appState.members[currentMemberKey];
    const pending = (profile.tasks || []).filter(tk => !tk.done).sort((a,b) => calcPriorityScore(b) - calcPriorityScore(a));
    if (pending[0]) startFlightFromTask(pending[0].id);
}

function startFlightFromTask(taskId) {
    const profile = appState.members[currentMemberKey];
    const task = (profile.tasks || []).find(tk => tk.id === taskId);
    if (!task) return;

    activeTaskIdForFlight = task.id;
    const homeCode = (typeof getMemberHomeAirportCode === 'function') ? getMemberHomeAirportCode(currentMemberKey) : "SGN";
    originAirport = AIRPORTS.find(a => a.code === (task.originCode || homeCode)) || AIRPORTS[0];
    destAirport = AIRPORTS.find(a => a.code === task.destCode) || AIRPORTS[2];
    document.getElementById('origin-select').value = originAirport.code;
    document.getElementById('dest-select').value = destAirport.code;

    selectedFocus = { id: 'custom', label: task.title, icon: '🎯', color: 'bg-cyan-600 border-cyan-300 text-white' };
    document.getElementById('custom-focus-input').value = task.title;

    onRouteChange();
    if (task.duration) selectedDuration = task.duration;
    updateBookingUI();
    switchPage('flight');
    goToSeatSelection();
}

function flyDirectlyFromCalendarEvent(evId) {
    const profile = appState.members[currentMemberKey];
    const ev = (profile.calendarEvents || []).find(e => e.id === evId);
    if (!ev) return;

    const homeCode = (typeof getMemberHomeAirportCode === 'function') ? getMemberHomeAirportCode(currentMemberKey) : "SGN";
    originAirport = AIRPORTS.find(a => a.code === (ev.originCode || homeCode)) || AIRPORTS[0];
    destAirport = AIRPORTS.find(a => a.code === (ev.destCode || "DAD")) || AIRPORTS[2];
    document.getElementById('origin-select').value = originAirport.code;
    document.getElementById('dest-select').value = destAirport.code;

    selectedDuration = ev.durationMins || 45;
    currentDistance = calcDistanceKm(originAirport.coords, destAirport.coords);
    selectedFocus = { id: 'custom', label: ev.subject, icon: '🎯', color: 'bg-cyan-600 border-cyan-300 text-white' };
    document.getElementById('custom-focus-input').value = ev.subject;

    updateBookingUI();
    switchPage('flight');
    goToSeatSelection();
}

function renderSeats() {
    const grid = document.getElementById('seat-grid');
    if (!grid) return;
    grid.innerHTML = '';
    const cols = ['A', 'C', '', 'D', 'F'];
    for (let r = 1; r <= 12; r++) {
        const rowNum = r < 10 ? '0' + r : '' + r;
        const rowEl = document.createElement('div');
        rowEl.className = 'grid grid-cols-5 gap-2 items-center w-full';
        cols.forEach(c => {
            if (c === '') {
                const aisle = document.createElement('div');
                aisle.className = 'text-center text-xs font-mono font-bold text-slate-400';
                aisle.innerText = rowNum;
                rowEl.appendChild(aisle);
            } else {
                const seatCode = rowNum + c;
                const isSelected = seatCode === selectedSeat;
                const btn = document.createElement('button');
                let style = 'bg-[#1e293b]/90 border-white/10 text-slate-400 hover:bg-slate-700';
                if (r <= 2) style = 'bg-amber-500/15 border-amber-400/40 text-amber-200 hover:bg-amber-500/25';
                if (isSelected) style = 'bg-[#3b82f6] border-blue-200 text-white shadow-lg scale-105';
                btn.className = `seat-box h-9 rounded-xl font-bold text-xs flex items-center justify-center border ${style}`;
                btn.innerHTML = isSelected ? `<span class="text-sm">${selectedFocus.icon}</span>` : seatCode;
                btn.onclick = () => openFocusPopover(seatCode);
                rowEl.appendChild(btn);
            }
        });
        grid.appendChild(rowEl);
    }
}

function renderFocusPills() {
    const container = document.getElementById('focus-pills-container');
    if (!container) return;
    container.innerHTML = '';
    FOCUS_MODES.forEach(mode => {
        const active = selectedFocus.id === mode.id;
        const pill = document.createElement('button');
        pill.className = `px-3 py-1.5 rounded-full text-xs font-bold flex items-center gap-1.5 border transition ${active ? mode.color + ' scale-105 shadow-md' : 'bg-slate-800/80 border-white/10 text-slate-300 hover:bg-slate-700'}`;
        pill.innerHTML = `<span>${mode.icon}</span><span>${mode.label}</span>`;
        pill.onclick = () => { selectedFocus = mode; renderFocusPills(); renderSeats(); };
        container.appendChild(pill);
    });
}

function openFocusPopover(seatCode) {
    selectedSeat = seatCode;
    appState.members[currentMemberKey].seat = seatCode;
    savePersistentState();
    setTextIfExist('seat-selected-badge', seatCode);
    setTextIfExist('pop-seat-code', seatCode);
    renderSeats(); renderFocusPills();
    document.getElementById('focus-popover-backdrop').classList.remove('hidden');
    document.getElementById('focus-popover-backdrop').classList.add('flex');
}

function closeFocusPopover() {
    document.getElementById('focus-popover-backdrop').classList.add('hidden');
    document.getElementById('focus-popover-backdrop').classList.remove('flex');
}

function confirmSeatAndFocus() {
    const customVal = document.getElementById('custom-focus-input').value.trim();
    if (customVal) selectedFocus = { id: 'custom', label: customVal, icon: '🎯', color: 'bg-cyan-600 border-cyan-300 text-white' };
    strictModeEnabled = document.getElementById('strict-mode-toggle').checked;
    closeFocusPopover(); renderSeats(); showBoardingPass();
}

function goToSeatSelection() {
    const t = I18N[currentLang];
    setTextIfExist('seat-header-aircraft', selectedAircraft);
    setTextIfExist('seat-header-route', `${originAirport.code} ➔ ${destAirport.code} (${currentDistance} km • ${selectedDuration} ${t.unitMin || 'phút'})`);
    document.getElementById('screen-booking').classList.add('hidden');
    document.getElementById('toggle-booking-btn').classList.add('hidden');
    document.getElementById('screen-seat').classList.remove('hidden');
    document.getElementById('screen-seat').classList.add('flex');
    renderSeats();
}

function backToBooking() {
    document.getElementById('screen-seat').classList.add('hidden');
    document.getElementById('screen-seat').classList.remove('flex');
    document.getElementById('screen-booking').classList.remove('hidden');
    document.getElementById('toggle-booking-btn').classList.remove('hidden');
}

function showBoardingPass() {
    const profile = appState.members[currentMemberKey];
    const t = I18N[currentLang];
    strictModeEnabled = document.getElementById('strict-mode-toggle').checked;
    document.getElementById('screen-seat').classList.add('hidden');
    document.getElementById('screen-seat').classList.remove('flex');

    const now = new Date();
    const stdStr = `${String(now.getHours()).padStart(2,'0')}:${String(now.getMinutes()).padStart(2,'0')}`;
    flightEtaString = calcRealTimeETA(selectedDuration);

    setTextIfExist('tk-aircraft', selectedAircraft);
    setTextIfExist('tk-passenger', profile.name);
    setTextIfExist('tk-realtime-span', `${stdStr} ➔ ${flightEtaString}`);
    setTextIfExist('tk-strict-badge', strictModeEnabled ? "🔒 STRICT LOCK ON" : "🔓 FREE MODE");
    setTextIfExist('tk-origin-code', originAirport.code);
    setTextIfExist('tk-origin-name', originAirport.name.split(' (')[0]);
    setTextIfExist('tk-dest-code', destAirport.code);
    setTextIfExist('tk-dest-name', destAirport.name.split(' (')[0]);
    setTextIfExist('tk-duration', `${selectedDuration} ${t.unitMin || 'phút'}`);
    setTextIfExist('tk-seat', selectedSeat);
    setTextIfExist('tk-dist', currentDistance + ' km');
    setTextIfExist('tk-focus', `${selectedFocus.icon} ${selectedFocus.label}`);
    const tkSvg = document.getElementById('tk-plane-svg');
    if (tkSvg) tkSvg.innerHTML = getAircraftSVG(selectedAircraft, 90);

    document.getElementById('screen-ticket').classList.remove('hidden');
    document.getElementById('screen-ticket').classList.add('flex');
}

function backToSeatFromTicket() {
    document.getElementById('screen-ticket').classList.add('hidden');
    document.getElementById('screen-ticket').classList.remove('flex');
    document.getElementById('screen-seat').classList.remove('hidden');
    document.getElementById('screen-seat').classList.add('flex');
}

function playCabinDingDong() {
    try {
        if (!window.audioCtx) window.audioCtx = new (window.AudioContext || window.webkitAudioContext)();
        const now = window.audioCtx.currentTime;
        const osc1 = window.audioCtx.createOscillator(), osc2 = window.audioCtx.createOscillator(), gain = window.audioCtx.createGain();
        osc1.frequency.setValueAtTime(659.25, now);
        osc2.frequency.setValueAtTime(523.25, now + 0.35);
        gain.gain.setValueAtTime(0.18, now);
        gain.gain.exponentialRampToValueAtTime(0.001, now + 1.2);
        osc1.connect(gain); osc2.connect(gain); gain.connect(window.audioCtx.destination);
        osc1.start(now); osc1.stop(now + 0.35);
        osc2.start(now + 0.35); osc2.stop(now + 1.2);
    } catch (e) {}
}

function startFlight() {
    document.getElementById('screen-booking').classList.add('hidden');
    document.getElementById('toggle-booking-btn').classList.add('hidden');
    document.getElementById('screen-seat').classList.add('hidden');
    document.getElementById('screen-seat').classList.remove('flex');
    document.getElementById('screen-ticket').classList.add('hidden');
    document.getElementById('screen-ticket').classList.remove('flex');
    document.getElementById('screen-flying').classList.remove('hidden');

    playCabinDingDong();
    const player = document.getElementById('lofi-player');
    if (player && player.paused) toggleLofi();

    isFlying = true; isPausedByViolation = false; violationCount = 0; currentFlightProgress = 0;
    updateSafetyHearts(); updateCameraViewsData();

    flightEtaString = calcRealTimeETA(selectedDuration);
    setTextIfExist('fly-eta-badge', flightEtaString);
    setTextIfExist('cockpit-eta', flightEtaString);
    setTextIfExist('cabin-eta', flightEtaString);

    const flySvg = document.getElementById('fly-mini-svg');
    if (flySvg) flySvg.innerHTML = getAircraftSVG(selectedAircraft, 45);
    setTextIfExist('fly-route-text', `${originAirport.code} ➔ ${destAirport.code}`);
    setTextIfExist('fly-sub-info', `${selectedAircraft.split(' ')[1] || selectedAircraft} • ${selectedSeat} • ${selectedFocus.icon} ${selectedFocus.label}`);

    totalFlightSeconds = selectedDuration * 60;
    remainingSeconds = totalFlightSeconds;

    if (map && typeof L !== 'undefined') {
        if (planeMarker) map.removeLayer(planeMarker);
        planeMarker = L.marker(originAirport.coords, { icon: createCustomAircraftMapIcon(), zIndexOffset: 1000 }).addTo(map);
    }

    if (typeof runTakeoffTaxiAndAtcSequence === 'function') {
        runTakeoffTaxiAndAtcSequence();
    }

    updateFlightTick();
    if (flightInterval) clearInterval(flightInterval);
    flightInterval = setInterval(() => {
        if (isPausedByViolation) return;
        remainingSeconds--;
        if (remainingSeconds <= 0) finishFlightSuccessfully();
        else updateFlightTick();
    }, 1000);
}

function completeFlightEarly() { finishFlightSuccessfully(); }

function finishFlightSuccessfully() {
    if (flightInterval) clearInterval(flightInterval);
    isFlying = false; playCabinDingDong();
    const profile = appState.members[currentMemberKey];
    profile.miles = (profile.miles || 0) + currentDistance;
    profile.flights = (profile.flights || 0) + 1;

    if (typeof awardPassportStamp === 'function') {
        awardPassportStamp(originAirport.code, destAirport.code, currentDistance, selectedFocus.label);
    }

    if (activeTaskIdForFlight) {
        const task = (profile.tasks || []).find(tk => tk.id === activeTaskIdForFlight);
        if (task) task.done = true;
        activeTaskIdForFlight = null;
    }
    savePersistentState();
    alert(`🎉 Chuyến bay ${selectedAircraft} (${originAirport.code} ➔ ${destAirport.code}) đã hạ cánh thành công!\n+${currentDistance} km dặm bay & +1 Con dấu Nhập cảnh vào Hộ chiếu 3D!`);
    abortFlight();
    switchPage('dashboard');
}

function updateSafetyHearts() {
    const left = Math.max(0, MAX_VIOLATIONS - violationCount);
    setTextIfExist('safety-hearts', '❤️'.repeat(left) + '🖤'.repeat(MAX_VIOLATIONS - left));
}

function playCockpitAlarmBeep() {
    try {
        if (!window.audioCtx) window.audioCtx = new (window.AudioContext || window.webkitAudioContext)();
        const osc = window.audioCtx.createOscillator(), gain = window.audioCtx.createGain();
        osc.type = 'sawtooth';
        osc.frequency.setValueAtTime(880, window.audioCtx.currentTime);
        osc.frequency.setValueAtTime(440, window.audioCtx.currentTime + 0.18);
        gain.gain.setValueAtTime(0.2, window.audioCtx.currentTime);
        osc.connect(gain); gain.connect(window.audioCtx.destination);
        osc.start(); osc.stop(window.audioCtx.currentTime + 0.35);
    } catch (e) {}
}

function triggerTurbulenceViolation() {
    if (!isFlying || !strictModeEnabled || isPausedByViolation) return;
    isPausedByViolation = true; violationCount++; updateSafetyHearts();
    if (violationCount >= MAX_VIOLATIONS) {
        isFlying = false; clearInterval(flightInterval); stopAlarmLoop();
        document.getElementById('turbulence-modal').classList.add('hidden');
        document.getElementById('turbulence-modal').classList.remove('flex');
        document.getElementById('crash-modal').classList.remove('hidden');
        document.getElementById('crash-modal').classList.add('flex');
        playCockpitAlarmBeep(); return;
    }
    setTextIfExist('violation-count-text', `${violationCount} / ${MAX_VIOLATIONS}`);
    document.getElementById('turbulence-modal').classList.remove('hidden');
    document.getElementById('turbulence-modal').classList.add('flex');
    playCockpitAlarmBeep();
    if (alarmInterval) clearInterval(alarmInterval);
    alarmInterval = setInterval(playCockpitAlarmBeep, 900);
}

function stopAlarmLoop() { if (alarmInterval) { clearInterval(alarmInterval); alarmInterval = null; } }
function resumeFromTurbulence() { stopAlarmLoop(); isPausedByViolation = false; document.getElementById('turbulence-modal').classList.add('hidden'); document.getElementById('turbulence-modal').classList.remove('flex'); }
function closeCrashModal() { document.getElementById('crash-modal').classList.add('hidden'); document.getElementById('crash-modal').classList.remove('flex'); abortFlight(); }

document.addEventListener('visibilitychange', () => { if (document.hidden) triggerTurbulenceViolation(); });

function updateFlightTick() {
    const hrs = Math.floor(remainingSeconds / 3600);
    const mins = Math.floor((remainingSeconds % 3600) / 60);
    const secs = remainingSeconds % 60;
    const timeFormatted = hrs > 0 ? `${hrs}:${mins<10?'0'+mins:mins}:${secs<10?'0'+secs:secs}` : `${mins<10?'0'+mins:mins}:${secs<10?'0'+secs:secs}`;

    setTextIfExist('countdown-timer', timeFormatted);
    setTextIfExist('cockpit-timer-display', timeFormatted);
    setTextIfExist('cabin-timer-display', timeFormatted);

    currentFlightProgress = (totalFlightSeconds - remainingSeconds) / totalFlightSeconds;
    const progBar = document.getElementById('flight-progress');
    if (progBar) progBar.style.width = `${currentFlightProgress * 100}%`;

    const distLeft = Math.max(0, Math.round(currentDistance * (1 - currentFlightProgress)));
    setTextIfExist('fly-dist-left', distLeft);
    setTextIfExist('cockpit-dist-display', `${distLeft} KM`);
    setTextIfExist('cabin-dist-display', distLeft);

    const lat = originAirport.coords[0] + (destAirport.coords[0] - originAirport.coords[0]) * currentFlightProgress;
    const lng = originAirport.coords[1] + (destAirport.coords[1] - originAirport.coords[1]) * currentFlightProgress;
    if (planeMarker) planeMarker.setLatLng([lat, lng]);
}

function centerOnPlane() {
    setCameraView('map');
    const curLat = originAirport.coords[0] + (destAirport.coords[0] - originAirport.coords[0]) * currentFlightProgress;
    const curLng = originAirport.coords[1] + (destAirport.coords[1] - originAirport.coords[1]) * currentFlightProgress;
    if (is2DMapActive && map && planeMarker) map.flyTo(planeMarker.getLatLng(), 7, { duration: 1.2 });
    else { targetRot.y = (curLng + 90) * (Math.PI / 180); targetRot.x = curLat * (Math.PI / 180) * 0.75; }
}

function abortFlight() {
    isFlying = false; isPausedByViolation = false; stopAlarmLoop();
    if (flightInterval) clearInterval(flightInterval);
    if (map && planeMarker) map.removeLayer(planeMarker);
    if (typeof closeAtcTaxiOverlay === 'function') closeAtcTaxiOverlay();
    setCameraView('map');
    document.getElementById('screen-flying').classList.add('hidden');
    document.getElementById('screen-booking').classList.remove('hidden');
    document.getElementById('toggle-booking-btn').classList.remove('hidden');
    updateBookingUI();
}
