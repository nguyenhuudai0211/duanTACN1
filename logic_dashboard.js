// ================= 0. KHỞI TẠO BIẾN TOÀN CỤC & DỰ PHÒNG =================
if (typeof currentLang === 'undefined') { window.currentLang = "vi"; }
if (typeof showLunarCalendar === 'undefined') { window.showLunarCalendar = true; }

let calViewYear = 2026;
let calViewMonth = 11;
let selectedFullDate = "2026-11-04";
let currentTaskFilter = "all";
let activeTaskIdForFlight = null;
let dragStartIndex = null;

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

// ================= 1. CHUYỂN ĐỔI 3 NGÔN NGỮ TOÀN HỆ THỐNG =================
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

    // Dịch giao diện Đặt vé & Chuyến bay
    setTextIfExist('lbl-origin-title', t.originTitle);
    setTextIfExist('lbl-dest-title', t.destTitle);
    setTextIfExist('lbl-auto-dur-title', t.autoDurTitle);
    setTextIfExist('lbl-btn-pick-seat', t.btnPickSeat);
    setTextIfExist('lbl-btn-fly-now', t.btnFlyNow);
    if (typeof isBookingCollapsed !== 'undefined') {
        setTextIfExist('toggle-booking-btn', isBookingCollapsed ? t.btnExpand : t.btnCollapse);
    }
    if (typeof is2DMapActive !== 'undefined') {
        setTextIfExist('quick-switch-proj-btn', is2DMapActive ? t.btnGlobe3D : t.btnMap2D);
    }

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

    if (typeof initAirportDropdowns === 'function') initAirportDropdowns();
    if (typeof updateBookingUI === 'function') updateBookingUI();
    if (typeof updateRealTimeClock === 'function') updateRealTimeClock();
    if (typeof updateWowLabelsByLang === 'function') updateWowLabelsByLang();
    renderCalendarGrid();
    renderDashboard();
    resetChat();
}

// ================= 2. LỊCH VẠN NIÊN & ÂM LỊCH =================
function getLunarDateInfo(year, month, day) {
    try {
        const dateObj = new Date(year, month - 1, day);
        const parts = new Intl.DateTimeFormat('en-u-ca-chinese', { day: 'numeric', month: 'numeric' }).formatToParts(dateObj);
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
            lDay, lMonth,
            shortStr: (lDay === 1 || day === 1) ? `${lDay}/${lMonth}` : `${lDay}`,
            fullVi: `Ngày ${String(lDay).padStart(2,'0')}/${String(lMonth).padStart(2,'0')} Âm lịch • Ngày ${canChiVi}`,
            fullEn: `Lunar Date: ${String(lDay).padStart(2,'0')}/${String(lMonth).padStart(2,'0')} (${canChiVi})`,
            fullZh: `農曆 ${lMonth}月${lDay}日 • ${canChiZh}`
        };
    } catch (e) {
        return { lDay: day, lMonth: month, shortStr: `${day}`, fullVi: "Âm lịch", fullEn: "Lunar", fullZh: "農曆" };
    }
}

function toggleLunarDisplay() {
    showLunarCalendar = !showLunarCalendar;
    const t = I18N[currentLang];
    setTextIfExist('btn-toggle-lunar', showLunarCalendar ? t.lunarOn : t.lunarOff);
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
    calViewYear = y; calViewMonth = m;
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
    return (profile.calendarEvents || []).filter(ev => doesEventMatchDate(ev, dateStr));
}

