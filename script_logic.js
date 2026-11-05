// ================= 0. BẢO VỆ DỮ LIỆU DỰ PHÒNG =================
if (typeof currentLang === 'undefined') { window.currentLang = "vi"; }
if (typeof showLunarCalendar === 'undefined') { window.showLunarCalendar = true; }

// ================= 1. CHUYỂN ĐỔI NGÔN NGỮ TOÀN DIỆN (DASHBOARD + VÉ MÁY BAY) =================
function setTextIfExist(id, text) {
    const el = document.getElementById(id);
    if (el && text !== undefined) el.innerText = text;
}

function setSelectorText(selector, text) {
    const el = document.querySelector(selector);
    if (el && text !== undefined) el.innerText = text;
}

function setAppLanguage(lang) {
    currentLang = lang;
    ['vi', 'en', 'zh'].forEach(l => {
        const btn = document.getElementById('lang-btn-' + l);
        if (btn) {
            btn.className = (l === lang)
                ? "px-2 py-1 rounded-lg bg-amber-400 text-black transition"
                : "px-2 py-1 rounded-lg text-slate-300 hover:text-white transition";
        }
    });

    const t = I18N[lang];
    // 1. Dịch Header & Dashboard
    setTextIfExist('lbl-member-top', t.memberTop);
    setTextIfExist('lbl-tab-dashboard', t.tabDash);
    setTextIfExist('lbl-tab-flight', t.tabFlight);
    setTextIfExist('lbl-banner-tag', t.bannerTag);
    setTextIfExist('lbl-banner-btn', t.bannerBtn);
    setTextIfExist('lbl-kpi-1-title', t.kpi1Title);
    setTextIfExist('lbl-kpi-1-sub', t.kpi1Sub);
    setTextIfExist('lbl-kpi-2-title', t.kpi2Title);
    setTextIfExist('lbl-kpi-2-sub', t.kpi2Sub);
    setTextIfExist('lbl-kpi-3-title', t.kpi3Title);
    setTextIfExist('lbl-kpi-4-title', t.kpi4Title);
    setTextIfExist('lbl-ai-badge', t.aiBadge);
    setTextIfExist('lbl-ai-sub', t.aiSub);
    setTextIfExist('lbl-remind-btn', t.remindBtn);
    setTextIfExist('lbl-smart-ctrl-title', t.smartCtrlTitle);
    setTextIfExist('lbl-smart-ctrl-desc', t.smartCtrlDesc);
    setTextIfExist('lbl-btn-aisort', t.btnAiSort);
    setTextIfExist('lbl-btn-sudden', t.btnSudden);
    setTextIfExist('lbl-todo-header', t.todoHeader);
    setTextIfExist('lbl-todo-sync-tag', t.todoSyncTag);
    setTextIfExist('lbl-todo-sub', t.todoSub);
    setTextIfExist('filter-all', t.filterAll);
    setTextIfExist('filter-pending', t.filterPending);
    setTextIfExist('filter-done', t.filterDone);
    setTextIfExist('lbl-quick-add-title', t.quickAddTitle);
    setTextIfExist('lbl-quick-deadline', t.quickDeadline);
    setTextIfExist('lbl-btn-save-task', t.btnSaveTask);
    setTextIfExist('lbl-cal-header', t.calHeader);
    setTextIfExist('lbl-cal-sub', t.calSub);
    setTextIfExist('btn-toggle-lunar', showLunarCalendar ? t.lunarOn : t.lunarOff);
    setTextIfExist('lbl-btn-today', t.btnToday);
    setTextIfExist('lbl-pick-date', t.pickDate);
    setTextIfExist('lbl-start-time', t.startTime);
    setTextIfExist('lbl-end-time', t.endTime);
    setTextIfExist('lbl-cat-type', t.catType);
    setTextIfExist('lbl-repeat-cycle', t.repeatCycle);
    setTextIfExist('lbl-btn-add-slot', t.btnAddSlot);
    setTextIfExist('lbl-autosync-check', t.autoSyncCheck);
    setTextIfExist('lbl-bot-header', t.botHeader);

    // 2. Dịch Bảng Đặt Vé, Chọn Ghế, Vé Boarding Pass & Trạm Bay 3D/2D
    setTextIfExist('lbl-origin-title', t.originTitle);
    setTextIfExist('lbl-dest-title', t.destTitle);
    setTextIfExist('lbl-auto-dur-title', t.autoDurTitle);
    setTextIfExist('lbl-btn-pick-seat', t.btnPickSeat);
    setTextIfExist('lbl-btn-fly-now', t.btnFlyNow);
    setTextIfExist('toggle-booking-btn', isBookingCollapsed ? t.btnExpand : t.btnCollapse);
    setTextIfExist('quick-switch-proj-btn', is2DMapActive ? t.btnGlobe3D : t.btnMap2D);

    // Các nút trong màn hình Chọn ghế, Vé Boarding Pass, Cabin & Cửa sổ
    setSelectorText('button[onclick="backToBooking()"]', t.btnBackBooking);
    setSelectorText('button[onclick="showBoardingPass()"]', t.btnContinueTicket);
    setSelectorText('button[onclick="confirmSeatAndFocus()"]', t.btnConfirmSeat);
    setSelectorText('button[onclick="backToSeatFromTicket()"]', t.btnChangeSeat);
    setSelectorText('#screen-ticket button[onclick="startFlight()"]', t.btnTakeoffTicket);
    setSelectorText('button[onclick="completeFlightEarly()"]', t.btnDoneFlight);
    setSelectorText('button[onclick="abortFlight()"]', t.btnAbortFlight);
    setTextIfExist('btn-reading-light', t.btnReadingLight);
    setTextIfExist('btn-tray-table', t.btnTrayTable);
    setSelectorText('button[onclick="cycleCabinMoodLight()"]', t.btnMoodLight);
    setSelectorText('button[onclick="callFlightAttendant()"]', t.btnCallFA);
    setSelectorText('button[onclick="toggleWindowShade()"]', t.btnWindowShade);

    const wkRow = document.getElementById('calendar-weekdays-row');
    if (wkRow) wkRow.innerHTML = t.weekdays.map((w, idx) => `<div class="${idx === 6 ? 'text-red-400' : ''}">${w}</div>`).join('');

    initAirportDropdowns();
    updateBookingUI();
    updateRealTimeClock();
    renderCalendarGrid();
    renderDashboard();
    resetChat();
}

function getLunarDateInfo(year, month, day) {
    try {
        const dateObj = new Date(year, month - 1, day);
        const parts = new Intl.DateTimeFormat('en-u-ca-chinese', {
            day: 'numeric',
            month: 'numeric'
        }).formatToParts(dateObj);

        let lDay = 1, lMonth = 1;
        parts.forEach(p => {
            if (p.type === 'day') lDay = parseInt(p.value) || 1;
            if (p.type === 'month') lMonth = parseInt(p.value) || 1;
        });

        const a = Math.floor((14 - month) / 12);
        const y = year + 4800 - a;
        const m = month + 12 * a - 3;
        const jdn = day + Math.floor((153 * m + 2) / 5) + 365 * y + Math.floor(y / 4) - Math.floor(y / 100) + Math.floor(y / 400) - 32045;
        const canIdx = (jdn + 9) % 10;
        const chiIdx = (jdn + 1) % 12;

        const canChiVi = `${CAN_VI[canIdx]} ${CHI_VI[chiIdx]}`;
        const canChiZh = `${CAN_ZH[canIdx]}${CHI_ZH[chiIdx]}日`;

        return {
            lDay,
            lMonth,
            shortStr: (lDay === 1 || day === 1) ? `${lDay}/${lMonth}` : `${lDay}`,
            fullVi: `Ngày ${String(lDay).padStart(2,'0')}/${String(lMonth).padStart(2,'0')} Âm lịch • Ngày ${canChiVi}`,
            fullEn: `Lunar Date: ${String(lDay).padStart(2,'0')}/${String(lMonth).padStart(2,'0')} (${canChiVi})`,
            fullZh: `農曆 ${lMonth}月${lDay}日 • ${canChiZh}`
        };
    } catch (e) {
        return { lDay: day, lMonth: month, shortStr: `${day}`, fullVi: "Âm lịch", fullEn: "Lunar", fullZh: "農曆" };
    }
}

