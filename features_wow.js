// ================= 1. PHÂN BỐ 6 THÀNH VIÊN Ở 6 SÂN BAY VIỆT NAM KHÁC NHAU & RADAR ĐỘI HÌNH =================
const SQUADRON_CONFIG = {
    huudai:    { name: "Hữu Đại",    home: "SGN", dest: "DAD", subject: "Điều khiển thông minh & Tự động hóa", aircraft: "Airbus A321neo", color: "#38bdf8" },
    quangminh: { name: "Quang Minh", home: "HAN", dest: "CXR", subject: "Thiết kế hệ thống truyền động cơ khí", aircraft: "Boeing 787-9",   color: "#facc15" },
    khanhthi:  { name: "Khánh Thi",  home: "DAD", dest: "PQC", subject: "Xác suất thống kê & Phân tích dữ liệu", aircraft: "Airbus A350-900", color: "#f472b6" },
    minhchau:  { name: "Minh Châu",  home: "CXR", dest: "HUI", subject: "Luyện đề TOEIC Reading Part 5-7",     aircraft: "Airbus A321neo", color: "#34d399" },
    uyennhi:   { name: "Uyên Nhi",   home: "PQC", dest: "DLI", subject: "Kinh tế vĩ mô & Tài chính doanh nghiệp", aircraft: "ATR 72-600",   color: "#a78bfa" },
    vanhoang:  { name: "Văn Hoàng",  home: "VCA", dest: "VDO", subject: "Lập trình Python & Mô phỏng AI",      aircraft: "Boeing 787-9",   color: "#fb923c" }
};

let captainVoiceEnabled = true;
let squadronRadarEnabled = true;
let squadronMarkers2D = [];
let squadronProgressTick = 0.25;
let atcStepTimer1 = null, atcStepTimer2 = null, atcStepTimer3 = null;
let liveWeatherCache = { temp: 28, wind: 11, code: 0 };

function getMemberHomeAirportCode(memberKey) {
    return (SQUADRON_CONFIG[memberKey] && SQUADRON_CONFIG[memberKey].home) ? SQUADRON_CONFIG[memberKey].home : "SGN";
}

function applyMemberHomeAirportRoute() {
    const cfg = SQUADRON_CONFIG[currentMemberKey] || SQUADRON_CONFIG.huudai;
    const oAir = AIRPORTS.find(a => a.code === cfg.home) || AIRPORTS[0];
    const dAir = AIRPORTS.find(a => a.code === cfg.dest) || AIRPORTS[2];
    originAirport = oAir;
    destAirport = dAir;

    const oSel = document.getElementById('origin-select');
    const dSel = document.getElementById('dest-select');
    if (oSel) oSel.value = originAirport.code;
    if (dSel) dSel.value = destAirport.code;
    onRouteChange();
    renderSquadronRadarOn2DMap();
}

function renderSquadronRadarOn2DMap() {
    if (!map || typeof L === 'undefined') return;
    squadronMarkers2D.forEach(m => map.removeLayer(m));
    squadronMarkers2D = [];
    if (!squadronRadarEnabled) return;

    Object.keys(SQUADRON_CONFIG).forEach((key, idx) => {
        if (key === currentMemberKey) return; // Thành viên đang chọn đã có máy bay chính
        const cfg = SQUADRON_CONFIG[key];
        const oAir = AIRPORTS.find(a => a.code === cfg.home) || AIRPORTS[0];
        const dAir = AIRPORTS.find(a => a.code === cfg.dest) || AIRPORTS[2];

        const tProg = (squadronProgressTick + idx * 0.17) % 1;
        const lat = oAir.coords[0] + (dAir.coords[0] - oAir.coords[0]) * tProg;
        const lng = oAir.coords[1] + (dAir.coords[1] - oAir.coords[1]) * tProg;
        const brng = calcBearingDeg(oAir.coords, dAir.coords);

        const line = L.polyline([oAir.coords, dAir.coords], { color: cfg.color, weight: 1.5, dashArray: '4, 6', opacity: 0.55 }).addTo(map);
        squadronMarkers2D.push(line);

        const icon = L.divIcon({
            className: 'squadron-peer-icon',
            html: `<div class="relative flex flex-col items-center">
                <div class="w-8 h-8">${getAircraftSVG(cfg.aircraft, brng)}</div>
                <span style="background:${cfg.color}" class="text-black font-black text-[9px] px-1.5 py-0.2 rounded shadow whitespace-nowrap -mt-1">${cfg.name} (${cfg.home}➔${cfg.dest})</span>
            </div>`,
            iconSize: [80, 42], iconAnchor: [40, 21]
        });

        const marker = L.marker([lat, lng], { icon }).addTo(map);
        marker.bindPopup(`<div class="text-slate-900 text-xs font-sans p-1">
            <div class="font-black text-sm">✈️ ${cfg.name}</div>
            <div class="text-[11px] font-bold text-blue-700">Chặng: ${cfg.home} ➔ ${cfg.dest} (${cfg.aircraft})</div>
            <div class="text-[11px] mt-1">📚 Đang học: <b>${cfg.subject}</b></div>
        </div>`);
        squadronMarkers2D.push(marker);
    });
}

