// ================= 1. CẤU HÌNH SÂN BAY CĂN CỨ CỦA 6 THÀNH VIÊN (KHÔNG CHÈN MÔN HỌC GIẢ) =================
const MEMBER_BASE_AIRPORTS = {
    huudai:    { name: "Hữu Đại",    home: "SGN", aircraft: "Airbus A321neo", color: "#38bdf8" },
    quangminh: { name: "Quang Minh", home: "HAN", aircraft: "Boeing 787-9",   color: "#facc15" },
    khanhthi:  { name: "Khánh Thi",  home: "DAD", aircraft: "Airbus A350-900", color: "#f472b6" },
    minhchau:  { name: "Minh Châu",  home: "CXR", aircraft: "Airbus A321neo", color: "#34d399" },
    uyennhi:   { name: "Uyên Nhi",   home: "PQC", aircraft: "ATR 72-600",     color: "#a78bfa" },
    vanhoang:  { name: "Văn Hoàng",  home: "VCA", aircraft: "Boeing 787-9",   color: "#fb923c" }
};

let captainVoiceEnabled = true;
let squadronRadarEnabled = true;
let zenFocusModeActive = false;
let squadronMarkers2D = [];
let squadronProgressTick = 0.35;
let atcStepTimer1 = null, atcStepTimer2 = null, atcStepTimer3 = null;
let liveWeatherCache = { temp: 28, wind: 11, code: 0 };

function getMemberHomeAirportCode(memberKey) {
    return (MEMBER_BASE_AIRPORTS[memberKey] && MEMBER_BASE_AIRPORTS[memberKey].home) ? MEMBER_BASE_AIRPORTS[memberKey].home : "SGN";
}

// Chỉ lấy nhiệm vụ/môn học THẬT do người dùng đã nhập trong danh sách của thành viên đó
function getMemberRealActiveTask(memberKey) {
    const m = appState.members[memberKey];
    if (!m || !m.tasks || m.tasks.length === 0) return null;
    const pending = m.tasks.filter(tk => !tk.done);
    return pending.length > 0 ? pending[0] : null;
}

function applyMemberHomeAirportRoute() {
    const cfg = MEMBER_BASE_AIRPORTS[currentMemberKey] || MEMBER_BASE_AIRPORTS.huudai;
    const activeTask = getMemberRealActiveTask(currentMemberKey);
    const oAir = AIRPORTS.find(a => a.code === cfg.home) || AIRPORTS[0];
    const targetDestCode = activeTask ? activeTask.destCode : (cfg.home === "DAD" ? "SGN" : "DAD");
    const dAir = AIRPORTS.find(a => a.code === targetDestCode) || AIRPORTS[2];

    originAirport = oAir;
    destAirport = dAir;

    const oSel = document.getElementById('origin-select');
    const dSel = document.getElementById('dest-select');
    if (oSel) oSel.value = originAirport.code;
    if (dSel) dSel.value = destAirport.code;
    onRouteChange();
    renderSquadronRadarOn2DMap();
    renderFidsDepartureBoard();
}

// ================= 2. RADAR 6 THÀNH VIÊN (CHỈ BAY KHI CÓ LỊCH THẬT, CHƯA CÓ LỊCH SẼ ĐỖ TẠI SÂN BAY) =================
function renderSquadronRadarOn2DMap() {
    if (!map || typeof L === 'undefined') return;
    squadronMarkers2D.forEach(m => {
        try { map.removeLayer(m); } catch (e) {}
    });
    squadronMarkers2D = [];
    if (!squadronRadarEnabled) return;

    Object.keys(MEMBER_BASE_AIRPORTS).forEach((key, idx) => {
        if (key === currentMemberKey) return;
        const cfg = MEMBER_BASE_AIRPORTS[key];
        const homeAir = AIRPORTS.find(a => a.code === cfg.home) || AIRPORTS[0];
        const realTask = getMemberRealActiveTask(key);

        if (realTask) {
            // Thành viên này ĐÃ CÓ lịch học thật do người dùng thêm -> Cho máy bay bay trên chặng đó
            const destAir = AIRPORTS.find(a => a.code === (realTask.destCode || "DAD")) || AIRPORTS[2];
            const tProg = (squadronProgressTick + idx * 0.17) % 1;
            const lat = homeAir.coords[0] + (destAir.coords[0] - homeAir.coords[0]) * tProg;
            const lng = homeAir.coords[1] + (destAir.coords[1] - homeAir.coords[1]) * tProg;
            const brng = calcBearingDeg(homeAir.coords, destAir.coords);

            const line = L.polyline([homeAir.coords, destAir.coords], { color: cfg.color, weight: 2, dashArray: '5, 6', opacity: 0.7 }).addTo(map);
            squadronMarkers2D.push(line);

            const icon = L.divIcon({
                className: 'squadron-peer-icon',
                html: `<div class="relative flex flex-col items-center">
                    <div class="w-8 h-8">${getAircraftSVG(cfg.aircraft, brng)}</div>
                    <span style="background:${cfg.color}" class="text-black font-black text-[9px] px-1.5 py-0.2 rounded shadow whitespace-nowrap -mt-1">✈️ ${cfg.name} (${cfg.home}➔${destAir.code})</span>
                </div>`,
                iconSize: [90, 42], iconAnchor: [45, 21]
            });

            const marker = L.marker([lat, lng], { icon }).addTo(map);
            marker.bindPopup(`<div class="text-slate-900 text-xs font-sans p-1">
                <div class="font-black text-sm">✈️ ${cfg.name} (Đang bay theo lịch)</div>
                <div class="text-[11px] font-bold text-blue-700">Chặng: ${cfg.home} ➔ ${destAir.code} • ⏰ ${realTask.slot}</div>
                <div class="text-[11px] mt-1">📚 Nhiệm vụ: <b>${realTask.title}</b></div>
            </div>`);
            squadronMarkers2D.push(marker);
        } else {
            // Thành viên CHƯA CÓ lịch học nào -> Đỗ yên tại sân bay căn cứ (Standby), không hiển thị môn học ảo
            const icon = L.divIcon({
                className: 'squadron-standby-icon',
                html: `<div class="flex items-center gap-1 bg-slate-950/90 border border-white/25 text-slate-300 px-2 py-0.5 rounded-full text-[9px] font-bold shadow-lg whitespace-nowrap">
                    <span class="w-2 h-2 rounded-full" style="background:${cfg.color}"></span>
                    <span>${cfg.name} (${cfg.home} • Chờ lịch)</span>
                </div>`,
                iconSize: [110, 22], iconAnchor: [55, -10]
            });

            const marker = L.marker(homeAir.coords, { icon }).addTo(map);
            marker.bindPopup(`<div class="text-slate-900 text-xs font-sans p-1">
                <div class="font-black text-sm">🛬 ${cfg.name} (Đang đỗ tại ${cfg.home})</div>
                <div class="text-[11px] text-slate-600 mt-0.5">Chưa có lịch học nào được thêm. Hãy chuyển sang hồ sơ <b>${cfg.name}</b> và thêm lịch học để cất cánh!</div>
            </div>`);
            squadronMarkers2D.push(marker);
        }
    });
}