// ================= 2. TRẠNG THÁI LỊCH VẠN NIÊN & RENDER LƯỚI LỊCH =================
let calViewYear = 2026;
let calViewMonth = 11;
let selectedFullDate = "2026-11-04";

function toggleLunarDisplay() {
    showLunarCalendar = !showLunarCalendar;
    const t = I18N[currentLang];
    document.getElementById('btn-toggle-lunar').innerText = showLunarCalendar ? t.lunarOn : t.lunarOff;
    renderCalendarGrid();
    updateSelectedDateBanner();
}

function changeCalendarMonth(delta) {
    calViewMonth += delta;
    if (calViewMonth > 12) { calViewMonth = 1; calViewYear++; }
    if (calViewMonth < 1) { calViewMonth = 12; calViewYear--; }
    document.getElementById('cal-month-select').value = String(calViewMonth);
    document.getElementById('cal-year-select').value = String(calViewYear);
    renderCalendarGrid();
}

function onMonthYearDropdownChange() {
    calViewMonth = parseInt(document.getElementById('cal-month-select').value) || 11;
    calViewYear = parseInt(document.getElementById('cal-year-select').value) || 2026;
    renderCalendarGrid();
}

function jumpToToday() {
    const now = new Date();
    calViewYear = now.getFullYear();
    calViewMonth = now.getMonth() + 1;
    const d = now.getDate();
    selectedFullDate = `${calViewYear}-${String(calViewMonth).padStart(2,'0')}-${String(d).padStart(2,'0')}`;
    document.getElementById('cal-month-select').value = String(calViewMonth);
    document.getElementById('cal-year-select').value = String(calViewYear);
    document.getElementById('direct-date-picker').value = selectedFullDate;
    renderCalendarGrid();
    renderDashboard();
}

function selectCalendarDate(dateStr) {
    selectedFullDate = dateStr;
    document.getElementById('direct-date-picker').value = dateStr;
    const [y, m] = dateStr.split('-').map(Number);
    calViewYear = y;
    calViewMonth = m;
    document.getElementById('cal-month-select').value = String(calViewMonth);
    document.getElementById('cal-year-select').value = String(calViewYear);
    renderCalendarGrid();
    renderDashboard();
}

function onDirectDateInputChange() {
    const val = document.getElementById('direct-date-picker').value;
    if (val) selectCalendarDate(val);
}

function onRepeatModeChange() {
    const mode = document.getElementById('slot-repeat-mode').value;
    document.getElementById('custom-repeat-box').classList.toggle('hidden', mode !== 'custom');
}

function doesEventMatchDate(ev, targetDateStr) {
    if (!ev.dateStr) return true;
    if (ev.dateStr === targetDateStr) return true;
    if (targetDateStr < ev.dateStr) return false;

    const [ey, em, ed] = ev.dateStr.split('-').map(Number);
    const [ty, tm, td] = targetDateStr.split('-').map(Number);
    const evDate = new Date(ey, em - 1, ed);
    const tgDate = new Date(ty, tm - 1, td);

    const mode = ev.repeatMode || 'none';
    if (mode === 'none') return false;
    if (mode === 'daily') return true;
    if (mode === 'weekly') return evDate.getDay() === tgDate.getDay();
    if (mode === 'monthly') return ed === td;
    if (mode === 'yearly') return (ed === td && em === tm);
    if (mode === 'custom') {
        const interval = Math.max(1, parseInt(ev.customInterval) || 1);
        const unit = ev.customUnit || 'tuần';
        const diffDays = Math.round((tgDate - evDate) / 86400000);
        if (unit === 'ngày') return (diffDays % interval === 0);
        if (unit === 'tuần') return (diffDays % (interval * 7) === 0);
        if (unit === 'tháng') {
            const monthDiff = (ty - ey) * 12 + (tm - em);
            return (ed === td && monthDiff >= 0 && monthDiff % interval === 0);
        }
        if (unit === 'năm') {
            const yearDiff = ty - ey;
            return (ed === td && em === tm && yearDiff >= 0 && yearDiff % interval === 0);
        }
    }
    return false;
}

function getEventsForDate(profile, dateStr) {
    const list = profile.calendarEvents || [];
    return list.filter(ev => doesEventMatchDate(ev, dateStr));
}

function updateSelectedDateBanner() {
    const [y, m, d] = selectedFullDate.split('-').map(Number);
    const dateObj = new Date(y, m - 1, d);
    const dow = dateObj.getDay();
    const t = I18N[currentLang];
    const dowName = t.fullWeekdays[dow];
    const lunar = getLunarDateInfo(y, m, d);

    const bannerEl = document.getElementById('selected-full-date-banner');
    const lunarEl = document.getElementById('selected-lunar-date-banner');

    if (currentLang === 'zh') {
        bannerEl.innerText = `📅 ${y}年${String(m).padStart(2,'0')}月${String(d).padStart(2,'0')}日 (${dowName})`;
        lunarEl.innerText = showLunarCalendar ? `🌙 ${lunar.fullZh}` : '';
    } else if (currentLang === 'en') {
        bannerEl.innerText = `📅 ${dowName}, ${String(d).padStart(2,'0')}/${String(m).padStart(2,'0')}/${y}`;
        lunarEl.innerText = showLunarCalendar ? `🌙 ${lunar.fullEn}` : '';
    } else {
        bannerEl.innerText = `📅 ${dowName}, Ngày ${String(d).padStart(2,'0')}/${String(m).padStart(2,'0')}/${y}`;
        lunarEl.innerText = showLunarCalendar ? `🌙 ${lunar.fullVi}` : '';
    }
}

function renderCalendarGrid() {
    const t = I18N[currentLang];
    document.getElementById('calendar-header-title').innerText = `${t.monthPrefix} ${String(calViewMonth).padStart(2,'0')} - ${calViewYear}`;

    const grid = document.getElementById('calendar-days-grid');
    grid.innerHTML = '';

    const firstDayObj = new Date(calViewYear, calViewMonth - 1, 1);
    const startOffset = (firstDayObj.getDay() + 6) % 7;
    const daysInMonth = new Date(calViewYear, calViewMonth, 0).getDate();
    const prevMonthDays = new Date(calViewYear, calViewMonth - 1, 0).getDate();

    const profile = appState.members[currentMemberKey];

    for (let i = startOffset - 1; i >= 0; i--) {
        const d = prevMonthDays - i;
        const cell = document.createElement('div');
        cell.className = "cal-cell rounded-xl p-1.5 bg-slate-900/30 border border-white/5 text-slate-600 flex flex-col justify-between";
        cell.innerHTML = `<div class="text-xs font-bold">${d}</div>`;
        grid.appendChild(cell);
    }

    for (let d = 1; d <= daysInMonth; d++) {
        const dateStr = `${calViewYear}-${String(calViewMonth).padStart(2,'0')}-${String(d).padStart(2,'0')}`;
        const isSelected = (dateStr === selectedFullDate);
        const dow = new Date(calViewYear, calViewMonth - 1, d).getDay();
        const isSunday = (dow === 0);

        const dayEvents = getEventsForDate(profile, dateStr);
        const lunar = getLunarDateInfo(calViewYear, calViewMonth, d);

        const cell = document.createElement('button');
        cell.className = `cal-cell rounded-xl p-1.5 border text-left flex flex-col justify-between relative ${
            isSelected
                ? 'bg-amber-400/20 border-2 border-amber-400 shadow-lg'
                : 'bg-slate-900/85 border-white/10 hover:bg-slate-800'
        }`;
        cell.onclick = () => selectCalendarDate(dateStr);

        let dotsHtml = '';
        if (dayEvents.length > 0) {
            dotsHtml = `<span class="px-1.5 py-0.2 rounded-full text-[9px] font-black bg-emerald-500 text-black">${dayEvents.length}</span>`;
        }

        cell.innerHTML = `
            <div class="flex items-start justify-between w-full">
                <span class="text-xs sm:text-sm font-black ${isSelected ? 'text-amber-300' : (isSunday ? 'text-red-400' : 'text-white')}">
                    ${String(d).padStart(2,'0')}
                </span>
                ${dotsHtml}
            </div>
            ${showLunarCalendar ? `
                <div class="text-[9px] font-semibold text-right w-full ${lunar.lDay === 1 || lunar.lDay === 15 ? 'text-red-400 font-bold' : 'text-slate-400'}">
                    ${lunar.shortStr}
                </div>
            ` : ''}
        `;
        grid.appendChild(cell);
    }

    updateSelectedDateBanner();
}