function updateSelectedDateBanner() {
    const [y, m, d] = selectedFullDate.split('-').map(Number);
    const dow = new Date(y, m - 1, d).getDay();
    const t = I18N[currentLang];
    const dowName = t.fullWeekdays[dow];
    const lunar = getLunarDateInfo(y, m, d);

    const bannerEl = document.getElementById('selected-full-date-banner');
    const lunarEl = document.getElementById('selected-lunar-date-banner');
    if (!bannerEl || !lunarEl) return;

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
    setTextIfExist('calendar-header-title', `${t.monthPrefix} ${String(calViewMonth).padStart(2,'0')} - ${calViewYear}`);
    const grid = document.getElementById('calendar-days-grid');
    if (!grid) return;
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
        const isSunday = (new Date(calViewYear, calViewMonth - 1, d).getDay() === 0);
        const dayEvents = getEventsForDate(profile, dateStr);
        const lunar = getLunarDateInfo(calViewYear, calViewMonth, d);

        const cell = document.createElement('button');
        cell.className = `cal-cell rounded-xl p-1.5 border text-left flex flex-col justify-between relative ${
            isSelected ? 'bg-amber-400/20 border-2 border-amber-400 shadow-lg' : 'bg-slate-900/85 border-white/10 hover:bg-slate-800'
        }`;
        cell.onclick = () => selectCalendarDate(dateStr);

        const dotsHtml = dayEvents.length > 0 ? `<span class="px-1.5 py-0.2 rounded-full text-[9px] font-black bg-emerald-500 text-black">${dayEvents.length}</span>` : '';
        cell.innerHTML = `
            <div class="flex items-start justify-between w-full">
                <span class="text-xs sm:text-sm font-black ${isSelected ? 'text-amber-300' : (isSunday ? 'text-red-400' : 'text-white')}">${String(d).padStart(2,'0')}</span>
                ${dotsHtml}
            </div>
            ${showLunarCalendar ? `<div class="text-[9px] font-semibold text-right w-full ${lunar.lDay === 1 || lunar.lDay === 15 ? 'text-red-400 font-bold' : 'text-slate-400'}">${lunar.shortStr}</div>` : ''}
        `;
        grid.appendChild(cell);
    }
    updateSelectedDateBanner();
}

// ================= 3. QUẢN LÝ NHIỆM VỤ, KÉO THẢ & ĐỒNG BỘ LỊCH =================
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
    const baseCoords = (typeof originAirport !== 'undefined' && originAirport) ? originAirport.coords : AIRPORTS[0].coords;
    const baseCode = (typeof originAirport !== 'undefined' && originAirport) ? originAirport.code : "SGN";
    AIRPORTS.forEach(a => {
        if (a.code === baseCode) return;
        const dKm = calcDistanceKm(baseCoords, a.coords);
        const fMins = calcStudyDurationFromDistance(dKm, selectedAircraft || "Airbus A321neo");
        const diff = Math.abs(fMins - targetMins);
        if (diff < minDiff) { minDiff = diff; bestAirport = a; }
    });
    return bestAirport;
}

function updateSlotDurationPreview() {
    const s = document.getElementById('new-slot-start').value;
    const e = document.getElementById('new-slot-end').value;
    const mins = calcMinutesBetweenTimes(s, e);
    const matchedAirport = findBestAirportForDuration(mins);
    setTextIfExist('calc-slot-mins-preview', `${mins}p (✈️${matchedAirport.code})`);
}

function calcPriorityScore(task) {
    const urgency = Math.max(5, 100 - task.hoursLeft * 1.4);
    return Math.round(task.importance * 18 + urgency * 0.6);
}