setInterval(() => {
    squadronProgressTick = (squadronProgressTick + 0.015) % 1;
    if (squadronRadarEnabled && is2DMapActive) renderSquadronRadarOn2DMap();
    renderFidsDepartureBoard();
}, 5000);

function toggleSquadronRadar() {
    squadronRadarEnabled = !squadronRadarEnabled;
    const btn = document.getElementById('btn-squadron-radar');
    if (btn) {
        btn.innerText = squadronRadarEnabled ? "📡 Vị trí 6 TV: BẬT" : "📡 Vị trí 6 TV: TẮT";
        btn.className = squadronRadarEnabled
            ? "glass-panel px-3 py-1.5 rounded-xl text-[10px] font-extrabold text-emerald-300 border border-emerald-400/40 shadow-xl whitespace-nowrap"
            : "glass-panel px-3 py-1.5 rounded-xl text-[10px] font-extrabold text-slate-400 border border-white/10 shadow-xl whitespace-nowrap";
    }
    renderSquadronRadarOn2DMap();
    document.querySelectorAll('.squadron-3d-pin').forEach(el => el.classList.toggle('hidden', !squadronRadarEnabled));
}

function updateSquadron3DPins() {
    if (!earthGroup || !camera) return;
    const wrapper = document.getElementById('globe-wrapper');
    if (!wrapper) return;

    Object.keys(MEMBER_BASE_AIRPORTS).forEach((key, idx) => {
        const pinId = 'sq-3d-pin-' + key;
        let el = document.getElementById(pinId);
        if (!el) {
            el = document.createElement('div');
            el.id = pinId;
            el.style.zIndex = "14";
            el.className = "squadron-3d-pin fixed pointer-events-none -translate-x-1/2 -translate-y-1/2 hidden";
            wrapper.appendChild(el);
        }
        if (!squadronRadarEnabled || key === currentMemberKey || is2DMapActive || currentCamView !== 'map') {
            el.classList.add('hidden');
            return;
        }
        const cfg = MEMBER_BASE_AIRPORTS[key];
        const homeAir = AIRPORTS.find(a => a.code === cfg.home) || AIRPORTS[0];
        const realTask = getMemberRealActiveTask(key);

        if (realTask) {
            const destAir = AIRPORTS.find(a => a.code === (realTask.destCode || "DAD")) || AIRPORTS[2];
            const tProg = (squadronProgressTick + idx * 0.17) % 1;
            const lat = homeAir.coords[0] + (destAir.coords[0] - homeAir.coords[0]) * tProg;
            const lng = homeAir.coords[1] + (destAir.coords[1] - homeAir.coords[1]) * tProg;
            el.innerHTML = `<div style="border-color:${cfg.color}" class="bg-slate-950/90 border text-[9px] font-bold text-white px-1.5 py-0.5 rounded-md shadow whitespace-nowrap">✈️ ${cfg.name} (${cfg.home}➔${destAir.code})</div>`;
            update3DPinOverlay(pinId, lat, lng, 1.035);
        } else {
            el.innerHTML = `<div style="border-color:${cfg.color}" class="bg-slate-950/75 border text-[8px] font-semibold text-slate-300 px-1.5 py-0.5 rounded-md shadow whitespace-nowrap">🛬 ${cfg.name} (${cfg.home})</div>`;
            update3DPinOverlay(pinId, homeAir.coords[0], homeAir.coords[1], 1.02);
        }
    });
}

