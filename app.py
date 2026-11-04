import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="StudyHub & 3D Flight Sim (VI / EN / 繁體中文)",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
    <style>
        #MainMenu, header, footer, [data-testid="stHeader"], [data-testid="stToolbar"] {
            display: none !important;
            visibility: hidden !important;
        }
        .block-container {
            padding: 0 !important;
            margin: 0 !important;
            max-width: 100vw !important;
        }
        iframe {
            position: fixed !important;
            top: 0 !important;
            left: 0 !important;
            right: 0 !important;
            bottom: 0 !important;
            width: 100vw !important;
            height: 100vh !important;
            border: none !important;
            margin: 0 !important;
            padding: 0 !important;
            z-index: 99999 !important;
            display: block !important;
        }
        body {
            margin: 0 !important;
            padding: 0 !important;
            overflow: hidden !important;
            background-color: #03060f !important;
        }
    </style>
""", unsafe_allow_html=True)

app_html = """
<!DOCTYPE html>
<html lang="vi" translate="no" class="notranslate">
<head>
    <meta charset="UTF-8">
    <meta name="google" content="notranslate">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
    <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@500;700;800&family=Noto+Sans+TC:wght@400;500;700;900&display=swap" rel="stylesheet">
    <style>
        * { box-sizing: border-box; }
        body { font-family: 'Plus Jakarta Sans', 'Noto Sans TC', sans-serif; background: #03060f; color: white; margin: 0; padding: 0; width: 100vw; height: 100vh; overflow: hidden; user-select: none; }
        .mono { font-family: 'JetBrains Mono', monospace; }

        input[type="time"]::-webkit-calendar-picker-indicator,
        input[type="date"]::-webkit-calendar-picker-indicator {
            filter: invert(0.8) sepia(1) saturate(5) hue-rotate(175deg);
            cursor: pointer;
        }

        .leaflet-container {
            background-color: #040b18 !important;
            width: 100% !important;
            height: 100% !important;
            font-family: 'Plus Jakarta Sans', 'Noto Sans TC', sans-serif !important;
        }
        .leaflet-container img, .leaflet-tile, .leaflet-marker-icon, .leaflet-marker-shadow {
            max-width: none !important;
            max-height: none !important;
        }

        #globe-wrapper {
            position: absolute; inset: 0; z-index: 2;
            background: radial-gradient(circle at center, #0a1636 0%, #040817 55%, #010308 100%);
            overflow: hidden; opacity: 1; transition: opacity 0.4s ease;
        }
        #globe-wrapper.globe-hidden { opacity: 0; pointer-events: none; z-index: 1; }

        #map-2d-wrapper {
            position: absolute; inset: 0; z-index: 1;
            background: #040b18; opacity: 0; pointer-events: none; transition: opacity 0.4s ease;
        }
        #map-2d-wrapper.active-2d { z-index: 3; opacity: 1; pointer-events: auto; }
        #map { position: absolute; inset: 0; width: 100% !important; height: 100% !important; }

        .map-night-filter { filter: brightness(0.58) contrast(1.25) saturate(0.85) hue-rotate(190deg); }
        .map-sunset-filter { filter: brightness(0.82) contrast(1.15) sepia(0.28) hue-rotate(-12deg); }
        .map-rain-filter { filter: brightness(0.65) contrast(1.2) saturate(0.7); }

        .page-layer-hidden { visibility: hidden !important; opacity: 0 !important; pointer-events: none !important; }
        .page-layer-visible { visibility: visible !important; opacity: 1 !important; pointer-events: auto !important; }

        .glass-panel { background: rgba(11, 17, 30, 0.92); backdrop-filter: blur(22px); border: 1px solid rgba(255, 255, 255, 0.16); }
        .dash-card { background: linear-gradient(145deg, #0f172a 0%, #0b1120 100%); border: 1px solid rgba(255, 255, 255, 0.1); box-shadow: 0 12px 32px rgba(0, 0, 0, 0.45); }

        .cal-cell { min-height: 50px; transition: all 0.15s ease; }
        .cal-cell:hover { transform: translateY(-1px); border-color: rgba(56, 189, 248, 0.6); }

        .focus-popover { background: rgba(20, 31, 53, 0.98); backdrop-filter: blur(28px); border: 1px solid rgba(56, 189, 248, 0.35); box-shadow: 0 25px 60px rgba(0, 0, 0, 0.9); }
        .fuselage {
            border-top-left-radius: 160px 240px; border-top-right-radius: 160px 240px;
            border-left: 3px solid rgba(56, 189, 248, 0.35); border-right: 3px solid rgba(56, 189, 248, 0.35); border-top: 3px solid rgba(56, 189, 248, 0.5);
            background: linear-gradient(180deg, rgba(20, 29, 47, 0.96) 0%, rgba(10, 14, 24, 0.98) 100%);
            box-shadow: inset 0 15px 40px rgba(56, 189, 248, 0.08), 0 20px 60px rgba(0,0,0,0.85);
        }
        .seat-box { transition: all 0.18s ease; }
        .seat-box:hover { transform: scale(1.07); }

        .ticket-cutout-left { position: absolute; left: -14px; top: 66%; width: 28px; height: 28px; background: #03060f; border-radius: 50%; }
        .ticket-cutout-right { position: absolute; right: -14px; top: 66%; width: 28px; height: 28px; background: #03060f; border-radius: 50%; }

        @keyframes pulse-bar { 0%, 100% { height: 4px; } 50% { height: 15px; } }
        .eq-bar { width: 3px; background: #38bdf8; border-radius: 2px; animation: pulse-bar 0.9s infinite ease-in-out; }
        .eq-bar:nth-child(2) { animation-delay: 0.2s; }
        .eq-bar:nth-child(3) { animation-delay: 0.4s; }

        @keyframes strobe-blink { 0%, 85%, 100% { opacity: 0.15; } 90%, 95% { opacity: 1; filter: drop-shadow(0 0 8px #ffffff); } }
        .strobe-light { animation: strobe-blink 1.5s infinite; }

        @keyframes radar-pulse { 0% { transform: scale(0.4); opacity: 0.85; } 100% { transform: scale(2.4); opacity: 0; } }
        .radar-ring { animation: radar-pulse 2.2s infinite ease-out; }

        @keyframes cloud-drift-right-to-left { 0% { transform: translateX(115vw) scale(0.85); opacity: 0; } 10% { opacity: 0.92; } 90% { opacity: 0.92; } 100% { transform: translateX(-45vw) scale(1.15); opacity: 0; } }
        .svg-cloud-1 { animation: cloud-drift-right-to-left 14s linear infinite; }
        .svg-cloud-2 { animation: cloud-drift-right-to-left 21s linear infinite; animation-delay: -6s; }
        .svg-cloud-3 { animation: cloud-drift-right-to-left 11s linear infinite; animation-delay: -3s; }
        .svg-cloud-4 { animation: cloud-drift-right-to-left 17s linear infinite; animation-delay: -11s; }
        .svg-cloud-5 { animation: cloud-drift-right-to-left 9s linear infinite; animation-delay: -5s; }

        @keyframes window-cloud-pass { 0% { transform: translateX(360px); } 100% { transform: translateX(-360px); } }
        .win-cloud-fast { animation: window-cloud-pass 7s linear infinite; }
        .win-cloud-slow { animation: window-cloud-pass 13s linear infinite; animation-delay: -5s; }

        @keyframes hud-sway { 0%, 100% { transform: rotate(-1.2deg) translateY(0px); } 50% { transform: rotate(1.2deg) translateY(3px); } }
        .hud-horizon { animation: hud-sway 6s ease-in-out infinite; }

        @keyframes rain-fall { 0% { background-position: 0px 0px; } 100% { background-position: -150px 500px; } }
        .rain-overlay { background-image: repeating-linear-gradient(105deg, transparent 0px, transparent 18px, rgba(186, 230, 253, 0.35) 19px, transparent 20px); background-size: 200px 200px; animation: rain-fall 0.55s linear infinite; }

        @keyframes red-alert { 0%, 100% { background: rgba(153, 27, 27, 0.94); } 50% { background: rgba(220, 38, 38, 0.98); } }
        .turbulence-alert { animation: red-alert 0.7s infinite; backdrop-filter: blur(16px); }

        @keyframes bot-glow { 0%, 100% { box-shadow: 0 0 15px rgba(212, 163, 73, 0.75), 0 0 30px rgba(212, 163, 73, 0.4); transform: translateY(0px); } 50% { box-shadow: 0 0 25px rgba(234, 179, 8, 1), 0 0 45px rgba(212, 163, 73, 0.65); transform: translateY(-4px); } }
        .bot-launcher-glow { animation: bot-glow 2.8s infinite ease-in-out; }

        .dragging-card { opacity: 0.45; border: 2px dashed #38bdf8 !important; }
        ::-webkit-scrollbar { width: 5px; height: 5px; }
        ::-webkit-scrollbar-thumb { background: rgba(255,255,255,0.25); border-radius: 10px; }
        .leaflet-control-attribution { display: none !important; }
    </style>
</head>
<body class="relative w-screen h-screen overflow-hidden bg-[#03060f] notranslate" translate="no">

    <audio id="lofi-player" loop crossorigin="anonymous"><source id="lofi-source" src="https://cdn.pixabay.com/download/audio/2022/05/27/audio_1808fbf07a.mp3" type="audio/mpeg"></audio>

    <!-- ================= THANH ĐIỀU HƯỚNG CHÍNH + CHỌN 3 NGÔN NGỮ ================= -->
    <header style="z-index: 8000;" class="fixed top-0 left-0 right-0 h-14 bg-[#080d1a]/95 backdrop-blur-xl border-b border-white/10 px-2.5 sm:px-4 flex items-center justify-between gap-2">
        <div class="flex items-center gap-2">
            <div class="flex items-center gap-2">
                <div class="w-8 h-8 rounded-xl bg-gradient-to-br from-blue-500 to-cyan-400 flex items-center justify-center text-black font-black text-base shadow">🌍</div>
                <div class="hidden xl:block">
                    <div id="lbl-appTitle" class="text-[11px] font-extrabold tracking-wider text-white">STUDYHUB & SATELLITE 3D</div>
                    <div class="text-[9px] text-emerald-400" id="save-status-indicator"><span data-i18n="saveSync">● Tự động đồng bộ</span></div>
                </div>
            </div>

            <div class="bg-slate-900 border border-white/15 px-2.5 py-1 rounded-xl flex items-center gap-1.5">
                <span class="text-xs">👤</span>
                <div>
                    <div data-i18n="memberTitle" class="text-[8px] text-amber-400 font-bold uppercase tracking-wider leading-none">Thành viên</div>
                    <select id="member-select" onchange="switchMemberProfile()" class="bg-transparent text-white font-extrabold text-xs focus:outline-none cursor-pointer pr-1">
                        <option value="huudai" class="bg-slate-900">Hữu Đại</option>
                        <option value="quangminh" class="bg-slate-900">Quang Minh</option>
                        <option value="khanhthi" class="bg-slate-900">Khánh Thi</option>
                        <option value="minhchau" class="bg-slate-900">Minh Châu</option>
                        <option value="uyennhi" class="bg-slate-900">Uyên Nhi</option>
                        <option value="vanhoang" class="bg-slate-900">Văn Hoàng</option>
                    </select>
                </div>
            </div>

            <div class="hidden md:flex items-center gap-2 bg-slate-900/90 border border-cyan-500/30 px-2.5 py-1 rounded-xl">
                <span class="w-2 h-2 rounded-full bg-emerald-400 animate-ping"></span>
                <div>
                    <div id="realtime-clock" class="mono text-xs font-extrabold text-cyan-300 leading-none">00:00:00</div>
                    <div id="realtime-date" class="text-[9px] text-slate-400 font-semibold leading-none mt-0.5">--/--/----</div>
                </div>
            </div>
        </div>

        <div class="bg-slate-900/90 p-1 rounded-xl border border-white/10 flex items-center gap-1">
            <button id="nav-btn-dashboard" onclick="switchPage('dashboard')" class="px-2.5 sm:px-3 py-1.5 rounded-lg text-xs font-extrabold bg-gradient-to-r from-blue-600 to-cyan-500 text-white shadow transition flex items-center gap-1.5">
                <span data-i18n="tabDash">📊 Bảng Điều Khiển Học Tập</span>
                <span id="nav-pending-badge" class="bg-black/30 text-white text-[10px] px-1.5 rounded-full">0</span>
            </button>
            <button id="nav-btn-flight" onclick="switchPage('flight')" class="px-2.5 sm:px-3 py-1.5 rounded-lg text-xs font-extrabold text-slate-400 hover:text-white transition flex items-center gap-1.5">
                <span data-i18n="tabFlight">✈️ Chuyến Bay 3D / 2D</span>
            </button>
        </div>

        <!-- 3 NGÔN NGỮ (BỎ CỜ, CHỈ ĐỂ CHỮ VI / EN / 繁體) -->
        <div class="flex items-center gap-1.5">
            <div class="bg-slate-900 border border-amber-400/40 p-0.5 rounded-xl flex items-center text-[10px] font-extrabold">
                <button id="lang-btn-vi" onclick="setAppLanguage('vi')" class="px-2 py-1 rounded-lg bg-amber-400 text-black transition">VI</button>
                <button id="lang-btn-en" onclick="setAppLanguage('en')" class="px-2 py-1 rounded-lg text-slate-300 hover:text-white transition">EN</button>
                <button id="lang-btn-zh" onclick="setAppLanguage('zh')" class="px-2 py-1 rounded-lg text-slate-300 hover:text-white transition">繁體</button>
            </div>

            <button onclick="toggleLofi()" class="bg-slate-900 hover:bg-slate-800 border border-white/10 px-2.5 py-1.5 rounded-xl flex items-center gap-1.5 text-xs font-bold text-slate-200 transition">
                <div id="eq-icon" class="hidden items-end gap-[2px] h-3.5"><div class="eq-bar"></div><div class="eq-bar"></div><div class="eq-bar"></div></div>
                <span id="lofi-btn-text" data-i18n="btnLofi">🎵 Nhạc Lofi</span>
            </button>
            <button onclick="openMediaModal()" class="bg-slate-900 hover:bg-slate-800 border border-cyan-500/30 px-2 py-1.5 rounded-xl text-xs font-bold text-cyan-400 transition">
                ⚙️
            </button>
        </div>
    </header>

    <!-- ========================================================================================= -->
    <!-- TRANG 1: BẢNG ĐIỀU KHIỂN HỌC TẬP -->
    <!-- ========================================================================================= -->
    <main id="page-dashboard" style="z-index: 30;" class="fixed inset-x-0 top-14 bottom-0 bg-[#03060f] overflow-y-auto px-3 sm:px-6 py-4 page-layer-visible">
        <div class="max-w-7xl mx-auto space-y-4 pb-20">

            <div id="deadline-banner" class="hidden bg-gradient-to-r from-blue-600/90 via-indigo-600/90 to-cyan-600/90 rounded-2xl p-3.5 shadow-xl border border-cyan-300/30 items-center justify-between gap-4">
                <div class="flex items-center gap-3">
                    <span class="text-xl animate-bounce">✈️</span>
                    <div>
                        <div data-i18n="bannerTag" class="text-[9px] font-black uppercase tracking-widest bg-black/30 px-2 py-0.5 rounded inline-block text-yellow-300">Thông báo Chuyến bay từ Lịch cá nhân</div>
                        <div id="deadline-banner-text" class="text-xs sm:text-sm font-extrabold text-white mt-0.5"></div>
                    </div>
                </div>
                <button onclick="startFocusFromTopTask()" data-i18n="bannerBtn" class="bg-yellow-400 text-black hover:bg-yellow-300 font-black text-xs px-3.5 py-2 rounded-xl shadow shrink-0">
                    🛫 Cất cánh học ngay
                </button>
            </div>

            <div class="grid grid-cols-2 lg:grid-cols-4 gap-3">
                <div class="dash-card rounded-2xl p-3.5 flex items-center justify-between">
                    <div>
                        <div data-i18n="kpiProfile" class="text-[11px] text-slate-400 font-semibold">Hồ sơ thành viên</div>
                        <div id="stat-member-name" class="text-base font-black text-amber-400 mt-0.5">Hữu Đại</div>
                        <div data-i18n="kpiProfileSub" class="text-[10px] text-slate-500">Đồng bộ Lịch ➔ Chuyến bay</div>
                    </div>
                    <div class="w-10 h-10 rounded-xl bg-amber-500/10 border border-amber-500/20 flex items-center justify-center text-lg">👤</div>
                </div>
                <div class="dash-card rounded-2xl p-3.5 flex items-center justify-between">
                    <div>
                        <div data-i18n="kpiTask" class="text-[11px] text-slate-400 font-semibold">Nhiệm vụ & Lịch bay</div>
                        <div id="stat-pending-count" class="text-xl font-black text-white mt-0.5 mono">0</div>
                        <div data-i18n="kpiTaskSub" class="text-[10px] text-cyan-400">Đang chờ cất cánh</div>
                    </div>
                    <div class="w-10 h-10 rounded-xl bg-cyan-500/10 border border-cyan-500/20 flex items-center justify-center text-lg">📋</div>
                </div>
                <div class="dash-card rounded-2xl p-3.5 flex items-center justify-between">
                    <div>
                        <div data-i18n="kpiDone" class="text-[11px] text-slate-400 font-semibold">Đã hoàn thành (✓)</div>
                        <div id="stat-done-count" class="text-xl font-black text-emerald-400 mt-0.5 mono">0</div>
                        <div id="stat-done-percent" class="text-[10px] text-emerald-500">Tiến độ: 0%</div>
                    </div>
                    <div class="w-10 h-10 rounded-xl bg-emerald-500/10 border border-emerald-500/20 flex items-center justify-center text-lg">✅</div>
                </div>
                <div class="dash-card rounded-2xl p-3.5 flex items-center justify-between">
                    <div>
                        <div data-i18n="kpiMiles" class="text-[11px] text-slate-400 font-semibold">Dặm bay tích lũy</div>
                        <div id="stat-miles-count" class="text-lg font-black text-blue-400 mt-0.5 mono">0 km</div>
                        <div id="stat-flights-count" class="text-[10px] text-slate-400">Đã hạ cánh: 0</div>
                    </div>
                    <div class="w-10 h-10 rounded-xl bg-blue-500/10 border border-blue-500/20 flex items-center justify-center text-lg">🛂</div>
                </div>
            </div>

            <div class="grid grid-cols-1 lg:grid-cols-12 gap-4">
                <div class="lg:col-span-8 bg-gradient-to-br from-blue-950/85 via-slate-900 to-slate-900 border border-cyan-500/30 rounded-3xl p-4 shadow-xl flex flex-col justify-between">
                    <div class="flex flex-wrap items-center justify-between gap-2 mb-2">
                        <div class="flex items-center gap-2">
                            <span data-i18n="aiTitle" class="bg-cyan-400 text-black font-black text-[10px] px-2.5 py-0.5 rounded-full uppercase tracking-wider">💡 Hôm nay nên học gì? (AI Đề xuất)</span>
                            <span data-i18n="aiSub" class="text-xs text-slate-400">Báo giờ bay tự động theo khung giờ đã đặt</span>
                        </div>
                        <button onclick="sendStudyReminderAlert()" data-i18n="btnAlarm" class="bg-white/10 hover:bg-white/15 text-amber-300 border border-amber-400/30 px-3 py-1 rounded-xl text-xs font-bold transition">
                            🔔 Kiểm tra báo thức
                        </button>
                    </div>
                    <div id="ai-today-suggestion" class="bg-black/40 border border-white/10 rounded-2xl p-3"></div>
                </div>

                <div class="lg:col-span-4 dash-card rounded-3xl p-4 flex flex-col justify-between">
                    <div>
                        <h3 data-i18n="smartTitle" class="text-sm font-extrabold text-white mb-1">⚡ Điều phối Lịch AI Thông Minh</h3>
                        <p data-i18n="smartSub" class="text-xs text-slate-400 leading-relaxed">Sắp xếp ưu tiên theo Deadline hoặc dời ca học khi bận đột xuất.</p>
                    </div>
                    <div class="space-y-2 mt-3">
                        <button onclick="aiSortTasks()" data-i18n="btnAiSort" class="w-full bg-gradient-to-r from-amber-500 to-yellow-500 hover:opacity-95 text-black font-black py-2 px-4 rounded-xl text-xs shadow transition">🤖 AI Sắp xếp Ưu tiên</button>
                        <button onclick="handleSuddenScheduleChange()" data-i18n="btnSudden" class="w-full bg-slate-800 hover:bg-slate-700 text-cyan-300 border border-cyan-500/30 font-bold py-2 px-4 rounded-xl text-xs transition">🌪️ Dời lịch đột xuất</button>
                    </div>
                </div>
            </div>

            <!-- CỘT TRÁI & PHẢI -->
            <div class="grid grid-cols-1 lg:grid-cols-12 gap-5">
                <div class="lg:col-span-6 dash-card rounded-3xl p-4 sm:p-5 flex flex-col">
                    <div class="flex flex-wrap items-center justify-between gap-2 mb-3">
                        <div>
                            <h2 class="text-sm sm:text-base font-extrabold text-white flex items-center gap-2">
                                <span data-i18n="todoTitle">✅ Danh Sách Nhiệm Vụ & Chặng Bay</span>
                                <span data-i18n="todoSync" class="text-[10px] bg-emerald-500/20 text-emerald-300 px-2 py-0.5 rounded-lg border border-emerald-400/30">⚡ Tự động nhận từ Lịch</span>
                            </h2>
                            <p data-i18n="todoSub" class="text-[11px] text-slate-400">Thêm môn học ở Lịch sẽ tự động nhảy sang đây kèm giờ bay!</p>
                        </div>
                        <div class="flex bg-slate-900 p-1 rounded-xl border border-white/10 text-xs font-bold">
                            <button id="filter-all" data-i18n="filterAll" onclick="setTaskFilter('all')" class="px-2.5 py-1 rounded-lg bg-blue-600 text-white">Tất cả</button>
                            <button id="filter-pending" data-i18n="filterPending" onclick="setTaskFilter('pending')" class="px-2.5 py-1 rounded-lg text-slate-400 hover:text-white">Đang làm</button>
                            <button id="filter-done" data-i18n="filterDone" onclick="setTaskFilter('done')" class="px-2.5 py-1 rounded-lg text-slate-400 hover:text-white">Đã xong ✓</button>
                        </div>
                    </div>

                    <div class="bg-slate-900/90 border border-white/15 rounded-2xl p-3 mb-4 space-y-2">
                        <div class="flex items-center justify-between">
                            <span data-i18n="quickAdd" class="text-xs font-bold text-cyan-400">+ Thêm nhanh bài tập / deadline lẻ:</span>
                        </div>
                        <div class="grid grid-cols-1 sm:grid-cols-12 gap-2">
                            <input type="text" id="quick-task-title" onkeydown="if(event.key==='Enter') addNewTask()" data-i18n-placeholder="quickPlh" placeholder="Nhập tên công việc (VD: Giải đề Toán...)" class="sm:col-span-6 bg-slate-800 text-white text-xs px-3 py-2 rounded-xl border border-white/10 focus:outline-none focus:border-cyan-400" />
                            <div class="sm:col-span-3 flex items-center bg-slate-800 rounded-xl border border-white/10 px-2.5">
                                <span data-i18n="lblDue" class="text-[10px] text-amber-300 font-bold mr-1.5 shrink-0">Hạn (Giờ):</span>
                                <input type="number" id="quick-task-hours" value="24" min="1" max="720" class="w-full bg-transparent text-white text-xs py-2 focus:outline-none font-bold" />
                            </div>
                            <select id="quick-task-importance" class="sm:col-span-3 bg-slate-800 text-amber-300 text-xs px-2 py-2 rounded-xl border border-white/10 font-bold focus:outline-none">
                                <option value="5">⭐⭐⭐⭐⭐</option><option value="4" selected>⭐⭐⭐⭐</option><option value="3">⭐⭐⭐</option><option value="2">⭐⭐</option>
                            </select>
                        </div>
                        <div class="grid grid-cols-1 sm:grid-cols-12 gap-2 items-center">
                            <div class="sm:col-span-5 flex items-center justify-between bg-slate-800 rounded-xl border border-cyan-500/30 px-2.5 py-1.5">
                                <span class="text-[10px] text-cyan-300 font-bold" data-i18n="lblTime">⏰ Giờ:</span>
                                <input type="time" id="quick-task-start" value="19:30" class="bg-transparent text-white text-xs font-mono font-bold focus:outline-none" />
                                <span class="text-xs text-slate-400">➔</span>
                                <input type="time" id="quick-task-end" value="20:25" class="bg-transparent text-amber-300 text-xs font-mono font-bold focus:outline-none" />
                            </div>
                            <div class="sm:col-span-4 flex items-center bg-slate-800 rounded-xl border border-white/10 px-2.5 py-1.5">
                                <select id="quick-task-dest" class="w-full bg-transparent text-white text-xs font-bold focus:outline-none"></select>
                            </div>
                            <button onclick="addNewTask()" data-i18n="btnSaveTask" class="sm:col-span-3 bg-gradient-to-r from-blue-600 to-cyan-500 hover:opacity-95 text-white font-extrabold py-2 px-3 rounded-xl text-xs shadow-lg transition">+ Lưu Việc</button>
                        </div>
                    </div>

                    <div id="todo-drag-list" class="space-y-2 flex-1 max-h-[540px] overflow-y-auto pr-1"></div>
                </div>

                <div class="lg:col-span-6 dash-card rounded-3xl p-4 sm:p-5 flex flex-col">
                    <div class="flex flex-wrap items-center justify-between gap-2 mb-2.5">
                        <div>
                            <h2 class="text-sm sm:text-base font-extrabold text-white flex items-center gap-2">
                                <span data-i18n="calTitle">🗓️ Lịch Biểu & Việc Cá Nhân</span>
                                <span id="timetable-owner-badge" class="text-xs text-amber-400 font-black"></span>
                            </h2>
                            <p data-i18n="calSub" class="text-[11px] text-slate-400">Tách riêng Lịch học, Việc cá nhân & Mở rộng cả Tháng/Năm</p>
                        </div>
                        <button onclick="toggleLunarDisplay()" id="btn-toggle-lunar" class="bg-amber-500/20 hover:bg-amber-500/30 text-amber-300 border border-amber-400/40 px-2.5 py-1 rounded-xl text-[11px] font-extrabold transition">🌙 Âm lịch: BẬT</button>
                    </div>

                    <div class="grid grid-cols-3 gap-2 bg-slate-900/90 p-2 rounded-2xl border border-white/10 mb-3 text-xs">
                        <div>
                            <div data-i18n="lblMonth" class="text-[9px] text-slate-400 font-bold uppercase mb-0.5">Chọn Tháng</div>
                            <select id="cal-month-select" onchange="onMonthYearDropdownChange()" class="w-full bg-slate-800 text-cyan-300 font-extrabold text-xs px-2 py-1.5 rounded-lg border border-white/10 focus:outline-none">
                                <option value="1">1</option><option value="2">2</option><option value="3">3</option><option value="4">4</option><option value="5">5</option><option value="6">6</option>
                                <option value="7">7</option><option value="8">8</option><option value="9">9</option><option value="10">10</option><option value="11" selected>11</option><option value="12">12</option>
                            </select>
                        </div>
                        <div>
                            <div data-i18n="lblYear" class="text-[9px] text-slate-400 font-bold uppercase mb-0.5">Chọn Năm</div>
                            <select id="cal-year-select" onchange="onMonthYearDropdownChange()" class="w-full bg-slate-800 text-amber-300 font-extrabold text-xs px-2 py-1.5 rounded-lg border border-white/10 focus:outline-none">
                                <option value="2025">2025</option><option value="2026" selected>2026</option><option value="2027">2027</option><option value="2028">2028</option><option value="2029">2029</option>
                            </select>
                        </div>
                        <div>
                            <div data-i18n="lblScope" class="text-[9px] text-emerald-400 font-bold uppercase mb-0.5">Chu kỳ áp dụng</div>
                            <select id="slot-repeat-scope" class="w-full bg-slate-800 text-emerald-300 font-extrabold text-xs px-2 py-1.5 rounded-lg border border-emerald-500/30 focus:outline-none">
                                <option value="Tuần" data-i18n="scWeek">📅 Trong tuần</option>
                                <option value="Tháng" selected data-i18n="scMonth">🗓️ Nguyên tháng</option>
                                <option value="Năm" data-i18n="scYear">📆 Nguyên năm</option>
                            </select>
                        </div>
                    </div>

                    <div id="calendar-weekdays-row" class="grid grid-cols-7 bg-slate-900 border-x border-b border-white/15 text-center py-1.5 text-[11px] font-extrabold text-slate-300"></div>
                    <div id="calendar-days-grid" class="grid grid-cols-7 gap-1 bg-slate-950/90 p-2 rounded-b-2xl border-x border-b border-white/15 mb-3"></div>

                    <div class="bg-slate-900/95 border border-emerald-500/35 rounded-2xl p-3.5 mb-3 space-y-2.5 shadow-lg">
                        <div class="flex flex-wrap items-center justify-between gap-2 border-b border-white/10 pb-2">
                            <div>
                                <div id="selected-full-date-banner" class="text-xs sm:text-sm font-black text-amber-300"></div>
                                <div id="selected-lunar-date-banner" class="text-[11px] text-cyan-300 font-semibold"></div>
                            </div>
                            <div class="flex items-center gap-1.5 bg-slate-800 border border-white/15 px-2.5 py-1 rounded-xl">
                                <span data-i18n="lblPickDate" class="text-[10px] text-slate-300 font-bold">Chọn ngày:</span>
                                <input type="date" id="direct-date-picker" value="2026-11-04" onchange="onDirectDateInputChange()" class="bg-transparent text-white text-xs font-mono font-bold focus:outline-none cursor-pointer" />
                            </div>
                        </div>

                        <div class="grid grid-cols-1 sm:grid-cols-12 gap-2 items-center">
                            <div class="sm:col-span-5 bg-slate-800 border border-white/15 rounded-xl px-2.5 py-1.5 flex items-center justify-between">
                                <span data-i18n="lblStart" class="text-[10px] text-slate-300 font-bold">⏰ Bắt đầu:</span>
                                <input type="time" id="new-slot-start" value="14:00" onchange="updateSlotDurationPreview()" class="bg-transparent text-cyan-300 font-mono font-extrabold text-xs focus:outline-none cursor-pointer" />
                            </div>
                            <div class="sm:col-span-5 bg-slate-800 border border-white/15 rounded-xl px-2.5 py-1.5 flex items-center justify-between">
                                <span data-i18n="lblEnd" class="text-[10px] text-slate-300 font-bold">🏁 Kết thúc:</span>
                                <input type="time" id="new-slot-end" value="15:30" onchange="updateSlotDurationPreview()" class="bg-transparent text-amber-300 font-mono font-extrabold text-xs focus:outline-none cursor-pointer" />
                            </div>
                            <div class="sm:col-span-2 text-center">
                                <span id="calc-slot-mins-preview" class="text-[10px] font-mono bg-cyan-500/20 text-cyan-300 px-2 py-1 rounded-lg font-bold block">90p</span>
                            </div>
                        </div>

                        <div class="grid grid-cols-1 sm:grid-cols-2 gap-2">
                            <div>
                                <div data-i18n="lblCat" class="text-[9px] text-slate-400 font-bold uppercase mb-0.5">Phân loại lịch</div>
                                <select id="new-slot-type" class="w-full bg-slate-800 text-white text-xs px-2.5 py-2 rounded-xl border border-white/15 font-bold focus:outline-none cursor-pointer">
                                    <option value="study" data-i18n="catStudy">📚 Lịch học (Tạo chuyến bay)</option>
                                    <option value="school" data-i18n="catSchool">🔴 Lịch học trên trường (Cố định)</option>
                                    <option value="personal" data-i18n="catPers">🟣 Việc cá nhân (Đi làm, sự kiện...)</option>
                                    <option value="free" data-i18n="catFree">🟢 Khung giờ trống tự học</option>
                                </select>
                            </div>
                            <div>
                                <div data-i18n="repeatCycle" class="text-[9px] text-emerald-400 font-bold uppercase mb-0.5">Chu kỳ lặp lại</div>
                                <select id="slot-repeat-mode" onchange="onRepeatModeChange()" class="w-full bg-slate-800 text-emerald-300 text-xs px-2.5 py-2 rounded-xl border border-emerald-500/30 font-extrabold focus:outline-none cursor-pointer">
                                    <option value="none" data-i18n="rpNone">1️⃣ Không lặp lại</option>
                                    <option value="weekly" data-i18n="rpWeek">🔄 Hàng tuần</option>
                                    <option value="monthly" selected data-i18n="rpMonth">🗓️ Hàng tháng</option>
                                    <option value="yearly" data-i18n="rpYear">📆 Hàng năm</option>
                                    <option value="daily" data-i18n="rpDay">☀️ Hàng ngày</option>
                                    <option value="custom" data-i18n="rpCustom">⚙️ Tùy chỉnh...</option>
                                </select>
                            </div>
                        </div>

                        <div id="custom-repeat-box" class="hidden bg-slate-800/90 border border-amber-400/40 rounded-xl p-2.5 flex flex-wrap items-center justify-between gap-2 text-xs">
                            <span data-i18n="lblCustomRp" class="text-amber-300 font-bold">⚙️ Lặp lại mỗi:</span>
                            <div class="flex items-center gap-1.5">
                                <input type="number" id="custom-repeat-interval" value="2" min="1" max="365" class="w-14 bg-slate-900 text-white font-mono font-bold text-center py-1 rounded-lg border border-white/15" />
                                <select id="custom-repeat-unit" class="bg-slate-900 text-cyan-300 font-bold px-2 py-1 rounded-lg border border-white/15">
                                    <option value="ngày" data-i18n="unitDay">Ngày</option><option value="tuần" selected data-i18n="unitWeek">Tuần</option>
                                    <option value="tháng" data-i18n="unitMonth">Tháng</option><option value="năm" data-i18n="unitYear">Năm</option>
                                </select>
                            </div>
                            <div class="flex items-center gap-1.5">
                                <span data-i18n="lblInDur" class="text-slate-300">Trong:</span>
                                <input type="text" id="custom-repeat-duration" value="3" placeholder="VD: 3..." class="w-16 bg-slate-900 text-amber-300 font-bold px-2 py-1 rounded-lg border border-white/15 text-xs text-center" />
                            </div>
                        </div>

                        <div class="flex gap-2">
                            <input type="text" id="new-slot-subject" data-i18n-placeholder="slotPlh" onkeydown="if(event.key==='Enter') saveNewTimetableSlot()" placeholder="Nhập môn học..." class="flex-1 bg-slate-800 text-white text-xs px-3 py-2 rounded-xl border border-white/15 focus:outline-none focus:border-emerald-400" />
                            <button onclick="saveNewTimetableSlot()" data-i18n="btnAddSlot" class="bg-emerald-600 hover:bg-emerald-500 text-white font-extrabold px-4 py-2 rounded-xl text-xs shrink-0 shadow-lg transition">+ Thêm Lịch</button>
                        </div>
                        <label class="flex items-center gap-2 pt-0.5 cursor-pointer text-[11px] text-cyan-300 font-semibold">
                            <input type="checkbox" id="auto-sync-to-flight" checked class="w-4 h-4 accent-emerald-500 rounded cursor-pointer" />
                            <span data-i18n="lblAutoSync">⚡ Tự động đẩy sang Danh sách Nhiệm vụ & Báo giờ</span>
                        </label>
                    </div>
                    <div id="timetable-slots-list" class="space-y-2 flex-1 max-h-[220px] overflow-y-auto pr-1"></div>
                </div>
            </div>
        </div>
    </main>

    <!-- ========================================================================================= -->
    <!-- TRANG 2: QUẢ ĐỊA CẦU 3D VŨ TRỤ ⟷ BẢN ĐỒ VỆ TINH 2D -->
    <!-- ========================================================================================= -->
    <section id="page-flight" style="z-index: 20;" class="fixed inset-x-0 top-14 bottom-0 overflow-hidden page-layer-hidden">
        <div id="globe-wrapper">
            <canvas id="globe-canvas" class="w-full h-full block cursor-grab active:cursor-grabbing"></canvas>
            <div id="globe-origin-pin" style="z-index: 15;" class="fixed pointer-events-none -translate-x-1/2 -translate-y-1/2 hidden"><div class="bg-cyan-400 text-black font-black text-[10px] px-2 py-0.5 rounded-md shadow-xl border border-black/40 whitespace-nowrap">✈️ <span id="globe-origin-code">SGN</span></div></div>
            <div id="globe-dest-pin" style="z-index: 15;" class="fixed pointer-events-none -translate-x-1/2 -translate-y-1/2 hidden"><div class="bg-yellow-400 text-black font-black text-[10px] px-2 py-0.5 rounded-md shadow-xl border border-black/40 whitespace-nowrap">🏁 <span id="globe-dest-code">DAD</span></div></div>
            <div id="globe-plane-pin" style="z-index: 18;" class="fixed pointer-events-none -translate-x-1/2 -translate-y-1/2 hidden"><div class="relative w-14 h-14 flex items-center justify-center"><div class="radar-ring absolute inset-1 rounded-full border-2 border-cyan-400/80"></div><div id="globe-plane-svg" class="w-12 h-12 relative z-10"></div></div></div>
        </div>
        <div id="map-2d-wrapper"><div id="map"></div></div>

        <div id="zoom-mode-controls" style="z-index: 60;" class="fixed right-4 top-1/3 -translate-y-1/2 flex flex-col items-end gap-2">
            <div class="glass-panel p-1.5 rounded-2xl flex flex-col items-center gap-1.5 shadow-2xl border border-cyan-400/30">
                <button onclick="zoomStepIn()" class="w-9 h-9 rounded-xl bg-slate-800 hover:bg-blue-600 text-white font-black text-base flex items-center justify-center transition border border-white/10">+</button>
                <div id="projection-mode-badge" class="text-[9px] font-mono font-extrabold text-cyan-300 px-1 py-0.5 text-center leading-tight">3D</div>
                <button onclick="zoomStepOut()" class="w-9 h-9 rounded-xl bg-slate-800 hover:bg-blue-600 text-white font-black text-base flex items-center justify-center transition border border-white/10">−</button>
            </div>
            <button onclick="toggleProjectionMode()" id="quick-switch-proj-btn" data-i18n="btnZoomIn" class="glass-panel px-3 py-2 rounded-xl text-[11px] font-extrabold text-amber-300 hover:text-white border border-amber-400/40 shadow-xl whitespace-nowrap">🔍 Phóng to 2D</button>
        </div>

        <div id="flight-top-hud" style="z-index: 7500;" class="fixed top-16 left-1/2 -translate-x-1/2 w-[96%] max-w-4xl hidden flex-wrap items-center justify-between gap-2 pointer-events-none">
            <div class="glass-panel p-1 rounded-2xl flex items-center gap-1 pointer-events-auto shadow-2xl border border-cyan-400/40">
                <button onclick="setCameraView('map')" data-i18n="camMap" class="cam-switch-btn cam-map px-2.5 py-1.5 rounded-xl text-[11px] font-extrabold bg-cyan-500 text-black shadow transition">🌍 Bản Đồ</button>
                <button onclick="setCameraView('cockpit')" data-i18n="camCockpit" class="cam-switch-btn cam-cockpit px-2.5 py-1.5 rounded-xl text-[11px] font-extrabold text-slate-300 hover:text-white transition">👨‍✈️ Phi công</button>
                <button onclick="setCameraView('cabin')" data-i18n="camCabin" class="cam-switch-btn cam-cabin px-2.5 py-1.5 rounded-xl text-[11px] font-extrabold text-slate-300 hover:text-white transition">💺 Cabin</button>
                <button onclick="setCameraView('window')" data-i18n="camWindow" class="cam-switch-btn cam-window px-2.5 py-1.5 rounded-xl text-[11px] font-extrabold text-slate-300 hover:text-white transition">🪟 Cửa Sổ</button>
            </div>
            <div class="glass-panel p-1 rounded-2xl flex items-center gap-1 pointer-events-auto shadow-2xl border border-amber-400/40">
                <button onclick="syncEnvironmentWithRealTime()" data-i18n="envAuto" class="env-switch-btn env-auto px-2.5 py-1.5 rounded-xl text-[11px] font-bold bg-amber-400 text-black shadow">🕒 Giờ thực</button>
                <button onclick="setFlightEnvironment('day')" data-i18n="envDay" class="env-switch-btn env-day px-2 py-1.5 rounded-xl text-[11px] font-bold text-slate-300 hover:text-white">☀️ Ngày</button>
                <button onclick="setFlightEnvironment('sunset')" data-i18n="envSunset" class="env-switch-btn env-sunset px-2 py-1.5 rounded-xl text-[11px] font-bold text-slate-300 hover:text-white">🌅 Hoàng hôn</button>
                <button onclick="setFlightEnvironment('night')" data-i18n="envNight" class="env-switch-btn env-night px-2 py-1.5 rounded-xl text-[11px] font-bold text-slate-300 hover:text-white">🌙 Đêm</button>
                <button onclick="setFlightEnvironment('rain')" data-i18n="envRain" class="env-switch-btn env-rain px-2 py-1.5 rounded-xl text-[11px] font-bold text-slate-300 hover:text-white">🌧️ Mưa</button>
            </div>
        </div>

        <div id="view-cockpit" style="z-index: 45;" class="fixed inset-x-0 top-14 bottom-0 hidden flex-col justify-between overflow-hidden">
            <div id="cockpit-sky-bg" class="absolute inset-0 bg-gradient-to-b from-[#040b1a] via-[#0c2249] to-[#1e3a8a] transition-all duration-700">
                <div id="cockpit-stars" class="absolute inset-0 opacity-90" style="background-image: radial-gradient(white 1px, transparent 1px), radial-gradient(rgba(255,255,255,0.7) 1.5px, transparent 1.5px); background-size: 55px 55px, 95px 95px;"></div>
                <div class="cloud-anim-1 absolute top-1/3 w-96 h-24 bg-white/10 blur-2xl rounded-full"></div>
                <div class="cloud-anim-2 absolute top-1/2 w-[500px] h-28 bg-cyan-300/10 blur-3xl rounded-full"></div>
                <div id="cockpit-rain-layer" class="rain-overlay absolute inset-0 hidden pointer-events-none"></div>
            </div>
            <div class="relative z-10 flex-1 flex items-center justify-center pointer-events-none mt-10">
                <div class="absolute inset-y-0 left-1/2 -translate-x-1/2 w-4 bg-gradient-to-r from-slate-950 via-slate-800 to-slate-950 border-x border-white/10"></div>
                <div class="w-[320px] sm:w-[440px] h-[230px] sm:h-[260px] border-2 border-emerald-400/50 rounded-3xl bg-emerald-950/15 backdrop-blur-[1px] p-4 flex flex-col justify-between shadow-[0_0_50px_rgba(16,185,129,0.15)]">
                    <div class="flex justify-between items-center text-[11px] font-mono font-bold text-emerald-400 border-b border-emerald-400/30 pb-1"><span>SPD: <b id="hud-speed">840 KM/H</b></span><span class="bg-emerald-400/20 px-2 py-0.5 rounded border border-emerald-400/40">HDG <b id="hud-heading">045°</b></span><span>ALT: <b id="hud-alt">36,000 FT</b></span></div>
                    <div class="relative flex-1 flex items-center justify-center overflow-hidden my-1">
                        <div class="hud-horizon w-52 flex flex-col items-center space-y-2.5">
                            <div class="w-28 border-b border-dashed border-emerald-400/60 text-[9px] font-mono text-emerald-400 flex justify-between"><span>+10</span><span>+10</span></div>
                            <div class="w-44 border-b-2 border-emerald-400 text-[10px] font-mono text-emerald-300 flex justify-between"><span>0</span><span>PITCH</span><span>0</span></div>
                            <div class="w-28 border-b border-dashed border-emerald-400/60 text-[9px] font-mono text-emerald-400 flex justify-between"><span>-10</span><span>-10</span></div>
                        </div>
                        <div class="absolute text-emerald-300 font-mono font-black text-base">─ ✛ ─</div>
                    </div>
                    <div class="flex justify-between items-center text-[10px] font-mono text-emerald-300 border-t border-emerald-400/30 pt-1"><span id="hud-aircraft-name">AIRBUS A321NEO</span><span id="hud-route-code">SGN ➔ DAD</span></div>
                </div>
            </div>
            <div class="relative z-10 h-44 bg-gradient-to-t from-[#05070e] via-[#0d1322] to-[#1a243b] border-t-4 border-slate-700/80 px-4 py-2.5 shadow-2xl">
                <div class="max-w-3xl mx-auto grid grid-cols-3 gap-3 h-24">
                    <div class="bg-[#060a12] border border-slate-700 rounded-xl p-2 flex flex-col justify-between font-mono">
                        <div class="text-[9px] text-cyan-400 font-bold flex justify-between"><span>PFD</span><span class="text-emerald-400">AP1+FD</span></div>
                        <div class="flex items-center justify-center"><div id="cockpit-plane-svg-preview" class="w-10 h-10"></div></div>
                        <div class="text-[9px] text-slate-400 flex justify-between"><span id="cockpit-real-clock">00:00</span><span>ETA <b id="cockpit-eta">--:--</b></span></div>
                    </div>
                    <div class="bg-[#060a12] border border-cyan-500/40 rounded-xl p-2 flex flex-col items-center justify-center font-mono">
                        <div class="text-[8px] text-amber-400 uppercase font-bold">TIMER</div>
                        <div id="cockpit-timer-display" class="text-xl sm:text-2xl font-extrabold text-white">55:00</div>
                        <div id="cockpit-task-display" class="text-[9px] text-cyan-300 truncate max-w-[140px]">💻 Work</div>
                    </div>
                    <div class="bg-[#060a12] border border-slate-700 rounded-xl p-2 flex flex-col justify-between font-mono relative overflow-hidden">
                        <div class="text-[9px] text-emerald-400 font-bold flex justify-between"><span>RADAR</span><span id="cockpit-dist-display">605 KM</span></div>
                        <div class="w-11 h-11 rounded-full border border-emerald-500/40 mx-auto flex items-center justify-center relative"><div class="radar-ring absolute inset-0 rounded-full border border-emerald-400"></div><span class="text-[10px]">✈️</span></div>
                    </div>
                </div>
            </div>
        </div>

        <div id="view-cabin" style="z-index: 45;" class="fixed inset-x-0 top-14 bottom-0 hidden flex-col items-center justify-center bg-gradient-to-b from-[#131129] via-[#0e172a] to-[#060913] p-4 overflow-hidden">
            <div id="cabin-ceiling-glow" class="absolute top-0 inset-x-0 h-32 bg-gradient-to-b from-purple-500/30 via-cyan-500/15 to-transparent blur-2xl pointer-events-none transition-all duration-700"></div>
            <div class="relative z-10 flex items-center gap-2 mb-3">
                <div class="bg-slate-900/90 border border-white/15 px-3 py-1 rounded-full flex items-center gap-2 text-[11px]">
                    <span class="text-amber-400 font-bold">🔔 FASTEN SEATBELT</span><span class="text-slate-600">|</span><span class="text-cyan-300 font-mono" id="cabin-real-clock">00:00:00</span>
                </div>
                <button onclick="cycleCabinMoodLight()" data-i18n="btnLed" class="bg-white/10 hover:bg-white/20 border border-white/20 px-3 py-1 rounded-full text-[11px] font-bold text-cyan-300">🌈 Đèn LED</button>
            </div>
            <div class="relative z-10 w-full max-w-lg bg-gradient-to-b from-[#1e293b] to-[#0f172a] border-4 border-slate-700/80 rounded-t-[40px] rounded-b-3xl p-4 sm:p-5 shadow-2xl mb-20">
                <div class="w-40 h-7 bg-slate-800 border border-white/10 rounded-b-xl mx-auto -mt-5 mb-3 flex items-center justify-center text-[10px] font-extrabold text-amber-300 tracking-widest">
                    SEAT <span id="cabin-seat-label" class="ml-1">06A</span>
                </div>
                <div class="bg-[#060a14] border-4 border-slate-950 rounded-2xl p-4 shadow-inner">
                    <div class="flex items-center justify-between border-b border-white/10 pb-2 mb-2.5">
                        <span id="cabin-aircraft-label" class="text-xs font-bold text-cyan-400 mono">Airbus A321neo</span>
                        <span id="cabin-route-label" class="text-xs font-extrabold text-yellow-400 mono">SGN ➔ DAD</span>
                    </div>
                    <div class="grid grid-cols-2 gap-3 items-center">
                        <div>
                            <div data-i18n="focusLbl" class="text-[10px] text-slate-400 uppercase font-bold">Mục tiêu</div>
                            <div id="cabin-task-title" class="text-sm font-extrabold text-white mt-0.5 truncate">💻 Work</div>
                            <div class="text-[11px] text-emerald-400 mt-1">👤 <b id="cabin-passenger-name">Hữu Đại</b></div>
                            <div class="text-[10px] text-slate-400 font-mono mt-1"><span data-i18n="etaLbl">ETA</span>: <b id="cabin-eta" class="text-amber-300">--:--</b></div>
                        </div>
                        <div class="bg-slate-900/90 border border-white/10 rounded-xl p-2.5 text-center">
                            <div data-i18n="timeLeft" class="text-[9px] text-slate-400 uppercase">Thời gian còn lại</div>
                            <div id="cabin-timer-display" class="text-2xl font-black text-cyan-400 mono">55:00</div>
                            <div class="text-[10px] text-amber-300"><span id="cabin-dist-display">605</span> km</div>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <div id="view-window" style="z-index: 45;" class="fixed inset-x-0 top-14 bottom-0 hidden flex-col items-center justify-center bg-[#090d18] p-4 overflow-hidden">
            <div class="relative z-20 flex items-center gap-3 mb-2">
                <button onclick="toggleWindowShade()" data-i18n="btnShade" class="glass-panel px-3.5 py-1 rounded-full text-xs font-extrabold text-amber-300 hover:text-white border border-amber-400/30">🪟 Kéo Rèm Cửa Sổ</button>
            </div>
            <div class="relative w-[280px] sm:w-[330px] h-[360px] sm:h-[400px] rounded-[150px] border-[16px] border-[#1e293b] shadow-[inset_0_0_40px_rgba(0,0,0,0.9),0_25px_70px_rgba(0,0,0,0.95)] overflow-hidden bg-gradient-to-b from-[#040b1d] via-[#0f2557] to-[#1e3a8a] mb-20" id="window-sky-container">
                <div id="window-stars" class="absolute inset-0 opacity-0 transition-opacity duration-700" style="background-image: radial-gradient(white 1.2px, transparent 1.2px), radial-gradient(rgba(255,255,255,0.6) 1px, transparent 1px); background-size: 45px 45px, 80px 80px;"></div>
                <div id="window-celestial" class="absolute top-10 right-12 w-11 h-11 rounded-full bg-yellow-100 shadow-[0_0_35px_#fef08a]"></div>
                <div class="cloud-anim-1 absolute top-36 w-64 h-14 bg-white/20 blur-xl rounded-full"></div>
                <div class="cloud-anim-3 absolute bottom-24 w-72 h-16 bg-white/15 blur-xl rounded-full"></div>
                <div id="window-city-lights" class="absolute bottom-0 inset-x-0 h-14 bg-gradient-to-t from-amber-500/25 via-orange-500/10 to-transparent"></div>
                <div class="absolute bottom-10 right-0 w-[240px] h-[125px] pointer-events-none">
                    <svg viewBox="0 0 300 160" class="w-full h-full drop-shadow-2xl">
                        <ellipse cx="145" cy="112" rx="34" ry="18" fill="#334155" stroke="#64748b" stroke-width="2"/><ellipse cx="115" cy="112" rx="8" ry="15" fill="#0f172a" stroke="#38bdf8" stroke-width="1.5"/>
                        <polygon points="300,35 35,95 55,112 300,98" fill="#cbd5e1" stroke="#94a3b8" stroke-width="2"/><polygon points="35,95 15,62 28,60 55,112" fill="#0ea5e9"/><circle cx="22" cy="62" r="5" fill="#ef4444" class="strobe-light"/>
                    </svg>
                </div>
                <div id="window-rain-layer" class="rain-overlay absolute inset-0 hidden pointer-events-none"></div>
                <div id="window-shade-panel" class="absolute inset-x-0 top-0 h-0 bg-gradient-to-b from-slate-800 to-slate-900 border-b-4 border-slate-600 transition-all duration-500 flex items-end justify-center pb-2 overflow-hidden"><div class="w-12 h-1.5 rounded-full bg-slate-400"></div></div>
            </div>
        </div>

        <button id="toggle-booking-btn" style="z-index: 60;" data-i18n="lblCollapse" onclick="toggleBookingCardSize()" class="fixed bottom-3 left-3 glass-panel px-3 py-1.5 rounded-xl text-[11px] font-extrabold text-cyan-300 hover:text-white shadow-lg border border-cyan-500/30">🔽 Thu gọn bảng</button>

        <div id="screen-booking" style="z-index: 60;" class="fixed bottom-3 left-1/2 -translate-x-1/2 w-[95%] max-w-md glass-panel rounded-3xl p-3.5 shadow-2xl transition-all duration-300">
            <div class="flex items-center justify-between gap-2 mb-2.5 pb-2 border-b border-white/10">
                <div class="flex items-center gap-2.5">
                    <div id="booking-plane-svg-box" class="w-10 h-10 rounded-xl bg-slate-900 border border-cyan-400/30 flex items-center justify-center p-1 shrink-0"></div>
                    <div>
                        <div class="flex items-center gap-1.5">
                            <span id="badge-origin" class="bg-cyan-400 text-black font-black text-[10px] px-1.5 py-0.5 rounded">SGN</span><span class="text-xs text-slate-400">➔</span>
                            <span id="badge-dest" class="bg-yellow-400 text-black font-black text-[10px] px-1.5 py-0.5 rounded">DAD</span><span id="badge-dist" class="text-[11px] font-mono text-cyan-300 font-bold ml-1">605 km</span>
                        </div>
                        <div id="banner-dest-title" class="text-xs font-extrabold text-white mt-0.5 truncate max-w-[175px]">TP.HCM ➔ Đà Nẵng</div>
                    </div>
                </div>
                <select id="aircraft-select" onchange="updateAircraft()" class="bg-slate-800 text-cyan-300 text-[11px] font-bold px-2 py-1.5 rounded-xl border border-cyan-500/30 focus:outline-none cursor-pointer">
                    <option value="Airbus A321neo">🛩️ A321neo (840 km/h)</option><option value="Boeing 787-9">✈️ B787-9 (910 km/h)</option><option value="Airbus A350-900">🛫 A350-900 (905 km/h)</option><option value="ATR 72-600">⚙️ ATR 72 (510 km/h)</option>
                </select>
            </div>

            <div class="grid grid-cols-11 gap-1.5 items-center bg-slate-900/90 p-2 rounded-2xl border border-white/10 mb-2.5">
                <div class="col-span-5">
                    <div data-i18n="lblOrigin" class="text-[9px] text-slate-400 uppercase font-bold mb-0.5">ĐIỂM KHỞI HÀNH</div>
                    <select id="origin-select" onchange="onRouteChange()" class="w-full bg-slate-800 text-white font-bold text-[11px] px-2 py-1.5 rounded-lg border border-white/10 focus:outline-none cursor-pointer"></select>
                </div>
                <div class="col-span-1 flex justify-center pt-3">
                    <button onclick="swapRoute()" class="w-7 h-7 rounded-full bg-slate-800 hover:bg-blue-600 text-cyan-400 hover:text-white font-bold text-xs flex items-center justify-center transition border border-white/10">⇄</button>
                </div>
                <div class="col-span-5">
                    <div data-i18n="lblDest" class="text-[9px] text-yellow-400 uppercase font-bold mb-0.5">ĐIỂM HẠ CÁNH</div>
                    <select id="dest-select" onchange="onRouteChange()" class="w-full bg-slate-800 text-white font-bold text-[11px] px-2 py-1.5 rounded-lg border border-yellow-400/40 focus:outline-none cursor-pointer"></select>
                </div>
            </div>

            <div class="bg-blue-950/50 border border-cyan-400/30 rounded-2xl p-2.5 mb-2.5 flex items-center justify-between">
                <div>
                    <div data-i18n="lblDuration" class="text-[9px] text-cyan-300 font-bold uppercase tracking-wider">⏱️ Thời gian (Theo khoảng cách)</div>
                    <div class="flex items-baseline gap-2 mt-0.5">
                        <span id="auto-calc-duration-text" class="text-base font-black text-yellow-400 mono">55 phút</span>
                        <span id="auto-calc-speed-text" class="text-[10px] text-slate-300">(605 km • 840 km/h)</span>
                    </div>
                </div>
                <div class="text-right font-mono">
                    <div data-i18n="lblEta" class="text-[9px] text-slate-400">ETA</div>
                    <div id="booking-realtime-eta" class="text-xs font-extrabold text-emerald-400">--:--</div>
                </div>
            </div>

            <div class="flex gap-2">
                <button onclick="goToSeatSelection()" data-i18n="btnPickSeat" class="w-1/2 bg-slate-800 hover:bg-slate-700 text-cyan-300 font-extrabold py-2.5 rounded-2xl text-xs border border-cyan-500/30 transition">💺 Chọn Ghế & In Vé</button>
                <button onclick="startFlight()" data-i18n="btnFlyNow" class="w-1/2 bg-gradient-to-r from-emerald-500 to-cyan-500 hover:opacity-95 text-black font-black py-2.5 rounded-2xl shadow-lg text-xs uppercase tracking-wider transition">🛫 Bay Ngay Lập Tức</button>
            </div>
        </div>

        <div id="screen-seat" style="z-index: 65;" class="fixed inset-x-0 top-14 bottom-0 bg-[#070b14]/95 backdrop-blur-xl hidden flex-col items-center justify-between py-3 px-4">
            <div class="w-full max-w-md flex items-center justify-between">
                <button onclick="backToBooking()" data-i18n="btnBackRoute" class="bg-slate-800 hover:bg-slate-700 text-slate-200 px-3 py-1.5 rounded-xl text-xs font-bold">‹ Đổi chặng</button>
                <div class="text-center">
                    <div id="seat-header-aircraft" class="text-[10px] text-cyan-400 font-extrabold uppercase tracking-widest">AIRBUS A321NEO</div>
                    <div id="seat-header-route" class="text-xs font-extrabold text-white">SGN ➔ DAD • 55p</div>
                </div>
                <span id="seat-selected-badge" class="bg-blue-600/30 border border-blue-400 text-blue-200 text-xs font-mono font-bold px-2 py-1 rounded-lg">06A</span>
            </div>

            <div class="relative w-full max-w-[320px] flex-1 max-h-[62vh] fuselage flex flex-col items-center pt-8 pb-6 px-5 overflow-y-auto my-2">
                <div class="w-28 h-5 border-b border-slate-700/80 mb-3 flex items-center justify-center text-[9px] font-mono text-slate-500 tracking-widest uppercase">Cockpit</div>
                <div class="grid grid-cols-5 w-full text-center text-xs font-extrabold text-slate-400 mb-2 px-1"><div>A</div><div>C</div><div></div><div>D</div><div>F</div></div>
                <div id="seat-grid" class="w-full space-y-1.5 pb-4"></div>
            </div>

            <div id="focus-popover-backdrop" style="z-index: 70;" class="fixed inset-0 bg-black/65 backdrop-blur-sm hidden items-center justify-center p-4">
                <div class="focus-popover w-full max-w-[350px] rounded-[26px] p-5 text-white">
                    <div class="flex justify-between items-center mb-1">
                        <span class="text-xs font-bold text-blue-300">Seat: <span id="pop-seat-code" class="mono text-white">06A</span></span>
                        <button onclick="closeFocusPopover()" class="text-slate-400 hover:text-white text-sm font-bold">✕</button>
                    </div>
                    <h3 data-i18n="focusQuest" class="text-sm font-extrabold text-white mb-3">Bạn muốn tập trung làm gì trên chuyến bay này?</h3>
                    <div class="flex flex-wrap gap-1.5 mb-3" id="focus-pills-container"></div>
                    <div id="custom-focus-box" class="mb-3">
                        <input type="text" id="custom-focus-input" data-i18n-placeholder="focusPlh" placeholder="Nhập mục tiêu (VD: Toán, Tạo app...)" class="w-full bg-slate-900/90 text-xs text-white px-3 py-2 rounded-xl border border-blue-400/40 focus:outline-none" />
                    </div>
                    <div class="bg-red-500/15 border border-red-400/30 p-2.5 rounded-2xl flex items-center justify-between mb-3.5">
                        <div>
                            <div data-i18n="lblStrict" class="text-xs font-extrabold text-red-200">🔒 Khóa Kỷ Luật (Strict Mode)</div>
                            <div data-i18n="lblStrictSub" class="text-[10px] text-slate-300">Báo động đỏ nếu rời khỏi màn hình học</div>
                        </div>
                        <input type="checkbox" id="strict-mode-toggle" checked class="w-4 h-4 accent-red-500 cursor-pointer" />
                    </div>
                    <button onclick="confirmSeatAndFocus()" data-i18n="btnConfirmPass" class="w-full bg-gradient-to-r from-blue-600 to-cyan-500 hover:opacity-95 text-white font-extrabold py-3 rounded-2xl text-xs shadow-lg">Xác nhận Ghế & Xuất Vé ➔</button>
                </div>
            </div>

            <div class="w-full max-w-md flex items-center justify-between px-2">
                <div data-i18n="hintSeat" class="text-xs text-slate-400">Chạm vào ghế bất kỳ hoặc bấm Tiếp tục</div>
                <button onclick="showBoardingPass()" data-i18n="btnContinue" class="bg-blue-600 hover:bg-blue-500 text-white font-extrabold px-5 py-2 rounded-xl text-xs shadow-lg">Tiếp tục ➔</button>
            </div>
        </div>

        <div id="screen-ticket" style="z-index: 65;" class="fixed inset-x-0 top-14 bottom-0 bg-black/85 backdrop-blur-md hidden items-center justify-center p-4">
            <div class="w-full max-w-sm flex flex-col items-center">
                <div class="w-full bg-[#121723] border border-white/15 rounded-3xl overflow-hidden shadow-2xl relative">
                    <div class="ticket-cutout-left"></div><div class="ticket-cutout-right"></div>
                    <div class="bg-gradient-to-r from-blue-600 to-cyan-500 px-5 py-2.5 flex justify-between items-center">
                        <span class="text-xs font-black tracking-widest uppercase text-white">BOARDING PASS</span>
                        <span id="tk-aircraft" class="text-[11px] font-mono font-bold bg-black/25 text-white px-2 py-0.5 rounded">Airbus A321neo</span>
                    </div>
                    <div class="p-5">
                        <div class="flex justify-between items-start mb-3">
                            <div>
                                <div data-i18n="passTitle" class="text-[9px] text-slate-400 uppercase">Hành khách</div>
                                <div id="tk-passenger" class="text-sm font-black text-amber-300 uppercase">HỮU ĐẠI</div>
                            </div>
                            <div class="text-right">
                                <div data-i18n="realTimeTitle" class="text-[9px] text-slate-400 uppercase">Giờ thực tế</div>
                                <div id="tk-realtime-span" class="text-xs font-extrabold text-emerald-400 mono">15:44 ➔ 16:39</div>
                            </div>
                        </div>
                        <div class="flex justify-between items-center my-3">
                            <div>
                                <div id="tk-origin-code" class="text-3xl font-black text-white">SGN</div>
                                <div id="tk-origin-name" class="text-[11px] text-slate-400">TP.HCM</div>
                            </div>
                            <div class="flex flex-col items-center">
                                <div id="tk-plane-svg" class="w-8 h-8"></div>
                                <span id="tk-duration" class="text-xs font-extrabold text-yellow-400 mt-0.5">55p</span>
                            </div>
                            <div class="text-right">
                                <div id="tk-dest-code" class="text-3xl font-black text-yellow-400">DAD</div>
                                <div id="tk-dest-name" class="text-[11px] text-slate-400">Đà Nẵng</div>
                            </div>
                        </div>
                        <div class="grid grid-cols-3 gap-2 pt-3 border-t border-white/10 text-xs mb-4">
                            <div>
                                <div data-i18n="seatTitle" class="text-slate-500 text-[9px] uppercase">Ghế</div>
                                <div id="tk-seat" class="font-extrabold text-cyan-400 mt-0.5 mono">06A</div>
                            </div>
                            <div>
                                <div data-i18n="distTitle" class="text-slate-500 text-[9px] uppercase">Khoảng cách</div>
                                <div id="tk-dist" class="font-bold text-white mt-0.5">605 km</div>
                            </div>
                            <div class="text-right">
                                <div data-i18n="focusTitle" class="text-slate-500 text-[9px] uppercase">Mục tiêu</div>
                                <div id="tk-focus" class="font-extrabold text-blue-300 mt-0.5 truncate">💻 Work</div>
                            </div>
                        </div>
                        <div class="border-b-2 border-dashed border-slate-700/80 my-3"></div>
                        <div class="flex justify-between items-center text-[10px] font-mono text-slate-400">
                            <span id="tk-strict-badge" class="text-red-400 font-bold">🔒 STRICT LOCK ON</span>
                            <span class="text-cyan-400 font-bold">GATE 04 • READY</span>
                        </div>
                    </div>
                </div>
                <div class="flex gap-2 w-full mt-3.5">
                    <button onclick="backToSeatFromTicket()" data-i18n="btnChangeSeat" class="w-1/3 bg-slate-800 hover:bg-slate-700 text-slate-300 font-bold py-3 rounded-2xl text-xs">‹ Đổi ghế</button>
                    <button onclick="startFlight()" data-i18n="btnTakeoff" class="w-2/3 bg-gradient-to-r from-emerald-500 to-cyan-500 hover:opacity-95 text-black font-black py-3 rounded-2xl shadow-xl text-xs uppercase tracking-wider">🛫 Cất Cánh Học</button>
                </div>
            </div>
        </div>

        <!-- MÀN HÌNH 4: ĐANG BAY -->
        <div id="screen-flying" style="z-index: 7500;" class="fixed bottom-3 left-1/2 -translate-x-1/2 w-[95%] max-w-lg glass-panel rounded-3xl p-3.5 shadow-2xl hidden">
            <div class="flex items-center justify-between border-b border-white/10 pb-2 mb-2">
                <div class="flex items-center gap-2.5">
                    <div id="fly-mini-svg" class="w-9 h-9 rounded-xl bg-slate-900 border border-cyan-400/40 p-1 flex items-center justify-center"></div>
                    <div>
                        <div class="text-xs font-extrabold text-white" id="fly-route-text">TP.HCM ➔ Đà Nẵng</div>
                        <div class="text-[10px] text-cyan-400 font-semibold" id="fly-sub-info">Airbus A321neo • Ghế 06A</div>
                    </div>
                </div>
                <div class="text-right">
                    <div class="text-[9px] text-slate-400 font-mono">ETA <b id="fly-eta-badge" class="text-amber-300">--:--</b></div>
                    <div id="safety-hearts" class="text-xs tracking-widest mt-0.5">❤️❤️❤️</div>
                </div>
            </div>
            <div class="flex items-end justify-between">
                <div>
                    <div class="text-[9px] uppercase tracking-widest text-slate-400 flex items-center gap-2">
                        <span data-i18n="lblTimeLeft">Thời gian bay còn lại</span>
                        <span id="telemetry-live-badge" class="text-[9px] text-emerald-400 font-mono">● 840 KM/H</span>
                    </div>
                    <div id="countdown-timer" class="mono text-2xl sm:text-3xl font-extrabold text-white tracking-tight">55:00</div>
                </div>
                <div class="text-right">
                    <div class="text-[11px] text-slate-300 font-semibold mb-1"><span data-i18n="lblDistLeft">Còn</span> <span id="fly-dist-left" class="text-yellow-400 font-bold">605</span> km</div>
                    <div class="flex gap-1.5">
                        <button onclick="centerOnPlane()" data-i18n="btnTarget" class="bg-slate-800 hover:bg-slate-700 text-xs px-2.5 py-1.5 rounded-xl text-slate-200 border border-white/10 font-bold">🎯</button>
                        <button onclick="completeFlightEarly()" data-i18n="btnFinish" class="bg-emerald-500/20 hover:bg-emerald-500/30 text-emerald-300 border border-emerald-500/30 px-2.5 py-1.5 rounded-xl text-xs font-bold">✓ Xong</button>
                        <button onclick="abortFlight()" data-i18n="btnAbort" class="bg-red-500/20 hover:bg-red-500/30 text-red-300 border border-red-500/30 px-2.5 py-1.5 rounded-xl text-xs font-bold">Hủy</button>
                    </div>
                </div>
            </div>
            <div class="w-full bg-slate-800 h-2 rounded-full overflow-hidden mt-2.5"><div id="flight-progress" class="bg-gradient-to-r from-blue-500 via-cyan-400 to-yellow-400 h-full w-0 transition-all duration-500"></div></div>
        </div>
    </section>

    <!-- MODAL TÙY CHỈNH ÂM THANH & BOT -->
    <div id="media-modal" style="z-index: 9000;" class="fixed inset-0 bg-black/75 backdrop-blur-md hidden items-center justify-center p-4">
        <div class="glass-panel w-full max-w-md rounded-3xl p-5 shadow-2xl">
            <div class="flex justify-between items-center mb-3">
                <h3 class="text-sm font-extrabold text-white">🎧 Settings</h3>
                <button onclick="closeMediaModal()" class="text-slate-400 hover:text-white text-lg font-bold">✕</button>
            </div>
            <div class="space-y-3 text-xs">
                <div class="bg-slate-900/90 p-3 rounded-2xl border border-white/10">
                    <label class="font-bold text-cyan-400 block mb-1">1. Chọn file Lofi từ máy (.mp3, .wav):</label>
                    <input type="file" accept="audio/*" onchange="handleLocalAudio(this)" class="w-full text-slate-300 file:mr-2 file:py-1 file:px-3 file:rounded-xl file:border-0 file:font-bold file:bg-blue-600 file:text-white cursor-pointer mb-1.5" />
                    <input type="text" id="audio-url-input" placeholder="Hoặc dán link MP3..." class="w-full bg-slate-800 text-white px-3 py-1.5 rounded-xl border border-white/10" />
                </div>
                <div class="bg-slate-900/90 p-3 rounded-2xl border border-white/10 flex items-center justify-between">
                    <div>
                        <div class="font-bold text-white">🛫 Tiếng động cơ máy bay (White Noise)</div>
                    </div>
                    <input type="checkbox" onchange="toggleCabinNoise(this.checked)" class="w-5 h-5 accent-cyan-400 cursor-pointer" />
                </div>
                <div class="bg-slate-900/90 p-3 rounded-2xl border border-amber-400/30">
                    <label class="font-bold text-amber-300 block mb-1">2. Đổi ảnh đại diện Chatbot AI:</label>
                    <input type="file" accept="image/*" onchange="handleBotAvatarUpload(this)" class="w-full text-slate-300 file:mr-2 file:py-1 file:px-3 file:rounded-xl file:border-0 file:font-bold file:bg-amber-500 file:text-black cursor-pointer" />
                </div>
            </div>
            <button onclick="applyCustomMedia()" class="mt-4 w-full bg-gradient-to-r from-blue-600 to-cyan-500 text-white font-extrabold py-2.5 rounded-xl text-xs">Lưu & Đóng</button>
        </div>
    </div>

    <!-- CHATBOT AI VÀNG KIM -->
    <div id="chatbot-launcher" onclick="toggleChatbotWindow()" style="position: fixed; bottom: 78px; right: 16px; z-index: 9999;" class="cursor-pointer flex items-center gap-2 bg-[#111827] hover:bg-[#1e293b] border-2 border-[#d4a349] pl-3 pr-1.5 py-1 rounded-full bot-launcher-glow shadow-2xl">
        <span class="text-xs font-extrabold text-amber-300 tracking-wide">💬 Chat AI</span>
        <div class="relative w-9 h-9 rounded-full bg-white p-0.5">
            <img id="bot-launcher-img" src="https://cdn-icons-png.flaticon.com/512/4712/4712109.png" class="w-full h-full rounded-full object-cover bg-gradient-to-b from-yellow-300 to-amber-500 p-0.5" />
            <span class="absolute -top-0.5 -right-0.5 w-2.5 h-2.5 bg-emerald-500 border-2 border-white rounded-full"></span>
        </div>
    </div>

    <div id="chatbot-window" style="position: fixed; bottom: 136px; right: 16px; z-index: 9999;" class="w-[335px] sm:w-[360px] h-[430px] bg-[#f8f9fa] text-slate-800 rounded-2xl shadow-2xl border-2 border-[#d4a349] hidden flex-col overflow-hidden">
        <div class="bg-[#d4a349] text-white px-4 py-2.5 flex items-center justify-between shadow">
            <div class="flex items-center gap-2">
                <div class="w-7 h-7 rounded-full bg-white p-0.5 shadow">
                    <img id="bot-header-img" src="https://cdn-icons-png.flaticon.com/512/4712/4712109.png" class="w-full h-full rounded-full object-cover bg-amber-400" />
                </div>
                <span id="lbl-bot-header" class="font-bold text-xs">Trợ lý Học tập AI</span>
            </div>
            <div class="flex items-center gap-3 text-white">
                <button onclick="resetChat()" title="Làm mới" class="text-xs font-bold">↺</button>
                <button onclick="toggleChatbotWindow()" class="text-base font-bold leading-none">✕</button>
            </div>
        </div>
        <div id="chat-messages" class="flex-1 p-3 overflow-y-auto space-y-2.5 bg-[#f7f8fc]"></div>
        <div class="px-2.5 py-1.5 bg-white border-t border-slate-100 flex gap-1.5 overflow-x-auto">
            <button onclick="sendQuickChat('q1')" id="lbl-q1" class="shrink-0 bg-amber-50 hover:bg-amber-100 text-[#b07d2b] border border-[#d4a349]/40 text-[10px] font-semibold px-2 py-1 rounded-full">💡 Hôm nay học gì?</button>
            <button onclick="sendQuickChat('q2')" id="lbl-q2" class="shrink-0 bg-amber-50 hover:bg-amber-100 text-[#b07d2b] border border-[#d4a349]/40 text-[10px] font-semibold px-2 py-1 rounded-full">📋 Việc đang làm</button>
            <button onclick="sendQuickChat('q3')" id="lbl-q3" class="shrink-0 bg-amber-50 hover:bg-amber-100 text-[#b07d2b] border border-[#d4a349]/40 text-[10px] font-semibold px-2 py-1 rounded-full">🌪️ Dời lịch</button>
        </div>
        <div class="p-2 bg-white border-t border-slate-200 flex items-center gap-2">
            <input type="text" id="chat-input" onkeydown="if(event.key==='Enter') sendChatMessage()" placeholder="..." class="flex-1 text-xs text-slate-800 px-2 py-1 focus:outline-none" />
            <button onclick="sendChatMessage()" class="w-7 h-7 rounded-full bg-[#d4a349] hover:bg-[#c29138] text-white flex items-center justify-center shadow text-xs">➤</button>
        </div>
    </div>

    <script>
        // ================= 1. HỆ THỐNG ĐA NGÔN NGỮ (I18N) =================
        let currentLang = "vi";
        let showLunarCalendar = true;

        const I18N = {
            vi: {
                appTitle: "STUDYHUB & SATELLITE 3D", saveSync: "● Đã tự động lưu", memberTitle: "Thành viên",
                tabDash: "📊 Bảng Điều Khiển", tabFlight: "✈️ Chuyến Bay 3D / 2D", btnLofi: "🎵 Nhạc Lofi",
                bannerTag: "Thông báo Chuyến bay từ Lịch", bannerBtn: "🛫 Cất cánh học ngay",
                kpiProfile: "Hồ sơ thành viên", kpiProfileSub: "Đồng bộ Lịch ➔ Chuyến bay",
                kpiTask: "Nhiệm vụ & Lịch bay", kpiTaskSub: "Đang chờ cất cánh", kpiDone: "Đã hoàn thành (✓)",
                kpiMiles: "Dặm bay tích lũy",
                aiTitle: "💡 Hôm nay nên học gì? (AI)", aiSub: "Báo giờ bay tự động theo lịch",
                btnAlarm: "🔔 Kiểm tra báo thức", smartTitle: "⚡ Điều phối Lịch AI Thông Minh",
                smartSub: "Sắp xếp thứ tự ưu tiên hoặc tự động dời ca học khi bạn bận đột xuất.",
                btnAiSort: "🤖 AI Sắp xếp Ưu tiên", btnSudden: "🌪️ Dời lịch đột xuất",
                todoTitle: "✅ Danh Sách Nhiệm Vụ & Chặng Bay", todoSync: "⚡ Nhận từ Lịch",
                todoSub: "Thêm môn học ở Lịch sẽ tự động nhảy sang đây kèm giờ bay!",
                filterAll: "Tất cả", filterPending: "Đang làm", filterDone: "Đã xong ✓",
                quickAdd: "+ Thêm nhanh bài tập / deadline lẻ:", quickPlh: "Nhập tên công việc (VD: Giải đề Toán...)",
                lblDue: "Hạn (Giờ):", lblTime: "⏰ Giờ:", btnSaveTask: "+ Lưu Việc",
                calTitle: "🗓️ Lịch Biểu & Việc Cá Nhân", calSub: "Tách riêng Việc cá nhân & Mở rộng Tháng/Năm",
                lblMonth: "Chọn Tháng", lblYear: "Chọn Năm", lblScope: "Chu kỳ lặp lại",
                scWeek: "📅 Trong tuần", scMonth: "🗓️ Nguyên tháng", scYear: "📆 Nguyên năm",
                btnToday: "Hôm nay", lblPickDate: "Chọn ngày:", lblStart: "⏰ Bắt đầu:", lblEnd: "🏁 Kết thúc:",
                lblCat: "Phân loại lịch",
                catStudy: "📚 Lịch học (Tạo chuyến bay)", catSchool: "🔴 Lịch trường (Cố định)", catPers: "🟣 Việc cá nhân", catFree: "🟢 Khung giờ trống",
                repeatCycle: "Lặp lại", rpNone: "1️⃣ Không lặp", rpWeek: "🔄 Hàng tuần", rpMonth: "🗓️ Hàng tháng", rpYear: "📆 Hàng năm", rpDay: "☀️ Hàng ngày", rpCustom: "⚙️ Tùy chỉnh...",
                lblCustomRp: "⚙️ Lặp mỗi:", unitDay: "Ngày", unitWeek: "Tuần", unitMonth: "Tháng", unitYear: "Năm", lblInDur: "Trong:",
                slotPlh: "Nhập môn học, sự kiện...", btnAddSlot: "+ Thêm Lịch", lblAutoSync: "⚡ Tự động đẩy sang Chuyến bay",
                btnZoomIn: "🔍 Phóng to 2D", btnZoomOut: "🌍 Quả Cầu 3D",
                camMap: "🌍 Bản đồ", camCockpit: "👨‍✈️ Phi công", camCabin: "💺 Cabin", camWindow: "🪟 Cửa sổ",
                envAuto: "🕒 Giờ thực", envDay: "☀️ Ngày", envSunset: "🌅 Hoàng hôn", envNight: "🌙 Đêm", envRain: "🌧️ Mưa",
                lblOrigin: "ĐIỂM KHỞI HÀNH", lblDest: "ĐIỂM HẠ CÁNH", lblDuration: "⏱️ THỜI GIAN (THEO KHOẢNG CÁCH)", lblEta: "HẠ CÁNH (ETA)",
                btnPickSeat: "💺 Chọn Ghế & In Vé", btnFlyNow: "🛫 Bay Ngay Lập Tức", btnBackRoute: "‹ Đổi chặng",
                focusQuest: "Bạn muốn tập trung làm gì trên chuyến bay này?", focusPlh: "Nhập mục tiêu (VD: Toán, Code...)",
                lblStrict: "🔒 Khóa Kỷ Luật", lblStrictSub: "Báo động đỏ nếu rời khỏi màn hình",
                btnConfirmPass: "Xác nhận Ghế & Xuất Vé ➔", hintSeat: "Chạm vào ghế bất kỳ hoặc bấm Tiếp tục", btnContinue: "Tiếp tục ➔",
                passTitle: "HÀNH KHÁCH", realTimeTitle: "GIỜ THỰC TẾ", seatTitle: "GHẾ", distTitle: "KHOẢNG CÁCH", focusTitle: "MỤC TIÊU",
                btnChangeSeat: "‹ Đổi ghế", btnTakeoff: "🛫 Cất Cánh Bắt Đầu Học",
                lblCollapse: "🔽 Thu gọn bảng", lblExpand: "🔼 Mở bảng đặt vé", lblTimeLeft: "Thời gian bay còn lại", lblDistLeft: "Còn",
                btnTarget: "🎯", btnFinish: "✓ Xong", btnAbort: "Hủy",
                botTitle: "Trợ lý Học tập AI", q1: "💡 Hôm nay học gì?", q2: "📋 Việc đang làm", q3: "🌪️ Dời lịch",
                weekdays: ["Thứ 2", "Thứ 3", "Thứ 4", "Thứ 5", "Thứ 6", "Thứ 7", "CN"],
                fullWeekdays: ["Chủ Nhật", "Thứ Hai", "Thứ Ba", "Thứ Tư", "Thứ Năm", "Thứ Sáu", "Thứ Bảy"],
                monthPrefix: "THÁNG", lunarOn: "🌙 Âm lịch: BẬT", lunarOff: "🌙 Âm lịch: TẮT"
            },
            en: {
                appTitle: "STUDYHUB & SATELLITE 3D", saveSync: "● Auto-saved", memberTitle: "Member",
                tabDash: "📊 Dashboard", tabFlight: "✈️ 3D / 2D Flight", btnLofi: "🎵 Lofi",
                bannerTag: "Flight Alert from Schedule", bannerBtn: "🛫 Takeoff & Study",
                kpiProfile: "Active Profile", kpiProfileSub: "Sync Calendar ➔ Flight",
                kpiTask: "Pending Tasks", kpiTaskSub: "Ready for takeoff", kpiDone: "Completed (✓)",
                kpiMiles: "Total Miles",
                aiTitle: "💡 What to study today? (AI)", aiSub: "Auto flight alarm based on schedule",
                btnAlarm: "🔔 Check Alarms", smartTitle: "⚡ Smart AI Dispatcher",
                smartSub: "Auto-sort priority or reschedule events dynamically.",
                btnAiSort: "🤖 AI Sort Priority", btnSudden: "🌪️ Reschedule Events",
                todoTitle: "✅ Task List & Flights", todoSync: "⚡ Auto-sync",
                todoSub: "Events added to Calendar will auto-generate flights here!",
                filterAll: "All", filterPending: "Pending", filterDone: "Done ✓",
                quickAdd: "+ Quick add task:", quickPlh: "Enter task name (e.g., Math...)",
                lblDue: "Due (h):", lblTime: "⏰ Time:", btnSaveTask: "+ Save Task",
                calTitle: "🗓️ Calendar & Events", calSub: "Separate School, Personal & Expand to Month/Year",
                lblMonth: "Month", lblYear: "Year", lblScope: "Recurrence",
                scWeek: "📅 Weekly", scMonth: "🗓️ Monthly", scYear: "📆 Yearly",
                btnToday: "Today", lblPickDate: "Pick date:", lblStart: "⏰ Start:", lblEnd: "🏁 End:",
                lblCat: "Category",
                catStudy: "📚 Study (Creates Flight)", catSchool: "🔴 School (Fixed)", catPers: "🟣 Personal (Work...)", catFree: "🟢 Free study block",
                repeatCycle: "Repeat", rpNone: "1️⃣ None", rpWeek: "🔄 Weekly", rpMonth: "🗓️ Monthly", rpYear: "📆 Yearly", rpDay: "☀️ Daily", rpCustom: "⚙️ Custom...",
                lblCustomRp: "⚙️ Repeat every:", unitDay: "Day(s)", unitWeek: "Week(s)", unitMonth: "Month(s)", unitYear: "Year(s)", lblInDur: "For:",
                slotPlh: "Enter subject, event name...", btnAddSlot: "+ Add Event", lblAutoSync: "⚡ Auto-push to Flights",
                btnZoomIn: "🔍 Zoom 2D", btnZoomOut: "🌍 3D Globe",
                camMap: "🌍 Map", camCockpit: "👨‍✈️ Pilot", camCabin: "💺 Cabin", camWindow: "🪟 Window",
                envAuto: "🕒 Auto", envDay: "☀️ Day", envSunset: "🌅 Sunset", envNight: "🌙 Night", envRain: "🌧️ Rain",
                lblOrigin: "DEPARTURE", lblDest: "ARRIVAL", lblDuration: "⏱️ STUDY TIME (DISTANCE)", lblEta: "EST. ARRIVAL",
                btnPickSeat: "💺 Pick Seat & Ticket", btnFlyNow: "🛫 Fly Now", btnBackRoute: "‹ Route",
                focusQuest: "What is your focus for this flight?", focusPlh: "Enter focus (e.g., Math...)",
                lblStrict: "🔒 Strict Mode", lblStrictSub: "Red alert if leaving screen",
                btnConfirmPass: "Confirm & Print Ticket ➔", hintSeat: "Tap any seat or click Continue", btnContinue: "Continue ➔",
                passTitle: "PASSENGER", realTimeTitle: "REAL TIME", seatTitle: "SEAT", distTitle: "DISTANCE", focusTitle: "FOCUS",
                btnChangeSeat: "‹ Seat", btnTakeoff: "🛫 Takeoff & Focus",
                lblCollapse: "🔽 Collapse", lblExpand: "🔼 Expand", lblTimeLeft: "Time remaining", lblDistLeft: "Left",
                btnTarget: "🎯", btnFinish: "✓ Done", btnAbort: "Abort",
                botTitle: "AI Assistant", q1: "💡 Study today?", q2: "📋 Pending tasks", q3: "🌪️ Reschedule",
                weekdays: ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
                fullWeekdays: ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"],
                monthPrefix: "MONTH", lunarOn: "🌙 Lunar: ON", lunarOff: "🌙 Lunar: OFF"
            },
            zh: {
                appTitle: "STUDYHUB & 3D 飛行艙", saveSync: "● 自動儲存", memberTitle: "成員",
                tabDash: "📊 學習儀表板", tabFlight: "✈️ 3D 飛行艙", btnLofi: "🎵 輕音樂",
                bannerTag: "來自個人行事曆的航班提醒", bannerBtn: "🛫 立即起飛",
                kpiProfile: "當前成員檔案", kpiProfileSub: "行事曆 ➔ 航班同步",
                kpiTask: "待辦任務", kpiTaskSub: "準備起飛", kpiDone: "已完成 (✓)",
                kpiMiles: "累計里程",
                aiTitle: "💡 今天學什麼？ (AI 推薦)", aiSub: "依據行事曆自動排程",
                btnAlarm: "🔔 檢查航班鬧鐘", smartTitle: "⚡ AI 智慧排程調度",
                smartSub: "自動優化優先級，突發狀況自動順延時段。",
                btnAiSort: "🤖 AI 優先排序", btnSudden: "🌪️ 突發狀況(順延)",
                todoTitle: "✅ 任務清單與航班", todoSync: "⚡ 行事曆自動同步",
                todoSub: "在右側新增行程將自動產生對應的專注航班！",
                filterAll: "全部", filterPending: "進行中", filterDone: "已完成 ✓",
                quickAdd: "+ 快速新增任務:", quickPlh: "輸入任務名稱 (如: 數學...)",
                lblDue: "期限(時):", lblTime: "⏰ 時間:", btnSaveTask: "+ 儲存任務",
                calTitle: "🗓️ 萬年曆與行程", calSub: "分類管理學校、個人行程，支援年月切換",
                lblMonth: "選擇月份", lblYear: "選擇年份", lblScope: "重複週期",
                scWeek: "📅 每週", scMonth: "🗓️ 每月", scYear: "📆 每年",
                btnToday: "今天", lblPickDate: "選擇日期:", lblStart: "⏰ 開始:", lblEnd: "🏁 結束:",
                lblCat: "行程分類",
                catStudy: "📚 學習/複習 (建立航班)", catSchool: "🔴 學校課程 (固定)", catPers: "🟣 個人事項 (打工...)", catFree: "🟢 空閒時段",
                repeatCycle: "重複設定", rpNone: "1️⃣ 不重複", rpWeek: "🔄 每週", rpMonth: "🗓️ 每月", rpYear: "📆 每年", rpDay: "☀️ 每天", rpCustom: "⚙️ 自訂週期...",
                lblCustomRp: "⚙️ 循環間隔:", unitDay: "天", unitWeek: "週", unitMonth: "個月", unitYear: "年", lblInDur: "持續:",
                slotPlh: "輸入課程或活動名稱...", btnAddSlot: "+ 新增行程", lblAutoSync: "⚡ 自動同步至左側航班",
                btnZoomIn: "🔍 放大 2D", btnZoomOut: "🌍 3D 地球",
                camMap: "🌍 地圖", camCockpit: "👨‍✈️ 駕駛艙", camCabin: "💺 客艙", camWindow: "🪟 窗戶",
                envAuto: "🕒 實際時間", envDay: "☀️ 白天", envSunset: "🌅 傍晚", envNight: "🌙 夜晚", envRain: "🌧️ 雨夜",
                lblOrigin: "出發地", lblDest: "目的地", lblDuration: "⏱️ 專注時間 (距離)", lblEta: "預計抵達 (ETA)",
                btnPickSeat: "💺 選擇座位與開票", btnFlyNow: "🛫 立即起飛", btnBackRoute: "‹ 更改航線",
                focusQuest: "這趟航班您的專注目標是？", focusPlh: "輸入目標 (如: 寫程式...)",
                lblStrict: "🔒 嚴格模式", lblStrictSub: "離開畫面將觸發紅燈警報",
                btnConfirmPass: "確認座位並取得登機證 ➔", hintSeat: "點擊任意座位或按繼續", btnContinue: "繼續 ➔",
                passTitle: "旅客", realTimeTitle: "實際時間", seatTitle: "座位", distTitle: "飛行距離", focusTitle: "專注目標",
                btnChangeSeat: "‹ 換座位", btnTakeoff: "🛫 起飛開始專注",
                lblCollapse: "🔽 收起面板", lblExpand: "🔼 展開面板", lblTimeLeft: "剩餘飛行時間", lblDistLeft: "剩餘",
                btnTarget: "🎯", btnFinish: "✓ 完成", btnAbort: "取消",
                botTitle: "AI 學習助理", q1: "💡 今天學什麼？", q2: "📋 待辦任務", q3: "🌪️ 突發狀況",
                weekdays: ["週一", "週二", "週三", "週四", "週五", "週六", "週日"],
                fullWeekdays: ["星期日", "星期一", "星期二", "星期三", "星期四", "星期五", "星期六"],
                monthPrefix: "月份", lunarOn: "🌙 農曆：開啟", lunarOff: "🌙 農曆：關閉"
            }
        };

        function setAppLanguage(lang) {
            currentLang = lang;
            ['vi', 'en', 'zh'].forEach(l => {
                const btn = document.getElementById('lang-btn-' + l);
                if (btn) {
                    btn.className = (l === lang) ? "px-2.5 py-1 rounded-lg bg-amber-400 text-black font-extrabold transition" : "px-2.5 py-1 rounded-lg text-slate-300 hover:text-white font-extrabold transition";
                }
            });

            document.querySelectorAll('[data-i18n]').forEach(el => {
                const key = el.getAttribute('data-i18n');
                if (I18N[lang] && I18N[lang][key]) el.innerHTML = I18N[lang][key];
            });

            document.querySelectorAll('[data-i18n-placeholder]').forEach(el => {
                const key = el.getAttribute('data-i18n-placeholder');
                if (I18N[lang] && I18N[lang][key]) el.placeholder = I18N[lang][key];
            });

            const t = I18N[lang];
            const wkRow = document.getElementById('calendar-weekdays-row');
            if (wkRow) wkRow.innerHTML = t.weekdays.map((w, idx) => `<div class="${idx === 6 ? 'text-red-400' : ''}">${w}</div>`).join('');

            renderCalendarGrid();
            renderDashboard();
            updateBookingUI();
            resetChat();
        }

        // ================= 2. THUẬT TOÁN TÍNH LỊCH VẠN NIÊN & ÂM LỊCH =================
        const CAN_VI = ["Giáp", "Ất", "Bính", "Đinh", "Mậu", "Kỷ", "Canh", "Tân", "Nhâm", "Quý"];
        const CHI_VI = ["Tý", "Sửu", "Dần", "Mão", "Thìn", "Tỵ", "Ngọ", "Mùi", "Thân", "Dậu", "Tuất", "Hợi"];
        const CAN_ZH = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"];
        const CHI_ZH = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"];

        function getLunarDateInfo(year, month, day) {
            try {
                const dateObj = new Date(year, month - 1, day);
                const parts = new Intl.DateTimeFormat('en-u-ca-chinese', { day: 'numeric', month: 'numeric' }).formatToParts(dateObj);
                let lDay = 1, lMonth = 1;
                parts.forEach(p => { if (p.type === 'day') lDay = parseInt(p.value) || 1; if (p.type === 'month') lMonth = parseInt(p.value) || 1; });

                const a = Math.floor((14 - month) / 12);
                const y = year + 4800 - a; const m = month + 12 * a - 3;
                const jdn = day + Math.floor((153 * m + 2) / 5) + 365 * y + Math.floor(y / 4) - Math.floor(y / 100) + Math.floor(y / 400) - 32045;
                const canIdx = (jdn + 9) % 10; const chiIdx = (jdn + 1) % 12;

                const canChiVi = `${CAN_VI[canIdx]} ${CHI_VI[chiIdx]}`;
                const canChiZh = `${CAN_ZH[canIdx]}${CHI_ZH[chiIdx]}日`;

                return {
                    lDay, lMonth,
                    shortStr: (lDay === 1 || day === 1) ? `${lDay}/${lMonth}` : `${lDay}`,
                    fullVi: `Ngày ${String(lDay).padStart(2,'0')}/${String(lMonth).padStart(2,'0')} Âm lịch • Ngày ${canChiVi}`,
                    fullEn: `Lunar: ${String(lDay).padStart(2,'0')}/${String(lMonth).padStart(2,'0')} (${canChiVi})`,
                    fullZh: `農曆 ${lMonth}月${lDay}日 • ${canChiZh}`
                };
            } catch (e) {
                return { lDay: day, lMonth: month, shortStr: `${day}`, fullVi: "Âm lịch", fullEn: "Lunar", fullZh: "農曆" };
            }
        }

        let calViewYear = 2026;
        let calViewMonth = 11;
        let selectedFullDate = "2026-11-04";

        function toggleLunarDisplay() {
            showLunarCalendar = !showLunarCalendar;
            document.getElementById('btn-toggle-lunar').innerText = showLunarCalendar ? I18N[currentLang].lunarOn : I18N[currentLang].lunarOff;
            renderCalendarGrid(); updateSelectedDateBanner();
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
            calViewYear = now.getFullYear(); calViewMonth = now.getMonth() + 1; const d = now.getDate();
            selectedFullDate = `${calViewYear}-${String(calViewMonth).padStart(2,'0')}-${String(d).padStart(2,'0')}`;
            document.getElementById('cal-month-select').value = String(calViewMonth);
            document.getElementById('cal-year-select').value = String(calViewYear);
            document.getElementById('direct-date-picker').value = selectedFullDate;
            renderCalendarGrid(); renderDashboard();
        }

        function selectCalendarDate(dateStr) {
            selectedFullDate = dateStr;
            document.getElementById('direct-date-picker').value = dateStr;
            const [y, m] = dateStr.split('-').map(Number);
            calViewYear = y; calViewMonth = m;
            document.getElementById('cal-month-select').value = String(calViewMonth);
            document.getElementById('cal-year-select').value = String(calViewYear);
            renderCalendarGrid(); renderDashboard();
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
            return list.filter(ev => doesEventMatchDate(ev, dateStr)).sort((a,b) => a.startT.localeCompare(b.startT));
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
                const isSunday = (new Date(calViewYear, calViewMonth - 1, d).getDay() === 0);
                const dayEvents = getEventsForDate(profile, dateStr);
                const lunar = getLunarDateInfo(calViewYear, calViewMonth, d);

                const cell = document.createElement('button');
                cell.className = `cal-cell rounded-xl p-1.5 border text-left flex flex-col justify-between relative ${isSelected ? 'bg-amber-400/20 border-2 border-amber-400 shadow-lg' : 'bg-slate-900/85 border-white/10 hover:bg-slate-800'}`;
                cell.onclick = () => selectCalendarDate(dateStr);

                let dotsHtml = dayEvents.length > 0 ? `<span class="px-1.5 py-0.2 rounded-full text-[9px] font-black bg-emerald-500 text-black">${dayEvents.length}</span>` : '';
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

        // ================= 5. TÍNH TOÁN QUẢ ĐỊA CẦU 3D & BẢN ĐỒ VỆ TINH 2D =================
        let scene, camera, renderer, earthGroup, earthMesh, routeArcLine;
        const GLOBE_RADIUS = 100;
        let globeCameraZ = 275, targetGlobeZ = 275, isDraggingGlobe = false, prevMouse = {x:0, y:0}, targetRot = {x:0.22, y:3.4}, lastTransitionTime = 0;

        function createFallbackEarthCanvas() {
            const c = document.createElement('canvas'); c.width = 1024; c.height = 512;
            const ctx = c.getContext('2d');
            const grad = ctx.createLinearGradient(0, 0, 0, 512);
            grad.addColorStop(0, '#0c4a6e'); grad.addColorStop(0.5, '#082f49'); grad.addColorStop(1, '#0c4a6e');
            ctx.fillStyle = grad; ctx.fillRect(0, 0, 1024, 512);
            return new THREE.CanvasTexture(c);
        }

        function latLngToVec3(lat, lng, radius = GLOBE_RADIUS) {
            const phi = (90 - lat) * (Math.PI / 180), theta = (lng + 180) * (Math.PI / 180);
            return new THREE.Vector3(-radius * Math.sin(phi) * Math.cos(theta), radius * Math.cos(phi), radius * Math.sin(phi) * Math.sin(theta));
        }

        function initThreeGlobe() {
            const canvas = document.getElementById('globe-canvas');
            scene = new THREE.Scene();
            camera = new THREE.PerspectiveCamera(45, window.innerWidth / (window.innerHeight - 56), 1, 2000);
            camera.position.z = globeCameraZ;
            renderer = new THREE.WebGLRenderer({ canvas: canvas, antialias: true, alpha: true });
            renderer.setSize(window.innerWidth, window.innerHeight - 56);
            renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));

            earthGroup = new THREE.Group(); scene.add(earthGroup);
            const earthMat = new THREE.MeshPhongMaterial({ map: createFallbackEarthCanvas(), shininess: 16, specular: new THREE.Color(0x1e3a8a) });
            earthMesh = new THREE.Mesh(new THREE.SphereGeometry(GLOBE_RADIUS, 64, 64), earthMat);
            earthGroup.add(earthMesh);
            new THREE.TextureLoader().load('https://unpkg.com/three-globe@2.31.0/example/img/earth-blue-marble.jpg', (tex) => { earthMat.map = tex; earthMat.needsUpdate = true; });
            earthGroup.add(new THREE.Mesh(new THREE.SphereGeometry(GLOBE_RADIUS * 1.035, 64, 64), new THREE.MeshBasicMaterial({ color: 0x38bdf8, transparent: true, opacity: 0.16, side: THREE.BackSide })));
            
            scene.add(new THREE.AmbientLight(0xdbeafe, 0.85));
            const dirLight = new THREE.DirectionalLight(0xffffff, 0.95); dirLight.position.set(250, 180, 300); scene.add(dirLight);

            canvas.addEventListener('mousedown', (e) => { isDraggingGlobe = true; prevMouse = { x: e.clientX, y: e.clientY }; });
            window.addEventListener('mousemove', (e) => {
                if (!isDraggingGlobe) return;
                targetRot.y += (e.clientX - prevMouse.x) * 0.0055;
                targetRot.x = Math.max(-1.2, Math.min(1.2, targetRot.x + (e.clientY - prevMouse.y) * 0.0055));
                prevMouse = { x: e.clientX, y: e.clientY };
            });
            window.addEventListener('mouseup', () => { isDraggingGlobe = false; });
            
            canvas.addEventListener('touchstart', (e) => { if (e.touches.length===1) { isDraggingGlobe=true; prevMouse={x:e.touches[0].clientX, y:e.touches[0].clientY}; } }, {passive:true});
            window.addEventListener('touchmove', (e) => {
                if (!isDraggingGlobe || e.touches.length!==1) return;
                targetRot.y += (e.touches[0].clientX - prevMouse.x)*0.0055;
                targetRot.x = Math.max(-1.2, Math.min(1.2, targetRot.x + (e.touches[0].clientY - prevMouse.y)*0.0055));
                prevMouse = { x: e.touches[0].clientX, y: e.touches[0].clientY };
            }, {passive:true});
            window.addEventListener('touchend', () => { isDraggingGlobe=false; });

            canvas.addEventListener('wheel', (e) => {
                e.preventDefault();
                if (Date.now() - lastTransitionTime < 650) return;
                const step = Math.sign(e.deltaY) * Math.min(Math.abs(e.deltaY) * 0.15, 10);
                targetGlobeZ = Math.max(150, Math.min(430, targetGlobeZ + step));
                if (targetGlobeZ <= 165 && e.deltaY < 0) { targetGlobeZ = 190; globeCameraZ = 190; activate2DSatelliteMap(); }
            }, { passive: false });
            animateThreeGlobe();
        }

        function update3DGlobeRouteArc() {
            if (!earthGroup) return;
            if (routeArcLine) { earthGroup.remove(routeArcLine); routeArcLine.geometry.dispose(); }
            const startVec = latLngToVec3(originAirport.coords[0], originAirport.coords[1], GLOBE_RADIUS * 1.005);
            const endVec = latLngToVec3(destAirport.coords[0], destAirport.coords[1], GLOBE_RADIUS * 1.005);
            const midVec = startVec.clone().add(endVec).multiplyScalar(0.5);
            midVec.normalize().multiplyScalar(GLOBE_RADIUS + Math.max(12, startVec.distanceTo(endVec) * 0.28));
            routeArcLine = new THREE.Line(new THREE.BufferGeometry().setFromPoints(new THREE.QuadraticBezierCurve3(startVec, midVec, endVec).getPoints(64)), new THREE.LineBasicMaterial({ color: 0x38bdf8, linewidth: 3 }));
            earthGroup.add(routeArcLine);
            const midLat = (originAirport.coords[0] + destAirport.coords[0]) / 2, midLng = (originAirport.coords[1] + destAirport.coords[1]) / 2;
            targetRot.y = (midLng + 90) * (Math.PI / 180); targetRot.x = midLat * (Math.PI / 180) * 0.75;
            document.getElementById('globe-origin-code').innerText = originAirport.code;
            document.getElementById('globe-dest-code').innerText = destAirport.code;
            document.getElementById('globe-plane-svg').innerHTML = getAircraftSVG(selectedAircraft, calcBearingDeg(originAirport.coords, destAirport.coords));
        }

        function update3DPinOverlay(elId, lat, lng, lift = 1.02) {
            const el = document.getElementById(elId);
            if (!el || is2DMapActive || currentCamView !== 'map') { if(el) el.classList.add('hidden'); return; }
            const worldVec = latLngToVec3(lat, lng, GLOBE_RADIUS * lift).applyMatrix4(earthGroup.matrixWorld);
            if (camera.position.clone().normalize().dot(worldVec.clone().normalize()) < 0.15) { el.classList.add('hidden'); return; }
            const projected = worldVec.clone().project(camera);
            el.style.left = `${(projected.x * 0.5 + 0.5) * window.innerWidth}px`; el.style.top = `${(-(projected.y * 0.5) + 0.5) * (window.innerHeight - 56) + 56}px`;
            el.classList.remove('hidden');
        }

        function animateThreeGlobe() {
            requestAnimationFrame(animateThreeGlobe);
            if (!earthGroup || !renderer) return;
            earthGroup.rotation.y += (targetRot.y - earthGroup.rotation.y) * 0.08;
            earthGroup.rotation.x += (targetRot.x - earthGroup.rotation.x) * 0.08;
            globeCameraZ += (targetGlobeZ - globeCameraZ) * 0.085; camera.position.z = globeCameraZ;
            renderer.render(scene, camera);
            update3DPinOverlay('globe-origin-pin', originAirport.coords[0], originAirport.coords[1], 1.02);
            update3DPinOverlay('globe-dest-pin', destAirport.coords[0], destAirport.coords[1], 1.02);
            if (isFlying) {
                const curLat = originAirport.coords[0] + (destAirport.coords[0] - originAirport.coords[0]) * currentFlightProgress;
                const curLng = originAirport.coords[1] + (destAirport.coords[1] - originAirport.coords[1]) * currentFlightProgress;
                update3DPinOverlay('globe-plane-pin', curLat, curLng, 1.05);
            } else { const pEl = document.getElementById('globe-plane-pin'); if (pEl) pEl.classList.add('hidden'); }
        }

        const map = L.map('map', { zoomControl: false, minZoom: 3, maxZoom: 18, zoomSnap: 0.5, zoomDelta: 0.5, wheelPxPerZoomLevel: 120 }).setView([13.5, 107.5], 6);
        L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}', { maxZoom: 18 }).addTo(map);
        L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/Reference/World_Boundaries_and_Places/MapServer/tile/{z}/{y}/{x}', { maxZoom: 18 }).addTo(map);
        map.getContainer().addEventListener('wheel', (e) => { if (is2DMapActive && e.deltaY > 0 && map.getZoom() <= 4 && (Date.now() - lastTransitionTime > 650)) activate3DSpaceGlobe(); }, { passive: true });

        function activate2DSatelliteMap() {
            lastTransitionTime = Date.now(); is2DMapActive = true;
            document.getElementById('globe-wrapper').classList.add('globe-hidden');
            document.getElementById('map-2d-wrapper').classList.add('active-2d');
            const refresh2DMap = () => { map.invalidateSize(true); if (isFlying && planeMarker) map.setView(planeMarker.getLatLng(), 7, { animate: false }); else if (routeLine) map.fitBounds(routeLine.getBounds(), { padding: [90, 90], maxZoom: 7, animate: false }); };
            refresh2DMap(); setTimeout(refresh2DMap, 80);
        }
        function activate3DSpaceGlobe() {
            lastTransitionTime = Date.now(); is2DMapActive = false; targetGlobeZ = 245; globeCameraZ = 190;
            document.getElementById('map-2d-wrapper').classList.remove('active-2d');
            document.getElementById('globe-wrapper').classList.remove('globe-hidden');
        }
        function zoomStepIn() { if (!is2DMapActive) { targetGlobeZ -= 30; if (targetGlobeZ <= 168) activate2DSatelliteMap(); } else map.zoomIn(1); }
        function zoomStepOut() { if (is2DMapActive) { if (map.getZoom() <= 4.5) activate3DSpaceGlobe(); else map.zoomOut(1); } else targetGlobeZ = Math.min(430, targetGlobeZ + 30); }

        // ================= 6. LƯU LỊCH CHU KỲ VÀ TỰ ĐỘNG ĐẨY QUA CHUYẾN BAY =================
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
            const t = I18N[currentLang];
            const dowName = t.fullWeekdays[new Date(y, m - 1, d).getDay()];
            const formattedDate = `${String(d).padStart(2,'0')}/${String(m).padStart(2,'0')}/${y}`;

            let repeatLabel = formattedDate;
            if (repeatMode === 'daily') repeatLabel = t.rpDay;
            else if (repeatMode === 'weekly') repeatLabel = `${t.rpWeek} (${dowName})`;
            else if (repeatMode === 'monthly') repeatLabel = `${t.rpMonth} (${String(d).padStart(2,'0')})`;
            else if (repeatMode === 'yearly') repeatLabel = `${t.rpYear} (${String(d).padStart(2,'0')}/${String(m).padStart(2,'0')})`;
            else if (repeatMode === 'custom') {
                const uLabel = customUnit === 'ngày' ? t.unitDay : (customUnit === 'tuần' ? t.unitWeek : (customUnit === 'tháng' ? t.unitMonth : t.unitYear));
                repeatLabel = `${customInterval} ${uLabel} (${t.lblInDur} ${customDur})`;
            }

            const profile = appState.members[currentMemberKey];
            const slotId = Date.now();
            profile.calendarEvents.push({
                id: slotId, dateStr: selectedFullDate, formattedDate, dowName,
                time: `${startT} - ${endT}`, startT, endT, durationMins, subject, type,
                repeatMode, customInterval, customUnit, repeatLabel, destCode: matchedAirport.code
            });

            if (autoSync) {
                let typePrefix = '📚';
                if (type === 'personal') typePrefix = '🟣';
                else if (type === 'school') typePrefix = '🔴';
                
                profile.tasks.unshift({
                    id: slotId + 1, linkedSlotId: slotId,
                    title: `${typePrefix} ${subject}`,
                    hoursLeft: 12, importance: type === 'personal' ? 4 : 5,
                    slot: `${startT} - ${endT}`,
                    destCode: matchedAirport.code, distKm: matchedDist, duration: durationMins,
                    scope: repeatLabel, syncedFromTimetable: true, done: false
                });
            }

            subjInput.value = '';
            savePersistentState();
            renderCalendarGrid(); renderDashboard();
        }

        function flyDirectlyFromCalendarEvent(evId) {
            const profile = appState.members[currentMemberKey];
            const ev = (profile.calendarEvents || []).find(e => e.id === evId);
            if (!ev) return;
            originAirport = AIRPORTS[0];
            destAirport = AIRPORTS.find(a => a.code === (ev.destCode || "DAD")) || AIRPORTS[2];
            selectedDuration = ev.durationMins || 45; currentDistance = calcDistanceKm(originAirport.coords, destAirport.coords);
            selectedFocus = { id: 'custom', label: ev.subject, icon: '🎯', color: 'bg-cyan-600 border-cyan-300 text-white' };
            document.getElementById('custom-focus-input').value = ev.subject;
            updateBookingUI(); switchPage('flight'); goToSeatSelection();
        }

        function removeCalendarEvent(evId) {
            const profile = appState.members[currentMemberKey];
            profile.calendarEvents = (profile.calendarEvents || []).filter(e => e.id !== evId);
            profile.tasks = (profile.tasks || []).filter(t => t.linkedSlotId !== evId);
            savePersistentState();
            renderCalendarGrid(); renderDashboard();
        }

        function fmtMins(m) {
            const t = I18N[currentLang];
            if (currentLang === 'en') return `${m} mins`;
            if (currentLang === 'zh') return `${m} 分鐘`;
            return `${m} phút`;
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
            document.getElementById('stat-done-percent').innerText = `${t.kpiDoneSub}${pct}% (${doneTasks.length}/${allTasks.length})`;
            document.getElementById('stat-miles-count').innerText = `${profile.miles || 0} km`;
            document.getElementById('stat-flights-count').innerText = `${t.kpiMilesSub}${profile.flights || 0}`;
            document.getElementById('timetable-owner-badge').innerText = `(${profile.name})`;

            const banner = document.getElementById('deadline-banner');
            if (pendingTasks.length > 0) {
                const top = pendingTasks[0];
                banner.classList.remove('hidden'); banner.classList.add('flex');
                document.getElementById('deadline-banner-text').innerText = `✈️ ${profile.name}: "${top.title}" • ⏰ ${top.slot} (SGN ➔ ${top.destCode || 'DAD'} • ${fmtMins(top.duration)})`;
            } else {
                banner.classList.add('hidden'); banner.classList.remove('flex');
            }

            const aiBox = document.getElementById('ai-today-suggestion');
            if (pendingTasks.length > 0) {
                const sorted = [...pendingTasks].sort((a, b) => calcPriorityScore(b) - calcPriorityScore(a));
                const top = sorted[0];
                aiBox.innerHTML = `
                    <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
                        <div>
                            <div class="flex flex-wrap items-center gap-2 mb-1">
                                <span class="bg-amber-400 text-black text-[10px] font-black px-2 py-0.5 rounded">🔔 ${top.slot}</span>
                                ${top.syncedFromTimetable ? `<span class="bg-emerald-500/20 text-emerald-300 border border-emerald-400/30 text-[10px] font-bold px-2 py-0.5 rounded">${t.todoSync}</span>` : ''}
                                <span class="text-xs text-amber-300">${'⭐'.repeat(top.importance)}</span>
                            </div>
                            <div class="text-sm sm:text-base font-extrabold text-white">${top.title}</div>
                            <div class="text-xs text-cyan-300 mt-1">✈️ SGN ➔ <b>${top.destCode || "DAD"} (${top.distKm || 605} km • ${fmtMins(top.duration)})</b></div>
                        </div>
                        <div class="flex sm:flex-col gap-2 shrink-0">
                            <button onclick="startFlightFromTask(${top.id})" class="bg-gradient-to-r from-emerald-500 to-cyan-500 hover:opacity-95 text-black font-black px-4 py-2 rounded-xl text-xs shadow-lg whitespace-nowrap">
                                🛫 ${fmtMins(top.duration)}
                            </button>
                        </div>
                    </div>
                `;
            } else {
                aiBox.innerHTML = `<div class="text-xs text-slate-300 py-1.5">💡 ${t.todoSub}</div>`;
            }

            const listEl = document.getElementById('todo-drag-list');
            listEl.innerHTML = '';
            let filteredTasks = allTasks;
            if (currentTaskFilter === 'pending') filteredTasks = pendingTasks;
            if (currentTaskFilter === 'done') filteredTasks = doneTasks;

            if (filteredTasks.length === 0) {
                listEl.innerHTML = `<div class="text-center py-8 bg-slate-900/40 rounded-2xl border border-dashed border-white/10"><div class="text-xs font-bold text-slate-300">${t.emptyTasks}</div></div>`;
            } else {
                filteredTasks.forEach((task) => {
                    const card = document.createElement('div');
                    card.draggable = true; card.dataset.index = allTasks.findIndex(tk => tk.id === task.id);
                    card.className = `p-3 rounded-2xl border transition cursor-grab active:cursor-grabbing flex flex-col sm:flex-row sm:items-center justify-between gap-2.5 ${task.done ? 'bg-emerald-950/20 border-emerald-500/30' : 'bg-slate-900/90 border-white/10 hover:border-cyan-400/40'}`;
                    card.addEventListener('dragstart', handleDragStart); card.addEventListener('dragover', handleDragOver); card.addEventListener('drop', handleDrop); card.addEventListener('dragend', handleDragEnd);

                    card.innerHTML = `
                        <div class="flex items-start gap-2.5">
                            <button onclick="toggleTaskDone(${task.id})" class="mt-0.5 w-6 h-6 rounded-full border-2 flex items-center justify-center font-black text-xs shrink-0 ${task.done ? 'bg-emerald-500 border-emerald-400 text-black shadow-lg' : 'bg-slate-800 border-slate-500 text-transparent hover:border-emerald-400'}">✓</button>
                            <div>
                                <div class="flex flex-wrap items-center gap-1.5 mb-1">
                                    <span class="text-[10px] font-black ${task.done ? 'bg-emerald-500/20 text-emerald-300 border border-emerald-500/30' : 'bg-amber-400 text-black'} px-2 py-0.5 rounded">⏰ ${task.slot}</span>
                                    ${task.syncedFromTimetable ? `<span class="text-[10px] font-bold bg-emerald-500/20 text-emerald-300 px-2 py-0.5 rounded">${t.todoSync}</span>` : ''}
                                    <span class="text-[10px] font-mono bg-white/10 text-cyan-300 px-2 py-0.5 rounded">✈️ SGN➔${task.destCode||'DAD'} (${task.distKm||605}km • ${fmtMins(task.duration)})</span>
                                    ${task.scope ? `<span class="text-[10px] text-purple-300 font-bold">🔄 ${task.scope}</span>` : ''}
                                </div>
                                <div class="text-xs sm:text-sm font-extrabold ${task.done ? 'line-through text-slate-400' : 'text-white'}">${task.title}</div>
                            </div>
                        </div>
                        <div class="flex items-center gap-1.5 shrink-0 self-end sm:self-center">
                            ${!task.done ? `<button onclick="startFlightFromTask(${task.id})" class="bg-gradient-to-r from-blue-600 to-cyan-500 hover:opacity-95 text-white px-3 py-1 rounded-xl text-[11px] font-extrabold shadow">🛫 ${fmtMins(task.duration)}</button>` : ''}
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
                slotsList.innerHTML = `<div class="text-center py-5 bg-slate-900/40 rounded-2xl border border-dashed border-white/10"><div class="text-xs font-bold text-slate-300">${t.emptySlots}</div></div>`;
            } else {
                dayEvents.forEach((ev) => {
                    let badgeStyle = 'bg-blue-500/20 text-cyan-300 border-cyan-500/30';
                    let typeLabel = t.catStudy;
                    if (ev.type === 'personal') { badgeStyle = 'bg-purple-950/40 text-purple-300 border-purple-400/40'; typeLabel = t.catPers; }
                    else if (ev.type === 'school') { badgeStyle = 'bg-red-950/35 text-red-300 border-red-400/30'; typeLabel = t.catSchool; }
                    else if (ev.type === 'free') { badgeStyle = 'bg-emerald-950/35 text-emerald-300 border-emerald-400/30'; typeLabel = t.catFree; }

                    const el = document.createElement('div');
                    el.className = `p-3 rounded-2xl border flex items-center justify-between gap-2 ${badgeStyle}`;
                    el.innerHTML = `
                        <div>
                            <div class="flex flex-wrap items-center gap-1.5">
                                <span class="text-[10px] font-mono font-extrabold px-2 py-0.5 rounded bg-black/40 text-amber-300">⏰ ${ev.time} (${fmtMins(ev.durationMins)})</span>
                                <span class="text-[10px] font-bold">${typeLabel.split('(')[0]}</span>
                                <span class="text-[9px] bg-white/10 px-1.5 py-0.5 rounded text-emerald-300 font-bold">🔄 ${ev.repeatLabel}</span>
                            </div>
                            <div class="text-xs font-extrabold text-white mt-1">${ev.subject}</div>
                        </div>
                        <div class="flex items-center gap-1 shrink-0">
                            <button onclick="flyDirectlyFromCalendarEvent(${ev.id})" class="bg-cyan-500 hover:bg-cyan-400 text-black font-black px-2.5 py-1 rounded-xl text-[10px] shadow">🛫</button>
                            <button onclick="removeCalendarEvent(${ev.id})" class="bg-red-500/20 hover:bg-red-500/40 text-red-200 px-2 py-1 rounded-xl text-xs font-bold">🗑️</button>
                        </div>
                    `;
                    slotsList.appendChild(el);
                });
            }
        }

        // Khởi chạy App
        setAppLanguage("vi");
    </script>
</body>
</html>
"""

components.html(app_html, height=800, scrolling=False)