// ================= 3. BIẾN TRẠNG THÁI CHUYẾN BAY & LƯU TRỮ LOCALSTORAGE =================
let currentTaskFilter = "all";
let activeTaskIdForFlight = null;

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
let alarmInterval = null, flightInterval = null, audioCtx = null, cabinNoiseNode = null;
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

let appState = JSON.parse(JSON.stringify(INITIAL_CLEAN_DB));

function loadPersistentState() {
    try {
        let raw = null;
        try { raw = window.parent.localStorage.getItem(STORAGE_KEY); } catch (e) {}
        if (!raw) raw = window.localStorage.getItem(STORAGE_KEY);
        if (raw) {
            const parsed = JSON.parse(raw);
            if (parsed && parsed.members) appState = parsed;
        }
    } catch (e) {}
}

function savePersistentState() {
    try {
        const serialized = JSON.stringify(appState);
        try { window.parent.localStorage.setItem(STORAGE_KEY, serialized); } catch (e) {}
        window.localStorage.setItem(STORAGE_KEY, serialized);
        const ind = document.getElementById('save-status-indicator');
        if (ind) ind.innerHTML = `<span class="text-cyan-400">● Auto-Saved ${getCurrentTimeStr()}</span>`;
    } catch (e) {}
}

loadPersistentState();
let currentMemberKey = appState.lastMember || "huudai";

function calcMinutesBetweenTimes(startStr, endStr) {
    if (!startStr || !endStr) return 45;
    const [sh, sm] = startStr.split(':').map(Number);
    const [eh, em] = endStr.split(':').map(Number);
    let diff = (eh * 60 + em) - (sh * 60 + sm);
    if (diff <= 0) diff += 24 * 60;
    return Math.max(10, diff);
}

function findBestAirportForDuration(targetMins) {
    let bestAirport = AIRPORTS[2];
    let minDiff = 999999;
    AIRPORTS.forEach(a => {
        if (a.code === "SGN") return;
        const dKm = calcDistanceKm(AIRPORTS[0].coords, a.coords);
        const fMins = calcStudyDurationFromDistance(dKm, selectedAircraft);
        const diff = Math.abs(fMins - targetMins);
        if (diff < minDiff) {
            minDiff = diff;
            bestAirport = a;
        }
    });
    return bestAirport;
}

function updateSlotDurationPreview() {
    const s = document.getElementById('new-slot-start').value;
    const e = document.getElementById('new-slot-end').value;
    const mins = calcMinutesBetweenTimes(s, e);
    const matchedAirport = findBestAirportForDuration(mins);
    const previewEl = document.getElementById('calc-slot-mins-preview');
    if (previewEl) {
        previewEl.innerText = `${mins}p (✈️${matchedAirport.code})`;
    }
}

// ================= 4. QUẢ ĐỊA CẦU 3D THREE.JS & BẢN ĐỒ VỆ TINH 2D LEAFLET =================
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
    } catch (err) {
        console.error("ThreeGlobe init error:", err);
    }
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

    document.getElementById('globe-origin-code').innerText = originAirport.code;
    document.getElementById('globe-dest-code').innerText = destAirport.code;
    document.getElementById('globe-plane-svg').innerHTML = getAircraftSVG(selectedAircraft, calcBearingDeg(originAirport.coords, destAirport.coords));
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
}

let map = null;
try {
    if (typeof L !== 'undefined') {
        map = L.map('map', { zoomControl: false, minZoom: 3, maxZoom: 18, zoomSnap: 0.5, zoomDelta: 0.5, wheelPxPerZoomLevel: 120 }).setView([13.5, 107.5], 6);
        L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}', { maxZoom: 18 }).addTo(map);
        L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/Reference/World_Boundaries_and_Places/MapServer/tile/{z}/{y}/{x}', { maxZoom: 18 }).addTo(map);

        map.getContainer().addEventListener('wheel', (e) => {
            if (is2DMapActive && e.deltaY > 0 && map.getZoom() <= 4 && (Date.now() - lastTransitionTime > 650)) activate3DSpaceGlobe();
        }, { passive: true });
    }
} catch (err) {
    console.error("Leaflet init error:", err);
}

let routeLine = null, originMarker = null, destMarker = null, planeMarker = null;

function activate2DSatelliteMap() {
    lastTransitionTime = Date.now(); is2DMapActive = true;
    const t = I18N[currentLang];
    document.getElementById('globe-wrapper').classList.add('globe-hidden');
    document.getElementById('map-2d-wrapper').classList.add('active-2d');
    document.getElementById('projection-mode-badge').innerHTML = "2D";
    document.getElementById('quick-switch-proj-btn').innerHTML = t.btnGlobe3D || "🌍 Quả cầu 3D";
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
    document.getElementById('projection-mode-badge').innerHTML = "3D";
    document.getElementById('quick-switch-proj-btn').innerHTML = t.btnMap2D || "🛰️ Bản đồ 2D";
}

function toggleProjectionMode() { if (is2DMapActive) activate3DSpaceGlobe(); else activate2DSatelliteMap(); }
function zoomStepIn() { if (!is2DMapActive) { targetGlobeZ -= 30; if (targetGlobeZ <= 168) activate2DSatelliteMap(); } else if (map) map.zoomIn(1); }
function zoomStepOut() { if (is2DMapActive) { if (map && map.getZoom() <= 4.5) activate3DSpaceGlobe(); else if (map) map.zoomOut(1); } else targetGlobeZ = Math.min(430, targetGlobeZ + 30); }