// ================= 3. BẢNG ĐIỆN TỬ LỊCH HỌC SÂN BAY (FIDS DEPARTURE BOARD) & ZEN FOCUS HUD =================
function renderFidsDepartureBoard() {
    const container = document.getElementById('fids-board-rows');
    if (!container) return;

    const profile = appState.members[currentMemberKey];
    const homeCode = getMemberHomeAirportCode(currentMemberKey);
    const tasks = profile.tasks || [];

    const now = new Date();
    const curMins = now.getHours() * 60 + now.getMinutes();

    if (tasks.length === 0) {
        container.innerHTML = `
            <div class="col-span-12 py-4 text-center text-xs text-slate-400 font-mono">
                📡 [STANDBY] Chưa có ca học nào trên bảng điện tử FIDS hôm nay. Hãy thêm lịch ở khung Thời Gian Biểu bên dưới để lên bảng điện tử!
            </div>
        `;
        return;
    }

    container.innerHTML = tasks.slice(0, 5).map((tk, i) => {
        const flightNo = `VN${202 + i * 15}`;
        const oCode = tk.originCode || homeCode;
        const dCode = tk.destCode || "DAD";

        let statusText = "SCHEDULED";
        let statusClass = "bg-blue-500/20 text-cyan-300 border-cyan-400/40";

        if (tk.done) {
            statusText = "LANDED ✓";
            statusClass = "bg-emerald-500/20 text-emerald-300 border-emerald-400/40";
        } else if (tk.slot && tk.slot.includes('-')) {
            const parts = tk.slot.split('-').map(s => s.trim());
            const [sh, sm] = (parts[0] || "00:00").split(':').map(Number);
            const [eh, em] = (parts[1] || "23:59").split(':').map(Number);
            const sMins = sh * 60 + sm;
            const eMins = eh * 60 + em;
            if (curMins >= sMins && curMins <= eMins) {
                statusText = "IN FLIGHT ✈️";
                statusClass = "bg-amber-400 text-black font-black animate-pulse";
            } else if (sMins > curMins && (sMins - curMins) <= 45) {
                statusText = "BOARDING 🔔";
                statusClass = "bg-yellow-500/25 text-yellow-300 border-yellow-400/50 animate-bounce";
            }
        }

        return `
            <div class="grid grid-cols-12 items-center bg-[#060a14] hover:bg-slate-900/90 border border-white/10 rounded-xl px-3 py-2 font-mono text-xs transition gap-2">
                <div class="col-span-2 font-extrabold text-amber-400">${tk.slot ? tk.slot.split(' ')[0] : '--:--'}</div>
                <div class="col-span-2 text-cyan-300 font-bold">${flightNo} (${oCode}➔${dCode})</div>
                <div class="col-span-5 font-sans font-extrabold text-white truncate">${tk.title}</div>
                <div class="col-span-2 text-right">
                    <span class="text-[10px] px-2 py-0.5 rounded border ${statusClass}">${statusText}</span>
                </div>
                <div class="col-span-1 text-right">
                    ${!tk.done ? `<button onclick="startFlightFromTask(${tk.id})" class="bg-cyan-500 hover:bg-cyan-400 text-black font-sans font-black px-2 py-0.5 rounded text-[10px]">Bay</button>` : `<span class="text-emerald-400">✓</span>`}
                </div>
            </div>
        `;
    }).join('');
}

function toggleZenFocusHud() {
    zenFocusModeActive = !zenFocusModeActive;
    const zenOverlay = document.getElementById('zen-focus-hud-overlay');
    if (!zenOverlay) return;
    if (zenFocusModeActive) {
        zenOverlay.classList.remove('hidden');
        zenOverlay.classList.add('flex');
        syncZenHudTick();
    } else {
        zenOverlay.classList.add('hidden');
        zenOverlay.classList.remove('flex');
    }
}

function syncZenHudTick() {
    if (!zenFocusModeActive) return;
    const timerTxt = document.getElementById('countdown-timer');
    const zenTimer = document.getElementById('zen-big-timer');
    const zenTask = document.getElementById('zen-task-label');
    const zenRoute = document.getElementById('zen-route-label');
    const zenBar = document.getElementById('zen-progress-bar');

    if (zenTimer && timerTxt) zenTimer.innerText = timerTxt.innerText;
    if (zenTask) zenTask.innerText = `${selectedFocus.icon} ${selectedFocus.label}`;
    if (zenRoute) zenRoute.innerText = `✈️ ${originAirport.code} ➔ ${destAirport.code} • GHẾ ${selectedSeat} • ${appState.members[currentMemberKey].name}`;
    if (zenBar) zenBar.style.width = `${(currentFlightProgress || 0) * 100}%`;
}
setInterval(syncZenHudTick, 500);

// ================= 4. LĂN BÁNH ĐƯỜNG BĂNG (TAXI) + ĐÀI ATC + GIỌNG CƠ TRƯỞNG =================
function toggleCaptainVoice() {
    captainVoiceEnabled = !captainVoiceEnabled;
    if (!captainVoiceEnabled && ('speechSynthesis' in window)) window.speechSynthesis.cancel();
    const btn = document.getElementById('btn-captain-voice-toggle');
    if (btn) {
        btn.innerText = captainVoiceEnabled ? "🔊 Cơ trưởng & ATC: BẬT" : "🔇 Cơ trưởng & ATC: TẮT";
        btn.className = captainVoiceEnabled
            ? "bg-amber-500/20 text-amber-300 border border-amber-400/40 px-2 py-0.5 rounded-lg text-[10px] font-extrabold transition"
            : "bg-slate-800 text-slate-400 border border-white/10 px-2 py-0.5 rounded-lg text-[10px] font-bold transition";
    }
}