setInterval(() => {
    squadronProgressTick = (squadronProgressTick + 0.012) % 1;
    if (squadronRadarEnabled && is2DMapActive) renderSquadronRadarOn2DMap();
}, 4000);

function toggleSquadronRadar() {
    squadronRadarEnabled = !squadronRadarEnabled;
    const btn = document.getElementById('btn-squadron-radar');
    if (btn) {
        btn.innerText = squadronRadarEnabled ? "📡 Đội hình 6 TV: BẬT" : "📡 Đội hình 6 TV: TẮT";
        btn.className = squadronRadarEnabled
            ? "glass-panel px-3 py-1.5 rounded-xl text-[10px] font-extrabold text-emerald-300 border border-emerald-400/40 shadow-xl whitespace-nowrap"
            : "glass-panel px-3 py-1.5 rounded-xl text-[10px] font-extrabold text-slate-400 border border-white/10 shadow-xl whitespace-nowrap";
    }
    renderSquadronRadarOn2DMap();
    document.querySelectorAll('.squadron-3d-pin').forEach(el => el.classList.toggle('hidden', !squadronRadarEnabled));
}

function updateSquadron3DPins() {
    if (!earthGroup || !camera) return;
    Object.keys(SQUADRON_CONFIG).forEach((key, idx) => {
        const pinId = 'sq-3d-pin-' + key;
        let el = document.getElementById(pinId);
        if (!el) {
            el = document.createElement('div');
            el.id = pinId;
            el.style.zIndex = "14";
            el.className = "squadron-3d-pin fixed pointer-events-none -translate-x-1/2 -translate-y-1/2 hidden";
            document.getElementById('globe-wrapper').appendChild(el);
        }
        if (!squadronRadarEnabled || key === currentMemberKey || is2DMapActive || currentCamView !== 'map') {
            el.classList.add('hidden');
            return;
        }
        const cfg = SQUADRON_CONFIG[key];
        const oAir = AIRPORTS.find(a => a.code === cfg.home) || AIRPORTS[0];
        const dAir = AIRPORTS.find(a => a.code === cfg.dest) || AIRPORTS[2];
        const tProg = (squadronProgressTick + idx * 0.17) % 1;
        const lat = oAir.coords[0] + (dAir.coords[0] - oAir.coords[0]) * tProg;
        const lng = oAir.coords[1] + (dAir.coords[1] - oAir.coords[1]) * tProg;

        el.innerHTML = `<div style="border-color:${cfg.color}" class="bg-slate-950/90 border text-[9px] font-bold text-white px-1.5 py-0.5 rounded-md shadow whitespace-nowrap">✈️ ${cfg.name} (${cfg.home}➔${cfg.dest})</div>`;
        update3DPinOverlay(pinId, lat, lng, 1.035);
    });
}