// ================= 5. TÍNH GIỜ BAY & MÔ HÌNH MÁY BAY SVG =================
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
    const a = Math.sin(dLat/2) * Math.sin(dLat/2) + Math.cos(coord1[0]*Math.PI/180) * Math.cos(coord2[0]*Math.PI/180) * Math.sin(dLon/2) * Math.sin(dLon/2);
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

    const clockEl = document.getElementById('realtime-clock');
    const dateEl = document.getElementById('realtime-date');
    if (clockEl) clockEl.innerText = `${hh}:${mm}:${ss}`;
    if (dateEl) dateEl.innerText = dateStr;

    const cClock = document.getElementById('cockpit-real-clock');
    const cbClock = document.getElementById('cabin-real-clock');
    if (cClock) cClock.innerText = `${hh}:${mm}:${ss}`;
    if (cbClock) cbClock.innerText = `${hh}:${mm}:${ss}`;

    if (!isFlying) {
        const etaEl = document.getElementById('booking-realtime-eta');
        if (etaEl) etaEl.innerText = `${hh}:${mm} ➔ ${calcRealTimeETA(selectedDuration)}`;
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

// ================= 6. CHUYỂN ĐỔI GÓC NHÌN BUỒNG LÁI / CABIN / CỬA SỔ =================
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
    const t = I18N[currentLang];
    document.getElementById('reading-light-beam').classList.toggle('hidden', !isReadingLightOn);
    const btn = document.getElementById('btn-reading-light');
    if (btn) {
        btn.innerText = t.btnReadingLight;
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
    const profile = appState.members[currentMemberKey];
    alert(`🛎️ Crew: Wishing passenger ${profile.name} (Seat ${selectedSeat}) a productive study flight!`);
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

    document.getElementById('hud-speed').innerText = `${specs.speedKmh} KM/H`;
    document.getElementById('hud-heading').innerText = `${brng}°`;
    document.getElementById('hud-alt').innerText = specs.altFt;
    document.getElementById('hud-aircraft-name').innerText = selectedAircraft.toUpperCase();
    document.getElementById('hud-route-code').innerText = `${originAirport.code} ➔ ${destAirport.code}`;
    document.getElementById('cockpit-plane-svg-preview').innerHTML = getAircraftSVG(selectedAircraft, 0);
    document.getElementById('cockpit-task-display').innerText = `${selectedFocus.icon} ${selectedFocus.label}`;

    document.getElementById('cabin-seat-label').innerText = selectedSeat;
    const winSeatTag = document.getElementById('cabin-window-seat-tag');
    if (winSeatTag) winSeatTag.innerText = selectedSeat;
    document.getElementById('cabin-aircraft-label').innerText = selectedAircraft;
    document.getElementById('cabin-route-label').innerText = `${originAirport.code} ➔ ${destAirport.code}`;
    document.getElementById('cabin-task-title').innerText = `${selectedFocus.icon} ${selectedFocus.label}`;
    document.getElementById('cabin-passenger-name').innerText = profile.name;
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

function switchMemberProfile() {
    currentMemberKey = document.getElementById('member-select').value;
    appState.lastMember = currentMemberKey;
    savePersistentState();
    renderCalendarGrid();
    renderDashboard();
    resetChat();
}

// ================= 7. QUẢN LÝ NHIỆM VỤ & ĐỒNG BỘ LỊCH VẠN NIÊN =================
function calcPriorityScore(task) {
    const urgency = Math.max(5, 100 - task.hoursLeft * 1.4);
    return Math.round(task.importance * 18 + urgency * 0.6);
}

function setTaskFilter(filter) {
    currentTaskFilter = filter;
    ['all', 'pending', 'done'].forEach(f => {
        const el = document.getElementById('filter-' + f);
        el.className = (f === filter) ? "px-2.5 py-1 rounded-lg bg-blue-600 text-white" : "px-2.5 py-1 rounded-lg text-slate-400 hover:text-white";
    });
    renderDashboard();
}

function addNewTask() {
    const titleInput = document.getElementById('quick-task-title');
    const title = titleInput.value.trim();
    if (!title) { titleInput.focus(); return; }
    const hours = parseInt(document.getElementById('quick-task-hours').value) || 24;
    const imp = parseInt(document.getElementById('quick-task-importance').value) || 4;
    const startT = document.getElementById('quick-task-start').value || "19:30";
    const endT = document.getElementById('quick-task-end').value || "20:25";
    const slotStr = `${startT} - ${endT}`;
    const destCode = document.getElementById('quick-task-dest').value || "DAD";

    const targetAirport = AIRPORTS.find(a => a.code === destCode) || AIRPORTS[2];
    const distKm = calcDistanceKm(AIRPORTS[0].coords, targetAirport.coords);
    const autoMins = calcStudyDurationFromDistance(distKm, selectedAircraft);

    const profile = appState.members[currentMemberKey];
    profile.tasks.unshift({
        id: Date.now(), title, hoursLeft: hours, importance: imp, slot: slotStr,
        destCode: targetAirport.code, distKm, duration: autoMins,
        dateStr: selectedFullDate, syncedFromTimetable: false, done: false
    });

    titleInput.value = '';
    savePersistentState();
    renderDashboard();
}

function toggleTaskDone(taskId) {
    const profile = appState.members[currentMemberKey];
    const task = profile.tasks.find(t => t.id === taskId);
    if (task) { task.done = !task.done; savePersistentState(); renderDashboard(); }
}

function deleteTask(taskId) {
    const profile = appState.members[currentMemberKey];
    profile.tasks = profile.tasks.filter(t => t.id !== taskId);
    savePersistentState();
    renderDashboard();
}

function saveNewTimetableSlot() {
    const startT = document.getElementById('new-slot-start').value || "14:00";
    const endT = document.getElementById('new-slot-end').value || "15:30";
    const subjInput = document.getElementById('new-slot-subject');
    const type = document.getElementById('new-slot-type').value;
    const repeatMode = document.getElementById('slot-repeat-mode').value;
    const customInterval = document.getElementById('custom-repeat-interval').value || "2";
    const customUnit = document.getElementById('custom-repeat-unit').value || "tuần";
    const customDur = document.getElementById('custom-repeat-duration').value || "3 tháng";
    const autoSync = document.getElementById('auto-sync-to-flight').checked;

    const subject = subjInput.value.trim();
    if (!subject) { subjInput.focus(); return; }

    const durationMins = calcMinutesBetweenTimes(startT, endT);
    const matchedAirport = findBestAirportForDuration(durationMins);
    const matchedDist = calcDistanceKm(AIRPORTS[0].coords, matchedAirport.coords);

    const [y, m, d] = selectedFullDate.split('-').map(Number);
    const dowName = I18N[currentLang].fullWeekdays[new Date(y, m - 1, d).getDay()];
    const formattedDate = `${String(d).padStart(2,'0')}/${String(m).padStart(2,'0')}/${y}`;

    let repeatLabel = "Chỉ ngày " + formattedDate;
    if (repeatMode === 'daily') repeatLabel = "Lặp hàng ngày";
    else if (repeatMode === 'weekly') repeatLabel = `Hàng tuần (${dowName})`;
    else if (repeatMode === 'monthly') repeatLabel = `Hàng tháng (Ngày ${String(d).padStart(2,'0')} mỗi tháng)`;
    else if (repeatMode === 'yearly') repeatLabel = `Hàng năm (${String(d).padStart(2,'0')}/${String(m).padStart(2,'0')})`;
    else if (repeatMode === 'custom') repeatLabel = `Mỗi ${customInterval} ${customUnit} (Trong ${customDur})`;

    const profile = appState.members[currentMemberKey];
    if (!profile.calendarEvents) profile.calendarEvents = [];

    const slotId = Date.now();
    profile.calendarEvents.push({
        id: slotId,
        dateStr: selectedFullDate,
        formattedDate: formattedDate,
        dowName: dowName,
        time: `${startT} - ${endT}`,
        durationMins: durationMins,
        subject: subject,
        type: type,
        repeatMode: repeatMode,
        customInterval: customInterval,
        customUnit: customUnit,
        repeatLabel: repeatLabel,
        destCode: matchedAirport.code
    });

    if (autoSync) {
        const typePrefix = type === 'personal' ? '💼 [Việc cá nhân]' : (type === 'school' ? '🏫 [Lịch trường]' : '📚 [Lịch học]');
        profile.tasks.unshift({
            id: slotId + 1,
            linkedSlotId: slotId,
            title: `${typePrefix} ${subject} (${dowName}, ${formattedDate})`,
            hoursLeft: 12,
            importance: type === 'personal' ? 4 : 5,
            slot: `${startT} - ${endT}`,
            destCode: matchedAirport.code,
            distKm: matchedDist,
            duration: durationMins,
            scope: repeatLabel,
            syncedFromTimetable: true,
            done: false
        });
    }

    subjInput.value = '';
    savePersistentState();
    renderCalendarGrid();
    renderDashboard();
}

function flyDirectlyFromCalendarEvent(evId) {
    const profile = appState.members[currentMemberKey];
    const ev = (profile.calendarEvents || []).find(e => e.id === evId);
    if (!ev) return;

    originAirport = AIRPORTS[0];
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

function removeCalendarEvent(evId) {
    const profile = appState.members[currentMemberKey];
    profile.calendarEvents = (profile.calendarEvents || []).filter(e => e.id !== evId);
    profile.tasks = (profile.tasks || []).filter(t => t.linkedSlotId !== evId);
    savePersistentState();
    renderCalendarGrid();
    renderDashboard();
}

function renderDashboard() {
    const t = I18N[currentLang];
    const profile = appState.members[currentMemberKey];
    const allTasks = profile.tasks || [];
    const pendingTasks = allTasks.filter(tk => !tk.done);
    const doneTasks = allTasks.filter(tk => tk.done);

    document.getElementById('stat-member-name').innerText = profile.name;
    document.getElementById('stat-pending-count').innerText = pendingTasks.length;
    document.getElementById('stat-done-count').innerText = doneTasks.length;
    document.getElementById('nav-pending-badge').innerText = pendingTasks.length;
    const pct = allTasks.length > 0 ? Math.round((doneTasks.length / allTasks.length) * 100) : 0;
    document.getElementById('stat-done-percent').innerText = `${pct}% (${doneTasks.length}/${allTasks.length})`;
    document.getElementById('stat-miles-count').innerText = `${profile.miles || 0} km`;
    document.getElementById('stat-flights-count').innerText = `${profile.flights || 0}`;
    document.getElementById('timetable-owner-badge').innerText = `(${profile.name})`;

    const banner = document.getElementById('deadline-banner');
    if (pendingTasks.length > 0) {
        const top = pendingTasks[0];
        banner.classList.remove('hidden'); banner.classList.add('flex');
        document.getElementById('deadline-banner-text').innerText = 
            `✈️ ${profile.name}: "${top.title}" • ⏰ ${top.slot} (SGN ➔ ${top.destCode || 'DAD'} • ${top.duration}p)`;
    } else {
        banner.classList.add('hidden'); banner.classList.remove('flex');
    }

    const aiBox = document.getElementById('ai-today-suggestion');
    if (pendingTasks.length > 0) {
        const sorted = [...pendingTasks].sort((a, b) => calcPriorityScore(b) - calcPriorityScore(a));
        const top = sorted[0];
        const dCode = top.destCode || "DAD";
        const dKm = top.distKm || 605;

        aiBox.innerHTML = `
            <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
                <div>
                    <div class="flex flex-wrap items-center gap-2 mb-1">
                        <span class="bg-amber-400 text-black text-[10px] font-black px-2 py-0.5 rounded">🔔 ${top.slot}</span>
                        ${top.scope ? `<span class="bg-emerald-500/20 text-emerald-300 border border-emerald-400/30 text-[10px] font-bold px-2 py-0.5 rounded">🔄 ${top.scope}</span>` : ''}
                        <span class="text-xs text-amber-300">${'⭐'.repeat(top.importance)}</span>
                    </div>
                    <div class="text-sm sm:text-base font-extrabold text-white">${top.title}</div>
                    <div class="text-xs text-cyan-300 mt-1">
                        ✈️ SGN ➔ <b>${dCode} (${dKm} km • ${top.duration} ${t.unitMin})</b>
                    </div>
                </div>
                <div class="flex sm:flex-col gap-2 shrink-0">
                    <button onclick="startFlightFromTask(${top.id})" class="bg-gradient-to-r from-emerald-500 to-cyan-500 hover:opacity-95 text-black font-black px-4 py-2 rounded-xl text-xs shadow-lg whitespace-nowrap">
                        🛫 Fly (${top.duration}m)
                    </button>
                    <button onclick="openWhyModal(${top.id})" class="bg-white/10 hover:bg-white/20 text-white font-bold px-3 py-1.5 rounded-xl text-[11px] whitespace-nowrap">
                        ❓ Info
                    </button>
                </div>
            </div>
        `;
    } else {
        aiBox.innerHTML = `<div class="text-xs text-slate-300 py-1.5">💡 ${t.calSub}</div>`;
    }

    const listEl = document.getElementById('todo-drag-list');
    listEl.innerHTML = '';

    let filteredTasks = allTasks;
    if (currentTaskFilter === 'pending') filteredTasks = pendingTasks;
    if (currentTaskFilter === 'done') filteredTasks = doneTasks;

    if (filteredTasks.length === 0) {
        listEl.innerHTML = `
            <div class="text-center py-8 bg-slate-900/40 rounded-2xl border border-dashed border-white/10">
                <div class="text-xl mb-1">✈️</div>
                <div class="text-xs font-bold text-slate-300">${t.emptyTasks}</div>
            </div>
        `;
    } else {
        filteredTasks.forEach((task) => {
            const realIdx = allTasks.findIndex(tk => tk.id === task.id);
            const dCode = task.destCode || "DAD";
            const dKm = task.distKm || 605;

            const card = document.createElement('div');
            card.draggable = true;
            card.dataset.index = realIdx;
            card.className = `p-3 rounded-2xl border transition cursor-grab active:cursor-grabbing flex flex-col sm:flex-row sm:items-center justify-between gap-2.5 ${
                task.done ? 'bg-emerald-950/20 border-emerald-500/30' : 'bg-slate-900/90 border-white/10 hover:border-cyan-400/40'
            }`;

            card.addEventListener('dragstart', handleDragStart);
            card.addEventListener('dragover', handleDragOver);
            card.addEventListener('drop', handleDrop);
            card.addEventListener('dragend', handleDragEnd);

            card.innerHTML = `
                <div class="flex items-start gap-2.5">
                    <button onclick="toggleTaskDone(${task.id})" class="mt-0.5 w-6 h-6 rounded-full border-2 flex items-center justify-center font-black text-xs transition shrink-0 ${
                        task.done ? 'bg-emerald-500 border-emerald-400 text-black shadow-lg' : 'bg-slate-800 border-slate-500 text-transparent hover:border-emerald-400'
                    }">✓</button>

                    <div>
                        <div class="flex flex-wrap items-center gap-1.5 mb-1">
                            <span class="text-[10px] font-black bg-amber-400 text-black px-2 py-0.5 rounded">⏰ ${task.slot}</span>
                            <span class="text-[10px] font-mono bg-white/10 text-cyan-300 px-2 py-0.5 rounded">✈️ SGN➔${dCode} (${dKm}km • ${task.duration}p)</span>
                            ${task.scope ? `<span class="text-[10px] text-emerald-300 font-bold">🔄 ${task.scope}</span>` : ''}
                        </div>
                        <div class="text-xs sm:text-sm font-extrabold ${task.done ? 'line-through text-slate-400' : 'text-white'}">${task.title}</div>
                    </div>
                </div>

                <div class="flex items-center gap-1.5 shrink-0 self-end sm:self-center">
                    ${!task.done ? `
                        <button onclick="startFlightFromTask(${task.id})" class="bg-gradient-to-r from-blue-600 to-cyan-500 hover:opacity-95 text-white px-3 py-1 rounded-xl text-[11px] font-extrabold shadow">
                            🛫 ${task.duration}m
                        </button>
                    ` : ''}
                    <button onclick="deleteTask(${task.id})" class="bg-red-500/15 hover:bg-red-500/30 text-red-300 px-2 py-1 rounded-xl text-xs font-bold">🗑️</button>
                </div>
            `;
            listEl.appendChild(card);
        });
    }

    const slotsList = document.getElementById('timetable-slots-list');
    slotsList.innerHTML = '';
    const dayEvents = getEventsForDate(profile, selectedFullDate);

    if (dayEvents.length === 0) {
        slotsList.innerHTML = `
            <div class="text-center py-5 bg-slate-900/40 rounded-2xl border border-dashed border-white/10">
                <div class="text-xs font-bold text-slate-300">${t.emptySlots} (${selectedFullDate})</div>
            </div>
        `;
    } else {
        dayEvents.forEach((ev) => {
            let badgeStyle = 'bg-blue-500/20 text-cyan-300 border-cyan-500/30';
            let typeLabel = '📚 Study';
            if (ev.type === 'personal') {
                badgeStyle = 'bg-purple-950/40 text-purple-300 border-purple-400/40';
                typeLabel = '🟣 Personal';
            } else if (ev.type === 'school') {
                badgeStyle = 'bg-red-950/35 text-red-300 border-red-400/30';
                typeLabel = '🔴 School';
            } else if (ev.type === 'free') {
                badgeStyle = 'bg-emerald-950/35 text-emerald-300 border-emerald-400/30';
                typeLabel = '🟢 Free Slot';
            }

            const el = document.createElement('div');
            el.className = `p-3 rounded-2xl border flex items-center justify-between gap-2 ${badgeStyle}`;
            el.innerHTML = `
                <div>
                    <div class="flex flex-wrap items-center gap-1.5">
                        <span class="text-[10px] font-mono font-extrabold px-2 py-0.5 rounded bg-black/40 text-amber-300">⏰ ${ev.time} (${ev.durationMins}p)</span>
                        <span class="text-[10px] font-bold">${typeLabel}</span>
                        <span class="text-[9px] bg-white/10 px-1.5 py-0.5 rounded text-emerald-300 font-bold">🔄 ${ev.repeatLabel}</span>
                    </div>
                    <div class="text-xs font-extrabold text-white mt-1">${ev.subject}</div>
                </div>
                <div class="flex items-center gap-1 shrink-0">
                    <button onclick="flyDirectlyFromCalendarEvent(${ev.id})" class="bg-cyan-500 hover:bg-cyan-400 text-black font-black px-2.5 py-1 rounded-xl text-[10px] shadow">
                        🛫 Fly
                    </button>
                    <button onclick="removeCalendarEvent(${ev.id})" class="bg-red-500/20 hover:bg-red-500/40 text-red-200 px-2 py-1 rounded-xl text-xs font-bold">🗑️</button>
                </div>
            `;
            slotsList.appendChild(el);
        });
    }
}

let dragStartIndex = null;
function handleDragStart() { dragStartIndex = +this.dataset.index; this.classList.add('dragging-card'); }
function handleDragOver(e) { e.preventDefault(); }
function handleDrop() {
    const dragEndIndex = +this.dataset.index;
    if (dragStartIndex === null || dragStartIndex === dragEndIndex) return;
    const tasks = appState.members[currentMemberKey].tasks;
    const [moved] = tasks.splice(dragStartIndex, 1);
    tasks.splice(dragEndIndex, 0, moved);
    savePersistentState();
    renderDashboard();
}
function handleDragEnd() { this.classList.remove('dragging-card'); }

function aiSortTasks() {
    const profile = appState.members[currentMemberKey];
    if (profile.tasks.length === 0) return;
    profile.tasks.sort((a, b) => {
        if (a.done !== b.done) return a.done ? 1 : -1;
        return calcPriorityScore(b) - calcPriorityScore(a);
    });
    savePersistentState();
    renderDashboard();
}

function handleSuddenScheduleChange() {
    const profile = appState.members[currentMemberKey];
    const pending = profile.tasks.filter(tk => !tk.done);
    if (pending.length === 0) return;
    const backupSlots = ["20:00 - 21:00 (Backup)", "21:15 - 22:15 (Late)", "08:00 - 09:00 (Morning)"];
    pending.forEach((tk, i) => { tk.slot = backupSlots[i % backupSlots.length]; });
    savePersistentState();
    renderDashboard();
    alert(`🌪️ Rescheduled ${pending.length} tasks!`);
}

function openWhyModal(taskId) {
    const profile = appState.members[currentMemberKey];
    const task = profile.tasks.find(tk => tk.id === taskId);
    if (!task) return;
    document.getElementById('why-modal-content').innerHTML = `
        <div class="bg-slate-900 p-3 rounded-2xl border border-white/10">
            <div class="text-sm font-extrabold text-white">${task.title}</div>
            <div class="text-xs text-amber-300 font-mono mt-1">⏰ ${task.slot} • 🔄 ${task.scope || '1x'}</div>
        </div>
    `;
    document.getElementById('why-schedule-modal').classList.remove('hidden');
    document.getElementById('why-schedule-modal').classList.add('flex');
}
function closeWhyModal() {
    document.getElementById('why-schedule-modal').classList.add('hidden');
    document.getElementById('why-schedule-modal').classList.remove('flex');
}

function sendStudyReminderAlert() {
    const profile = appState.members[currentMemberKey];
    const pending = profile.tasks.filter(tk => !tk.done);
    if (pending.length === 0) alert(`🔔 ${profile.name}: 0 pending flights!`);
    else alert(`⏰ ${profile.name}: "${pending[0].title}" (${pending[0].slot} • ${pending[0].duration} mins)!`);
}

function startFocusFromTopTask() {
    const profile = appState.members[currentMemberKey];
    const pending = profile.tasks.filter(tk => !tk.done).sort((a,b) => calcPriorityScore(b) - calcPriorityScore(a));
    if (pending[0]) startFlightFromTask(pending[0].id);
}

function startFlightFromTask(taskId) {
    const profile = appState.members[currentMemberKey];
    const task = profile.tasks.find(tk => tk.id === taskId);
    if (!task) return;

    activeTaskIdForFlight = task.id;
    originAirport = AIRPORTS[0];
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

// ================= 8. LOGIC ĐẶT VÉ, CHỌN GHẾ & BOARDING PASS =================
function toggleBookingCardSize() {
    const card = document.getElementById('screen-booking');
    const btn = document.getElementById('toggle-booking-btn');
    const t = I18N[currentLang];
    isBookingCollapsed = !isBookingCollapsed;
    if (isBookingCollapsed) { card.classList.add('translate-y-[130%]'); btn.innerText = t.btnExpand; }
    else { card.classList.remove('translate-y-[130%]'); btn.innerText = t.btnCollapse; }
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
        let html = `<optgroup label="${t.vnGroup}" class="bg-slate-900">`;
        vnAirports.forEach(a => {
            const dist = calcDistanceKm(AIRPORTS[0].coords, a.coords);
            const mins = calcStudyDurationFromDistance(dist, "Airbus A321neo");
            html += `<option value="${a.code}">${a.code} - ${a.name} ${withTimeHint ? `(~${mins}m)` : ''}</option>`;
        });
        html += `</optgroup><optgroup label="${t.intGroup}" class="bg-slate-900">`;
        intAirports.forEach(a => {
            const dist = calcDistanceKm(AIRPORTS[0].coords, a.coords);
            const mins = calcStudyDurationFromDistance(dist, "Airbus A321neo");
            html += `<option value="${a.code}">${a.code} - ${a.name} ${withTimeHint ? `(~${mins}m)` : ''}</option>`;
        });
        html += `</optgroup>`;
        return html;
    };

    if (oSel) { oSel.innerHTML = buildOptions(false); oSel.value = prevOrigin; }
    if (dSel) { dSel.innerHTML = buildOptions(false); dSel.value = prevDest; }
    if (qSel) { qSel.innerHTML = buildOptions(true); qSel.value = prevQuick; }
}

function onRouteChange() {
    const oCode = document.getElementById('origin-select').value;
    const dCode = document.getElementById('dest-select').value;
    if (oCode === dCode) {
        const alt = AIRPORTS.find(a => a.code !== oCode);
        document.getElementById('dest-select').value = alt.code;
    }
    originAirport = AIRPORTS.find(a => a.code === document.getElementById('origin-select').value) || AIRPORTS[0];
    destAirport = AIRPORTS.find(a => a.code === document.getElementById('dest-select').value) || AIRPORTS[2];
    currentDistance = calcDistanceKm(originAirport.coords, destAirport.coords);
    selectedDuration = calcStudyDurationFromDistance(currentDistance, selectedAircraft);
    updateBookingUI();
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
    document.getElementById('booking-plane-svg-box').innerHTML = getAircraftSVG(selectedAircraft, 45);
    document.getElementById('badge-origin').innerText = originAirport.code;
    document.getElementById('badge-dest').innerText = destAirport.code;
    document.getElementById('badge-dist').innerText = `${currentDistance} km`;
    document.getElementById('banner-dest-title').innerText = `${originAirport.name.split(' (')[0]} ➔ ${destAirport.name}`;
    document.getElementById('auto-calc-duration-text').innerText = formatDurationLabel(selectedDuration);
    document.getElementById('auto-calc-speed-text').innerText = `(${currentDistance} km • ${specs.speedKmh} km/h)`;

    const now = new Date();
    document.getElementById('booking-realtime-eta').innerText = `${String(now.getHours()).padStart(2,'0')}:${String(now.getMinutes()).padStart(2,'0')} ➔ ${calcRealTimeETA(selectedDuration)}`;

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

function renderSeats() {
    const grid = document.getElementById('seat-grid');
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
    document.getElementById('seat-selected-badge').innerText = seatCode;
    document.getElementById('pop-seat-code').innerText = seatCode;
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
    document.getElementById('seat-header-aircraft').innerText = selectedAircraft;
    document.getElementById('seat-header-route').innerText = `${originAirport.code} ➔ ${destAirport.code} (${currentDistance} km • ${selectedDuration} ${t.unitMin})`;
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

    document.getElementById('tk-aircraft').innerText = selectedAircraft;
    document.getElementById('tk-passenger').innerText = profile.name;
    document.getElementById('tk-realtime-span').innerText = `${stdStr} ➔ ${flightEtaString}`;
    document.getElementById('tk-strict-badge').innerText = strictModeEnabled ? "🔒 STRICT LOCK ON" : "🔓 FREE MODE";
    document.getElementById('tk-origin-code').innerText = originAirport.code;
    document.getElementById('tk-origin-name').innerText = originAirport.name.split(' (')[0];
    document.getElementById('tk-dest-code').innerText = destAirport.code;
    document.getElementById('tk-dest-name').innerText = destAirport.name.split(' (')[0];
    document.getElementById('tk-duration').innerText = `${selectedDuration} ${t.unitMin}`;
    document.getElementById('tk-seat').innerText = selectedSeat;
    document.getElementById('tk-dist').innerText = currentDistance + ' km';
    document.getElementById('tk-focus').innerText = `${selectedFocus.icon} ${selectedFocus.label}`;
    document.getElementById('tk-plane-svg').innerHTML = getAircraftSVG(selectedAircraft, 90);

    document.getElementById('screen-ticket').classList.remove('hidden');
    document.getElementById('screen-ticket').classList.add('flex');
}

function backToSeatFromTicket() {
    document.getElementById('screen-ticket').classList.add('hidden');
    document.getElementById('screen-ticket').classList.remove('flex');
    document.getElementById('screen-seat').classList.remove('hidden');
    document.getElementById('screen-seat').classList.add('flex');
}

// ================= 9. VẬN HÀNH CHUYẾN BAY & STRICT MODE =================
function playCabinDingDong() {
    try {
        if (!audioCtx) audioCtx = new (window.AudioContext || window.webkitAudioContext)();
        const now = audioCtx.currentTime;
        const osc1 = audioCtx.createOscillator(), osc2 = audioCtx.createOscillator(), gain = audioCtx.createGain();
        osc1.frequency.setValueAtTime(659.25, now);
        osc2.frequency.setValueAtTime(523.25, now + 0.35);
        gain.gain.setValueAtTime(0.18, now);
        gain.gain.exponentialRampToValueAtTime(0.001, now + 1.2);
        osc1.connect(gain); osc2.connect(gain); gain.connect(audioCtx.destination);
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
    document.getElementById('fly-eta-badge').innerText = flightEtaString;
    document.getElementById('cockpit-eta').innerText = flightEtaString;
    document.getElementById('cabin-eta').innerText = flightEtaString;

    document.getElementById('fly-mini-svg').innerHTML = getAircraftSVG(selectedAircraft, 45);
    document.getElementById('fly-route-text').innerText = `${originAirport.code} ➔ ${destAirport.code}`;
    document.getElementById('fly-sub-info').innerText = `${selectedAircraft.split(' ')[1] || selectedAircraft} • ${selectedSeat} • ${selectedFocus.icon} ${selectedFocus.label}`;

    totalFlightSeconds = selectedDuration * 60;
    remainingSeconds = totalFlightSeconds;

    if (map && typeof L !== 'undefined') {
        if (planeMarker) map.removeLayer(planeMarker);
        planeMarker = L.marker(originAirport.coords, { icon: createCustomAircraftMapIcon(), zIndexOffset: 1000 }).addTo(map);
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

    if (activeTaskIdForFlight) {
        const task = profile.tasks.find(tk => tk.id === activeTaskIdForFlight);
        if (task) task.done = true;
        activeTaskIdForFlight = null;
    }
    savePersistentState();
    alert(`🎉 ${selectedAircraft} (${originAirport.code} ➔ ${destAirport.code}) Landed! +${currentDistance} km!`);
    abortFlight();
    switchPage('dashboard');
}

function updateSafetyHearts() {
    const left = Math.max(0, MAX_VIOLATIONS - violationCount);
    document.getElementById('safety-hearts').innerText = '❤️'.repeat(left) + '🖤'.repeat(MAX_VIOLATIONS - left);
}

function playCockpitAlarmBeep() {
    try {
        if (!audioCtx) audioCtx = new (window.AudioContext || window.webkitAudioContext)();
        const osc = audioCtx.createOscillator(), gain = audioCtx.createGain();
        osc.type = 'sawtooth';
        osc.frequency.setValueAtTime(880, audioCtx.currentTime);
        osc.frequency.setValueAtTime(440, audioCtx.currentTime + 0.18);
        gain.gain.setValueAtTime(0.2, audioCtx.currentTime);
        osc.connect(gain); gain.connect(audioCtx.destination);
        osc.start(); osc.stop(audioCtx.currentTime + 0.35);
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
    document.getElementById('violation-count-text').innerText = `${violationCount} / ${MAX_VIOLATIONS}`;
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

    document.getElementById('countdown-timer').innerText = timeFormatted;
    document.getElementById('cockpit-timer-display').innerText = timeFormatted;
    document.getElementById('cabin-timer-display').innerText = timeFormatted;

    currentFlightProgress = (totalFlightSeconds - remainingSeconds) / totalFlightSeconds;
    document.getElementById('flight-progress').style.width = `${currentFlightProgress * 100}%`;

    const distLeft = Math.max(0, Math.round(currentDistance * (1 - currentFlightProgress)));
    document.getElementById('fly-dist-left').innerText = distLeft;
    document.getElementById('cockpit-dist-display').innerText = `${distLeft} KM`;
    document.getElementById('cabin-dist-display').innerText = distLeft;

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
    setCameraView('map');
    document.getElementById('screen-flying').classList.add('hidden');
    document.getElementById('screen-booking').classList.remove('hidden');
    document.getElementById('toggle-booking-btn').classList.remove('hidden');
    updateBookingUI();
}

// ================= 10. CHATBOT AI ĐA NGÔN NGỮ & ÂM THANH LOFI =================
function toggleChatbotWindow() {
    const win = document.getElementById('chatbot-window');
    win.classList.toggle('hidden'); win.classList.toggle('flex');
}

function getCurrentTimeStr() {
    const now = new Date();
    return `${String(now.getHours()).padStart(2,'0')}:${String(now.getMinutes()).padStart(2,'0')}`;
}

function sendQuickChat(text) { document.getElementById('chat-input').value = text; sendChatMessage(); }

function sendChatMessage() {
    const input = document.getElementById('chat-input');
    const text = input.value.trim();
    if (!text) return;
    input.value = '';

    const box = document.getElementById('chat-messages');
    box.innerHTML += `<div class="flex flex-col items-end"><div class="bg-[#d4a349] text-white font-semibold text-xs px-3.5 py-2 rounded-2xl rounded-tr-sm shadow-sm max-w-[82%]">${text}</div><span class="text-[9px] text-slate-400 mt-0.5">${getCurrentTimeStr()}</span></div>`;
    box.scrollTop = box.scrollHeight;

    setTimeout(() => {
        const reply = generateSmartBotReply(text);
        const botAvatar = document.getElementById('bot-launcher-img').src;
        box.innerHTML += `<div class="flex items-start gap-2"><img src="${botAvatar}" class="w-7 h-7 rounded-full bg-amber-400 p-0.5 border border-[#d4a349] shrink-0 mt-1 object-cover" /><div class="max-w-[84%]"><div class="bg-[#fae5be] p-1 rounded-2xl rounded-tl-sm shadow-sm"><div class="bg-white rounded-xl p-2.5 text-xs text-slate-800 leading-relaxed">${reply}</div></div><span class="text-[9px] text-slate-400 mt-0.5 block">${getCurrentTimeStr()}</span></div></div>`;
        box.scrollTop = box.scrollHeight;
    }, 250);
}

function generateSmartBotReply(q) {
    const profile = appState.members[currentMemberKey];
    const pending = profile.tasks.filter(tk => !tk.done);
    if (currentLang === 'zh') {
        return `您好 <b>${profile.name}</b>！🇹🇼<br>目前您有 <b>${pending.length} 項待辦任務</b>。您可以點擊右側萬年曆選擇日期與重複週期（每週、每月同日或自訂週期），系統將自動為您安排專注航班！`;
    }
    if (currentLang === 'en') {
        return `Hello <b>${profile.name}</b>! 🇬🇧<br>You currently have <b>${pending.length} pending tasks</b>. Pick any date on the monthly calendar and set your custom recurrence!`;
    }
    return `Chào <b>${profile.name}</b>! 🇻🇳<br>Hiện bạn có <b>${pending.length} nhiệm vụ</b> đang chờ. Bạn có thể bấm chọn trực tiếp ngày trên tờ Lịch Tháng (có cả Âm lịch & Thứ) và chọn chu kỳ lặp lại tùy ý nhé!`;
}

function resetChat() {
    const profile = appState.members[currentMemberKey];
    const botAvatar = document.getElementById('bot-launcher-img').src;
    let welcome = `Xin chào <b>${profile.name}</b>! 🙋‍♀️<br>Đã tích hợp Lịch Vạn Niên (Thứ/Ngày/Tháng/Năm + Âm lịch), Chu kỳ lặp lại tùy chọn và 3 ngôn ngữ (Việt / Anh / Đài Phồn Thể)!`;
    if (currentLang === 'zh') welcome = `您好 <b>${profile.name}</b>！🙋‍♀️<br>我是您的 AI 學習助理。系統已支援繁體中文、國農曆月曆與自訂重複週期！`;
    else if (currentLang === 'en') welcome = `Hello <b>${profile.name}</b>! 🙋‍♀️<br>Monthly Calendar with Lunar dates, Custom Recurrence & 3 Languages (VI / EN / 繁體) are ready!`;

    document.getElementById('chat-messages').innerHTML = `
        <div class="flex items-start gap-2">
            <img src="${botAvatar}" class="w-7 h-7 rounded-full bg-amber-400 p-0.5 border border-[#d4a349] shrink-0 mt-1 object-cover" />
            <div>
                <div class="bg-[#fae5be] p-1 rounded-2xl rounded-tl-sm shadow-sm">
                    <div class="bg-white rounded-xl p-2.5 text-xs text-slate-800 leading-relaxed">${welcome}</div>
                </div>
                <span class="text-[9px] text-slate-400 mt-0.5 block">${getCurrentTimeStr()}</span>
            </div>
        </div>
    `;
}

function handleBotAvatarUpload(input) {
    if (input.files && input.files[0]) {
        const url = URL.createObjectURL(input.files[0]);
        document.getElementById('bot-launcher-img').src = url;
        document.getElementById('bot-header-img').src = url;
        resetChat();
    }
}

function toggleLofi() {
    const p = document.getElementById('lofi-player');
    const eq = document.getElementById('eq-icon');
    const txt = document.getElementById('lofi-btn-text');
    if (p.paused) { p.play().then(() => { eq.classList.remove('hidden'); eq.classList.add('flex'); txt.innerText = "Playing"; }).catch(() => {}); }
    else { p.pause(); eq.classList.add('hidden'); eq.classList.remove('flex'); txt.innerText = "🎵 Lofi"; }
}

function toggleCabinNoise(enable) {
    if (enable) {
        if (!audioCtx) audioCtx = new (window.AudioContext || window.webkitAudioContext)();
        const bufferSize = 2 * audioCtx.sampleRate;
        const noiseBuffer = audioCtx.createBuffer(1, bufferSize, audioCtx.sampleRate);
        const output = noiseBuffer.getChannelData(0);
        let lastOut = 0.0;
        for (let i = 0; i < bufferSize; i++) {
            const white = Math.random() * 2 - 1;
            output[i] = (lastOut + (0.02 * white)) / 1.02;
            lastOut = output[i]; output[i] *= 0.15;
        }
        cabinNoiseNode = audioCtx.createBufferSource();
        cabinNoiseNode.buffer = noiseBuffer; cabinNoiseNode.loop = true;
        cabinNoiseNode.connect(audioCtx.destination); cabinNoiseNode.start(0);
    } else if (cabinNoiseNode) {
        cabinNoiseNode.stop(); cabinNoiseNode.disconnect(); cabinNoiseNode = null;
    }
}

function openMediaModal() { document.getElementById('media-modal').classList.remove('hidden'); document.getElementById('media-modal').classList.add('flex'); }
function closeMediaModal() { document.getElementById('media-modal').classList.add('hidden'); document.getElementById('media-modal').classList.remove('flex'); }
function handleLocalAudio(input) {
    if (input.files && input.files[0]) {
        const url = URL.createObjectURL(input.files[0]);
        const p = document.getElementById('lofi-player');
        p.src = url; p.play();
        document.getElementById('eq-icon').classList.remove('hidden');
        document.getElementById('eq-icon').classList.add('flex');
    }
}
function applyCustomMedia() {
    const aUrl = document.getElementById('audio-url-input').value.trim();
    if (aUrl) { const p = document.getElementById('lofi-player'); p.src = aUrl; p.play(); }
    closeMediaModal();
}

// ================= 11. KHỞI CHẠY TOÀN BỘ HỆ THỐNG =================
document.getElementById('member-select').value = currentMemberKey;
initThreeGlobe();
updateRealTimeClock();
initAirportDropdowns();
syncEnvironmentWithRealTime();
updateSlotDurationPreview();
onRouteChange();
renderCalendarGrid();
renderDashboard();
resetChat();