function speakCaptainAnnouncement(text) {
    if (!captainVoiceEnabled || !('speechSynthesis' in window)) return;
    try {
        window.speechSynthesis.cancel();
        const u = new SpeechSynthesisUtterance(text);
        u.rate = 0.98; u.pitch = 0.92;
        const voices = window.speechSynthesis.getVoices();
        const langKey = currentLang === 'zh' ? 'zh' : (currentLang === 'en' ? 'en' : 'vi');
        const v = voices.find(vo => vo.lang.toLowerCase().includes(langKey));
        if (v) u.voice = v;
        window.speechSynthesis.speak(u);
    } catch (e) {}
}

function runTakeoffTaxiAndAtcSequence() {
    const overlay = document.getElementById('atc-taxi-overlay');
    if (!overlay) return;
    overlay.classList.remove('hidden'); overlay.classList.add('flex');

    const profile = appState.members[currentMemberKey];
    const tier = getFrequentFlyerTier(profile.miles || 0);
    const stageText = document.getElementById('atc-stage-text');
    const subText = document.getElementById('atc-sub-text');
    const prog = document.getElementById('atc-taxi-bar');

    stageText.innerHTML = `🗼 [ATC TOWER ${originAirport.code} - 118.1 MHz]: Cấp huấn lệnh lăn bánh`;
    subText.innerHTML = `"${selectedAircraft}, đường băng 25R thông thoáng, gió ${liveWeatherCache.wind} km/h. Cho phép lăn ra đường băng chuẩn bị cất cánh đi ${destAirport.code}!"`;
    prog.style.width = "33%";

    if (atcStepTimer1) clearTimeout(atcStepTimer1);
    if (atcStepTimer2) clearTimeout(atcStepTimer2);
    if (atcStepTimer3) clearTimeout(atcStepTimer3);

    atcStepTimer1 = setTimeout(() => {
        stageText.innerHTML = `🛞 [RUNWAY TAXIING]: Máy bay đang lăn ra đường băng 25R...`;
        subText.innerHTML = `Mục tiêu ca học: "${selectedFocus.label}" • Hành khách ${profile.name} (${tier.name}) ổn định tại ghế ${selectedSeat}.`;
        prog.style.width = "68%";
    }, 2800);

    atcStepTimer2 = setTimeout(() => {
        stageText.innerHTML = `🎙️ [CAPTAIN PA]: Phát thanh Cơ trưởng & Tăng tốc V1... Rotate!`;
        let speechMsg = `Cơ trưởng xin chào hành khách ${profile.name}. Chuyến bay tập trung từ ${originAirport.name.split(' (')[0]} đi ${destAirport.name} thời lượng ${selectedDuration} phút xin phép cất cánh. Chúc bạn hoàn thành mục tiêu học tập!`;
        if (currentLang === 'en') speechMsg = `Captain speaking. Welcome passenger ${profile.name} aboard our focus flight from ${originAirport.code} to ${destAirport.code}. Flight time is ${selectedDuration} minutes. Cleared for takeoff!`;
        if (currentLang === 'zh') speechMsg = `機長廣播：歡迎旅客 ${profile.name} 搭乘從 ${originAirport.code} 前往 ${destAirport.code} 的專注航班，飛行時間 ${selectedDuration} 分鐘，現在起飛！`;
        subText.innerHTML = `"${speechMsg}"`;
        prog.style.width = "100%";
        speakCaptainAnnouncement(speechMsg);
    }, 5600);

    atcStepTimer3 = setTimeout(() => {
        closeAtcTaxiOverlay();
    }, 10500);
}

function closeAtcTaxiOverlay() {
    if (atcStepTimer1) clearTimeout(atcStepTimer1);
    if (atcStepTimer2) clearTimeout(atcStepTimer2);
    if (atcStepTimer3) clearTimeout(atcStepTimer3);
    const overlay = document.getElementById('atc-taxi-overlay');
    if (overlay) { overlay.classList.add('hidden'); overlay.classList.remove('flex'); }
}

// ================= 5. THỜI TIẾT THỰC TẾ, HỘ CHIẾU 3D THẬT 100% & XUẤT ẢNH VÉ PNG =================
async function updateDestinationLiveWeather(airportCode) {
    const air = AIRPORTS.find(a => a.code === airportCode) || destAirport;
    const badge = document.getElementById('live-weather-badge');
    try {
        const res = await fetch(`https://api.open-meteo.com/v1/forecast?latitude=${air.coords[0]}&longitude=${air.coords[1]}&current_weather=true`);
        const data = await res.json();
        if (data && data.current_weather) {
            liveWeatherCache.temp = Math.round(data.current_weather.temperature);
            liveWeatherCache.wind = Math.round(data.current_weather.windspeed);
            liveWeatherCache.code = data.current_weather.weathercode;
            const icon = liveWeatherCache.code >= 51 ? "🌧️ Mưa" : (liveWeatherCache.code >= 1 ? "⛅ Có mây" : "☀️ Quang đãng");
            if (badge) badge.innerHTML = `${icon} tại <b>${air.code}</b>: <b>${liveWeatherCache.temp}°C</b> • Gió ${liveWeatherCache.wind} km/h`;
        }
    } catch (e) {
        if (badge) badge.innerHTML = `☀️ Thời tiết <b>${air.code}</b>: 28°C • Gió 10 km/h`;
    }
}