function setTaskFilter(filter) {
    currentTaskFilter = filter;
    ['all', 'pending', 'done'].forEach(f => {
        const el = document.getElementById('filter-' + f);
        if (el) el.className = (f === filter) ? "px-2.5 py-1 rounded-lg bg-blue-600 text-white" : "px-2.5 py-1 rounded-lg text-slate-400 hover:text-white";
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
    const destCode = document.getElementById('quick-task-dest').value || "DAD";

    const baseOrigin = (typeof originAirport !== 'undefined' && originAirport) ? originAirport : AIRPORTS[0];
    const targetAirport = AIRPORTS.find(a => a.code === destCode) || AIRPORTS[2];
    const distKm = calcDistanceKm(baseOrigin.coords, targetAirport.coords);
    const autoMins = calcStudyDurationFromDistance(distKm, selectedAircraft);

    const profile = appState.members[currentMemberKey];
    profile.tasks.unshift({
        id: Date.now(), title, hoursLeft: hours, importance: imp, slot: `${startT} - ${endT}`,
        originCode: baseOrigin.code, destCode: targetAirport.code, distKm, duration: autoMins,
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

    const baseOrigin = (typeof originAirport !== 'undefined' && originAirport) ? originAirport : AIRPORTS[0];
    const durationMins = calcMinutesBetweenTimes(startT, endT);
    const matchedAirport = findBestAirportForDuration(durationMins);
    const matchedDist = calcDistanceKm(baseOrigin.coords, matchedAirport.coords);

    const [y, m, d] = selectedFullDate.split('-').map(Number);
    const dowName = I18N[currentLang].fullWeekdays[new Date(y, m - 1, d).getDay()];
    const formattedDate = `${String(d).padStart(2,'0')}/${String(m).padStart(2,'0')}/${y}`;

    let repeatLabel = "Chỉ ngày " + formattedDate;
    if (repeatMode === 'daily') repeatLabel = "Lặp hàng ngày";
    else if (repeatMode === 'weekly') repeatLabel = `Hàng tuần (${dowName})`;
    else if (repeatMode === 'monthly') repeatLabel = `Hàng tháng (Ngày ${String(d).padStart(2,'0')})`;
    else if (repeatMode === 'yearly') repeatLabel = `Hàng năm (${String(d).padStart(2,'0')}/${String(m).padStart(2,'0')})`;
    else if (repeatMode === 'custom') repeatLabel = `Mỗi ${customInterval} ${customUnit} (${customDur})`;

    const profile = appState.members[currentMemberKey];
    if (!profile.calendarEvents) profile.calendarEvents = [];

    const slotId = Date.now();
    profile.calendarEvents.push({
        id: slotId, dateStr: selectedFullDate, formattedDate, dowName,
        time: `${startT} - ${endT}`, durationMins, subject, type, repeatMode,
        customInterval, customUnit, repeatLabel, originCode: baseOrigin.code, destCode: matchedAirport.code
    });

    if (autoSync) {
        const typePrefix = type === 'personal' ? '💼 [Việc cá nhân]' : (type === 'school' ? '🏫 [Lịch trường]' : '📚 [Lịch học]');
        profile.tasks.unshift({
            id: slotId + 1, linkedSlotId: slotId,
            title: `${typePrefix} ${subject} (${dowName}, ${formattedDate})`,
            hoursLeft: 12, importance: type === 'personal' ? 4 : 5,
            slot: `${startT} - ${endT}`, originCode: baseOrigin.code, destCode: matchedAirport.code,
            distKm: matchedDist, duration: durationMins, scope: repeatLabel,
            syncedFromTimetable: true, done: false
        });
    }

    subjInput.value = '';
    savePersistentState();
    renderCalendarGrid();
    renderDashboard();
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
    const homeCode = (typeof getMemberHomeAirportCode === 'function') ? getMemberHomeAirportCode(currentMemberKey) : "SGN";

    setTextIfExist('stat-member-name', profile.name);
    setTextIfExist('stat-pending-count', pendingTasks.length);
    setTextIfExist('stat-done-count', doneTasks.length);
    setTextIfExist('nav-pending-badge', pendingTasks.length);
    const pct = allTasks.length > 0 ? Math.round((doneTasks.length / allTasks.length) * 100) : 0;
    setTextIfExist('stat-done-percent', `${pct}% (${doneTasks.length}/${allTasks.length})`);
    setTextIfExist('stat-miles-count', `${profile.miles || 0} km`);
    setTextIfExist('stat-flights-count', `${profile.flights || 0}`);
    setTextIfExist('timetable-owner-badge', `(${profile.name} • ✈️${homeCode})`);

    if (typeof updateVipBadgeOnDashboard === 'function') updateVipBadgeOnDashboard();

    const banner = document.getElementById('deadline-banner');
    if (banner) {
        if (pendingTasks.length > 0) {
            const top = pendingTasks[0];
            banner.classList.remove('hidden'); banner.classList.add('flex');
            setTextIfExist('deadline-banner-text', `✈️ ${profile.name}: "${top.title}" • ⏰ ${top.slot} (${top.originCode || homeCode} ➔ ${top.destCode || 'DAD'} • ${top.duration}p)`);
        } else {
            banner.classList.add('hidden'); banner.classList.remove('flex');
        }
    }

    const aiBox = document.getElementById('ai-today-suggestion');
    if (aiBox) {
        if (pendingTasks.length > 0) {
            const sorted = [...pendingTasks].sort((a, b) => calcPriorityScore(b) - calcPriorityScore(a));
            const top = sorted[0];
            const oCode = top.originCode || homeCode;
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
                        <div class="text-xs text-cyan-300 mt-1">✈️ ${oCode} ➔ <b>${dCode} (${dKm} km • ${top.duration} ${t.unitMin || 'phút'})</b></div>
                    </div>
                    <div class="flex sm:flex-col gap-2 shrink-0">
                        <button onclick="startFlightFromTask(${top.id})" class="bg-gradient-to-r from-emerald-500 to-cyan-500 hover:opacity-95 text-black font-black px-4 py-2 rounded-xl text-xs shadow-lg whitespace-nowrap">🛫 Bay (${top.duration}p)</button>
                        <button onclick="openWhyModal(${top.id})" class="bg-white/10 hover:bg-white/20 text-white font-bold px-3 py-1.5 rounded-xl text-[11px] whitespace-nowrap">❓ Info</button>
                    </div>
                </div>
            `;
        } else {
            aiBox.innerHTML = `<div class="text-xs text-slate-300 py-1.5">💡 ${t.calSub}</div>`;
        }
    }

    const listEl = document.getElementById('todo-drag-list');
    if (listEl) {
        listEl.innerHTML = '';
        let filteredTasks = allTasks;
        if (currentTaskFilter === 'pending') filteredTasks = pendingTasks;
        if (currentTaskFilter === 'done') filteredTasks = doneTasks;

        if (filteredTasks.length === 0) {
            listEl.innerHTML = `<div class="text-center py-8 bg-slate-900/40 rounded-2xl border border-dashed border-white/10"><div class="text-xl mb-1">✈️</div><div class="text-xs font-bold text-slate-300">${t.emptyTasks}</div></div>`;
        } else {
            filteredTasks.forEach((task) => {
                const realIdx = allTasks.findIndex(tk => tk.id === task.id);
                const oCode = task.originCode || homeCode;
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
                                <span class="text-[10px] font-mono bg-white/10 text-cyan-300 px-2 py-0.5 rounded">✈️ ${oCode}➔${dCode} (${dKm}km • ${task.duration}p)</span>
                                ${task.scope ? `<span class="text-[10px] text-emerald-300 font-bold">🔄 ${task.scope}</span>` : ''}
                            </div>
                            <div class="text-xs sm:text-sm font-extrabold ${task.done ? 'line-through text-slate-400' : 'text-white'}">${task.title}</div>
                        </div>
                    </div>
                    <div class="flex items-center gap-1.5 shrink-0 self-end sm:self-center">
                        ${!task.done ? `<button onclick="startFlightFromTask(${task.id})" class="bg-gradient-to-r from-blue-600 to-cyan-500 hover:opacity-95 text-white px-3 py-1 rounded-xl text-[11px] font-extrabold shadow">🛫 Bay (${task.duration}p)</button>` : ''}
                        <button onclick="deleteTask(${task.id})" class="bg-red-500/15 hover:bg-red-500/30 text-red-300 px-2 py-1 rounded-xl text-xs font-bold">🗑️</button>
                    </div>
                `;
                listEl.appendChild(card);
            });
        }
    }

    const slotsList = document.getElementById('timetable-slots-list');
    if (slotsList) {
        slotsList.innerHTML = '';
        const dayEvents = getEventsForDate(profile, selectedFullDate);
        if (dayEvents.length === 0) {
            slotsList.innerHTML = `<div class="text-center py-5 bg-slate-900/40 rounded-2xl border border-dashed border-white/10"><div class="text-xs font-bold text-slate-300">${t.emptySlots} (${selectedFullDate})</div></div>`;
        } else {
            dayEvents.forEach((ev) => {
                let badgeStyle = 'bg-blue-500/20 text-cyan-300 border-cyan-500/30';
                let typeLabel = '📚 Study';
                if (ev.type === 'personal') { badgeStyle = 'bg-purple-950/40 text-purple-300 border-purple-400/40'; typeLabel = '🟣 Personal'; }
                else if (ev.type === 'school') { badgeStyle = 'bg-red-950/35 text-red-300 border-red-400/30'; typeLabel = '🔴 School'; }
                else if (ev.type === 'free') { badgeStyle = 'bg-emerald-950/35 text-emerald-300 border-emerald-400/30'; typeLabel = '🟢 Free'; }

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
                        <button onclick="flyDirectlyFromCalendarEvent(${ev.id})" class="bg-cyan-500 hover:bg-cyan-400 text-black font-black px-2.5 py-1 rounded-xl text-[10px] shadow">🛫 Bay</button>
                        <button onclick="removeCalendarEvent(${ev.id})" class="bg-red-500/20 hover:bg-red-500/40 text-red-200 px-2 py-1 rounded-xl text-xs font-bold">🗑️</button>
                    </div>
                `;
                slotsList.appendChild(el);
            });
        }
    }
}

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
    if (!profile.tasks || profile.tasks.length === 0) return;
    profile.tasks.sort((a, b) => (a.done !== b.done) ? (a.done ? 1 : -1) : (calcPriorityScore(b) - calcPriorityScore(a)));
    savePersistentState();
    renderDashboard();
}

function handleSuddenScheduleChange() {
    const profile = appState.members[currentMemberKey];
    const pending = (profile.tasks || []).filter(tk => !tk.done);
    if (pending.length === 0) return;
    const backupSlots = ["20:00 - 21:00 (Backup)", "21:15 - 22:15 (Late)", "08:00 - 09:00 (Morning)"];
    pending.forEach((tk, i) => { tk.slot = backupSlots[i % backupSlots.length]; });
    savePersistentState();
    renderDashboard();
    alert(`🌪️ Đã tự động dời ${pending.length} ca học sang khung giờ dự phòng!`);
}

function openWhyModal(taskId) {
    const profile = appState.members[currentMemberKey];
    const task = (profile.tasks || []).find(tk => tk.id === taskId);
    if (!task) return;
    document.getElementById('why-modal-content').innerHTML = `
        <div class="bg-slate-900 p-3 rounded-2xl border border-white/10">
            <div class="text-sm font-extrabold text-white">${task.title}</div>
            <div class="text-xs text-amber-300 font-mono mt-1">⏰ ${task.slot} • 🔄 ${task.scope || '1 lần'}</div>
            <div class="text-xs text-cyan-300 mt-1">✈️ Chặng bay: ${task.originCode || 'SGN'} ➔ ${task.destCode || 'DAD'} (${task.distKm || 605} km • ${task.duration} phút)</div>
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
    const pending = (profile.tasks || []).filter(tk => !tk.done);
    if (pending.length === 0) alert(`🔔 ${profile.name}: Hiện không có chuyến bay nào đang chờ!`);
    else alert(`⏰ Báo thức chuyến bay của ${profile.name}:\n"${pending[0].title}"\nKhung giờ: ${pending[0].slot} (${pending[0].duration} phút)`);
}

function switchMemberProfile() {
    currentMemberKey = document.getElementById('member-select').value;
    appState.lastMember = currentMemberKey;
    selectedSeat = appState.members[currentMemberKey].seat || "06A";
    savePersistentState();
    if (typeof applyMemberHomeAirportRoute === 'function') applyMemberHomeAirportRoute();
    renderCalendarGrid();
    renderDashboard();
    resetChat();
}

// ================= 4. CHATBOT AI & ÂM THANH LOFI / WHITE NOISE =================
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
    const pending = (profile.tasks || []).filter(tk => !tk.done);
    const homeCode = (typeof getMemberHomeAirportCode === 'function') ? getMemberHomeAirportCode(currentMemberKey) : "SGN";
    if (currentLang === 'zh') {
        return `您好 <b>${profile.name}</b>（基地機場：<b>${homeCode}</b>）！🇹🇼<br>目前您有 <b>${pending.length} 項待辦任務</b>。點擊起飛即可體驗塔台 ATC 滑行、機長語音廣播與 3D 護照印章！`;
    }
    if (currentLang === 'en') {
        return `Hello <b>${profile.name}</b> (Base Airport: <b>${homeCode}</b>)! 🇬🇧<br>You have <b>${pending.length} pending tasks</b>. Take off to experience ATC runway taxi, Captain PA voice, and 3D Passport Stamps!`;
    }
    return `Chào <b>${profile.name}</b> (Sân bay căn cứ: <b>${homeCode}</b>)! 🇻🇳<br>Hiện bạn có <b>${pending.length} nhiệm vụ</b> đang chờ. Khi cất cánh sẽ có mô phỏng lăn bánh đường băng ATC, giọng cơ trưởng đọc tên bạn và đóng dấu Hộ chiếu 3D!`;
}

function resetChat() {
    const profile = appState.members[currentMemberKey];
    const botAvatar = document.getElementById('bot-launcher-img').src;
    const homeCode = (typeof getMemberHomeAirportCode === 'function') ? getMemberHomeAirportCode(currentMemberKey) : "SGN";
    let welcome = `Xin chào <b>${profile.name}</b> (Căn cứ: <b>✈️ ${homeCode}</b>)! 🙋‍♀️<br>Đã kích hoạt Radar 6 thành viên ở 6 sân bay VN, Phát thanh Cơ trưởng & ATC, Thời tiết thực tế và Hộ chiếu VIP!`;
    if (currentLang === 'zh') welcome = `您好 <b>${profile.name}</b>（基地：<b>✈️ ${homeCode}</b>）！🙋‍♀️<br>已啟用 6 成員雷達、機長廣播與 ATC 滑行、即時天氣與 VIP 護照！`;
    else if (currentLang === 'en') welcome = `Hello <b>${profile.name}</b> (Base: <b>✈️ ${homeCode}</b>)! 🙋‍♀️<br>6-Member Squadron Radar, Captain PA & ATC Taxi, Live Weather & VIP Passport are active!`;

    const msgBox = document.getElementById('chat-messages');
    if (msgBox) {
        msgBox.innerHTML = `<div class="flex items-start gap-2"><img src="${botAvatar}" class="w-7 h-7 rounded-full bg-amber-400 p-0.5 border border-[#d4a349] shrink-0 mt-1 object-cover" /><div><div class="bg-[#fae5be] p-1 rounded-2xl rounded-tl-sm shadow-sm"><div class="bg-white rounded-xl p-2.5 text-xs text-slate-800 leading-relaxed">${welcome}</div></div><span class="text-[9px] text-slate-400 mt-0.5 block">${getCurrentTimeStr()}</span></div></div>`;
    }
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
        if (!window.audioCtx) window.audioCtx = new (window.AudioContext || window.webkitAudioContext)();
        const bufferSize = 2 * window.audioCtx.sampleRate;
        const noiseBuffer = window.audioCtx.createBuffer(1, bufferSize, window.audioCtx.sampleRate);
        const output = noiseBuffer.getChannelData(0);
        let lastOut = 0.0;
        for (let i = 0; i < bufferSize; i++) {
            const white = Math.random() * 2 - 1;
            output[i] = (lastOut + (0.02 * white)) / 1.02;
            lastOut = output[i]; output[i] *= 0.15;
        }
        window.cabinNoiseNode = window.audioCtx.createBufferSource();
        window.cabinNoiseNode.buffer = noiseBuffer; window.cabinNoiseNode.loop = true;
        window.cabinNoiseNode.connect(window.audioCtx.destination); window.cabinNoiseNode.start(0);
    } else if (window.cabinNoiseNode) {
        window.cabinNoiseNode.stop(); window.cabinNoiseNode.disconnect(); window.cabinNoiseNode = null;
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