// ================= 2. LĂN BÁNH ĐƯỜNG BĂNG (TAXI) + ĐÀI ATC + GIỌNG CƠ TRƯỞNG (CÓ BẬT/TẮT TIẾNG) =================
function toggleCaptainVoice() {
    captainVoiceEnabled = !captainVoiceEnabled;
    if (!captainVoiceEnabled && ('speechSynthesis' in window)) window.speechSynthesis.cancel();
    const btn = document.getElementById('btn-captain-voice-toggle');
    if (btn) {
        btn.innerText = captainVoiceEnabled ? "🔊 Cơ trưởng & ATC: BẬT" : "🔇 Cơ trưởng & ATC: TẮT";
        btn.className = captainVoiceEnabled
            ? "bg-amber-500/20 text-amber-300 border border-amber-400/40 px-2.5 py-1 rounded-xl text-[10px] font-extrabold transition"
            : "bg-slate-800 text-slate-400 border border-white/10 px-2.5 py-1 rounded-xl text-[10px] font-bold transition";
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

    // Bước 1: Xin phép đài chỉ huy ATC
    stageText.innerHTML = `🗼 [ATC TOWER ${originAirport.code} - 118.1 MHz]: Cấp huấn lệnh lăn bánh`;
    subText.innerHTML = `"${selectedAircraft}, đường băng 25R thông thoáng, gió ${liveWeatherCache.wind} km/h. Cho phép lăn ra đường băng chuẩn bị cất cánh đi ${destAirport.code}!"`;
    prog.style.width = "33%";

    if (atcStepTimer1) clearTimeout(atcStepTimer1);
    if (atcStepTimer2) clearTimeout(atcStepTimer2);
    if (atcStepTimer3) clearTimeout(atcStepTimer3);

    atcStepTimer1 = setTimeout(() => {
        stageText.innerHTML = `🛞 [RUNWAY TAXIING]: Máy bay đang lăn ra đường băng 25R...`;
        subText.innerHTML = `Kiểm tra cánh tà Flaps 1+F • Đèn Strobe ON • Hành khách ${profile.name} (${tier.name}) thắt dây an toàn tại ghế ${selectedSeat}.`;
        prog.style.width = "68%";
    }, 2800);

    atcStepTimer2 = setTimeout(() => {
        stageText.innerHTML = `🎙️ [CAPTAIN PA]: Phát thanh Cơ trưởng & Tăng tốc V1... Rotate!`;
        let speechMsg = `Cơ trưởng xin chào hành khách ${profile.name}. Chuyến bay tập trung từ ${originAirport.name.split(' (')[0]} đi ${destAirport.name} thời lượng ${selectedDuration} phút xin phép cất cánh. Chúc bạn học tập hiệu quả!`;
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

// ================= 3. THỜI TIẾT THỰC TẾ TẠI SÂN BAY ĐẾN (OPEN-METEO API) =================
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

function syncWindowWithLiveWeather() {
    if (liveWeatherCache.code >= 51) setFlightEnvironment('rain');
    else syncEnvironmentWithRealTime();
}

// ================= 4. THẺ VIP FREQUENT FLYER, HỘ CHIẾU 3D & HỘP ĐEN PHÂN TÍCH =================
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
}

function awardPassportStamp(originCode, destCode, distKm, subject) {
    const profile = appState.members[currentMemberKey];
    if (!profile.passportStamps) profile.passportStamps = [];
    const now = new Date();
    const dateStr = `${String(now.getDate()).padStart(2,'0')}/${String(now.getMonth()+1).padStart(2,'0')}/${now.getFullYear()}`;
    profile.passportStamps.unshift({
        origin: originCode, dest: destCode, dist: distKm, date: dateStr, subject: subject || "Focus Study"
    });
    savePersistentState();
}

function openPassportAndBlackboxModal() {
    const profile = appState.members[currentMemberKey];
    const homeCode = getMemberHomeAirportCode(currentMemberKey);
    const tier = getFrequentFlyerTier(profile.miles || 0);

    if (!profile.passportStamps || profile.passportStamps.length === 0) {
        profile.passportStamps = [
            { origin: homeCode, dest: SQUADRON_CONFIG[currentMemberKey].dest, dist: calcDistanceKm(AIRPORTS.find(a=>a.code===homeCode).coords, AIRPORTS.find(a=>a.code===SQUADRON_CONFIG[currentMemberKey].dest).coords), date: "06/11/2026", subject: SQUADRON_CONFIG[currentMemberKey].subject }
        ];
    }

    let stampsHtml = profile.passportStamps.map((s, idx) => `
        <div class="border-2 border-dashed ${idx % 2 === 0 ? 'border-emerald-400/70 bg-emerald-950/25 rotate-[-2deg]' : 'border-amber-400/70 bg-amber-950/25 rotate-[2deg]'} rounded-2xl p-2.5 text-center shadow-lg">
            <div class="text-[8px] font-mono font-black uppercase tracking-widest text-cyan-300">VIETNAM IMMIGRATION • ARRIVAL</div>
            <div class="text-sm font-black text-white my-0.5">✈️ ${s.origin} ➔ ${s.dest}</div>
            <div class="text-[10px] font-bold text-amber-300">+${s.dist} km • ${s.date}</div>
            <div class="text-[9px] text-slate-300 truncate mt-0.5">${s.subject}</div>
        </div>
    `).join('');

    let leaderboardHtml = Object.keys(appState.members).map(k => {
        const m = appState.members[k];
        const cfg = SQUADRON_CONFIG[k];
        const mTier = getFrequentFlyerTier(m.miles || 0);
        const doneCount = (m.tasks || []).filter(tk => tk.done).length;
        return `
            <div class="bg-slate-900/90 border border-white/10 rounded-xl p-2.5 flex items-center justify-between">
                <div>
                    <div class="text-xs font-extrabold text-white flex items-center gap-1.5">
                        <span>👤 ${m.name}</span>
                        <span class="text-[9px] bg-blue-500/20 text-cyan-300 px-1.5 py-0.2 rounded">Căn cứ: ${cfg.home}</span>
                        <span class="text-[9px] px-1.5 py-0.2 rounded border ${mTier.bg}">${mTier.name}</span>
                    </div>
                    <div class="text-[10px] text-slate-400 mt-0.5">Chặng mẫu: ${cfg.home} ➔ ${cfg.dest} • Đang học: ${cfg.subject}</div>
                </div>
                <div class="text-right font-mono">
                    <div class="text-xs font-black text-amber-300">${m.miles || 0} km</div>
                    <div class="text-[10px] text-emerald-400">${m.flights || 0} chuyến • ${doneCount} xong</div>
                </div>
            </div>
        `;
    }).join('');

    document.getElementById('passport-modal-body').innerHTML = `
        <div class="bg-gradient-to-r from-blue-950 via-slate-900 to-indigo-950 border border-amber-400/40 rounded-2xl p-3.5 mb-3 flex flex-wrap items-center justify-between gap-2">
            <div>
                <div class="text-[9px] text-amber-300 font-bold uppercase tracking-widest">PASSPORT & FREQUENT FLYER CARD</div>
                <div class="text-base font-black text-white mt-0.5">🛂 ${profile.name} • Sân bay căn cứ: ${homeCode}</div>
                <div class="text-xs text-cyan-300">Tích lũy: <b>${profile.miles || 0} km</b> • Đã bay: <b>${profile.flights || 0} chuyến</b></div>
            </div>
            <div class="px-3 py-1.5 rounded-xl border font-black text-xs ${tier.bg}">${tier.name}</div>
        </div>
        <div class="text-xs font-extrabold text-amber-300 mb-2">💮 Bộ sưu tập Con dấu Nhập cảnh (Passport Stamps):</div>
        <div class="grid grid-cols-2 sm:grid-cols-3 gap-2.5 mb-4 max-h-40 overflow-y-auto p-1">${stampsHtml}</div>
        <div class="text-xs font-extrabold text-cyan-300 mb-2">📊 Hộp Đen Đội Hình 6 Thành Viên (6 Sân bay Việt Nam):</div>
        <div class="space-y-1.5 max-h-48 overflow-y-auto pr-1">${leaderboardHtml}</div>
    `;
    document.getElementById('passport-blackbox-modal').classList.remove('hidden');
    document.getElementById('passport-blackbox-modal').classList.add('flex');
}

function closePassportAndBlackboxModal() {
    document.getElementById('passport-blackbox-modal').classList.add('hidden');
    document.getElementById('passport-blackbox-modal').classList.remove('flex');
}

// ================= 5. MENU ĐỒ ĂN / TRÀ SỮA KHOANG THƯƠNG GIA & TẢI ẢNH VÉ PNG TÙY CHỌN =================
function serveCabinItem(icon, name) {
    const slot = document.getElementById('cabin-served-items');
    if (slot) {
        slot.innerHTML = `<span class="text-xl animate-bounce inline-block">${icon}</span> <span class="text-[11px] font-extrabold text-emerald-800">${name}</span>`;
    }
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

// ================= 6. TỰ ĐỘNG GẮN CÁC NÚT ĐIỀU KHIỂN MỚI VÀO GIAO DIỆN =================
function injectWowUIElements() {
    // 1. Gắn huy hiệu Hạng thẻ VIP vào Thẻ KPI số 1
    const statName = document.getElementById('stat-member-name');
    if (statName && !document.getElementById('vip-tier-badge')) {
        const badge = document.createElement('span');
        badge.id = 'vip-tier-badge';
        badge.className = "ml-1.5 text-[10px] font-black px-2 py-0.5 rounded-full border";
        statName.parentElement.appendChild(badge);
    }

    // 2. Gắn nút Hộ Chiếu 3D & Hộp Đen vào Header
    const headerRight = document.querySelector('header > div:last-child');
    if (headerRight && !document.getElementById('btn-open-passport')) {
        const passBtn = document.createElement('button');
        passBtn.id = 'btn-open-passport';
        passBtn.onclick = openPassportAndBlackboxModal;
        passBtn.className = "bg-amber-500/20 hover:bg-amber-500/30 border border-amber-400/40 px-2.5 py-1.5 rounded-xl text-xs font-extrabold text-amber-300 transition flex items-center gap-1";
        passBtn.innerHTML = `🛂 <span class="hidden sm:inline">Hộ Chiếu & VIP</span>`;
        headerRight.insertBefore(passBtn, headerRight.firstChild);
    }

    // 3. Gắn nút Bật/Tắt Radar Đội hình 6 Thành viên ở cụm Zoom 2D/3D
    const zoomCtrl = document.getElementById('zoom-mode-controls');
    if (zoomCtrl && !document.getElementById('btn-squadron-radar')) {
        const radBtn = document.createElement('button');
        radBtn.id = 'btn-squadron-radar';
        radBtn.onclick = toggleSquadronRadar;
        radBtn.className = "glass-panel px-3 py-1.5 rounded-xl text-[10px] font-extrabold text-emerald-300 border border-emerald-400/40 shadow-xl whitespace-nowrap";
        radBtn.innerText = "📡 Đội hình 6 TV: BẬT";
        zoomCtrl.appendChild(radBtn);
    }

    // 4. Gắn Thanh Thời tiết thực tế + Nút Bật/Tắt tiếng Cơ trưởng & ATC vào Bảng đặt vé
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
        const actionRow = bookingCard.querySelector('.flex.gap-2:last-child');
        bookingCard.insertBefore(wxBar, actionRow);
    }

    // 5. Gắn nút Tùy chọn Tải ảnh Vé Boarding Pass (.PNG) vào màn hình Vé
    const ticketScreen = document.querySelector('#screen-ticket > div');
    if (ticketScreen && !document.getElementById('btn-download-ticket-png')) {
        const dlBtn = document.createElement('button');
        dlBtn.id = 'btn-download-ticket-png';
        dlBtn.onclick = downloadBoardingPassPNG;
        dlBtn.className = "w-full mt-2.5 bg-slate-900 hover:bg-slate-800 text-amber-300 border border-amber-400/40 font-extrabold py-2 rounded-2xl text-xs shadow transition";
        dlBtn.innerHTML = "📸 Tải ảnh Vé Boarding Pass (PNG - Tùy chọn)";
        ticketScreen.insertBefore(dlBtn, ticketScreen.lastElementChild);
    }

    // 6. Gắn Menu Phục vụ Trà sữa / Cà phê Hạng Thương Gia vào Bàn học trong khoang Cabin
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

    // 7. Tạo Overlay Mô phỏng Lăn bánh Đường băng & Đài Không Lưu ATC + Modal Hộ Chiếu 3D
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

            <!-- MODAL HỘ CHIẾU 3D & HỘP ĐEN ĐỘI HÌNH 6 THÀNH VIÊN -->
            <div id="passport-blackbox-modal" style="z-index: 9200;" class="fixed inset-0 bg-black/80 backdrop-blur-md hidden items-center justify-center p-4">
                <div class="glass-panel w-full max-w-2xl rounded-3xl p-5 shadow-2xl border border-amber-400/40">
                    <div class="flex justify-between items-center mb-3 pb-2 border-b border-white/10">
                        <h3 class="text-sm sm:text-base font-black text-amber-300">🛂 Cuốn Hộ Chiếu 3D, Hạng Thẻ VIP & Radar 6 Thành Viên</h3>
                        <button onclick="closePassportAndBlackboxModal()" class="text-slate-400 hover:text-white text-lg font-bold">✕</button>
                    </div>
                    <div id="passport-modal-body"></div>
                    <button onclick="closePassportAndBlackboxModal()" class="mt-4 w-full bg-gradient-to-r from-amber-500 to-yellow-500 text-black font-black py-2.5 rounded-xl text-xs uppercase">Đóng Hộ Chiếu</button>
                </div>
            </div>
        `;
        document.body.appendChild(modalsWrapper);
    }
}

// ================= 7. KHỞI CHẠY HỆ THỐNG =================
document.getElementById('member-select').value = currentMemberKey;
injectWowUIElements();
initThreeGlobe();
updateRealTimeClock();
initAirportDropdowns();
applyMemberHomeAirportRoute();
syncEnvironmentWithRealTime();
updateSlotDurationPreview();
renderCalendarGrid();
renderDashboard();
resetChat();