function getFrequentFlyerTier(miles) {
    if (miles >= 3000) return { name: "💎 DIAMOND VIP", bg: "bg-cyan-500/20 text-cyan-300 border-cyan-400/50" };
    if (miles >= 1200) return { name: "🥇 GOLD ELITE", bg: "bg-amber-500/20 text-amber-300 border-amber-400/50" };
    if (miles >= 400)  return { name: "🥈 SILVER CLUB", bg: "bg-slate-300/20 text-slate-200 border-slate-300/50" };
    return { name: "🥉 CLASSIC", bg: "bg-emerald-500/20 text-emerald-300 border-emerald-400/40" };
}

function updateVipBadgeOnDashboard() {
    const profile = appState.members[currentMemberKey];
    const tier = getFrequentFlyerTier(profile.miles || 0);
    const el = document.getElementById('vip-tier-badge');
    if (el) {
        el.className = `text-[10px] font-black px-2 py-0.5 rounded-full border ${tier.bg}`;
        el.innerText = tier.name;
    }
    renderFidsDepartureBoard();
}

function awardPassportStamp(originCode, destCode, distKm, subject) {
    const profile = appState.members[currentMemberKey];
    if (!profile.passportStamps) profile.passportStamps = [];
    const now = new Date();
    const dateStr = `${String(now.getDate()).padStart(2,'0')}/${String(now.getMonth()+1).padStart(2,'0')}/${now.getFullYear()}`;
    profile.passportStamps.unshift({
        origin: originCode, dest: destCode, dist: distKm, date: dateStr, subject: subject || "Ca học tập trung"
    });
    savePersistentState();
}

function openPassportAndBlackboxModal() {
    const profile = appState.members[currentMemberKey];
    const homeCode = getMemberHomeAirportCode(currentMemberKey);
    const tier = getFrequentFlyerTier(profile.miles || 0);
    const stamps = profile.passportStamps || [];

    let stampsHtml = stamps.length === 0
        ? `<div class="col-span-3 text-center py-6 bg-slate-900/50 rounded-2xl border border-dashed border-white/10 text-xs text-slate-400">🛂 Chưa có con dấu nhập cảnh nào. Hãy hoàn thành 1 chuyến bay học tập để nhận con dấu đầu tiên!</div>`
        : stamps.map((s, idx) => `
            <div class="border-2 border-dashed ${idx % 2 === 0 ? 'border-emerald-400/70 bg-emerald-950/25 rotate-[-2deg]' : 'border-amber-400/70 bg-amber-950/25 rotate-[2deg]'} rounded-2xl p-2.5 text-center shadow-lg">
                <div class="text-[8px] font-mono font-black uppercase tracking-widest text-cyan-300">IMMIGRATION • COMPLETED</div>
                <div class="text-sm font-black text-white my-0.5">✈️ ${s.origin} ➔ ${s.dest}</div>
                <div class="text-[10px] font-bold text-amber-300">+${s.dist} km • ${s.date}</div>
                <div class="text-[9px] text-slate-300 truncate mt-0.5">${s.subject}</div>
            </div>
        `).join('');

    let leaderboardHtml = Object.keys(appState.members).map(k => {
        const m = appState.members[k];
        const cfg = MEMBER_BASE_AIRPORTS[k];
        const mTier = getFrequentFlyerTier(m.miles || 0);
        const pendingCount = (m.tasks || []).filter(tk => !tk.done).length;
        const doneCount = (m.tasks || []).filter(tk => tk.done).length;
        const realTask = getMemberRealActiveTask(k);

        return `
            <div class="bg-slate-900/90 border border-white/10 rounded-xl p-2.5 flex items-center justify-between">
                <div>
                    <div class="text-xs font-extrabold text-white flex items-center gap-1.5">
                        <span>👤 ${m.name}</span>
                        <span class="text-[9px] bg-blue-500/20 text-cyan-300 px-1.5 py-0.2 rounded">Căn cứ: ${cfg.home}</span>
                        <span class="text-[9px] px-1.5 py-0.2 rounded border ${mTier.bg}">${mTier.name}</span>
                    </div>
                    <div class="text-[10px] text-slate-400 mt-0.5">
                        ${realTask ? `🛫 Đang có lịch: <b class="text-amber-300">${realTask.title}</b> (${realTask.slot})` : `🛬 Đang đỗ tại ${cfg.home} (Chưa thêm lịch học)`}
                    </div>
                </div>
                <div class="text-right font-mono">
                    <div class="text-xs font-black text-amber-300">${m.miles || 0} km</div>
                    <div class="text-[10px] text-emerald-400">${doneCount} xong • ${pendingCount} chờ</div>
                </div>
            </div>
        `;
    }).join('');

    document.getElementById('passport-modal-body').innerHTML = `
        <div class="bg-gradient-to-r from-blue-950 via-slate-900 to-indigo-950 border border-amber-400/40 rounded-2xl p-3.5 mb-3 flex flex-wrap items-center justify-between gap-2">
            <div>
                <div class="text-[9px] text-amber-300 font-bold uppercase tracking-widest">PASSPORT & FREQUENT FLYER CARD</div>
                <div class="text-base font-black text-white mt-0.5">🛂 ${profile.name} • Sân bay căn cứ: ${homeCode}</div>
                <div class="text-xs text-cyan-300">Tích lũy: <b>${profile.miles || 0} km</b> • Đã hạ cánh: <b>${profile.flights || 0} chuyến</b></div>
            </div>
            <div class="px-3 py-1.5 rounded-xl border font-black text-xs ${tier.bg}">${tier.name}</div>
        </div>
        <div class="text-xs font-extrabold text-amber-300 mb-2">💮 Con dấu Nhập cảnh (Chỉ đóng dấu khi hoàn thành ca học thật):</div>
        <div class="grid grid-cols-2 sm:grid-cols-3 gap-2.5 mb-4 max-h-40 overflow-y-auto p-1">${stampsHtml}</div>
        <div class="text-xs font-extrabold text-cyan-300 mb-2">📊 Trạng thái Thực tế của 6 Thành Viên (6 Sân bay căn cứ VN):</div>
        <div class="space-y-1.5 max-h-48 overflow-y-auto pr-1">${leaderboardHtml}</div>
    `;
    document.getElementById('passport-blackbox-modal').classList.remove('hidden');
    document.getElementById('passport-blackbox-modal').classList.add('flex');
}

function closePassportAndBlackboxModal() {
    document.getElementById('passport-blackbox-modal').classList.add('hidden');
    document.getElementById('passport-blackbox-modal').classList.remove('flex');
}

function serveCabinItem(icon, name) {
    const slot = document.getElementById('cabin-served-items');
    if (slot) slot.innerHTML = `<span class="text-xl animate-bounce inline-block">${icon}</span> <span class="text-[11px] font-extrabold text-emerald-800">${name}</span>`;
    playCabinDingDong();
}

function downloadBoardingPassPNG() {
    const cardEl = document.querySelector('#screen-ticket .bg-\\[\\#121723\\]');
    if (!cardEl || typeof html2canvas === 'undefined') {
        alert("Đang chuẩn bị máy in ảnh vé... Bạn hãy thử bấm lại sau 1 giây nhé!");
        return;
    }
    html2canvas(cardEl, { backgroundColor: '#03060f', scale: 2, useCORS: true }).then(canvas => {
        const a = document.createElement('a');
        a.download = `BoardingPass_${appState.members[currentMemberKey].name}_${originAirport.code}_${destAirport.code}.png`;
        a.href = canvas.toDataURL('image/png');
        a.click();
    });
}

// ================= 6. TỰ ĐỘNG NÂNG CẤP GIAO DIỆN TẬP TRUNG HỌC & BẢNG ĐIỆN TỬ FIDS =================
function injectWowUIElements() {
    try {
        const statName = document.getElementById('stat-member-name');
        if (statName && !document.getElementById('vip-tier-badge')) {
            const badge = document.createElement('span');
            badge.id = 'vip-tier-badge';
            badge.className = "ml-1.5 text-[10px] font-black px-2 py-0.5 rounded-full border";
            statName.parentElement.appendChild(badge);
        }
    } catch (e) {}

    // Chèn Bảng Điện Tử Lịch Học Sân Bay (FIDS Departure Board) vào Dashboard
    try {
        const dashContainer = document.querySelector('#page-dashboard > div');
        if (dashContainer && !document.getElementById('fids-departure-board')) {
            const fidsBoard = document.createElement('div');
            fidsBoard.id = 'fids-departure-board';
            fidsBoard.className = "bg-gradient-to-b from-[#0b1326] to-[#060a14] border-2 border-amber-400/35 rounded-3xl p-4 shadow-2xl";
            fidsBoard.innerHTML = `
                <div class="flex flex-wrap items-center justify-between gap-2 pb-2.5 mb-2.5 border-b border-white/10">
                    <div class="flex items-center gap-2">
                        <span class="bg-amber-400 text-black font-mono font-black text-xs px-2.5 py-0.5 rounded uppercase tracking-wider">🛫 FIDS • DEPARTURE STUDY BOARD</span>
                        <span class="text-xs font-extrabold text-white">Bảng Điện Tử Lịch Bay Học Tập Trong Ngày</span>
                    </div>
                    <span class="text-[11px] font-mono text-emerald-400">● Dữ liệu thật từ Thời Gian Biểu</span>
                </div>
                <div class="grid grid-cols-12 px-3 pb-1 text-[10px] font-mono font-bold text-slate-400 uppercase">
                    <div class="col-span-2">GIỜ HỌC</div>
                    <div class="col-span-2">CHUYẾN BAY</div>
                    <div class="col-span-5">MÔN HỌC / NHIỆM VỤ</div>
                    <div class="col-span-2 text-right">TRẠNG THÁI</div>
                    <div class="col-span-1 text-right">CẤT CÁNH</div>
                </div>
                <div id="fids-board-rows" class="space-y-1.5"></div>
            `;
            // Đặt ngay bên dưới 4 thẻ KPI
            const kpiGrid = dashContainer.children[1];
            dashContainer.insertBefore(fidsBoard, kpiGrid.nextSibling);
        }
    } catch (e) {}

    try {
        const headerRight = document.querySelector('header > div:last-child');
        if (headerRight && !document.getElementById('btn-open-passport')) {
            const passBtn = document.createElement('button');
            passBtn.id = 'btn-open-passport';
            passBtn.onclick = openPassportAndBlackboxModal;
            passBtn.className = "bg-amber-500/20 hover:bg-amber-500/30 border border-amber-400/40 px-2.5 py-1.5 rounded-xl text-xs font-extrabold text-amber-300 transition flex items-center gap-1";
            passBtn.innerHTML = `🛂 <span class="hidden sm:inline">Hộ Chiếu & VIP</span>`;
            headerRight.insertBefore(passBtn, headerRight.firstChild);
        }
    } catch (e) {}

    try {
        const zoomCtrl = document.getElementById('zoom-mode-controls');
        if (zoomCtrl && !document.getElementById('btn-squadron-radar')) {
            const radBtn = document.createElement('button');
            radBtn.id = 'btn-squadron-radar';
            radBtn.onclick = toggleSquadronRadar;
            radBtn.className = "glass-panel px-3 py-1.5 rounded-xl text-[10px] font-extrabold text-emerald-300 border border-emerald-400/40 shadow-xl whitespace-nowrap";
            radBtn.innerText = "📡 Vị trí 6 TV: BẬT";
            zoomCtrl.appendChild(radBtn);
        }
    } catch (e) {}

    // Nút bật chế độ Zen Focus HUD trên thanh Dock khi đang bay
    try {
        const flyDockRight = document.querySelector('#screen-flying .flex.items-center.gap-1\\.5:last-child');
        if (flyDockRight && !document.getElementById('btn-zen-focus')) {
            const zenBtn = document.createElement('button');
            zenBtn.id = 'btn-zen-focus';
            zenBtn.onclick = toggleZenFocusHud;
            zenBtn.className = "bg-amber-400 hover:bg-amber-300 text-black px-2.5 py-1.5 rounded-xl text-[11px] font-black shadow";
            zenBtn.innerHTML = "🧘 Zen HUD";
            flyDockRight.insertBefore(zenBtn, flyDockRight.firstChild);
        }
    } catch (e) {}

    try {
        const bookingCard = document.getElementById('screen-booking');
        if (bookingCard && !document.getElementById('live-weather-bar')) {
            const wxBar = document.createElement('div');
            wxBar.id = 'live-weather-bar';
            wxBar.className = "flex flex-wrap items-center justify-between gap-1.5 bg-slate-900/90 border border-white/10 rounded-xl px-2.5 py-1.5 mb-2 text-[10px]";
            wxBar.innerHTML = `
                <span id="live-weather-badge" class="text-cyan-300 font-semibold">☀️ Thời tiết DAD: 28°C</span>
                <div class="flex items-center gap-1">
                    <button id="btn-captain-voice-toggle" onclick="toggleCaptainVoice()" class="bg-amber-500/20 text-amber-300 border border-amber-400/40 px-2 py-0.5 rounded-lg text-[10px] font-extrabold transition">🔊 Cơ trưởng & ATC: BẬT</button>
                </div>
            `;
            bookingCard.insertBefore(wxBar, bookingCard.lastElementChild);
        }
    } catch (e) {}

    try {
        const ticketScreen = document.querySelector('#screen-ticket > div');
        if (ticketScreen && !document.getElementById('btn-download-ticket-png')) {
            const dlBtn = document.createElement('button');
            dlBtn.id = 'btn-download-ticket-png';
            dlBtn.onclick = downloadBoardingPassPNG;
            dlBtn.className = "w-full mt-2.5 bg-slate-900 hover:bg-slate-800 text-amber-300 border border-amber-400/40 font-extrabold py-2 rounded-2xl text-xs shadow transition";
            dlBtn.innerHTML = "📸 Tải ảnh Vé Boarding Pass (PNG - Tùy chọn)";
            ticketScreen.insertBefore(dlBtn, ticketScreen.lastElementChild);
        }
    } catch (e) {}

    try {
        const trayEl = document.getElementById('cabin-tray-table-open');
        if (trayEl && !document.getElementById('cabin-catering-menu')) {
            const menuDiv = document.createElement('div');
            menuDiv.id = 'cabin-catering-menu';
            menuDiv.className = "mt-2 pt-2 border-t border-slate-400/50 flex flex-wrap items-center justify-between gap-1.5";
            menuDiv.innerHTML = `
                <div class="flex items-center gap-1 text-[10px] font-extrabold text-slate-700">
                    <span>🍽️ Menu VIP:</span>
                    <button onclick="serveCabinItem('🧋','Trà sữa Trân châu')" class="bg-white hover:bg-amber-100 px-2 py-0.5 rounded-lg shadow-sm">🧋 Trà sữa</button>
                    <button onclick="serveCabinItem('🍵','Matcha Latte')" class="bg-white hover:bg-emerald-100 px-2 py-0.5 rounded-lg shadow-sm">🍵 Matcha</button>
                    <button onclick="serveCabinItem('☕','Espresso')" class="bg-white hover:bg-amber-100 px-2 py-0.5 rounded-lg shadow-sm">☕ Cà phê</button>
                    <button onclick="serveCabinItem('🥐','Croissant')" class="bg-white hover:bg-yellow-100 px-2 py-0.5 rounded-lg shadow-sm">🥐 Bánh</button>
                </div>
                <div id="cabin-served-items" class="text-xs font-bold text-slate-800">☕ 📓</div>
            `;
            trayEl.appendChild(menuDiv);
        }
    } catch (e) {}

    try {
        if (!document.getElementById('atc-taxi-overlay')) {
            const modalsWrapper = document.createElement('div');
            modalsWrapper.innerHTML = `
                <!-- OVERLAY MÔ PHỎNG LĂN BÁNH ĐƯỜNG BĂNG & ĐÀI ATC -->
                <div id="atc-taxi-overlay" style="z-index: 8200;" class="fixed top-16 left-1/2 -translate-x-1/2 w-[94%] max-w-lg glass-panel rounded-3xl p-4 border-2 border-amber-400/50 shadow-2xl hidden flex-col gap-2">
                    <div class="flex items-center justify-between">
                        <span id="atc-stage-text" class="text-xs font-black text-amber-300 uppercase tracking-wider">🗼 [ATC TOWER]</span>
                        <div class="flex items-center gap-1.5">
                            <button onclick="toggleCaptainVoice()" class="text-[10px] bg-white/10 hover:bg-white/20 text-white px-2 py-0.5 rounded-lg font-bold">🔊/🔇 Tiếng</button>
                            <button onclick="closeAtcTaxiOverlay()" class="text-[10px] bg-emerald-500 hover:bg-emerald-400 text-black font-black px-2.5 py-0.5 rounded-lg">Bỏ qua ➔ Bay luôn</button>
                        </div>
                    </div>
                    <div id="atc-sub-text" class="text-xs text-slate-200 leading-relaxed font-mono bg-black/40 p-2.5 rounded-xl border border-white/10"></div>
                    <div class="w-full bg-slate-800 h-1.5 rounded-full overflow-hidden">
                        <div id="atc-taxi-bar" class="bg-gradient-to-r from-amber-400 to-emerald-400 h-full w-1/3 transition-all duration-700"></div>
                    </div>
                </div>

                <!-- CHẾ ĐỘ SIÊU TẬP TRUNG ZEN FOCUS HUD -->
                <div id="zen-focus-hud-overlay" style="z-index: 8800;" class="fixed inset-0 bg-[#03060f]/90 backdrop-blur-2xl hidden flex-col items-center justify-center p-6 text-center">
                    <div id="zen-route-label" class="text-xs font-mono font-bold text-cyan-400 tracking-widest uppercase mb-2">✈️ SGN ➔ DAD • GHẾ 06A</div>
                    <div id="zen-task-label" class="text-xl sm:text-3xl font-extrabold text-white mb-4 max-w-2xl">💻 Tập trung học tập</div>
                    <div id="zen-big-timer" class="mono text-6xl sm:text-8xl font-black text-amber-400 tracking-tight my-4 drop-shadow-[0_0_35px_rgba(250,204,21,0.35)]">55:00</div>
                    <div class="w-full max-w-md bg-slate-800 h-2.5 rounded-full overflow-hidden my-6 border border-white/10">
                        <div id="zen-progress-bar" class="bg-gradient-to-r from-cyan-400 to-amber-400 h-full w-0 transition-all duration-500"></div>
                    </div>
                    <div class="flex items-center gap-3">
                        <button onclick="toggleLofi()" class="bg-slate-800 hover:bg-slate-700 text-slate-200 font-bold px-4 py-2.5 rounded-2xl text-xs border border-white/15">🎵 Bật/Tắt Lofi</button>
                        <button onclick="toggleZenFocusHud()" class="bg-gradient-to-r from-cyan-500 to-blue-600 text-white font-black px-6 py-2.5 rounded-2xl text-xs shadow-xl">🔙 Quay lại Buồng lái</button>
                    </div>
                </div>

                <!-- MODAL HỘ CHIẾU 3D & HỘP ĐEN ĐỘI HÌNH 6 THÀNH VIÊN -->
                <div id="passport-blackbox-modal" style="z-index: 9200;" class="fixed inset-0 bg-black/80 backdrop-blur-md hidden items-center justify-center p-4">
                    <div class="glass-panel w-full max-w-2xl rounded-3xl p-5 shadow-2xl border border-amber-400/40">
                        <div class="flex justify-between items-center mb-3 pb-2 border-b border-white/10">
                            <h3 class="text-sm sm:text-base font-black text-amber-300">🛂 Cuốn Hộ Chiếu 3D, Hạng Thẻ VIP & Trạng Thái 6 Thành Viên</h3>
                            <button onclick="closePassportAndBlackboxModal()" class="text-slate-400 hover:text-white text-lg font-bold">✕</button>
                        </div>
                        <div id="passport-modal-body"></div>
                        <button onclick="closePassportAndBlackboxModal()" class="mt-4 w-full bg-gradient-to-r from-amber-500 to-yellow-500 text-black font-black py-2.5 rounded-xl text-xs uppercase">Đóng Hộ Chiếu</button>
                    </div>
                </div>
            `;
            document.body.appendChild(modalsWrapper);
        }
    } catch (e) {}
}

// ================= 7. KHỞI CHẠY HỆ THỐNG =================
try { document.getElementById('member-select').value = currentMemberKey; } catch (e) {}
try { injectWowUIElements(); } catch (e) {}
try { initThreeGlobe(); } catch (e) {}
try { updateRealTimeClock(); } catch (e) {}
try { initAirportDropdowns(); } catch (e) {}
try { applyMemberHomeAirportRoute(); } catch (e) {}
try { syncEnvironmentWithRealTime(); } catch (e) {}
try { updateSlotDurationPreview(); } catch (e) {}
try { renderCalendarGrid(); } catch (e) {}
try { renderDashboard(); } catch (e) {}
try { renderFidsDepartureBoard(); } catch (e) {}
try { resetChat(); } catch (e) {}
