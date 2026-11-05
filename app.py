import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
                page_title="StudyHub & 3D Flight Sim (VI / EN / 繁體)",
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

        .glass-panel {
            background: rgba(11, 17, 30, 0.92);
            backdrop-filter: blur(22px);
            border: 1px solid rgba(255, 255, 255, 0.16);
        }

        .dash-card {
            background: linear-gradient(145deg, #0f172a 0%, #0b1120 100%);
            border: 1px solid rgba(255, 255, 255, 0.1);
            box-shadow: 0 12px 32px rgba(0, 0, 0, 0.45);
        }

        .cal-cell {
            min-height: 50px;
            transition: all 0.15s ease;
        }
        .cal-cell:hover {
            transform: translateY(-1px);
            border-color: rgba(56, 189, 248, 0.6);
        }

        .focus-popover {
            background: rgba(20, 31, 53, 0.98);
            backdrop-filter: blur(28px);
            border: 1px solid rgba(56, 189, 248, 0.35);
            box-shadow: 0 25px 60px rgba(0, 0, 0, 0.9);
        }

        .fuselage {
            border-top-left-radius: 160px 240px;
            border-top-right-radius: 160px 240px;
            border-left: 3px solid rgba(56, 189, 248, 0.35);
            border-right: 3px solid rgba(56, 189, 248, 0.35);
            border-top: 3px solid rgba(56, 189, 248, 0.5);
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

        @keyframes cloud-drift-right-to-left {
            0% { transform: translateX(115vw) scale(0.85); opacity: 0; }
            10% { opacity: 0.92; }
            90% { opacity: 0.92; }
            100% { transform: translateX(-45vw) scale(1.15); opacity: 0; }
        }
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
        .rain-overlay {
            background-image: repeating-linear-gradient(105deg, transparent 0px, transparent 18px, rgba(186, 230, 253, 0.35) 19px, transparent 20px);
            background-size: 200px 200px;
            animation: rain-fall 0.55s linear infinite;
        }

        @keyframes red-alert { 0%, 100% { background: rgba(153, 27, 27, 0.94); } 50% { background: rgba(220, 38, 38, 0.98); } }
        .turbulence-alert { animation: red-alert 0.7s infinite; backdrop-filter: blur(16px); }

        @keyframes bot-glow {
            0%, 100% { box-shadow: 0 0 15px rgba(212, 163, 73, 0.75), 0 0 30px rgba(212, 163, 73, 0.4); transform: translateY(0px); }
            50% { box-shadow: 0 0 25px rgba(234, 179, 8, 1), 0 0 45px rgba(212, 163, 73, 0.65); transform: translateY(-4px); }
        }
        .bot-launcher-glow { animation: bot-glow 2.8s infinite ease-in-out; }

        .dragging-card { opacity: 0.45; border: 2px dashed #38bdf8 !important; }
        ::-webkit-scrollbar { width: 5px; height: 5px; }
        ::-webkit-scrollbar-thumb { background: rgba(255,255,255,0.25); border-radius: 10px; }
        .leaflet-control-attribution { display: none !important; }
    </style>
</head>
<body class="relative w-screen h-screen overflow-hidden bg-[#03060f] notranslate" translate="no">

    <!-- AUDIO LOFI -->
    <audio id="lofi-player" loop crossorigin="anonymous">
        <source id="lofi-source" src="https://cdn.pixabay.com/download/audio/2022/05/27/audio_1808fbf07a.mp3" type="audio/mpeg">
    </audio>

    <!-- ================= THANH ĐIỀU HƯỚNG CHÍNH + CHỌN 3 NGÔN NGỮ (VI / EN / 繁體) ================= -->
    <header style="z-index: 8000;" class="fixed top-0 left-0 right-0 h-14 bg-[#080d1a]/95 backdrop-blur-xl border-b border-white/10 px-2.5 sm:px-4 flex items-center justify-between gap-2">
        <div class="flex items-center gap-2">
            <div class="flex items-center gap-2">
                <div class="w-8 h-8 rounded-xl bg-gradient-to-br from-blue-500 to-cyan-400 flex items-center justify-center text-black font-black text-base shadow">🌍</div>
                <div class="hidden xl:block">
                    <div class="text-[11px] font-extrabold tracking-wider text-white">STUDYHUB & SATELLITE 3D</div>
                    <div class="text-[9px] text-emerald-400" id="save-status-indicator">● Auto-Save Ready</div>
                </div>
            </div>

            <!-- Chọn Thành viên (Chỉ hiển thị đúng Tên) -->
            <div class="bg-slate-900 border border-white/15 px-2.5 py-1 rounded-xl flex items-center gap-1.5">
                <span class="text-xs">👤</span>
                <div>
                    <div id="lbl-member-top" class="text-[8px] text-amber-400 font-bold uppercase tracking-wider leading-none">Thành viên</div>
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

            <!-- ĐỒNG HỒ THỜI GIAN THỰC -->
            <div class="hidden md:flex items-center gap-2 bg-slate-900/90 border border-cyan-500/30 px-2.5 py-1 rounded-xl">
                <span class="w-2 h-2 rounded-full bg-emerald-400 animate-ping"></span>
                <div>
                    <div id="realtime-clock" class="mono text-xs font-extrabold text-cyan-300 leading-none">00:00:00</div>
                    <div id="realtime-date" class="text-[9px] text-slate-400 font-semibold leading-none mt-0.5">--/--/----</div>
                </div>
            </div>
        </div>

        <!-- Chuyển Đổi 2 Giao Diện Riêng Biệt -->
        <div class="bg-slate-900/90 p-1 rounded-xl border border-white/10 flex items-center gap-1">
            <button id="nav-btn-dashboard" onclick="switchPage('dashboard')" class="px-2.5 sm:px-3 py-1.5 rounded-lg text-xs font-extrabold bg-gradient-to-r from-blue-600 to-cyan-500 text-white shadow transition flex items-center gap-1.5">
                <span id="lbl-tab-dashboard">📊 Bảng Điều Khiển Học Tập</span>
                <span id="nav-pending-badge" class="bg-black/30 text-white text-[10px] px-1.5 rounded-full">0</span>
            </button>
            <button id="nav-btn-flight" onclick="switchPage('flight')" class="px-2.5 sm:px-3 py-1.5 rounded-lg text-xs font-extrabold text-slate-400 hover:text-white transition flex items-center gap-1.5">
                <span id="lbl-tab-flight">✈️ Chuyến Bay 3D / 2D</span>
            </button>
        </div>

        <!-- BỘ CHUYỂN ĐỔI 3 NGÔN NGỮ: ĐÃ BỎ CỜ ĐỂ KHÔNG BỊ HIỆN CHỮ gb EN, vn VI -->
        <div class="flex items-center gap-1.5">
            <div class="bg-slate-900 border border-amber-400/40 p-0.5 rounded-xl flex items-center text-[10px] font-extrabold">
                <button id="lang-btn-vi" onclick="setAppLanguage('vi')" class="px-2.5 py-1 rounded-lg bg-amber-400 text-black transition">VI</button>
                <button id="lang-btn-en" onclick="setAppLanguage('en')" class="px-2.5 py-1 rounded-lg text-slate-300 hover:text-white transition">EN</button>
                <button id="lang-btn-zh" onclick="setAppLanguage('zh')" class="px-2.5 py-1 rounded-lg text-slate-300 hover:text-white transition">繁體</button>
            </div>

            <button onclick="toggleLofi()" class="bg-slate-900 hover:bg-slate-800 border border-white/10 px-2.5 py-1.5 rounded-xl flex items-center gap-1.5 text-xs font-bold text-slate-200 transition">
                <div id="eq-icon" class="hidden items-end gap-[2px] h-3.5">
                    <div class="eq-bar"></div><div class="eq-bar"></div><div class="eq-bar"></div>
                </div>
                <span id="lofi-btn-text">🎵 Lofi</span>
            </button>
            <button onclick="openMediaModal()" class="bg-slate-900 hover:bg-slate-800 border border-cyan-500/30 px-2 py-1.5 rounded-xl text-xs font-bold text-cyan-400 transition">
                ⚙️
            </button>
        </div>
    </header>

    <!-- ========================================================================================= -->
    <!-- TRANG 1: BẢNG ĐIỀU KHIỂN HỌC TẬP, TO-DO LIST & LỊCH VẠN NIÊN THÁNG/NĂM ĐỒNG BỘ            -->
    <!-- ========================================================================================= -->
    <main id="page-dashboard" style="z-index: 30;" class="fixed inset-x-0 top-14 bottom-0 bg-[#03060f] overflow-y-auto px-3 sm:px-6 py-4 page-layer-visible">
        <div class="max-w-7xl mx-auto space-y-4 pb-20">

            <div id="deadline-banner" class="hidden bg-gradient-to-r from-blue-600/90 via-indigo-600/90 to-cyan-600/90 rounded-2xl p-3.5 shadow-xl border border-cyan-300/30 items-center justify-between gap-4">
                <div class="flex items-center gap-3">
                    <span class="text-xl animate-bounce">✈️</span>
                    <div>
                        <div id="lbl-banner-tag" class="text-[9px] font-black uppercase tracking-widest bg-black/30 px-2 py-0.5 rounded inline-block text-yellow-300">Thông báo Chuyến bay từ Lịch cá nhân</div>
                        <div id="deadline-banner-text" class="text-xs sm:text-sm font-extrabold text-white mt-0.5"></div>
                    </div>
                </div>
                <button onclick="startFocusFromTopTask()" id="lbl-banner-btn" class="bg-yellow-400 text-black hover:bg-yellow-300 font-black text-xs px-3.5 py-2 rounded-xl shadow shrink-0">
                    🛫 Cất cánh học ngay
                </button>
            </div>

            <!-- 4 THẺ THỐNG KÊ KPI -->
            <div class="grid grid-cols-2 lg:grid-cols-4 gap-3">
                <div class="dash-card rounded-2xl p-3.5 flex items-center justify-between">
                    <div>
                        <div id="lbl-kpi-1-title" class="text-[11px] text-slate-400 font-semibold">Hồ sơ thành viên</div>
                        <div id="stat-member-name" class="text-base font-black text-amber-400 mt-0.5">Hữu Đại</div>
                        <div id="lbl-kpi-1-sub" class="text-[10px] text-slate-500">Đồng bộ Lịch ➔ Chuyến bay</div>
                    </div>
                    <div class="w-10 h-10 rounded-xl bg-amber-500/10 border border-amber-500/20 flex items-center justify-center text-lg">👤</div>
                </div>

                <div class="dash-card rounded-2xl p-3.5 flex items-center justify-between">
                    <div>
                        <div id="lbl-kpi-2-title" class="text-[11px] text-slate-400 font-semibold">Nhiệm vụ & Lịch bay</div>
                        <div id="stat-pending-count" class="text-xl font-black text-white mt-0.5 mono">0</div>
                        <div id="lbl-kpi-2-sub" class="text-[10px] text-cyan-400">Đang chờ cất cánh</div>
                    </div>
                    <div class="w-10 h-10 rounded-xl bg-cyan-500/10 border border-cyan-500/20 flex items-center justify-center text-lg">📋</div>
                </div>

                <div class="dash-card rounded-2xl p-3.5 flex items-center justify-between">
                    <div>
                        <div id="lbl-kpi-3-title" class="text-[11px] text-slate-400 font-semibold">Đã hoàn thành (✓)</div>
                        <div id="stat-done-count" class="text-xl font-black text-emerald-400 mt-0.5 mono">0</div>
                        <div id="stat-done-percent" class="text-[10px] text-emerald-500">0%</div>
                    </div>
                    <div class="w-10 h-10 rounded-xl bg-emerald-500/10 border border-emerald-500/20 flex items-center justify-center text-lg">✅</div>
                </div>

                <div class="dash-card rounded-2xl p-3.5 flex items-center justify-between">
                    <div>
                        <div id="lbl-kpi-4-title" class="text-[11px] text-slate-400 font-semibold">Dặm bay tích lũy</div>
                        <div id="stat-miles-count" class="text-lg font-black text-blue-400 mt-0.5 mono">0 km</div>
                        <div id="stat-flights-count" class="text-[10px] text-slate-400">0</div>
                    </div>
                    <div class="w-10 h-10 rounded-xl bg-blue-500/10 border border-blue-500/20 flex items-center justify-center text-lg">🛂</div>
                </div>
            </div>

            <!-- KHU VỰC AI ĐỀ XUẤT -->
            <div class="grid grid-cols-1 lg:grid-cols-12 gap-4">
                <div class="lg:col-span-8 bg-gradient-to-br from-blue-950/85 via-slate-900 to-slate-900 border border-cyan-500/30 rounded-3xl p-4 shadow-xl flex flex-col justify-between">
                    <div class="flex flex-wrap items-center justify-between gap-2 mb-2">
                        <div class="flex items-center gap-2">
                            <span id="lbl-ai-badge" class="bg-cyan-400 text-black font-black text-[10px] px-2.5 py-0.5 rounded-full uppercase tracking-wider">💡 Hôm nay nên học gì? (AI Đề xuất)</span>
                            <span id="lbl-ai-sub" class="text-xs text-slate-400">Báo giờ bay tự động theo khung giờ đã đặt</span>
                        </div>
                        <button onclick="sendStudyReminderAlert()" id="lbl-remind-btn" class="bg-white/10 hover:bg-white/15 text-amber-300 border border-amber-400/30 px-3 py-1 rounded-xl text-xs font-bold transition">
                            🔔 Kiểm tra báo thức bay
                        </button>
                    </div>
                    <div id="ai-today-suggestion" class="bg-black/40 border border-white/10 rounded-2xl p-3"></div>
                </div>

                <div class="lg:col-span-4 dash-card rounded-3xl p-4 flex flex-col justify-between">
                    <div>
                        <h3 id="lbl-smart-ctrl-title" class="text-sm font-extrabold text-white mb-1">⚡ Điều phối Lịch AI Thông Minh</h3>
                        <p id="lbl-smart-ctrl-desc" class="text-xs text-slate-400 leading-relaxed">
                            Sắp xếp thứ tự ưu tiên theo Deadline hoặc tự động dời toàn bộ ca học khi bạn có việc đột xuất.
                        </p>
                    </div>
                    <div class="space-y-2 mt-3">
                        <button onclick="aiSortTasks()" id="lbl-btn-aisort" class="w-full bg-gradient-to-r from-amber-500 to-yellow-500 hover:opacity-95 text-black font-black py-2 px-4 rounded-xl text-xs shadow transition">
                            🤖 AI Sắp xếp Thứ tự Ưu tiên
                        </button>
                        <button onclick="handleSuddenScheduleChange()" id="lbl-btn-sudden" class="w-full bg-slate-800 hover:bg-slate-700 text-cyan-300 border border-cyan-500/30 font-bold py-2 px-4 rounded-xl text-xs transition">
                            🌪️ Có lịch đột xuất (Tự động dời ca)
                        </button>
                    </div>
                </div>
            </div>

            <!-- CỘT TRÁI & CỘT PHẢI -->
            <div class="grid grid-cols-1 lg:grid-cols-12 gap-5">
                <!-- CỘT TRÁI (6 PHẦN) -->
                <div class="lg:col-span-6 dash-card rounded-3xl p-4 sm:p-5 flex flex-col">
                    <div class="flex flex-wrap items-center justify-between gap-2 mb-3">
                        <div>
                            <h2 class="text-sm sm:text-base font-extrabold text-white flex items-center gap-2">
                                <span id="lbl-todo-header">✅ Danh Sách Nhiệm Vụ & Chặng Bay</span>
                                <span id="lbl-todo-sync-tag" class="text-[10px] bg-emerald-500/20 text-emerald-300 px-2 py-0.5 rounded-lg border border-emerald-400/30">⚡ Tự động nhận từ Lịch</span>
                            </h2>
                            <p id="lbl-todo-sub" class="text-[11px] text-slate-400">Thêm môn học ở Lịch bên phải sẽ tự động nhảy sang đây kèm giờ bay!</p>
                        </div>

                        <div class="flex bg-slate-900 p-1 rounded-xl border border-white/10 text-xs font-bold">
                            <button id="filter-all" onclick="setTaskFilter('all')" class="px-2.5 py-1 rounded-lg bg-blue-600 text-white">Tất cả</button>
                            <button id="filter-pending" onclick="setTaskFilter('pending')" class="px-2.5 py-1 rounded-lg text-slate-400 hover:text-white">Đang làm</button>
                            <button id="filter-done" onclick="setTaskFilter('done')" class="px-2.5 py-1 rounded-lg text-slate-400 hover:text-white">Đã xong ✓</button>
                        </div>
                    </div>

                    <div class="bg-slate-900/90 border border-white/15 rounded-2xl p-3 mb-4 space-y-2">
                        <div class="flex items-center justify-between">
                            <span id="lbl-quick-add-title" class="text-xs font-bold text-cyan-400">+ Thêm nhanh bài tập / deadline lẻ:</span>
                        </div>
                        <div class="grid grid-cols-1 sm:grid-cols-12 gap-2">
                            <input type="text" id="quick-task-title" onkeydown="if(event.key==='Enter') addNewTask()" placeholder="Nhập tên công việc..." class="sm:col-span-6 bg-slate-800 text-white text-xs px-3 py-2 rounded-xl border border-white/10 focus:outline-none focus:border-cyan-400" />
                            <div class="sm:col-span-3 flex items-center bg-slate-800 rounded-xl border border-white/10 px-2.5">
                                <span id="lbl-quick-deadline" class="text-[10px] text-amber-300 font-bold mr-1.5 shrink-0">Hạn (Giờ):</span>
                                <input type="number" id="quick-task-hours" value="24" min="1" max="720" class="w-full bg-transparent text-white text-xs py-2 focus:outline-none font-bold" />
                            </div>
                            <select id="quick-task-importance" class="sm:col-span-3 bg-slate-800 text-amber-300 text-xs px-2 py-2 rounded-xl border border-white/10 font-bold focus:outline-none">
                                <option value="5">⭐⭐⭐⭐⭐</option>
                                <option value="4" selected>⭐⭐⭐⭐</option>
                                <option value="3">⭐⭐⭐</option>
                                <option value="2">⭐⭐</option>
                            </select>
                        </div>
                        <div class="grid grid-cols-1 sm:grid-cols-12 gap-2 items-center">
                            <div class="sm:col-span-5 flex items-center justify-between bg-slate-800 rounded-xl border border-cyan-500/30 px-2.5 py-1.5">
                                <span class="text-[10px] text-cyan-300 font-bold">⏰</span>
                                <input type="time" id="quick-task-start" value="19:30" class="bg-transparent text-white text-xs font-mono font-bold focus:outline-none" />
                                <span class="text-xs text-slate-400">➔</span>
                                <input type="time" id="quick-task-end" value="20:25" class="bg-transparent text-amber-300 text-xs font-mono font-bold focus:outline-none" />
                            </div>
                            <div class="sm:col-span-4 flex items-center bg-slate-800 rounded-xl border border-white/10 px-2.5 py-1.5">
                                <select id="quick-task-dest" class="w-full bg-transparent text-white text-xs font-bold focus:outline-none"></select>
                            </div>
                            <button onclick="addNewTask()" id="lbl-btn-save-task" class="sm:col-span-3 bg-gradient-to-r from-blue-600 to-cyan-500 hover:opacity-95 text-white font-extrabold py-2 px-3 rounded-xl text-xs shadow-lg transition">
                                + Lưu Việc
                            </button>
                        </div>
                    </div>

                    <div id="todo-drag-list" class="space-y-2 flex-1 max-h-[540px] overflow-y-auto pr-1"></div>
                </div>

                <!-- CỘT PHẢI (6 PHẦN): BẢNG LỊCH THÁNG & CHU KỲ TÙY CHỌN -->
                <div class="lg:col-span-6 dash-card rounded-3xl p-4 sm:p-5 flex flex-col">
                    <div class="flex flex-wrap items-center justify-between gap-2 mb-2.5">
                        <div>
                            <h2 class="text-sm sm:text-base font-extrabold text-white flex items-center gap-2">
                                <span id="lbl-cal-header">🗓️ Lịch Biểu & Việc Cá Nhân</span>
                                <span id="timetable-owner-badge" class="text-xs text-amber-400 font-black"></span>
                            </h2>
                            <p id="lbl-cal-sub" class="text-[11px] text-slate-400">Bấm chọn trực tiếp ngày trên tờ lịch để xem Thứ/Ngày/Tháng/Năm & Âm lịch</p>
                        </div>

                        <button onclick="toggleLunarDisplay()" id="btn-toggle-lunar" class="bg-amber-500/20 hover:bg-amber-500/30 text-amber-300 border border-amber-400/40 px-2.5 py-1 rounded-xl text-[11px] font-extrabold transition">
                            🌙 Âm lịch: BẬT
                        </button>
                    </div>

                    <div class="bg-gradient-to-r from-emerald-700 via-emerald-600 to-teal-600 rounded-t-2xl px-3.5 py-2 flex flex-wrap items-center justify-between gap-2 shadow">
                        <div class="flex items-center gap-2">
                            <button onclick="changeCalendarMonth(-1)" class="w-7 h-7 rounded-full bg-white text-emerald-800 hover:bg-yellow-200 font-black flex items-center justify-center shadow">‹</button>
                            <span id="calendar-header-title" class="text-sm sm:text-base font-black text-white tracking-wide uppercase">THÁNG 11 - 2026</span>
                            <button onclick="changeCalendarMonth(1)" class="w-7 h-7 rounded-full bg-white text-emerald-800 hover:bg-yellow-200 font-black flex items-center justify-center shadow">›</button>
                        </div>

                        <div class="flex items-center gap-1.5 text-xs">
                            <select id="cal-month-select" onchange="onMonthYearDropdownChange()" class="bg-white text-slate-900 font-extrabold text-xs px-2 py-1 rounded-lg focus:outline-none cursor-pointer">
                                <option value="1">1</option><option value="2">2</option><option value="3">3</option>
                                <option value="4">4</option><option value="5">5</option><option value="6">6</option>
                                <option value="7">7</option><option value="8">8</option><option value="9">9</option>
                                <option value="10">10</option><option value="11" selected>11</option><option value="12">12</option>
                            </select>
                            <select id="cal-year-select" onchange="onMonthYearDropdownChange()" class="bg-white text-slate-900 font-extrabold text-xs px-2 py-1 rounded-lg focus:outline-none cursor-pointer">
                                <option value="2025">2025</option>
                                <option value="2026" selected>2026</option>
                                <option value="2027">2027</option>
                                <option value="2028">2028</option>
                                <option value="2029">2029</option>
                            </select>
                            <button onclick="jumpToToday()" id="lbl-btn-today" class="bg-slate-900/90 hover:bg-black text-amber-300 font-extrabold px-2.5 py-1 rounded-lg text-[11px]">Hôm nay</button>
                        </div>
                    </div>

                    <div id="calendar-weekdays-row" class="grid grid-cols-7 bg-slate-900 border-x border-b border-white/15 text-center py-1.5 text-[11px] font-extrabold text-slate-300">
                        <div>Thứ 2</div><div>Thứ 3</div><div>Thứ 4</div><div>Thứ 5</div><div>Thứ 6</div><div>Thứ 7</div><div class="text-red-400">CN</div>
                    </div>

                    <div id="calendar-days-grid" class="grid grid-cols-7 gap-1 bg-slate-950/90 p-2 rounded-b-2xl border-x border-b border-white/15 mb-3"></div>

                    <div class="bg-slate-900/95 border border-emerald-500/35 rounded-2xl p-3.5 mb-3 space-y-2.5 shadow-lg">
                        <div class="flex flex-wrap items-center justify-between gap-2 border-b border-white/10 pb-2">
                            <div>
                                <div id="selected-full-date-banner" class="text-xs sm:text-sm font-black text-amber-300">
                                    📅 Thứ Tư, Ngày 04/11/2026
                                </div>
                                <div id="selected-lunar-date-banner" class="text-[11px] text-cyan-300 font-semibold">
                                    🌙 Âm lịch: Ngày 26/09
                                </div>
                            </div>
                            <div class="flex items-center gap-1.5 bg-slate-800 border border-white/15 px-2.5 py-1 rounded-xl">
                                <span class="text-[10px] text-slate-300 font-bold" id="lbl-pick-date">Chọn ngày:</span>
                                <input type="date" id="direct-date-picker" value="2026-11-04" onchange="onDirectDateInputChange()" class="bg-transparent text-white text-xs font-mono font-bold focus:outline-none cursor-pointer" />
                            </div>
                        </div>

                        <div class="grid grid-cols-1 sm:grid-cols-12 gap-2 items-center">
                            <div class="sm:col-span-5 bg-slate-800 border border-white/15 rounded-xl px-2.5 py-1.5 flex items-center justify-between">
                                <span id="lbl-start-time" class="text-[10px] text-slate-300 font-bold">⏰ Bắt đầu:</span>
                                <input type="time" id="new-slot-start" value="14:00" onchange="updateSlotDurationPreview()" class="bg-transparent text-cyan-300 font-mono font-extrabold text-xs focus:outline-none cursor-pointer" />
                            </div>
                            <div class="sm:col-span-5 bg-slate-800 border border-white/15 rounded-xl px-2.5 py-1.5 flex items-center justify-between">
                                <span id="lbl-end-time" class="text-[10px] text-slate-300 font-bold">🏁 Kết thúc:</span>
                                <input type="time" id="new-slot-end" value="15:30" onchange="updateSlotDurationPreview()" class="bg-transparent text-amber-300 font-mono font-extrabold text-xs focus:outline-none cursor-pointer" />
                            </div>
                            <div class="sm:col-span-2 text-center">
                                <span id="calc-slot-mins-preview" class="text-[10px] font-mono bg-cyan-500/20 text-cyan-300 px-2 py-1 rounded-lg font-bold block">90p</span>
                            </div>
                        </div>

                        <div class="grid grid-cols-1 sm:grid-cols-2 gap-2">
                            <div>
                                <div id="lbl-cat-type" class="text-[9px] text-slate-400 font-bold uppercase mb-0.5">Phân loại lịch</div>
                                <select id="new-slot-type" class="w-full bg-slate-800 text-white text-xs px-2.5 py-2 rounded-xl border border-white/15 font-bold focus:outline-none cursor-pointer">
                                    <option value="study" id="opt-cat-study">📚 Lịch học / Ôn bài (Tạo chuyến bay)</option>
                                    <option value="school" id="opt-cat-school">🔴 Lịch học trên trường (Cố định)</option>
                                    <option value="personal" id="opt-cat-personal">🟣 Việc cá nhân (Đi làm, sự kiện...)</option>
                                    <option value="free" id="opt-cat-free">🟢 Khung giờ trống tự học</option>
                                </select>
                            </div>

                            <div>
                                <div id="lbl-repeat-cycle" class="text-[9px] text-emerald-400 font-bold uppercase mb-0.5">Chu kỳ lặp lại (Tự chọn)</div>
                                <select id="slot-repeat-mode" onchange="onRepeatModeChange()" class="w-full bg-slate-800 text-emerald-300 text-xs px-2.5 py-2 rounded-xl border border-emerald-500/30 font-extrabold focus:outline-none cursor-pointer">
                                    <option value="none" id="opt-rp-none">1️⃣ Không lặp lại (Chỉ ngày này)</option>
                                    <option value="weekly" id="opt-rp-weekly">🔄 Hàng tuần (Cùng Thứ mỗi tuần)</option>
                                    <option value="monthly" id="opt-rp-monthly" selected>🗓️ Hàng tháng (Cùng Ngày này mỗi tháng)</option>
                                    <option value="yearly" id="opt-rp-yearly">📆 Hàng năm (Cùng Ngày/Tháng mỗi năm)</option>
                                    <option value="daily" id="opt-rp-daily">☀️ Hàng ngày (Mỗi ngày)</option>
                                    <option value="custom" id="opt-rp-custom">⚙️ Tùy chỉnh chu kỳ...</option>
                                </select>
                            </div>
                        </div>

                        <div id="custom-repeat-box" class="hidden bg-slate-800/90 border border-amber-400/40 rounded-xl p-2.5 flex flex-wrap items-center justify-between gap-2 text-xs">
                            <span id="lbl-custom-every" class="text-amber-300 font-bold">⚙️ Lặp lại mỗi:</span>
                            <div class="flex items-center gap-1.5">
                                <input type="number" id="custom-repeat-interval" value="2" min="1" max="365" class="w-14 bg-slate-900 text-white font-mono font-bold text-center py-1 rounded-lg border border-white/15" />
                                <select id="custom-repeat-unit" class="bg-slate-900 text-cyan-300 font-bold px-2 py-1 rounded-lg border border-white/15">
                                    <option value="day" id="opt-u-day">Ngày</option>
                                    <option value="week" id="opt-u-week" selected>Tuần</option>
                                    <option value="month" id="opt-u-month">Tháng</option>
                                    <option value="year" id="opt-u-year">Năm</option>
                                </select>
                            </div>
                            <div class="flex items-center gap-1.5">
                                <span id="lbl-custom-for" class="text-slate-300">Trong:</span>
                                <input type="text" id="custom-repeat-duration" value="3 tháng" class="w-24 bg-slate-900 text-amber-300 font-bold px-2 py-1 rounded-lg border border-white/15 text-xs" />
                            </div>
                        </div>

                        <div class="flex gap-2">
                            <input type="text" id="new-slot-subject" onkeydown="if(event.key==='Enter') saveNewTimetableSlot()" placeholder="Nhập môn học, ca làm, sự kiện..." class="flex-1 bg-slate-800 text-white text-xs px-3 py-2 rounded-xl border border-white/15 focus:outline-none focus:border-emerald-400" />
                            <button onclick="saveNewTimetableSlot()" id="lbl-btn-add-slot" class="bg-emerald-600 hover:bg-emerald-500 text-white font-extrabold px-4 py-2 rounded-xl text-xs shrink-0 shadow-lg transition">
                                + Thêm Lịch
                            </button>
                        </div>

                        <label class="flex items-center gap-2 pt-0.5 cursor-pointer text-[11px] text-cyan-300 font-semibold">
                            <input type="checkbox" id="auto-sync-to-flight" checked class="w-4 h-4 accent-emerald-500 rounded cursor-pointer" />
                            <span id="lbl-autosync-check">⚡ Tự động đẩy sang Danh sách Nhiệm vụ & Báo giờ Chuyến bay bên trái</span>
                        </label>
                    </div>

                    <div id="timetable-slots-list" class="space-y-2 flex-1 max-h-[220px] overflow-y-auto pr-1"></div>
                </div>
            </div>
        </div>
    </main>

    <!-- ========================================================================================= -->
    <!-- TRANG 2: QUẢ ĐỊA CẦU 3D VŨ TRỤ (THU NHỎ) ⟷ BẢN ĐỒ VỆ TINH 2D                              -->
    <!-- ========================================================================================= -->
    <section id="page-flight" style="z-index: 20;" class="fixed inset-x-0 top-14 bottom-0 overflow-hidden page-layer-hidden">

        <div id="globe-wrapper">
            <canvas id="globe-canvas" class="w-full h-full block cursor-grab active:cursor-grabbing"></canvas>

            <div id="globe-origin-pin" style="z-index: 15;" class="fixed pointer-events-none -translate-x-1/2 -translate-y-1/2 hidden">
                <div class="bg-cyan-400 text-black font-black text-[10px] px-2 py-0.5 rounded-md shadow-xl border border-black/40 whitespace-nowrap">✈️ <span id="globe-origin-code">SGN</span></div>
            </div>
            <div id="globe-dest-pin" style="z-index: 15;" class="fixed pointer-events-none -translate-x-1/2 -translate-y-1/2 hidden">
                <div class="bg-yellow-400 text-black font-black text-[10px] px-2 py-0.5 rounded-md shadow-xl border border-black/40 whitespace-nowrap">🏁 <span id="globe-dest-code">DAD</span></div>
            </div>
            <div id="globe-plane-pin" style="z-index: 18;" class="fixed pointer-events-none -translate-x-1/2 -translate-y-1/2 hidden">
                <div class="relative w-14 h-14 flex items-center justify-center">
                    <div class="radar-ring absolute inset-1 rounded-full border-2 border-cyan-400/80"></div>
                    <div id="globe-plane-svg" class="w-12 h-12 relative z-10"></div>
                </div>
            </div>
        </div>

        <div id="map-2d-wrapper">
            <div id="map"></div>
        </div>

        <div id="zoom-mode-controls" style="z-index: 60;" class="fixed right-4 top-1/3 -translate-y-1/2 flex flex-col items-end gap-2">
            <div class="glass-panel p-1.5 rounded-2xl flex flex-col items-center gap-1.5 shadow-2xl border border-cyan-400/30">
                <button onclick="zoomStepIn()" class="w-9 h-9 rounded-xl bg-slate-800 hover:bg-blue-600 text-white font-black text-base flex items-center justify-center transition border border-white/10">+</button>
                <div id="projection-mode-badge" class="text-[9px] font-mono font-extrabold text-cyan-300 px-1 py-0.5 text-center leading-tight">3D</div>
                <button onclick="zoomStepOut()" class="w-9 h-9 rounded-xl bg-slate-800 hover:bg-blue-600 text-white font-black text-base flex items-center justify-center transition border border-white/10">−</button>
            </div>

            <button onclick="toggleProjectionMode()" id="quick-switch-proj-btn" class="glass-panel px-3 py-2 rounded-xl text-[11px] font-extrabold text-amber-300 hover:text-white border border-amber-400/40 shadow-xl whitespace-nowrap">
                🛰️ Bản đồ 2D
            </button>
        </div>

        <!-- GÓC NHÌN 2: BUỒNG LÁI PHI CÔNG -->
        <div id="view-cockpit" style="z-index: 45;" class="fixed inset-x-0 top-14 bottom-0 hidden flex-col justify-between overflow-hidden">
            <div id="cockpit-sky-bg" class="absolute inset-0 bg-gradient-to-b from-sky-500 via-blue-400 to-sky-200 transition-all duration-700 overflow-hidden">
                <div id="cockpit-stars" class="absolute inset-0 opacity-0 transition-opacity duration-700" style="background-image: radial-gradient(white 1.2px, transparent 1.2px), radial-gradient(rgba(255,255,255,0.7) 1.5px, transparent 1.5px); background-size: 55px 55px, 95px 95px;"></div>

                <div class="svg-cloud-1 absolute top-10 left-0 w-72 text-white/85 pointer-events-none">
                    <svg viewBox="0 0 200 80" fill="currentColor"><path d="M45 65 h115 a22 22 0 0 0 0 -44 a28 28 0 0 0 -52 -12 a34 34 0 0 0 -63 18 a20 20 0 0 0 0 38 z"/></svg>
                </div>
                <div class="svg-cloud-2 absolute top-28 left-0 w-96 text-white/70 pointer-events-none">
                    <svg viewBox="0 0 200 80" fill="currentColor"><path d="M45 65 h115 a22 22 0 0 0 0 -44 a28 28 0 0 0 -52 -12 a34 34 0 0 0 -63 18 a20 20 0 0 0 0 38 z"/></svg>
                </div>
                <div class="svg-cloud-3 absolute top-44 left-0 w-80 text-white/90 pointer-events-none">
                    <svg viewBox="0 0 200 80" fill="currentColor"><path d="M45 65 h115 a22 22 0 0 0 0 -44 a28 28 0 0 0 -52 -12 a34 34 0 0 0 -63 18 a20 20 0 0 0 0 38 z"/></svg>
                </div>
                <div class="svg-cloud-4 absolute top-16 left-0 w-64 text-white/60 pointer-events-none">
                    <svg viewBox="0 0 200 80" fill="currentColor"><path d="M45 65 h115 a22 22 0 0 0 0 -44 a28 28 0 0 0 -52 -12 a34 34 0 0 0 -63 18 a20 20 0 0 0 0 38 z"/></svg>
                </div>
                <div class="svg-cloud-5 absolute top-56 left-0 w-[420px] text-white/80 pointer-events-none">
                    <svg viewBox="0 0 200 80" fill="currentColor"><path d="M45 65 h115 a22 22 0 0 0 0 -44 a28 28 0 0 0 -52 -12 a34 34 0 0 0 -63 18 a20 20 0 0 0 0 38 z"/></svg>
                </div>

                <div id="cockpit-rain-layer" class="rain-overlay absolute inset-0 hidden pointer-events-none"></div>
            </div>

            <div class="relative z-10 w-full bg-gradient-to-b from-[#070b14] to-[#111827]/90 border-b-2 border-slate-700 px-4 py-1.5 flex items-center justify-center gap-6 text-[10px] font-mono text-slate-400 shadow-lg">
                <span class="text-emerald-400 font-bold">● APU GEN ON</span>
                <span>● SEATBELT SIGN: ON</span>
                <span class="hidden sm:inline">● ANTI-ICE: AUTO</span>
                <span class="text-cyan-400 font-bold">● AUTOPILOT: NAV + VNAV</span>
            </div>

            <div class="relative z-10 flex-1 flex items-center justify-center pointer-events-none">
                <div class="absolute inset-y-0 left-1/2 -translate-x-1/2 w-3.5 bg-gradient-to-r from-slate-950 via-slate-800 to-slate-950 border-x border-white/10"></div>

                <div class="w-[300px] sm:w-[390px] h-[185px] sm:h-[210px] border-2 border-emerald-400/60 rounded-3xl bg-emerald-950/15 backdrop-blur-[1px] p-3.5 flex flex-col justify-between shadow-[0_0_40px_rgba(16,185,129,0.2)]">
                    <div class="flex justify-between items-center text-[11px] font-mono font-bold text-emerald-300 border-b border-emerald-400/30 pb-1">
                        <span>SPD: <b id="hud-speed">840 KM/H</b></span>
                        <span class="bg-emerald-400/20 px-2 py-0.5 rounded border border-emerald-400/40">HDG <b id="hud-heading">045°</b></span>
                        <span>ALT: <b id="hud-alt">36,000 FT</b></span>
                    </div>

                    <div class="relative flex-1 flex items-center justify-center overflow-hidden my-1">
                        <div class="hud-horizon w-48 flex flex-col items-center space-y-2">
                            <div class="w-24 border-b border-dashed border-emerald-300/70 text-[9px] font-mono text-emerald-300 flex justify-between"><span>+10</span><span>+10</span></div>
                            <div class="w-40 border-b-2 border-emerald-300 text-[10px] font-mono text-emerald-200 flex justify-between"><span>0</span><span>PITCH</span><span>0</span></div>
                            <div class="w-24 border-b border-dashed border-emerald-300/70 text-[9px] font-mono text-emerald-300 flex justify-between"><span>-10</span><span>-10</span></div>
                        </div>
                        <div class="absolute text-emerald-300 font-mono font-black text-base">─ ✛ ─</div>
                    </div>

                    <div class="flex justify-between items-center text-[10px] font-mono text-emerald-200 border-t border-emerald-400/30 pt-1">
                        <span id="hud-aircraft-name">AIRBUS A321NEO</span>
                        <span id="hud-route-code">SGN ➔ DAD</span>
                    </div>
                </div>
            </div>

            <div class="relative z-10 bg-gradient-to-t from-[#04070e] via-[#0d1322] to-[#1a243b] border-t-4 border-slate-600 px-4 pt-3 pb-24 shadow-2xl">
                <div class="max-w-4xl mx-auto grid grid-cols-3 gap-3 h-28">
                    <div class="bg-[#060a12] border-2 border-slate-700 rounded-xl p-2.5 flex flex-col justify-between font-mono shadow-inner">
                        <div class="text-[10px] text-cyan-400 font-bold flex justify-between"><span>PFD • ATTITUDE</span><span class="text-emerald-400">AP1+FD</span></div>
                        <div class="flex items-center justify-between px-2">
                            <span class="text-[10px] text-amber-300">MACH 0.79</span>
                            <div id="cockpit-plane-svg-preview" class="w-10 h-10"></div>
                            <span class="text-[10px] text-cyan-300">FL360</span>
                        </div>
                        <div class="text-[10px] text-slate-400 flex justify-between"><span id="cockpit-real-clock">00:00:00</span><span>ETA <b id="cockpit-eta" class="text-emerald-400">--:--</b></span></div>
                    </div>

                    <div class="bg-[#060a12] border-2 border-cyan-500/40 rounded-xl p-2.5 flex flex-col items-center justify-center font-mono shadow-inner">
                        <div class="text-[9px] text-amber-400 uppercase font-bold tracking-wider">FOCUS MISSION TIMER</div>
                        <div id="cockpit-timer-display" class="text-2xl sm:text-3xl font-extrabold text-white my-0.5">55:00</div>
                        <div id="cockpit-task-display" class="text-[10px] text-cyan-300 truncate max-w-[180px]">💻 Work</div>
                    </div>

                    <div class="bg-[#060a12] border-2 border-slate-700 rounded-xl p-2.5 flex flex-col justify-between font-mono relative overflow-hidden shadow-inner">
                        <div class="text-[10px] text-emerald-400 font-bold flex justify-between"><span>NAV RADAR</span><span id="cockpit-dist-display" class="text-yellow-400">605 KM</span></div>
                        <div class="w-12 h-12 rounded-full border border-emerald-500/40 mx-auto flex items-center justify-center relative">
                            <div class="radar-ring absolute inset-0 rounded-full border border-emerald-400"></div>
                            <span class="text-xs">✈️</span>
                        </div>
                        <div class="text-[9px] text-slate-400 text-center">WX RADAR + TCAS ON</div>
                    </div>
                </div>
            </div>
        </div>

        <!-- GÓC NHÌN 3: TRONG KHOANG CABIN -->
        <div id="view-cabin" style="z-index: 45;" class="fixed inset-x-0 top-14 bottom-0 hidden flex-col justify-between bg-gradient-to-b from-[#15192b] via-[#0e1526] to-[#070b14] overflow-hidden">
            <div id="cabin-ceiling-glow" class="absolute top-0 inset-x-0 h-28 bg-gradient-to-b from-cyan-500/30 via-blue-500/15 to-transparent blur-xl pointer-events-none transition-all duration-700"></div>

            <div class="relative z-10 w-full bg-gradient-to-b from-[#1e293b] to-[#0f172a] border-b-2 border-slate-700 px-4 py-2 flex flex-wrap items-center justify-between gap-2 shadow-xl">
                <div class="flex items-center gap-3 text-xs">
                    <span class="bg-amber-500/20 text-amber-300 border border-amber-400/30 px-2.5 py-0.5 rounded-full font-extrabold text-[10px]">🔔 FASTEN SEATBELT</span>
                    <span class="bg-emerald-500/20 text-emerald-300 border border-emerald-400/30 px-2.5 py-0.5 rounded-full font-extrabold text-[10px]">🚭 NO SMOKING</span>
                    <span id="cabin-air-status" class="text-[11px] text-cyan-300 font-semibold hidden sm:inline">❄️ Cabin: 22°C</span>
                </div>

                <div class="flex flex-wrap items-center gap-1.5">
                    <button onclick="toggleReadingLight()" id="btn-reading-light" class="bg-slate-800 hover:bg-slate-700 border border-white/15 px-2.5 py-1 rounded-xl text-[11px] font-bold text-slate-200 transition">
                        💡 Đèn đọc sách
                    </button>
                    <button onclick="toggleTrayTable()" id="btn-tray-table" class="bg-blue-600/30 hover:bg-blue-600/40 border border-blue-400/40 px-2.5 py-1 rounded-xl text-[11px] font-bold text-cyan-200 transition">
                        🍱 Gấp/Mở bàn học
                    </button>
                    <button onclick="cycleCabinMoodLight()" id="btn-cabin-led" class="bg-slate-800 hover:bg-slate-700 border border-white/15 px-2.5 py-1 rounded-xl text-[11px] font-bold text-amber-300 transition">
                        🌈 Đèn LED trần
                    </button>
                    <button onclick="callFlightAttendant()" id="btn-call-crew" class="bg-slate-800 hover:bg-slate-700 border border-white/15 px-2.5 py-1 rounded-xl text-[11px] font-bold text-emerald-300 transition">
                        🛎️ Gọi tiếp viên
                    </button>
                </div>
            </div>

            <div id="reading-light-beam" class="fixed top-24 left-1/2 -translate-x-1/2 w-[420px] h-[420px] bg-yellow-200/15 blur-3xl rounded-full pointer-events-none hidden z-10"></div>

            <div class="relative z-10 flex-1 flex items-center justify-center gap-4 sm:gap-8 px-4 pb-20 overflow-y-auto">
                <div class="hidden md:flex flex-col items-center">
                    <div id="cabin-side-window" class="relative w-36 h-52 rounded-[70px] border-[10px] border-slate-700 bg-gradient-to-b from-sky-500 via-blue-400 to-sky-200 shadow-2xl overflow-hidden">
                        <div class="win-cloud-fast absolute top-14 w-32 text-white/85">
                            <svg viewBox="0 0 200 80" fill="currentColor"><path d="M45 65 h115 a22 22 0 0 0 0 -44 a28 28 0 0 0 -52 -12 a34 34 0 0 0 -63 18 a20 20 0 0 0 0 38 z"/></svg>
                        </div>
                        <div class="win-cloud-slow absolute top-28 w-36 text-white/70">
                            <svg viewBox="0 0 200 80" fill="currentColor"><path d="M45 65 h115 a22 22 0 0 0 0 -44 a28 28 0 0 0 -52 -12 a34 34 0 0 0 -63 18 a20 20 0 0 0 0 38 z"/></svg>
                        </div>
                        <svg viewBox="0 0 120 80" class="absolute bottom-2 right-0 w-28">
                            <polygon points="120,25 15,60 25,70 120,55" fill="#cbd5e1"/>
                            <polygon points="15,60 5,38 14,36 25,70" fill="#0ea5e9"/>
                            <circle cx="9" cy="38" r="3" fill="#ef4444" class="strobe-light"/>
                        </svg>
                    </div>
                    <span class="text-[10px] text-slate-400 font-bold mt-1.5">SEAT <b id="cabin-window-seat-tag" class="text-cyan-300">06A</b></span>
                </div>

                <div class="w-full max-w-md bg-gradient-to-b from-[#1e293b] to-[#0f172a] border-4 border-slate-700 rounded-t-[44px] rounded-b-3xl p-4 shadow-2xl relative">
                    <div class="w-36 h-6 bg-slate-800 border border-white/10 rounded-b-xl mx-auto -mt-4 mb-2.5 flex items-center justify-center text-[10px] font-extrabold text-amber-300 tracking-widest">
                        SEAT <span id="cabin-seat-label" class="ml-1">06A</span>
                    </div>

                    <div class="bg-[#060a14] border-4 border-slate-950 rounded-2xl p-3.5 shadow-inner">
                        <div class="flex items-center justify-between border-b border-white/10 pb-1.5 mb-2">
                            <span id="cabin-aircraft-label" class="text-[11px] font-bold text-cyan-400 mono">Airbus A321neo</span>
                            <span id="cabin-real-clock" class="text-[10px] text-slate-400 mono">00:00:00</span>
                            <span id="cabin-route-label" class="text-[11px] font-extrabold text-yellow-400 mono">SGN ➔ DAD</span>
                        </div>

                        <div class="grid grid-cols-2 gap-2.5 items-center">
                            <div>
                                <div id="lbl-cabin-goal" class="text-[9px] text-slate-400 uppercase font-bold">Mục tiêu đang học</div>
                                <div id="cabin-task-title" class="text-xs sm:text-sm font-extrabold text-white mt-0.5 truncate">💻 Work</div>
                                <div class="text-[10px] text-emerald-400 mt-0.5">👤 <b id="cabin-passenger-name">Hữu Đại</b></div>
                                <div class="text-[10px] text-slate-400 font-mono">ETA: <b id="cabin-eta" class="text-amber-300">--:--</b></div>
                            </div>

                            <div class="bg-slate-900/90 border border-white/10 rounded-xl p-2 text-center">
                                <div id="lbl-cabin-rem" class="text-[8px] text-slate-400 uppercase">Thời gian còn lại</div>
                                <div id="cabin-timer-display" class="text-xl font-black text-cyan-400 mono">55:00</div>
                                <div class="text-[9px] text-amber-300"><span id="cabin-dist-display">605</span> km</div>
                            </div>
                        </div>
                    </div>

                    <div id="cabin-tray-table-open" class="mt-3 bg-gradient-to-b from-slate-200 to-slate-300 text-slate-900 rounded-2xl p-3 shadow-xl border-b-4 border-slate-400 transition-all">
                        <div class="flex items-center justify-between">
                            <div class="flex items-center gap-2.5">
                                <span class="text-2xl">💻</span>
                                <div>
                                    <div id="lbl-tray-title" class="text-[10px] font-black uppercase text-slate-600">Bàn học cá nhân trên máy bay</div>
                                    <div id="lbl-tray-sub" class="text-xs font-extrabold text-slate-900">Đang mở bàn • Tập trung tối đa</div>
                                </div>
                            </div>
                            <div class="flex items-center gap-2 text-xl"><span>☕</span><span>📓</span></div>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- GÓC NHÌN 4: QUA CỬA SỔ MÁY BAY -->
        <div id="view-window" style="z-index: 45;" class="fixed inset-x-0 top-14 bottom-0 hidden flex-col items-center justify-center bg-[#090d18] p-4 overflow-hidden">
            <div class="relative z-20 flex items-center gap-3 mb-2">
                <button onclick="toggleWindowShade()" id="btn-window-shade" class="glass-panel px-3.5 py-1 rounded-full text-xs font-extrabold text-amber-300 hover:text-white border border-amber-400/30">
                    🪟 Kéo Rèm Cửa Sổ Lên / Xuống
                </button>
            </div>

            <div class="relative w-[270px] sm:w-[320px] h-[330px] sm:h-[365px] rounded-[150px] border-[16px] border-[#1e293b] shadow-[inset_0_0_40px_rgba(0,0,0,0.9),0_25px_70px_rgba(0,0,0,0.95)] overflow-hidden bg-gradient-to-b from-sky-500 via-blue-400 to-sky-200 mb-20" id="window-sky-container">
                <div id="window-stars" class="absolute inset-0 opacity-0 transition-opacity duration-700" style="background-image: radial-gradient(white 1.2px, transparent 1.2px), radial-gradient(rgba(255,255,255,0.6) 1px, transparent 1px); background-size: 45px 45px, 80px 80px;"></div>
                <div id="window-celestial" class="absolute top-10 right-12 w-11 h-11 rounded-full bg-yellow-300 shadow-[0_0_35px_#fef08a]"></div>

                <div class="win-cloud-fast absolute top-24 w-48 text-white/90 pointer-events-none">
                    <svg viewBox="0 0 200 80" fill="currentColor"><path d="M45 65 h115 a22 22 0 0 0 0 -44 a28 28 0 0 0 -52 -12 a34 34 0 0 0 -63 18 a20 20 0 0 0 0 38 z"/></svg>
                </div>
                <div class="win-cloud-slow absolute top-44 w-56 text-white/75 pointer-events-none">
                    <svg viewBox="0 0 200 80" fill="currentColor"><path d="M45 65 h115 a22 22 0 0 0 0 -44 a28 28 0 0 0 -52 -12 a34 34 0 0 0 -63 18 a20 20 0 0 0 0 38 z"/></svg>
                </div>

                <div id="window-city-lights" class="absolute bottom-0 inset-x-0 h-14 bg-gradient-to-t from-amber-500/25 via-orange-500/10 to-transparent"></div>

                <div class="absolute bottom-10 right-0 w-[230px] h-[120px] pointer-events-none">
                    <svg viewBox="0 0 300 160" class="w-full h-full drop-shadow-2xl">
                        <ellipse cx="145" cy="112" rx="34" ry="18" fill="#334155" stroke="#64748b" stroke-width="2"/>
                        <ellipse cx="115" cy="112" rx="8" ry="15" fill="#0f172a" stroke="#38bdf8" stroke-width="1.5"/>
                        <polygon points="300,35 35,95 55,112 300,98" fill="#cbd5e1" stroke="#94a3b8" stroke-width="2"/>
                        <polygon points="35,95 15,62 28,60 55,112" fill="#0ea5e9"/>
                        <circle cx="22" cy="62" r="5" fill="#ef4444" class="strobe-light"/>
                    </svg>
                </div>

                <div id="window-rain-layer" class="rain-overlay absolute inset-0 hidden pointer-events-none"></div>
                <div id="window-shade-panel" class="absolute inset-x-0 top-0 h-0 bg-gradient-to-b from-slate-800 to-slate-900 border-b-4 border-slate-600 transition-all duration-500 flex items-end justify-center pb-2 overflow-hidden">
                    <div class="w-12 h-1.5 rounded-full bg-slate-400"></div>
                </div>
            </div>
        </div>

        <button id="toggle-booking-btn" style="z-index: 60;" onclick="toggleBookingCardSize()" class="fixed bottom-3 left-3 glass-panel px-3 py-1.5 rounded-xl text-[11px] font-extrabold text-cyan-300 hover:text-white shadow-lg border border-cyan-500/30">
            🔽 Thu gọn bảng
        </button>

        <!-- MÀN HÌNH 1 TRONG TRẠM BAY: BẢNG ĐẶT VÉ -->
        <div id="screen-booking" style="z-index: 60;" class="fixed bottom-3 left-1/2 -translate-x-1/2 w-[95%] max-w-md glass-panel rounded-3xl p-3.5 shadow-2xl transition-all duration-300">
            <div class="flex items-center justify-between gap-2 mb-2.5 pb-2 border-b border-white/10">
                <div class="flex items-center gap-2.5">
                    <div id="booking-plane-svg-box" class="w-10 h-10 rounded-xl bg-slate-900 border border-cyan-400/30 flex items-center justify-center p-1 shrink-0"></div>
                    <div>
                        <div class="flex items-center gap-1.5">
                            <span id="badge-origin" class="bg-cyan-400 text-black font-black text-[10px] px-1.5 py-0.5 rounded">SGN</span>
                            <span class="text-xs text-slate-400">➔</span>
                            <span id="badge-dest" class="bg-yellow-400 text-black font-black text-[10px] px-1.5 py-0.5 rounded">DAD</span>
                            <span id="badge-dist" class="text-[11px] font-mono text-cyan-300 font-bold ml-1">605 km</span>
                        </div>
                        <div id="banner-dest-title" class="text-xs font-extrabold text-white mt-0.5 truncate max-w-[175px]">TP.HCM ➔ Đà Nẵng</div>
                    </div>
                </div>

                <select id="aircraft-select" onchange="updateAircraft()" class="bg-slate-800 text-cyan-300 text-[11px] font-bold px-2 py-1.5 rounded-xl border border-cyan-500/30 focus:outline-none cursor-pointer">
                    <option value="Airbus A321neo">🛩️ A321neo (840 km/h)</option>
                    <option value="Boeing 787-9">✈️ B787-9 (910 km/h)</option>
                    <option value="Airbus A350-900">🛫 A350-900 (905 km/h)</option>
                    <option value="ATR 72-600">⚙️ ATR 72 (510 km/h)</option>
                </select>
            </div>

            <div class="grid grid-cols-11 gap-1.5 items-center bg-slate-900/90 p-2 rounded-2xl border border-white/10 mb-2.5">
                <div class="col-span-5">
                    <div id="lbl-origin-title" class="text-[9px] text-slate-400 uppercase font-bold mb-0.5">Điểm khởi hành</div>
                    <select id="origin-select" onchange="onRouteChange()" class="w-full bg-slate-800 text-white font-bold text-[11px] px-2 py-1.5 rounded-lg border border-white/10 focus:outline-none cursor-pointer"></select>
                </div>
                <div class="col-span-1 flex justify-center pt-3">
                    <button onclick="swapRoute()" class="w-7 h-7 rounded-full bg-slate-800 hover:bg-blue-600 text-cyan-400 hover:text-white font-bold text-xs flex items-center justify-center transition border border-white/10">⇄</button>
                </div>
                <div class="col-span-5">
                    <div id="lbl-dest-title" class="text-[9px] text-yellow-400 uppercase font-bold mb-0.5">Điểm hạ cánh</div>
                    <select id="dest-select" onchange="onRouteChange()" class="w-full bg-slate-800 text-white font-bold text-[11px] px-2 py-1.5 rounded-lg border border-yellow-400/40 focus:outline-none cursor-pointer"></select>
                </div>
            </div>

            <div class="bg-blue-950/50 border border-cyan-400/30 rounded-2xl p-2.5 mb-2.5 flex items-center justify-between">
                <div>
                    <div id="lbl-auto-dur-title" class="text-[9px] text-cyan-300 font-bold uppercase tracking-wider">⏱️ Thời gian học (Tính theo khoảng cách)</div>
                    <div class="flex items-baseline gap-2 mt-0.5">
                        <span id="auto-calc-duration-text" class="text-base font-black text-yellow-400 mono">55 phút</span>
                        <span id="auto-calc-speed-text" class="text-[10px] text-slate-300">(605 km • 840 km/h)</span>
                    </div>
                </div>
                <div class="text-right font-mono">
                    <div id="lbl-eta-title" class="text-[9px] text-slate-400">Hạ cánh dự kiến (ETA)</div>
                    <div id="booking-realtime-eta" class="text-xs font-extrabold text-emerald-400">--:--</div>
                </div>
            </div>

            <div class="flex gap-2">
                <button onclick="goToSeatSelection()" id="lbl-btn-pick-seat" class="w-1/2 bg-slate-800 hover:bg-slate-700 text-cyan-300 font-extrabold py-2.5 rounded-2xl text-xs border border-cyan-500/30 transition">
                    💺 Chọn Ghế & In Vé
                </button>
                <button onclick="startFlight()" id="lbl-btn-fly-now" class="w-1/2 bg-gradient-to-r from-emerald-500 to-cyan-500 hover:opacity-95 text-black font-black py-2.5 rounded-2xl shadow-lg text-xs uppercase tracking-wider transition">
                    🛫 Bay Ngay Lập Tức
                </button>
            </div>
        </div>

        <!-- MÀN HÌNH 2 TRONG TRẠM BAY: CHỌN GHẾ NGỒI -->
        <div id="screen-seat" style="z-index: 65;" class="fixed inset-x-0 top-14 bottom-0 bg-[#070b14]/95 backdrop-blur-xl hidden flex-col items-center justify-between py-3 px-4">
            <div class="w-full max-w-md flex items-center justify-between">
                <button onclick="backToBooking()" id="btn-seat-back" class="bg-slate-800 hover:bg-slate-700 text-slate-200 px-3 py-1.5 rounded-xl text-xs font-bold">‹ Quay lại</button>
                <div class="text-center">
                    <div id="seat-header-aircraft" class="text-[10px] text-cyan-400 font-extrabold uppercase tracking-widest">AIRBUS A321NEO</div>
                    <div id="seat-header-route" class="text-xs font-extrabold text-white">SGN ➔ DAD • 55p</div>
                </div>
                <span id="seat-selected-badge" class="bg-blue-600/30 border border-blue-400 text-blue-200 text-xs font-mono font-bold px-2 py-1 rounded-lg">06A</span>
            </div>

            <div class="relative w-full max-w-[320px] flex-1 max-h-[62vh] fuselage flex flex-col items-center pt-8 pb-6 px-5 overflow-y-auto my-2">
                <div class="w-28 h-5 border-b border-slate-700/80 mb-3 flex items-center justify-center text-[9px] font-mono text-slate-500 tracking-widest uppercase">Cockpit</div>
                <div class="grid grid-cols-5 w-full text-center text-xs font-extrabold text-slate-400 mb-2 px-1">
                    <div>A</div><div>C</div><div></div><div>D</div><div>F</div>
                </div>
                <div id="seat-grid" class="w-full space-y-1.5 pb-4"></div>
            </div>

            <div id="focus-popover-backdrop" style="z-index: 70;" class="fixed inset-0 bg-black/65 backdrop-blur-sm hidden items-center justify-center p-4">
                <div class="focus-popover w-full max-w-[350px] rounded-[26px] p-5 text-white">
                    <div class="flex justify-between items-center mb-1">
                        <span class="text-xs font-bold text-blue-300">Seat: <span id="pop-seat-code" class="mono text-white">06A</span></span>
                        <button onclick="closeFocusPopover()" class="text-slate-400 hover:text-white text-sm font-bold">✕</button>
                    </div>
                    <h3 id="lbl-pop-focus-q" class="text-sm font-extrabold text-white mb-3">What do you want to focus?</h3>
                    <div class="flex flex-wrap gap-1.5 mb-3" id="focus-pills-container"></div>
                    <div id="custom-focus-box" class="mb-3">
                        <input type="text" id="custom-focus-input" placeholder="Nhập mục tiêu..." class="w-full bg-slate-900/90 text-xs text-white px-3 py-2 rounded-xl border border-blue-400/40 focus:outline-none" />
                    </div>
                    <div class="bg-red-500/15 border border-red-400/30 p-2.5 rounded-2xl flex items-center justify-between mb-3.5">
                        <div>
                            <div class="text-xs font-extrabold text-red-200">🔒 Strict Mode</div>
                            <div id="lbl-strict-desc" class="text-[10px] text-slate-300">Cảnh báo nếu rời khỏi màn hình học</div>
                        </div>
                        <input type="checkbox" id="strict-mode-toggle" checked class="w-4 h-4 accent-red-500 cursor-pointer" />
                    </div>
                    <button onclick="confirmSeatAndFocus()" id="btn-confirm-seat" class="w-full bg-gradient-to-r from-blue-600 to-cyan-500 hover:opacity-95 text-white font-extrabold py-3 rounded-2xl text-xs shadow-lg">
                        Xác nhận & Xuất Vé Boarding Pass ➔
                    </button>
                </div>
            </div>

            <div class="w-full max-w-md flex items-center justify-between px-2">
                <div id="lbl-seat-hint" class="text-xs text-slate-400">Chạm vào ghế bất kỳ hoặc bấm Tiếp tục</div>
                <button onclick="showBoardingPass()" id="btn-seat-continue" class="bg-blue-600 hover:bg-blue-500 text-white font-extrabold px-5 py-2 rounded-xl text-xs shadow-lg">Tiếp tục ➔</button>
            </div>
        </div>

        <!-- MÀN HÌNH 3 TRONG TRẠM BAY: VÉ BOARDING PASS -->
        <div id="screen-ticket" style="z-index: 65;" class="fixed inset-x-0 top-14 bottom-0 bg-black/85 backdrop-blur-md hidden items-center justify-center p-4">
            <div class="w-full max-w-sm flex flex-col items-center">
                <div class="w-full bg-[#121723] border border-white/15 rounded-3xl overflow-hidden shadow-2xl relative">
                    <div class="ticket-cutout-left"></div>
                    <div class="ticket-cutout-right"></div>

                    <div class="bg-gradient-to-r from-blue-600 to-cyan-500 px-5 py-2.5 flex justify-between items-center">
                        <span class="text-xs font-black tracking-widest uppercase text-white">BOARDING PASS</span>
                        <span id="tk-aircraft" class="text-[11px] font-mono font-bold bg-black/25 text-white px-2 py-0.5 rounded">Airbus A321neo</span>
                    </div>

                    <div class="p-5">
                        <div class="flex justify-between items-start mb-3">
                            <div>
                                <div class="text-[9px] text-slate-400 uppercase">PASSENGER</div>
                                <div id="tk-passenger" class="text-sm font-black text-amber-300 uppercase">HỮU ĐẠI</div>
                            </div>
                            <div class="text-right">
                                <div class="text-[9px] text-slate-400 uppercase">STD ➔ ETA</div>
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
                                <div class="text-slate-500 text-[9px] uppercase">SEAT</div>
                                <div id="tk-seat" class="font-extrabold text-cyan-400 mt-0.5 mono">06A</div>
                            </div>
                            <div>
                                <div class="text-slate-500 text-[9px] uppercase">DISTANCE</div>
                                <div id="tk-dist" class="font-bold text-white mt-0.5">605 km</div>
                            </div>
                            <div class="text-right">
                                <div class="text-slate-500 text-[9px] uppercase">FOCUS</div>
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
                    <button onclick="backToSeatFromTicket()" id="btn-tk-change-seat" class="w-1/3 bg-slate-800 hover:bg-slate-700 text-slate-300 font-bold py-3 rounded-2xl text-xs">‹ Đổi ghế</button>
                    <button onclick="startFlight()" id="btn-tk-takeoff" class="w-2/3 bg-gradient-to-r from-emerald-500 to-cyan-500 hover:opacity-95 text-black font-black py-3 rounded-2xl shadow-xl text-xs uppercase tracking-wider">
                        🛫 Cất Cánh Bắt Đầu Học
                    </button>
                </div>
            </div>
        </div>

        <!-- MÀN HÌNH 4 TRONG TRẠM BAY: THANH DOCK NHỎ GỌN Ở ĐÁY -->
        <div id="screen-flying" style="z-index: 7500;" class="fixed bottom-2.5 left-1/2 -translate-x-1/2 w-[96%] max-w-4xl glass-panel rounded-2xl px-3.5 py-2 shadow-2xl hidden border border-cyan-500/30">
            <div class="flex flex-wrap items-center justify-between gap-2">
                <div class="flex items-center gap-2.5">
                    <div id="fly-mini-svg" class="w-8 h-8 rounded-xl bg-slate-900 border border-cyan-400/40 p-1 flex items-center justify-center shrink-0"></div>
                    <div>
                        <div class="flex items-center gap-2">
                            <span class="text-xs font-extrabold text-white" id="fly-route-text">SGN ➔ DAD</span>
                            <span class="text-[10px] text-amber-300 font-mono"><b id="fly-dist-left">605</b>km</span>
                            <span class="text-[10px] text-slate-400 font-mono hidden sm:inline">• ETA <b id="fly-eta-badge" class="text-emerald-400">--:--</b></span>
                        </div>
                        <div class="text-[10px] text-cyan-400 font-semibold flex items-center gap-2">
                            <span id="fly-sub-info">A321neo • 06A</span>
                            <span id="safety-hearts" class="text-[10px] tracking-widest">❤️❤️❤️</span>
                        </div>
                    </div>
                    <div id="countdown-timer" class="mono text-xl sm:text-2xl font-black text-yellow-400 tracking-tight ml-1">55:00</div>
                </div>

                <div class="flex flex-wrap items-center gap-1.5">
                    <div class="flex items-center gap-1 bg-slate-900/90 p-1 rounded-xl border border-white/10">
                        <button onclick="setCameraView('map')" id="btn-cam-map" class="cam-switch-btn cam-map px-2 py-1 rounded-lg text-[10px] font-extrabold bg-cyan-500 text-black transition">🌍 Map</button>
                        <button onclick="setCameraView('cockpit')" id="btn-cam-cockpit" class="cam-switch-btn cam-cockpit px-2 py-1 rounded-lg text-[10px] font-extrabold text-slate-300 hover:text-white transition">👨‍✈️ Cockpit</button>
                        <button onclick="setCameraView('cabin')" id="btn-cam-cabin" class="cam-switch-btn cam-cabin px-2 py-1 rounded-lg text-[10px] font-extrabold text-slate-300 hover:text-white transition">💺 Cabin</button>
                        <button onclick="setCameraView('window')" id="btn-cam-window" class="cam-switch-btn cam-window px-2 py-1 rounded-lg text-[10px] font-extrabold text-slate-300 hover:text-white transition">🪟 Window</button>
                    </div>

                    <div class="flex items-center gap-0.5 bg-slate-900/90 p-1 rounded-xl border border-white/10">
                        <button onclick="setFlightEnvironment('day')" class="env-switch-btn env-day px-1.5 py-1 rounded-lg text-[10px] font-bold text-slate-300 hover:text-white">☀️</button>
                        <button onclick="setFlightEnvironment('sunset')" class="env-switch-btn env-sunset px-1.5 py-1 rounded-lg text-[10px] font-bold text-slate-300 hover:text-white">🌅</button>
                        <button onclick="setFlightEnvironment('night')" class="env-switch-btn env-night px-1.5 py-1 rounded-lg text-[10px] font-bold text-slate-300 hover:text-white">🌙</button>
                        <button onclick="setFlightEnvironment('rain')" class="env-switch-btn env-rain px-1.5 py-1 rounded-lg text-[10px] font-bold text-slate-300 hover:text-white">🌧️</button>
                    </div>
                </div>

                <div class="flex items-center gap-1.5">
                    <button onclick="centerOnPlane()" class="bg-slate-800 hover:bg-slate-700 text-xs px-2 py-1.5 rounded-xl text-slate-200 border border-white/10 font-bold">🎯</button>
                    <button onclick="completeFlightEarly()" id="btn-fly-done" class="bg-emerald-500/20 hover:bg-emerald-500/30 text-emerald-300 border border-emerald-500/30 px-2.5 py-1.5 rounded-xl text-[11px] font-bold">✓ Xong</button>
                    <button onclick="abortFlight()" id="btn-fly-abort" class="bg-red-500/20 hover:bg-red-500/30 text-red-300 border border-red-500/30 px-2.5 py-1.5 rounded-xl text-[11px] font-bold">Hủy</button>
                </div>
            </div>

            <div class="w-full bg-slate-800 h-1.5 rounded-full overflow-hidden mt-1.5">
                <div id="flight-progress" class="bg-gradient-to-r from-blue-500 via-cyan-400 to-yellow-400 h-full w-0 transition-all duration-500"></div>
            </div>
        </div>
    </section>

    <!-- MODAL GIẢI THÍCH -->
    <div id="why-schedule-modal" style="z-index: 9000;" class="fixed inset-0 bg-black/75 backdrop-blur-md hidden items-center justify-center p-4">
        <div class="glass-panel w-full max-w-md rounded-3xl p-5 shadow-2xl border border-cyan-400/40">
            <div class="flex justify-between items-center mb-3">
                <h3 id="lbl-why-title" class="text-sm font-extrabold text-white">🧠 Chi tiết Lịch & Chuyến bay</h3>
                <button onclick="closeWhyModal()" class="text-slate-400 hover:text-white font-bold">✕</button>
            </div>
            <div id="why-modal-content" class="space-y-2.5 text-xs text-slate-200"></div>
            <button onclick="closeWhyModal()" class="mt-4 w-full bg-gradient-to-r from-blue-600 to-cyan-500 text-white font-extrabold py-2.5 rounded-xl text-xs">OK</button>
        </div>
    </div>

    <!-- CẢNH BÁO ĐỎ STRICT MODE -->
    <div id="turbulence-modal" style="z-index: 9500;" class="fixed inset-0 turbulence-alert hidden flex-col items-center justify-center p-6 text-center">
        <div class="text-5xl mb-2 animate-bounce">🚨</div>
        <h2 id="lbl-turb-title" class="text-xl sm:text-2xl font-black text-white uppercase mb-2">CẢNH BÁO: BẠN ĐÃ RỜI KHỎI BUỒNG LÁI TẬP TRUNG!</h2>
        <p id="lbl-turb-desc" class="text-xs sm:text-sm text-red-100 max-w-md mb-4">Đồng hồ tập trung đã bị TẠM DỪNG vì bạn vừa chuyển sang cửa sổ khác!</p>
        <div class="bg-black/50 border border-red-300/30 rounded-2xl p-3.5 w-full max-w-xs mb-5">
            <div id="lbl-turb-count" class="text-[11px] text-red-200 uppercase font-bold">Vi phạm kỷ luật</div>
            <div id="violation-count-text" class="text-xl font-black text-yellow-400 mono">1 / 3</div>
        </div>
        <button onclick="resumeFromTurbulence()" id="btn-turb-resume" class="bg-white hover:bg-yellow-300 text-red-900 font-black px-6 py-3.5 rounded-2xl shadow-2xl text-xs uppercase">
            🔒 Quay lại Học tiếp ngay
        </button>
    </div>

    <div id="crash-modal" style="z-index: 9500;" class="fixed inset-0 bg-black/95 backdrop-blur-xl hidden flex-col items-center justify-center p-6 text-center">
        <div class="text-5xl mb-2">💥</div>
        <h2 id="lbl-crash-title" class="text-xl font-black text-red-500 uppercase mb-2">CHUYẾN BAY BỊ HỦY DO MẤT TẬP TRUNG QUÁ 3 LẦN</h2>
        <button onclick="closeCrashModal()" id="btn-crash-back" class="mt-4 bg-red-600 hover:bg-red-500 text-white font-extrabold px-6 py-3 rounded-2xl text-xs uppercase">Quay lại</button>
    </div>

    <!-- MODAL TÙY CHỈNH ÂM THANH & BOT -->
    <div id="media-modal" style="z-index: 9000;" class="fixed inset-0 bg-black/75 backdrop-blur-md hidden items-center justify-center p-4">
        <div class="glass-panel w-full max-w-md rounded-3xl p-5 shadow-2xl">
            <div class="flex justify-between items-center mb-3">
                <h3 id="lbl-media-title" class="text-sm font-extrabold text-white">🎧 Tùy Chỉnh Âm Thanh & Giao Diện</h3>
                <button onclick="closeMediaModal()" class="text-slate-400 hover:text-white text-lg font-bold">✕</button>
            </div>
            <div class="space-y-3 text-xs">
                <div class="bg-slate-900/90 p-3 rounded-2xl border border-white/10">
                    <label id="lbl-media-lofi" class="font-bold text-cyan-400 block mb-1">1. Chọn file nhạc Lofi từ máy (.mp3, .wav):</label>
                    <input type="file" accept="audio/*" onchange="handleLocalAudio(this)" class="w-full text-slate-300 file:mr-2 file:py-1 file:px-3 file:rounded-xl file:border-0 file:font-bold file:bg-blue-600 file:text-white cursor-pointer mb-1.5" />
                    <input type="text" id="audio-url-input" placeholder="MP3 URL..." class="w-full bg-slate-800 text-white px-3 py-1.5 rounded-xl border border-white/10" />
                </div>

                <div class="bg-slate-900/90 p-3 rounded-2xl border border-white/10 flex items-center justify-between">
                    <div>
                        <div id="lbl-media-noise" class="font-bold text-white">🛫 Tiếng động cơ máy bay (Cabin White Noise)</div>
                    </div>
                    <input type="checkbox" onchange="toggleCabinNoise(this.checked)" class="w-5 h-5 accent-cyan-400 cursor-pointer" />
                </div>

                <div class="bg-slate-900/90 p-3 rounded-2xl border border-amber-400/30">
                    <label id="lbl-media-bot" class="font-bold text-amber-300 block mb-1">2. Đổi ảnh đại diện Chatbot AI:</label>
                    <input type="file" accept="image/*" onchange="handleBotAvatarUpload(this)" class="w-full text-slate-300 file:mr-2 file:py-1 file:px-3 file:rounded-xl file:border-0 file:font-bold file:bg-amber-500 file:text-black cursor-pointer" />
                </div>
            </div>
            <button onclick="applyCustomMedia()" id="btn-media-save" class="mt-4 w-full bg-gradient-to-r from-blue-600 to-cyan-500 text-white font-extrabold py-2.5 rounded-xl text-xs">Lưu & Đóng</button>
        </div>
    </div>

    <!-- CHATBOT AI VÀNG KIM -->
    <div id="chatbot-launcher" onclick="toggleChatbotWindow()" style="position: fixed; bottom: 78px; right: 16px; z-index: 9999;" class="cursor-pointer flex items-center gap-2 bg-[#111827] hover:bg-[#1e293b] border-2 border-[#d4a349] pl-3 pr-1.5 py-1 rounded-full bot-launcher-glow shadow-2xl">
        <span id="lbl-chat-launcher" class="text-xs font-extrabold text-amber-300 tracking-wide">💬 Chat AI</span>
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
                <button onclick="resetChat()" class="text-xs font-bold">↺</button>
                <button onclick="toggleChatbotWindow()" class="text-base font-bold leading-none">✕</button>
            </div>
        </div>

        <div id="chat-messages" class="flex-1 p-3 overflow-y-auto space-y-2.5 bg-[#f7f8fc]"></div>

        <div class="px-2.5 py-1.5 bg-white border-t border-slate-100 flex gap-1.5 overflow-x-auto">
            <button id="btn-q1" onclick="sendQuickChat(this.innerText)" class="shrink-0 bg-amber-50 hover:bg-amber-100 text-[#b07d2b] border border-[#d4a349]/40 text-[10px] font-semibold px-2 py-1 rounded-full">💡 Hôm nay học gì?</button>
            <button id="btn-q2" onclick="sendQuickChat(this.innerText)" class="shrink-0 bg-amber-50 hover:bg-amber-100 text-[#b07d2b] border border-[#d4a349]/40 text-[10px] font-semibold px-2 py-1 rounded-full">📋 Việc đang làm</button>
            <button id="btn-q3" onclick="sendQuickChat(this.innerText)" class="shrink-0 bg-amber-50 hover:bg-amber-100 text-[#b07d2b] border border-[#d4a349]/40 text-[10px] font-semibold px-2 py-1 rounded-full">🌪️ Dời lịch</button>
        </div>

        <div class="p-2 bg-white border-t border-slate-200 flex items-center gap-2">
            <input type="text" id="chat-input" onkeydown="if(event.key==='Enter') sendChatMessage()" placeholder="Nhập tin nhắn..." class="flex-1 text-xs text-slate-800 px-2 py-1 focus:outline-none" />
            <button onclick="sendChatMessage()" class="w-7 h-7 rounded-full bg-[#d4a349] hover:bg-[#c29138] text-white flex items-center justify-center shadow text-xs">➤</button>
        </div>
    </div>

    <script>
        // Hàm gán text an toàn tuyệt đối (không bao giờ gây lỗi dừng script)
        function setTxt(id, val) {
            const el = document.getElementById(id);
            if (el && val !== undefined) el.innerText = val;
        }
        function setPlh(id, val) {
            const el = document.getElementById(id);
            if (el && val !== undefined) el.placeholder = val;
        }

        // ================= 1. TỪ ĐIỂN ĐA NGÔN NGỮ TOÀN DIỆN (VI / EN / 繁體中文) =================
        let currentLang = "vi";
        let showLunarCalendar = true;

        const I18N = {
            vi: {
                saveReady: "● Tự động lưu dữ liệu",
                memberTop: "Thành viên",
                tabDash: "📊 Bảng Điều Khiển Học Tập",
                tabFlight: "✈️ Chuyến Bay 3D / 2D",
                bannerTag: "Thông báo Chuyến bay từ Lịch cá nhân",
                bannerBtn: "🛫 Cất cánh học ngay",
                kpi1Title: "Hồ sơ thành viên",
                kpi1Sub: "Đồng bộ Lịch ➔ Chuyến bay",
                kpi2Title: "Nhiệm vụ & Lịch bay",
                kpi2Sub: "Đang chờ cất cánh",
                kpi3Title: "Đã hoàn thành (✓)",
                kpi4Title: "Dặm bay tích lũy",
                aiBadge: "💡 Hôm nay nên học gì? (AI Đề xuất)",
                aiSub: "Báo giờ bay tự động theo khung giờ đã đặt",
                remindBtn: "🔔 Kiểm tra báo thức bay",
                smartCtrlTitle: "⚡ Điều phối Lịch AI Thông Minh",
                smartCtrlDesc: "Sắp xếp thứ tự ưu tiên theo Deadline hoặc tự động dời toàn bộ ca học khi bạn có việc đột xuất.",
                btnAiSort: "🤖 AI Sắp xếp Thứ tự Ưu tiên",
                btnSudden: "🌪️ Có lịch đột xuất (Tự động dời ca)",
                todoHeader: "✅ Danh Sách Nhiệm Vụ & Chặng Bay",
                todoSyncTag: "⚡ Tự động nhận từ Lịch",
                todoSub: "Thêm môn học ở Lịch bên phải sẽ tự động nhảy sang đây kèm giờ bay!",
                filterAll: "Tất cả",
                filterPending: "Đang làm",
                filterDone: "Đã xong ✓",
                quickAddTitle: "+ Thêm nhanh bài tập / deadline lẻ:",
                quickTaskPlh: "Nhập tên công việc (VD: Giải đề Toán, Tạo app...)",
                quickDeadline: "Hạn (Giờ):",
                btnSaveTask: "+ Lưu Việc",
                calHeader: "🗓️ Lịch Biểu & Việc Cá Nhân",
                calSub: "Bấm chọn trực tiếp ngày trên tờ lịch để xem Thứ/Ngày/Tháng/Năm & Âm lịch",
                lunarOn: "🌙 Âm lịch: BẬT",
                lunarOff: "🌙 Âm lịch: TẮT",
                btnToday: "Hôm nay",
                weekdays: ["Thứ 2", "Thứ 3", "Thứ 4", "Thứ 5", "Thứ 6", "Thứ 7", "CN"],
                fullWeekdays: ["Chủ Nhật", "Thứ Hai", "Thứ Ba", "Thứ Tư", "Thứ Năm", "Thứ Sáu", "Thứ Bảy"],
                monthPrefix: "THÁNG",
                pickDate: "Chọn ngày:",
                startTime: "⏰ Bắt đầu:",
                endTime: "🏁 Kết thúc:",
                catType: "Phân loại lịch",
                catStudy: "📚 Lịch học / Ôn bài (Tạo chuyến bay)",
                catSchool: "🔴 Lịch học trên trường (Cố định)",
                catPers: "🟣 Việc cá nhân (Đi làm, sự kiện...)",
                catFree: "🟢 Khung giờ trống tự học",
                repeatCycle: "Chu kỳ lặp lại (Tự chọn)",
                rpNone: "1️⃣ Không lặp lại (Chỉ ngày này)",
                rpWeekly: "🔄 Hàng tuần (Cùng Thứ mỗi tuần)",
                rpMonthly: "🗓️ Hàng tháng (Cùng Ngày này mỗi tháng)",
                rpYearly: "📆 Hàng năm (Cùng Ngày/Tháng mỗi năm)",
                rpDaily: "☀️ Hàng ngày (Mỗi ngày)",
                rpCustom: "⚙️ Tùy chỉnh chu kỳ (Tự nhập bao lâu tùy ý)...",
                customEvery: "⚙️ Lặp lại mỗi:",
                uDay: "Ngày", uWeek: "Tuần", uMonth: "Tháng", uYear: "Năm",
                customFor: "Trong:",
                slotSubjPlh: "Nhập môn học, ca làm, sự kiện (VD: Toán, Đi làm...)",
                btnAddSlot: "+ Thêm Lịch",
                autoSyncCheck: "⚡ Tự động đẩy sang Danh sách Nhiệm vụ & Báo giờ Chuyến bay bên trái",
                originTitle: "ĐIỂM KHỞI HÀNH",
                destTitle: "ĐIỂM HẠ CÁNH",
                autoDurTitle: "⏱️ THỜI GIAN HỌC (TÍNH THEO KHOẢNG CÁCH)",
                etaTitle: "Hạ cánh dự kiến (ETA)",
                btnPickSeat: "💺 Chọn Ghế & In Vé",
                btnFlyNow: "🛫 BAY NGAY LẬP TỨC",
                btnCollapse: "🔽 Thu gọn bảng",
                btnExpand: "🔼 Mở bảng đặt vé",
                btnMap2D: "🛰️ Bản đồ 2D",
                btnGlobe3D: "🌍 Quả cầu 3D",
                btnSeatBack: "‹ Quay lại",
                popFocusQ: "Bạn muốn tập trung làm gì trên chuyến bay này?",
                popFocusPlh: "Nhập mục tiêu (VD: Toán, Tạo app...)",
                strictDesc: "Cảnh báo nếu rời khỏi màn hình học",
                btnConfirmSeat: "Xác nhận & Xuất Vé Boarding Pass ➔",
                seatHint: "Chạm vào ghế bất kỳ hoặc bấm Tiếp tục",
                btnContinue: "Tiếp tục ➔",
                btnChangeSeat: "‹ Đổi ghế",
                btnTakeoff: "🛫 Cất Cánh Bắt Đầu Học",
                btnFlyDone: "✓ Xong",
                btnFlyAbort: "Hủy",
                btnReadLight: "💡 Đèn đọc sách",
                btnTrayTable: "🍱 Gấp/Mở bàn học",
                btnCabinLed: "🌈 Đèn LED trần",
                btnCallCrew: "🛎️ Gọi tiếp viên",
                cabinGoal: "Mục tiêu đang học",
                cabinRem: "Thời gian còn lại",
                trayTitle: "Bàn học cá nhân trên máy bay",
                traySub: "Đang mở bàn • Tập trung tối đa",
                btnWinShade: "🪟 Kéo Rèm Cửa Sổ Lên / Xuống",
                botHeader: "Trợ lý Học tập AI",
                chatLauncher: "💬 Chat AI",
                q1: "💡 Hôm nay học gì?",
                q2: "📋 Việc đang làm",
                q3: "🌪️ Dời lịch",
                chatPlh: "Nhập tin nhắn...",
                emptyTasks: "Chưa có nhiệm vụ nào ở mục này",
                emptySlots: "Chưa có lịch nào trong ngày này",
                unitMin: "phút",
                unitHr: "giờ",
                vnGroup: "🇻🇳 Sân bay Việt Nam (22)",
                intGroup: "🌏 Sân bay Quốc tế (12)",
                flyBtnShort: "🛫 Bay"
            },
            en: {
                saveReady: "● Auto-Save Ready",
                memberTop: "Member",
                tabDash: "📊 Study Dashboard",
                tabFlight: "✈️ 3D / 2D Flight Sim",
                bannerTag: "Flight Alert from Personal Schedule",
                bannerBtn: "🛫 Takeoff & Study Now",
                kpi1Title: "Active Profile",
                kpi1Sub: "Auto-Sync Schedule ➔ Flight",
                kpi2Title: "Pending Tasks & Flights",
                kpi2Sub: "Ready for takeoff",
                kpi3Title: "Completed (✓)",
                kpi4Title: "Total Flight Miles",
                aiBadge: "💡 What to study today? (AI Recommended)",
                aiSub: "Automatic flight alarm synced with your schedule",
                remindBtn: "🔔 Check Flight Alarm",
                smartCtrlTitle: "⚡ Smart AI Schedule Dispatcher",
                smartCtrlDesc: "Automatically prioritize tasks by deadline or reschedule sessions when unexpected events happen.",
                btnAiSort: "🤖 AI Sort by Priority",
                btnSudden: "🌪️ Unexpected Event (Auto-Reschedule)",
                todoHeader: "✅ Task List & Flight Routes",
                todoSyncTag: "⚡ Auto-Synced from Calendar",
                todoSub: "Adding a schedule on the right automatically creates a flight task here!",
                filterAll: "All",
                filterPending: "Pending",
                filterDone: "Done ✓",
                quickAddTitle: "+ Quick add standalone task / deadline:",
                quickTaskPlh: "Enter task name (e.g. Math, Build App...)",
                quickDeadline: "Due (Hrs):",
                btnSaveTask: "+ Save Task",
                calHeader: "🗓️ Monthly Calendar & Personal Events",
                calSub: "Click any date on the calendar grid to view Day of Week, Solar & Lunar Date",
                lunarOn: "🌙 Lunar: ON",
                lunarOff: "🌙 Lunar: OFF",
                btnToday: "Today",
                weekdays: ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
                fullWeekdays: ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"],
                monthPrefix: "MONTH",
                pickDate: "Pick Date:",
                startTime: "⏰ Start:",
                endTime: "🏁 End:",
                catType: "Category",
                catStudy: "📚 Study / Review (Auto-create Flight)",
                catSchool: "🔴 School Class (Fixed Schedule)",
                catPers: "🟣 Personal Event (Work, Club...)",
                catFree: "🟢 Free Time Slot",
                repeatCycle: "Recurrence Cycle (Custom)",
                rpNone: "1️⃣ Does not repeat (This date only)",
                rpWeekly: "🔄 Weekly (Same day every week)",
                rpMonthly: "🗓️ Monthly (Same date every month)",
                rpYearly: "📆 Yearly (Same date every year)",
                rpDaily: "☀️ Daily (Every day)",
                rpCustom: "⚙️ Custom recurrence...",
                customEvery: "⚙️ Repeat every:",
                uDay: "Day(s)", uWeek: "Week(s)", uMonth: "Month(s)", uYear: "Year(s)",
                customFor: "For:",
                slotSubjPlh: "Enter subject, shift, or event (e.g. Math, Part-time...)...",
                btnAddSlot: "+ Add Event",
                autoSyncCheck: "⚡ Auto-push to Task List & Flight Alarm on the left",
                originTitle: "DEPARTURE AIRPORT",
                destTitle: "DESTINATION AIRPORT",
                autoDurTitle: "⏱️ FOCUS TIME (CALCULATED BY DISTANCE)",
                etaTitle: "Est. Arrival (ETA)",
                btnPickSeat: "💺 Select Seat & Ticket",
                btnFlyNow: "🛫 FLY IMMEDIATELY",
                btnCollapse: "🔽 Hide Panel",
                btnExpand: "🔼 Show Booking Panel",
                btnMap2D: "🛰️ 2D Map",
                btnGlobe3D: "🌍 3D Globe",
                btnSeatBack: "‹ Back",
                popFocusQ: "What do you want to focus on during this flight?",
                popFocusPlh: "Enter focus goal (e.g. Math, Coding...)",
                strictDesc: "Red alert if leaving the study screen",
                btnConfirmSeat: "Confirm Seat & Get Boarding Pass ➔",
                seatHint: "Tap any seat or click Continue",
                btnContinue: "Continue ➔",
                btnChangeSeat: "‹ Change Seat",
                btnTakeoff: "🛫 Takeoff & Start Studying",
                btnFlyDone: "✓ Done",
                btnFlyAbort: "Abort",
                btnReadLight: "💡 Reading Light",
                btnTrayTable: "🍱 Tray Table",
                btnCabinLed: "🌈 Cabin LED",
                btnCallCrew: "🛎️ Call Crew",
                cabinGoal: "Current Focus Goal",
                cabinRem: "Time Remaining",
                trayTitle: "In-Flight Personal Study Desk",
                traySub: "Tray Open • Maximum Focus Mode",
                btnWinShade: "🪟 Toggle Window Shade Up / Down",
                botHeader: "AI Study Assistant",
                chatLauncher: "💬 Chat AI",
                q1: "💡 What to study today?",
                q2: "📋 Pending tasks",
                q3: "🌪️ Reschedule",
                chatPlh: "Type a message...",
                emptyTasks: "No tasks in this view yet",
                emptySlots: "No events scheduled for this date",
                unitMin: "mins",
                unitHr: "hrs",
                vnGroup: "🇻🇳 Vietnam Airports (22)",
                intGroup: "🌏 International Airports (12)",
                flyBtnShort: "🛫 Fly"
            },
            zh: {
                saveReady: "● 自動儲存就緒",
                memberTop: "小組成員",
                tabDash: "📊 學習與日程儀表板",
                tabFlight: "✈️ 3D / 2D 專注飛行艙",
                bannerTag: "來自個人行事曆的航班提醒",
                bannerBtn: "🛫 立即起飛專注學習",
                kpi1Title: "當前成員檔案",
                kpi1Sub: "行事曆 ➔ 航班自動同步",
                kpi2Title: "待辦任務與航班",
                kpi2Sub: "準備起飛",
                kpi3Title: "已完成任務 (✓)",
                kpi4Title: "累計飛行里程",
                aiBadge: "💡 今天該學什麼？（AI 智慧推薦）",
                aiSub: "根據您設定的時段自動提醒航班起飛時間",
                remindBtn: "🔔 檢查航班鬧鐘",
                smartCtrlTitle: "⚡ AI 智慧排程調度中心",
                smartCtrlDesc: "根據截止時間自動排序優先級，或在遇到突發狀況時自動順延學習時段。",
                btnAiSort: "🤖 AI 智慧優先級排序",
                btnSudden: "🌪️ 突發行程（自動順延時段）",
                todoHeader: "✅ 任務清單與飛行航線",
                todoSyncTag: "⚡ 與右側行事曆自動同步",
                todoSub: "在右側行事曆新增課程或個人事項，將自動同步至此並設定航班時間！",
                filterAll: "全部",
                filterPending: "進行中",
                filterDone: "已完成 ✓",
                quickAddTitle: "+ 快速新增單獨作業 / 截止期限：",
                quickTaskPlh: "輸入任務名稱（如：微積分、寫程式...）",
                quickDeadline: "期限(小時):",
                btnSaveTask: "+ 儲存任務",
                calHeader: "🗓️ 萬年曆與個人行程表",
                calSub: "直接點擊月曆上的日期，即可查看星期、國曆與農曆日期",
                lunarOn: "🌙 農曆：開啟",
                lunarOff: "🌙 農曆：關閉",
                btnToday: "今天",
                weekdays: ["週一", "週二", "週三", "週四", "週五", "週六", "週日"],
                fullWeekdays: ["星期日", "星期一", "星期二", "星期三", "星期四", "星期五", "星期六"],
                monthPrefix: "月份",
                pickDate: "選擇日期:",
                startTime: "⏰ 開始時間:",
                endTime: "🏁 結束時間:",
                catType: "行程類別",
                catStudy: "📚 學習 / 溫習（自動建立專注航班）",
                catSchool: "🔴 學校固定課表",
                catPers: "🟣 個人事項（打工、社團活動...）",
                catFree: "🟢 空閒自習時段",
                repeatCycle: "重複週期（自由設定）",
                rpNone: "1️⃣ 不重複（僅限此日）",
                rpWeekly: "🔄 每週重複（每週同一天）",
                rpMonthly: "🗓️ 每月重複（每月同日）",
                rpYearly: "📆 每年重複（每年同月同日）",
                rpDaily: "☀️ 每天重複",
                rpCustom: "⚙️ 自訂重複週期...",
                customEvery: "⚙️ 每隔：",
                uDay: "天", uWeek: "週", uMonth: "個月", uYear: "年",
                customFor: "持續：",
                slotSubjPlh: "輸入課程、打工或活動名稱（如：數學、打工...）",
                btnAddSlot: "+ 新增行程",
                autoSyncCheck: "⚡ 自動同步至左側任務清單並設定專注航班鬧鐘",
                originTitle: "出發機場",
                destTitle: "目的地機場",
                autoDurTitle: "⏱️ 專注學習時間（依航程距離自動計算）",
                etaTitle: "預計抵達時間 (ETA)",
                btnPickSeat: "💺 選擇座位與登機證",
                btnFlyNow: "🛫 立即起飛專注",
                btnCollapse: "🔽 收起面板",
                btnExpand: "🔼 展開訂票面板",
                btnMap2D: "🛰️ 2D 地圖",
                btnGlobe3D: "🌍 3D 地球",
                btnSeatBack: "‹ 返回",
                popFocusQ: "這趟飛行您想專注做什麼？",
                popFocusPlh: "輸入專注目標（如：微積分、專題...）",
                strictDesc: "若離開學習畫面將觸發紅色警報",
                btnConfirmSeat: "確認座位並取得登機證 ➔",
                seatHint: "點擊任一座位或按繼續",
                btnContinue: "繼續 ➔",
                btnChangeSeat: "‹ 更換座位",
                btnTakeoff: "🛫 起飛開始專注學習",
                btnFlyDone: "✓ 提早完成",
                btnFlyAbort: "取消飛行",
                btnReadLight: "💡 閱讀燈",
                btnTrayTable: "🍱 摺疊書桌",
                btnCabinLed: "🌈 客艙氛圍燈",
                btnCallCrew: "🛎️ 呼叫空服員",
                cabinGoal: "當前專注目標",
                cabinRem: "剩餘飛行時間",
                trayTitle: "機上個人專屬書桌",
                traySub: "書桌已展開 • 極致專注模式",
                btnWinShade: "🪟 拉起 / 放下機窗遮陽板",
                botHeader: "AI 智慧學習助理",
                chatLauncher: "💬 AI 助理",
                q1: "💡 今天該學什麼？",
                q2: "📋 查看待辦事項",
                q3: "🌪️ 突發狀況順延",
                chatPlh: "輸入訊息...",
                emptyTasks: "目前尚無任何待辦任務",
                emptySlots: "此日期尚無安排任何行程",
                unitMin: "分鐘",
                unitHr: "小時",
                vnGroup: "🇻🇳 越南國內機場 (22)",
                intGroup: "🌏 國際航線機場 (12)",
                flyBtnShort: "🛫 起飛"
            }
        };

        // ================= 2. DỮ LIỆU 34 SÂN BAY ĐA NGÔN NGỮ (VI / EN / 繁體) =================
        const AIRPORTS = [
            { code: "SGN", name: "TP.HCM (Tân Sơn Nhất)", name_en: "Ho Chi Minh City (Tan Son Nhat)", name_zh: "胡志明市 (新山一)", group: "VN", coords: [10.8188, 106.6519] },
            { code: "HAN", name: "Hà Nội (Nội Bài)", name_en: "Hanoi (Noi Bai)", name_zh: "河內 (內排)", group: "VN", coords: [21.2212, 105.8072] },
            { code: "DAD", name: "Đà Nẵng", name_en: "Da Nang", name_zh: "峴港", group: "VN", coords: [16.0439, 108.1994] },
            { code: "CXR", name: "Cam Ranh (Khánh Hòa)", name_en: "Cam Ranh (Nha Trang)", name_zh: "金蘭 (芽莊)", group: "VN", coords: [11.9982, 109.2194] },
            { code: "UIH", name: "Phù Cát (Quy Nhơn)", name_en: "Phu Cat (Quy Nhon)", name_zh: "符吉 (歸仁)", group: "VN", coords: [13.9550, 109.0422] },
            { code: "LTH", name: "Long Thành (Đồng Nai)", name_en: "Long Thanh (Dong Nai)", name_zh: "隆城 (同奈)", group: "VN", coords: [10.7850, 107.0650] },
            { code: "PQC", name: "Phú Quốc (Kiên Giang)", name_en: "Phu Quoc Island", name_zh: "富國島", group: "VN", coords: [10.1698, 103.9931] },
            { code: "DLI", name: "Đà Lạt (Liên Khương)", name_en: "Da Lat (Lien Khuong)", name_zh: "大叻 (聯姜)", group: "VN", coords: [11.7500, 108.3667] },
            { code: "HPH", name: "Hải Phòng (Cát Bi)", name_en: "Hai Phong (Cat Bi)", name_zh: "海防 (吉碑)", group: "VN", coords: [20.8194, 106.7250] },
            { code: "VII", name: "Vinh (Nghệ An)", name_en: "Vinh (Nghe An)", name_zh: "榮市 (乂安)", group: "VN", coords: [18.7376, 105.6708] },
            { code: "HUI", name: "Huế (Phú Bài)", name_en: "Hue (Phu Bai)", name_zh: "順化 (富牌)", group: "VN", coords: [16.4015, 107.7026] },
            { code: "VCA", name: "Cần Thơ", name_en: "Can Tho", name_zh: "芹苴", group: "VN", coords: [10.0851, 105.7119] },
            { code: "VDH", name: "Đồng Hới (Quảng Bình)", name_en: "Dong Hoi (Quang Binh)", name_zh: "洞海 (廣平)", group: "VN", coords: [17.5150, 106.5905] },
            { code: "THD", name: "Thanh Hóa (Thọ Xuân)", name_en: "Thanh Hoa (Tho Xuan)", name_zh: "清化 (壽春)", group: "VN", coords: [19.9017, 105.4678] },
            { code: "VDO", name: "Vân Đồn (Quảng Ninh)", name_en: "Van Don (Ha Long)", name_zh: "雲屯 (廣寧)", group: "VN", coords: [21.1178, 107.4142] },
            { code: "VCL", name: "Chu Lai (Quảng Nam)", name_en: "Chu Lai (Quang Nam)", name_zh: "茱萊 (廣南)", group: "VN", coords: [15.4061, 108.7056] },
            { code: "TBB", name: "Tuy Hòa (Phú Yên)", name_en: "Tuy Hoa (Phu Yen)", name_zh: "綏和 (富安)", group: "VN", coords: [13.0494, 109.3336] },
            { code: "BMV", name: "Buôn Ma Thuột (Đắk Lắk)", name_en: "Buon Ma Thuot", name_zh: "邦美蜀", group: "VN", coords: [12.6683, 108.1200] },
            { code: "PXU", name: "Pleiku (Gia Lai)", name_en: "Pleiku (Gia Lai)", name_zh: "波來古 (嘉萊)", group: "VN", coords: [14.0045, 108.0172] },
            { code: "VCS", name: "Côn Đảo (Bà Rịa - VT)", name_en: "Con Dao Island", name_zh: "崑崙島", group: "VN", coords: [8.7325, 106.6336] },
            { code: "DIN", name: "Điện Biên Phủ", name_en: "Dien Bien Phu", name_zh: "奠邊府", group: "VN", coords: [21.3975, 103.0078] },
            { code: "CAH", name: "Cà Mau", name_en: "Ca Mau", name_zh: "金甌", group: "VN", coords: [9.1756, 105.1794] },
            // 12 Sân bay Quốc tế
            { code: "TPE", name: "Đài Bắc - Đào Viên (Đài Loan)", name_en: "Taipei Taoyuan (Taiwan)", name_zh: "臺北桃園 (臺灣)", group: "INT", coords: [25.0797, 121.2342] },
            { code: "BKK", name: "Bangkok (Thái Lan)", name_en: "Bangkok Suvarnabhumi (Thailand)", name_zh: "曼谷 (泰國)", group: "INT", coords: [13.6900, 100.7501] },
            { code: "SIN", name: "Singapore (Changi)", name_en: "Singapore Changi", name_zh: "新加坡 (樟宜)", group: "INT", coords: [1.3644, 103.9915] },
            { code: "KUL", name: "Kuala Lumpur (Malaysia)", name_en: "Kuala Lumpur (Malaysia)", name_zh: "吉隆坡 (馬來西亞)", group: "INT", coords: [2.7456, 101.7072] },
            { code: "HKG", name: "Hong Kong", name_en: "Hong Kong Int'l", name_zh: "香港國際機場", group: "INT", coords: [22.3080, 113.9185] },
            { code: "ICN", name: "Seoul Incheon (Hàn Quốc)", name_en: "Seoul Incheon (Korea)", name_zh: "首爾仁川 (韓國)", group: "INT", coords: [37.4602, 126.4407] },
            { code: "HND", name: "Tokyo Haneda (Nhật Bản)", name_en: "Tokyo Haneda (Japan)", name_zh: "東京羽田 (日本)", group: "INT", coords: [35.5494, 139.7798] },
            { code: "MNL", name: "Manila (Philippines)", name_en: "Manila (Philippines)", name_zh: "馬尼拉 (菲律賓)", group: "INT", coords: [14.5086, 121.0194] },
            { code: "PEK", name: "Bắc Kinh (Trung Quốc)", name_en: "Beijing Capital (China)", name_zh: "北京首都", group: "INT", coords: [40.0799, 116.6031] },
            { code: "SYD", name: "Sydney (Úc)", name_en: "Sydney Kingsford (Australia)", name_zh: "雪梨 (澳洲)", group: "INT", coords: [-33.9399, 151.1753] },
            { code: "CDG", name: "Paris (Pháp)", name_en: "Paris Charles de Gaulle (France)", name_zh: "巴黎戴高樂 (法國)", group: "INT", coords: [49.0097, 2.5479] },
            { code: "JFK", name: "New York (Mỹ)", name_en: "New York JFK (USA)", name_zh: "紐約甘迺迪 (美國)", group: "INT", coords: [40.6413, -73.7781] }
        ];

        function getAirportLocalName(airport) {
            if (!airport) return "";
            if (currentLang === 'en') return airport.name_en || airport.name;
            if (currentLang === 'zh') return airport.name_zh || airport.name;
            return airport.name;
        }

        const FOCUS_MODES = [
            { id: "focus", label: "Focus", icon: "⚛️", color: "bg-slate-600/90 border-slate-400 text-white" },
            { id: "work", label: "Work", icon: "💻", color: "bg-blue-600 border-blue-300 text-white" },
            { id: "meditate", label: "Meditate", icon: "🧘", color: "bg-indigo-500 border-indigo-300 text-white" },
            { id: "read", label: "Read", icon: "📖", color: "bg-teal-600 border-teal-300 text-white" },
            { id: "exercise", label: "Exercise", icon: "🏃", color: "bg-sky-500 border-sky-300 text-white" }
        ];

        let currentTaskFilter = "all";
        let activeTaskIdForFlight = null;

        let originAirport = AIRPORTS[0]; // SGN
        let destAirport = AIRPORTS[2];   // DAD
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

        function setAppLanguage(lang) {
            currentLang = lang;
            ['vi', 'en', 'zh'].forEach(l => {
                const btn = document.getElementById('lang-btn-' + l);
                if (btn) {
                    btn.className = (l === lang)
                        ? "px-2.5 py-1 rounded-lg bg-amber-400 text-black transition"
                        : "px-2.5 py-1 rounded-lg text-slate-300 hover:text-white transition";
                }
            });

            const t = I18N[lang];
            setTxt('save-status-indicator', t.saveReady);
            setTxt('lbl-member-top', t.memberTop);
            setTxt('lbl-tab-dashboard', t.tabDash);
            setTxt('lbl-tab-flight', t.tabFlight);
            setTxt('lbl-banner-tag', t.bannerTag);
            setTxt('lbl-banner-btn', t.bannerBtn);
            setTxt('lbl-kpi-1-title', t.kpi1Title);
            setTxt('lbl-kpi-1-sub', t.kpi1Sub);
            setTxt('lbl-kpi-2-title', t.kpi2Title);
            setTxt('lbl-kpi-2-sub', t.kpi2Sub);
            setTxt('lbl-kpi-3-title', t.kpi3Title);
            setTxt('lbl-kpi-4-title', t.kpi4Title);
            setTxt('lbl-ai-badge', t.aiBadge);
            setTxt('lbl-ai-sub', t.aiSub);
            setTxt('lbl-remind-btn', t.remindBtn);
            setTxt('lbl-smart-ctrl-title', t.smartCtrlTitle);
            setTxt('lbl-smart-ctrl-desc', t.smartCtrlDesc);
            setTxt('lbl-btn-aisort', t.btnAiSort);
            setTxt('lbl-btn-sudden', t.btnSudden);
            setTxt('lbl-todo-header', t.todoHeader);
            setTxt('lbl-todo-sync-tag', t.todoSyncTag);
            setTxt('lbl-todo-sub', t.todoSub);
            setTxt('filter-all', t.filterAll);
            setTxt('filter-pending', t.filterPending);
            setTxt('filter-done', t.filterDone);
            setTxt('lbl-quick-add-title', t.quickAddTitle);
            setPlh('quick-task-title', t.quickTaskPlh);
            setTxt('lbl-quick-deadline', t.quickDeadline);
            setTxt('lbl-btn-save-task', t.btnSaveTask);
            setTxt('lbl-cal-header', t.calHeader);
            setTxt('lbl-cal-sub', t.calSub);
            setTxt('btn-toggle-lunar', showLunarCalendar ? t.lunarOn : t.lunarOff);
            setTxt('lbl-btn-today', t.btnToday);
            setTxt('lbl-pick-date', t.pickDate);
            setTxt('lbl-start-time', t.startTime);
            setTxt('lbl-end-time', t.endTime);
            setTxt('lbl-cat-type', t.catType);
            setTxt('opt-cat-study', t.catStudy);
            setTxt('opt-cat-school', t.catSchool);
            setTxt('opt-cat-personal', t.catPers);
            setTxt('opt-cat-free', t.catFree);
            setTxt('lbl-repeat-cycle', t.repeatCycle);
            setTxt('opt-rp-none', t.rpNone);
            setTxt('opt-rp-weekly', t.rpWeekly);
            setTxt('opt-rp-monthly', t.rpMonthly);
            setTxt('opt-rp-yearly', t.rpYearly);
            setTxt('opt-rp-daily', t.rpDaily);
            setTxt('opt-rp-custom', t.rpCustom);
            setTxt('lbl-custom-every', t.customEvery);
            setTxt('opt-u-day', t.uDay);
            setTxt('opt-u-week', t.uWeek);
            setTxt('opt-u-month', t.uMonth);
            setTxt('opt-u-year', t.uYear);
            setTxt('lbl-custom-for', t.customFor);
            setPlh('new-slot-subject', t.slotSubjPlh);
            setTxt('lbl-btn-add-slot', t.btnAddSlot);
            setTxt('lbl-autosync-check', t.autoSyncCheck);

            // Dịch toàn bộ Trạm Bay, Vé & Cabin
            setTxt('lbl-origin-title', t.originTitle);
            setTxt('lbl-dest-title', t.destTitle);
            setTxt('lbl-auto-dur-title', t.autoDurTitle);
            setTxt('lbl-eta-title', t.etaTitle);
            setTxt('lbl-btn-pick-seat', t.btnPickSeat);
            setTxt('lbl-btn-fly-now', t.btnFlyNow);
            setTxt('toggle-booking-btn', isBookingCollapsed ? t.btnExpand : t.btnCollapse);
            setTxt('quick-switch-proj-btn', is2DMapActive ? t.btnGlobe3D : t.btnMap2D);
            setTxt('btn-seat-back', t.btnSeatBack);
            setTxt('lbl-pop-focus-q', t.popFocusQ);
            setPlh('custom-focus-input', t.popFocusPlh);
            setTxt('lbl-strict-desc', t.strictDesc);
            setTxt('btn-confirm-seat', t.btnConfirmSeat);
            setTxt('lbl-seat-hint', t.seatHint);
            setTxt('btn-seat-continue', t.btnContinue);
            setTxt('btn-tk-change-seat', t.btnChangeSeat);
            setTxt('btn-tk-takeoff', t.btnTakeoff);
            setTxt('btn-fly-done', t.btnFlyDone);
            setTxt('btn-fly-abort', t.btnFlyAbort);
            setTxt('btn-reading-light', t.btnReadLight);
            setTxt('btn-tray-table', t.btnTrayTable);
            setTxt('btn-cabin-led', t.btnCabinLed);
            setTxt('btn-call-crew', t.btnCallCrew);
            setTxt('lbl-cabin-goal', t.cabinGoal);
            setTxt('lbl-cabin-rem', t.cabinRem);
            setTxt('lbl-tray-title', t.trayTitle);
            setTxt('lbl-tray-sub', t.traySub);
            setTxt('btn-window-shade', t.btnWinShade);

            // Chatbot
            setTxt('lbl-bot-header', t.botHeader);
            setTxt('lbl-chat-launcher', t.chatLauncher);
            setTxt('btn-q1', t.q1);
            setTxt('btn-q2', t.q2);
            setTxt('btn-q3', t.q3);
            setPlh('chat-input', t.chatPlh);

            const wkRow = document.getElementById('calendar-weekdays-row');
            if (wkRow) wkRow.innerHTML = t.weekdays.map((w, idx) => `<div class="${idx === 6 ? 'text-red-400' : ''}">${w}</div>`).join('');

            initAirportDropdowns();
            updateBookingUI();
            renderCalendarGrid();
            renderDashboard();
            resetChat();
        }

        // ================= 3. THUẬT TOÁN TÍNH LỊCH VẠN NIÊN & ÂM LỊCH =================
        const CAN_VI = ["Giáp", "Ất", "Bính", "Đinh", "Mậu", "Kỷ", "Canh", "Tân", "Nhâm", "Quý"];
        const CHI_VI = ["Tý", "Sửu", "Dần", "Mão", "Thìn", "Tỵ", "Ngọ", "Mùi", "Thân", "Dậu", "Tuất", "Hợi"];
        const CAN_ZH = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"];
        const CHI_ZH = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"];

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

        let calViewYear = 2026;
        let calViewMonth = 11;
        let selectedFullDate = "2026-11-04";

        function toggleLunarDisplay() {
            showLunarCalendar = !showLunarCalendar;
            const t = I18N[currentLang];
            setTxt('btn-toggle-lunar', showLunarCalendar ? t.lunarOn : t.lunarOff);
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
                const unit = ev.customUnit || 'week';
                const diffDays = Math.round((tgDate - evDate) / 86400000);
                if (unit === 'day' || unit === 'ngày') return (diffDays % interval === 0);
                if (unit === 'week' || unit === 'tuần') return (diffDays % (interval * 7) === 0);
                if (unit === 'month' || unit === 'tháng') {
                    const monthDiff = (ty - ey) * 12 + (tm - em);
                    return (ed === td && monthDiff >= 0 && monthDiff % interval === 0);
                }
                if (unit === 'year' || unit === 'năm') {
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
            setTxt('calendar-header-title', `${t.monthPrefix} ${String(calViewMonth).padStart(2,'0')} - ${calViewYear}`);

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

        // ================= 4. QUẢ ĐỊA CẦU 3D & BẢN ĐỒ VỆ TINH 2D =================
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
            const canvas = document.getElementById('globe-canvas');
            scene = new THREE.Scene();
            const w = window.innerWidth || 1200, h = (window.innerHeight - 56) || 700;
            camera = new THREE.PerspectiveCamera(45, w / h, 1, 2000);
            camera.position.z = globeCameraZ;

            renderer = new THREE.WebGLRenderer({ canvas: canvas, antialias: true, alpha: true });
            renderer.setSize(w, h);
            renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));

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
                const nw = window.innerWidth, nh = window.innerHeight - 56;
                camera.aspect = nw / nh; camera.updateProjectionMatrix();
                renderer.setSize(nw, nh); map.invalidateSize(true);
            });

            animateThreeGlobe();
        }

        function update3DGlobeRouteArc() {
            if (!earthGroup) return;
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

            setTxt('globe-origin-code', originAirport.code);
            setTxt('globe-dest-code', destAirport.code);
            document.getElementById('globe-plane-svg').innerHTML = getAircraftSVG(selectedAircraft, calcBearingDeg(originAirport.coords, destAirport.coords));
        }

        function update3DPinOverlay(elId, lat, lng, lift = 1.02) {
            const el = document.getElementById(elId);
            if (!el || is2DMapActive || currentCamView !== 'map') { if (el) el.classList.add('hidden'); return; }
            const worldVec = latLngToVec3(lat, lng, GLOBE_RADIUS * lift).applyMatrix4(earthGroup.matrixWorld);
            if (camera.position.clone().normalize().dot(worldVec.clone().normalize()) < 0.15) { el.classList.add('hidden'); return; }
            const projected = worldVec.clone().project(camera);
            el.style.left = `${(projected.x * 0.5 + 0.5) * window.innerWidth}px`;
            el.style.top = `${(-(projected.y * 0.5) + 0.5) * (window.innerHeight - 56) + 56}px`;
            el.classList.remove('hidden');
        }

        function animateThreeGlobe() {
            requestAnimationFrame(animateThreeGlobe);
            if (!earthGroup || !renderer) return;
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

        const map = L.map('map', { zoomControl: false, minZoom: 3, maxZoom: 18, zoomSnap: 0.5, zoomDelta: 0.5, wheelPxPerZoomLevel: 120 }).setView([13.5, 107.5], 6);
        L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}', { maxZoom: 18 }).addTo(map);
        L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/Reference/World_Boundaries_and_Places/MapServer/tile/{z}/{y}/{x}', { maxZoom: 18 }).addTo(map);

        map.getContainer().addEventListener('wheel', (e) => {
            if (is2DMapActive && e.deltaY > 0 && map.getZoom() <= 4 && (Date.now() - lastTransitionTime > 650)) activate3DSpaceGlobe();
        }, { passive: true });

        let routeLine = null, originMarker = null, destMarker = null, planeMarker = null;

        function activate2DSatelliteMap() {
            lastTransitionTime = Date.now(); is2DMapActive = true;
            document.getElementById('globe-wrapper').classList.add('globe-hidden');
            document.getElementById('map-2d-wrapper').classList.add('active-2d');
            setTxt('projection-mode-badge', "2D");
            setTxt('quick-switch-proj-btn', I18N[currentLang].btnGlobe3D);
            const refresh2DMap = () => {
                map.invalidateSize(true);
                if (isFlying && planeMarker) map.setView(planeMarker.getLatLng(), 7, { animate: false });
                else if (routeLine) map.fitBounds(routeLine.getBounds(), { padding: [90, 90], maxZoom: 7, animate: false });
            };
            refresh2DMap(); setTimeout(refresh2DMap, 100);
        }

        function activate3DSpaceGlobe() {
            lastTransitionTime = Date.now(); is2DMapActive = false; targetGlobeZ = 245; globeCameraZ = 190;
            document.getElementById('map-2d-wrapper').classList.remove('active-2d');
            document.getElementById('globe-wrapper').classList.remove('globe-hidden');
            setTxt('projection-mode-badge', "3D");
            setTxt('quick-switch-proj-btn', I18N[currentLang].btnMap2D);
        }

        function toggleProjectionMode() { if (is2DMapActive) activate3DSpaceGlobe(); else activate2DSatelliteMap(); }
        function zoomStepIn() { if (!is2DMapActive) { targetGlobeZ -= 30; if (targetGlobeZ <= 168) activate2DSatelliteMap(); } else map.zoomIn(1); }
        function zoomStepOut() { if (is2DMapActive) { if (map.getZoom() <= 4.5) activate3DSpaceGlobe(); else map.zoomOut(1); } else targetGlobeZ = Math.min(430, targetGlobeZ + 30); }

        // ================= 5. TÍNH GIỜ BAY & MÔ HÌNH MÁY BAY =================
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
            const t = I18N[currentLang];
            if (mins < 60) return `${mins} ${t.unitMin}`;
            const h = Math.floor(mins / 60), m = mins % 60;
            return m > 0 ? `${h}h ${m}m (${mins} ${t.unitMin})` : `${h} ${t.unitHr} (${mins} ${t.unitMin})`;
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

            setTxt('realtime-clock', `${hh}:${mm}:${ss}`);
            setTxt('realtime-date', dateStr);
            setTxt('cockpit-real-clock', `${hh}:${mm}:${ss}`);
            setTxt('cabin-real-clock', `${hh}:${mm}:${ss}`);

            if (!isFlying) {
                setTxt('booking-realtime-eta', `${hh}:${mm} ➔ ${calcRealTimeETA(selectedDuration)}`);
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

        // ================= 6. LƯU TRỮ DỮ LIỆU VĨNH VIỄN CHO 6 THÀNH VIÊN =================
        const INITIAL_CLEAN_DB = {
            lastMember: "huudai",
            members: {
                huudai:    { name: "Hữu Đại",    seat: "06A", miles: 0, flights: 0, tasks: [], calendarEvents: [] },
                quangminh: { name: "Quang Minh", seat: "06A", miles: 0, flights: 0, tasks: [], calendarEvents: [] },
                khanhthi:  { name: "Khánh Thi",  seat: "04F", miles: 0, flights: 0, tasks: [], calendarEvents: [] },
                minhchau:  { name: "Minh Châu",  seat: "05A", miles: 0, flights: 0, tasks: [], calendarEvents: [] },
                uyennhi:   { name: "Uyên Nhi",   seat: "03C", miles: 0, flights: 0, tasks: [], calendarEvents: [] },
                vanhoang:  { name: "Văn Hoàng",  seat: "07F", miles: 0, flights: 0, tasks: [], calendarEvents: [] }
            }
        };

        const STORAGE_KEY = "studyhub_focus_flight_clean_v4";
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
                setTxt('save-status-indicator', `${I18N[currentLang].saveReady} (${getCurrentTimeStr()})`);
            } catch (e) {}
        }

        loadPersistentState();
        let currentMemberKey = appState.lastMember || "huudai";

        // ================= 7. CHUYỂN ĐỔI GÓC NHÌN & LỊCH VẠN NIÊN =================
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
            if (view === 'map' && is2DMapActive) setTimeout(() => map.invalidateSize(true), 60);
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
            mapEl.className = "";
            if (mode === 'night') mapEl.classList.add('map-night-filter');
            if (mode === 'sunset') mapEl.classList.add('map-sunset-filter');
            if (mode === 'rain') mapEl.classList.add('map-rain-filter');

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
            document.getElementById('btn-reading-light').className = isReadingLightOn
                ? "bg-yellow-400 text-black px-2.5 py-1 rounded-xl text-[11px] font-extrabold shadow"
                : "bg-slate-800 hover:bg-slate-700 border border-white/15 px-2.5 py-1 rounded-xl text-[11px] font-bold text-slate-200 transition";
        }

        function toggleTrayTable() {
            isTrayTableOpen = !isTrayTableOpen;
            document.getElementById('cabin-tray-table-open').classList.toggle('hidden', !isTrayTableOpen);
        }

        function callFlightAttendant() {
            playCabinDingDong();
            const profile = appState.members[currentMemberKey];
            if (currentLang === 'en') alert(`🛎️ Cabin Crew: Wishing passenger ${profile.name} (Seat ${selectedSeat}) a productive study flight!`);
            else if (currentLang === 'zh') alert(`🛎️ 座艙長廣播：祝旅客 ${profile.name}（座位 ${selectedSeat}）有個高效專注的學習飛行！`);
            else alert(`🛎️ Tiếp viên trưởng: Chúc hành khách ${profile.name} (Ghế ${selectedSeat}) có một chuyến bay học tập thật hiệu quả!`);
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

            setTxt('hud-speed', `${specs.speedKmh} KM/H`);
            setTxt('hud-heading', `${brng}°`);
            setTxt('hud-alt', specs.altFt);
            setTxt('hud-aircraft-name', selectedAircraft.toUpperCase());
            setTxt('hud-route-code', `${originAirport.code} ➔ ${destAirport.code}`);
            document.getElementById('cockpit-plane-svg-preview').innerHTML = getAircraftSVG(selectedAircraft, 0);
            setTxt('cockpit-task-display', `${selectedFocus.icon} ${selectedFocus.label}`);

            setTxt('cabin-seat-label', selectedSeat);
            setTxt('cabin-window-seat-tag', selectedSeat);
            setTxt('cabin-aircraft-label', selectedAircraft);
            setTxt('cabin-route-label', `${originAirport.code} ➔ ${destAirport.code}`);
            setTxt('cabin-task-title', `${selectedFocus.icon} ${selectedFocus.label}`);
            setTxt('cabin-passenger-name', profile.name);
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
                setTimeout(() => { map.invalidateSize(true); updateBookingUI(); }, 80);
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

        // ================= 8. QUẢN LÝ NHIỆM VỤ & LỊCH VẠN NIÊN CÓ CHU KỲ TÙY CHỌN =================
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
            const customUnit = document.getElementById('custom-repeat-unit').value || "week";
            const customDur = document.getElementById('custom-repeat-duration').value || "3";
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
            if (repeatMode === 'daily') repeatLabel = t.rpDaily;
            else if (repeatMode === 'weekly') repeatLabel = `${t.rpWeekly} (${dowName})`;
            else if (repeatMode === 'monthly') repeatLabel = `${t.rpMonthly} (${String(d).padStart(2,'0')})`;
            else if (repeatMode === 'yearly') repeatLabel = `${t.rpYearly} (${String(d).padStart(2,'0')}/${String(m).padStart(2,'0')})`;
            else if (repeatMode === 'custom') repeatLabel = `${customInterval} ${customUnit} (${customDur})`;

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
                const iconPrefix = type === 'personal' ? '💼' : (type === 'school' ? '🏫' : '📚');
                profile.tasks.unshift({
                    id: slotId + 1,
                    linkedSlotId: slotId,
                    title: `${iconPrefix} ${subject} (${dowName}, ${formattedDate})`,
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

            setTxt('stat-member-name', profile.name);
            setTxt('stat-pending-count', pendingTasks.length);
            setTxt('stat-done-count', doneTasks.length);
            setTxt('nav-pending-badge', pendingTasks.length);
            const pct = allTasks.length > 0 ? Math.round((doneTasks.length / allTasks.length) * 100) : 0;
            setTxt('stat-done-percent', `${pct}% (${doneTasks.length}/${allTasks.length})`);
            setTxt('stat-miles-count', `${profile.miles || 0} km`);
            setTxt('stat-flights-count', `${profile.flights || 0}`);
            setTxt('timetable-owner-badge', `(${profile.name})`);

            const banner = document.getElementById('deadline-banner');
            if (pendingTasks.length > 0) {
                const top = pendingTasks[0];
                banner.classList.remove('hidden'); banner.classList.add('flex');
                setTxt('deadline-banner-text', `✈️ ${profile.name}: "${top.title}" • ⏰ ${top.slot} (SGN ➔ ${top.destCode || 'DAD'} • ${top.duration} ${t.unitMin})`);
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
                                ${t.flyBtnShort} (${top.duration}m)
                            </button>
                            <button onclick="openWhyModal(${top.id})" class="bg-white/10 hover:bg-white/20 text-white font-bold px-3 py-1.5 rounded-xl text-[11px] whitespace-nowrap">
                                ❓ Info
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
                                    <span class="text-[10px] font-mono bg-white/10 text-cyan-300 px-2 py-0.5 rounded">✈️ SGN➔${dCode} (${dKm}km • ${task.duration}m)</span>
                                    ${task.scope ? `<span class="text-[10px] text-emerald-300 font-bold">🔄 ${task.scope}</span>` : ''}
                                </div>
                                <div class="text-xs sm:text-sm font-extrabold ${task.done ? 'line-through text-slate-400' : 'text-white'}">${task.title}</div>
                            </div>
                        </div>

                        <div class="flex items-center gap-1.5 shrink-0 self-end sm:self-center">
                            ${!task.done ? `
                                <button onclick="startFlightFromTask(${task.id})" class="bg-gradient-to-r from-blue-600 to-cyan-500 hover:opacity-95 text-white px-3 py-1 rounded-xl text-[11px] font-extrabold shadow">
                                    ${t.flyBtnShort} (${task.duration}m)
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
                    let typeLabel = t.catStudy.split(' (')[0];
                    if (ev.type === 'personal') {
                        badgeStyle = 'bg-purple-950/40 text-purple-300 border-purple-400/40';
                        typeLabel = t.catPers.split(' (')[0];
                    } else if (ev.type === 'school') {
                        badgeStyle = 'bg-red-950/35 text-red-300 border-red-400/30';
                        typeLabel = t.catSchool.split(' (')[0];
                    } else if (ev.type === 'free') {
                        badgeStyle = 'bg-emerald-950/35 text-emerald-300 border-emerald-400/30';
                        typeLabel = t.catFree;
                    }

                    const el = document.createElement('div');
                    el.className = `p-3 rounded-2xl border flex items-center justify-between gap-2 ${badgeStyle}`;
                    el.innerHTML = `
                        <div>
                            <div class="flex flex-wrap items-center gap-1.5">
                                <span class="text-[10px] font-mono font-extrabold px-2 py-0.5 rounded bg-black/40 text-amber-300">⏰ ${ev.time} (${ev.durationMins}m)</span>
                                <span class="text-[10px] font-bold">${typeLabel}</span>
                                <span class="text-[9px] bg-white/10 px-1.5 py-0.5 rounded text-emerald-300 font-bold">🔄 ${ev.repeatLabel}</span>
                            </div>
                            <div class="text-xs font-extrabold text-white mt-1">${ev.subject}</div>
                        </div>
                        <div class="flex items-center gap-1 shrink-0">
                            <button onclick="flyDirectlyFromCalendarEvent(${ev.id})" class="bg-cyan-500 hover:bg-cyan-400 text-black font-black px-2.5 py-1 rounded-xl text-[10px] shadow">
                                ${t.flyBtnShort}
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

        // ================= 9. LOGIC TRẠM BAY & ĐỒNG BỘ 100% ĐA NGÔN NGỮ =================
        function toggleBookingCardSize() {
            const card = document.getElementById('screen-booking');
            const btn = document.getElementById('toggle-booking-btn');
            const t = I18N[currentLang];
            isBookingCollapsed = !isBookingCollapsed;
            if (isBookingCollapsed) {
                card.classList.add('translate-y-[130%]');
                btn.innerText = t.btnExpand;
            } else {
                card.classList.remove('translate-y-[130%]');
                btn.innerText = t.btnCollapse;
            }
        }

        function initAirportDropdowns() {
            const oSel = document.getElementById('origin-select');
            const dSel = document.getElementById('dest-select');
            const qSel = document.getElementById('quick-task-dest');
            if (!oSel || !dSel || !qSel) return;

            const prevO = oSel.value || originAirport.code;
            const prevD = dSel.value || destAirport.code;
            const prevQ = qSel.value || "DAD";

            const t = I18N[currentLang];
            const vnAirports = AIRPORTS.filter(a => a.group === 'VN');
            const intAirports = AIRPORTS.filter(a => a.group === 'INT');

            const buildOptions = (withTimeHint = false) => {
                let html = `<optgroup label="${t.vnGroup}" class="bg-slate-900">`;
                vnAirports.forEach(a => {
                    const dist = calcDistanceKm(AIRPORTS[0].coords, a.coords);
                    const mins = calcStudyDurationFromDistance(dist, "Airbus A321neo");
                    const localName = getAirportLocalName(a);
                    html += `<option value="${a.code}">${a.code} - ${localName} ${withTimeHint ? `(~${mins}m)` : ''}</option>`;
                });
                html += `</optgroup><optgroup label="${t.intGroup}" class="bg-slate-900">`;
                intAirports.forEach(a => {
                    const dist = calcDistanceKm(AIRPORTS[0].coords, a.coords);
                    const mins = calcStudyDurationFromDistance(dist, "Airbus A321neo");
                    const localName = getAirportLocalName(a);
                    html += `<option value="${a.code}">${a.code} - ${localName} ${withTimeHint ? `(~${mins}m)` : ''}</option>`;
                });
                html += `</optgroup>`;
                return html;
            };

            oSel.innerHTML = buildOptions(false);
            dSel.innerHTML = buildOptions(false);
            qSel.innerHTML = buildOptions(true);

            oSel.value = prevO;
            dSel.value = prevD;
            qSel.value = prevQ;
        }

        function onRouteChange() {
            const oSel = document.getElementById('origin-select');
            const dSel = document.getElementById('dest-select');
            if (!oSel || !dSel) return;

            const oCode = oSel.value;
            const dCode = dSel.value;
            if (oCode === dCode) {
                const alt = AIRPORTS.find(a => a.code !== oCode);
                dSel.value = alt.code;
            }
            originAirport = AIRPORTS.find(a => a.code === oSel.value) || AIRPORTS[0];
            destAirport = AIRPORTS.find(a => a.code === dSel.value) || AIRPORTS[2];
            currentDistance = calcDistanceKm(originAirport.coords, destAirport.coords);
            selectedDuration = calcStudyDurationFromDistance(currentDistance, selectedAircraft);
            updateBookingUI();
        }

        function swapRoute() {
            const temp = originAirport;
            originAirport = destAirport;
            destAirport = temp;
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
            const t = I18N[currentLang];
            const specs = getAircraftSpecs(selectedAircraft);
            const oLocal = getAirportLocalName(originAirport).split(' (')[0];
            const dLocal = getAirportLocalName(destAirport);

            document.getElementById('booking-plane-svg-box').innerHTML = getAircraftSVG(selectedAircraft, 45);
            setTxt('badge-origin', originAirport.code);
            setTxt('badge-dest', destAirport.code);
            setTxt('badge-dist', `${currentDistance} km`);
            setTxt('banner-dest-title', `${oLocal} ➔ ${dLocal}`);
            setTxt('auto-calc-duration-text', formatDurationLabel(selectedDuration));
            setTxt('auto-calc-speed-text', `(${currentDistance} km • ${specs.speedKmh} km/h)`);

            // Đồng bộ thêm các nhãn nút Camera & Modal theo ngôn ngữ hiện tại
            if (currentLang === 'en') {
                setTxt('btn-cam-map', '🌍 Map');
                setTxt('btn-cam-cockpit', '👨‍✈️ Pilot');
                setTxt('btn-cam-cabin', '💺 Cabin');
                setTxt('btn-cam-window', '🪟 Window');
                setTxt('lbl-why-title', '🧠 Schedule & Flight Details');
                setTxt('lbl-turb-title', 'WARNING: YOU LEFT THE FOCUS COCKPIT!');
                setTxt('lbl-turb-desc', 'Focus timer is PAUSED because you switched tabs or windows!');
                setTxt('lbl-turb-count', 'Discipline Violations');
                setTxt('btn-turb-resume', '🔒 Return to Cockpit & Continue');
                setTxt('lbl-crash-title', 'FLIGHT CANCELLED DUE TO 3 VIOLATIONS');
                setTxt('btn-crash-back', 'Back');
                setTxt('lbl-media-title', '🎧 Audio & Avatar Settings');
                setTxt('lbl-media-lofi', '1. Upload custom Lofi audio (.mp3, .wav):');
                setTxt('lbl-media-noise', '🛫 Cabin Engine White Noise');
                setTxt('lbl-media-bot', '2. Change AI Chatbot Avatar:');
                setTxt('btn-media-save', 'Save & Close');
            } else if (currentLang === 'zh') {
                setTxt('btn-cam-map', '🌍 地圖');
                setTxt('btn-cam-cockpit', '👨‍✈️ 駕駛艙');
                setTxt('btn-cam-cabin', '💺 客艙');
                setTxt('btn-cam-window', '🪟 機窗');
                setTxt('lbl-why-title', '🧠 排程與專注航班詳情');
                setTxt('lbl-turb-title', '警告：您已離開專注駕駛艙！');
                setTxt('lbl-turb-desc', '系統偵測到您切換視窗，專注計時器已暫停！');
                setTxt('lbl-turb-count', '違規次數');
                setTxt('btn-turb-resume', '🔒 返回駕駛艙繼續學習');
                setTxt('lbl-crash-title', '因分心超過 3 次，航班已取消');
                setTxt('btn-crash-back', '返回');
                setTxt('lbl-media-title', '🎧 音效與介面設定');
                setTxt('lbl-media-lofi', '1. 上傳自訂 Lofi 音樂 (.mp3, .wav)：');
                setTxt('lbl-media-noise', '🛫 客艙引擎白噪音 (White Noise)');
                setTxt('lbl-media-bot', '2. 更換 AI 助理頭像：');
                setTxt('btn-media-save', '儲存並關閉');
            } else {
                setTxt('btn-cam-map', '🌍 Bản đồ');
                setTxt('btn-cam-cockpit', '👨‍✈️ Phi công');
                setTxt('btn-cam-cabin', '💺 Cabin');
                setTxt('btn-cam-window', '🪟 Cửa sổ');
                setTxt('lbl-why-title', '🧠 Chi tiết Lịch & Chuyến bay');
                setTxt('lbl-turb-title', 'CẢNH BÁO: BẠN ĐÃ RỜI KHỎI BUỒNG LÁI TẬP TRUNG!');
                setTxt('lbl-turb-desc', 'Đồng hồ tập trung đã bị TẠM DỪNG vì bạn vừa chuyển sang cửa sổ khác!');
                setTxt('lbl-turb-count', 'Vi phạm kỷ luật');
                setTxt('btn-turb-resume', '🔒 Quay lại Học tiếp ngay');
                setTxt('lbl-crash-title', 'CHUYẾN BAY BỊ HỦY DO MẤT TẬP TRUNG QUÁ 3 LẦN');
                setTxt('btn-crash-back', 'Quay lại');
                setTxt('lbl-media-title', '🎧 Tùy Chỉnh Âm Thanh & Giao Diện');
                setTxt('lbl-media-lofi', '1. Chọn file nhạc Lofi từ máy (.mp3, .wav):');
                setTxt('lbl-media-noise', '🛫 Tiếng động cơ máy bay (Cabin White Noise)');
                setTxt('lbl-media-bot', '2. Đổi ảnh đại diện Chatbot AI:');
                setTxt('btn-media-save', 'Lưu & Đóng');
            }

            const now = new Date();
            setTxt('booking-realtime-eta', `${String(now.getHours()).padStart(2,'0')}:${String(now.getMinutes()).padStart(2,'0')} ➔ ${calcRealTimeETA(selectedDuration)}`);

            if (routeLine) map.removeLayer(routeLine);
            if (originMarker) map.removeLayer(originMarker);
            if (destMarker) map.removeLayer(destMarker);

            originMarker = L.marker(originAirport.coords, { icon: createAirportBadge(originAirport.code, false) }).addTo(map);
            destMarker = L.marker(destAirport.coords, { icon: createAirportBadge(destAirport.code, true) }).addTo(map);
            routeLine = L.polyline([originAirport.coords, destAirport.coords], { color: '#38bdf8', weight: 3.5, dashArray: '8, 8', opacity: 0.95 }).addTo(map);

            if (is2DMapActive) {
                map.invalidateSize(true);
                map.fitBounds(routeLine.getBounds(), { padding: [90, 90], maxZoom: 7 });
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
            setTxt('seat-selected-badge', seatCode);
            setTxt('pop-seat-code', seatCode);
            renderSeats();
            renderFocusPills();
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
            closeFocusPopover();
            renderSeats();
            showBoardingPass();
        }

        function goToSeatSelection() {
            setTxt('seat-header-aircraft', selectedAircraft);
            setTxt('seat-header-route', `${originAirport.code} ➔ ${destAirport.code} (${currentDistance} km • ${formatDurationLabel(selectedDuration)})`);
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
            strictModeEnabled = document.getElementById('strict-mode-toggle').checked;
            document.getElementById('screen-seat').classList.add('hidden');
            document.getElementById('screen-seat').classList.remove('flex');

            const now = new Date();
            const stdStr = `${String(now.getHours()).padStart(2,'0')}:${String(now.getMinutes()).padStart(2,'0')}`;
            flightEtaString = calcRealTimeETA(selectedDuration);

            setTxt('tk-aircraft', selectedAircraft);
            setTxt('tk-passenger', profile.name);
            setTxt('tk-realtime-span', `${stdStr} ➔ ${flightEtaString}`);
            setTxt('tk-strict-badge', strictModeEnabled ? "🔒 STRICT LOCK ON" : "🔓 FREE MODE");
            setTxt('tk-origin-code', originAirport.code);
            setTxt('tk-origin-name', getAirportLocalName(originAirport).split(' (')[0]);
            setTxt('tk-dest-code', destAirport.code);
            setTxt('tk-dest-name', getAirportLocalName(destAirport).split(' (')[0]);
            setTxt('tk-duration', formatDurationLabel(selectedDuration));
            setTxt('tk-seat', selectedSeat);
            setTxt('tk-dist', currentDistance + ' km');
            setTxt('tk-focus', `${selectedFocus.icon} ${selectedFocus.label}`);
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
            if (player.paused) toggleLofi();

            isFlying = true;
            isPausedByViolation = false;
            violationCount = 0;
            currentFlightProgress = 0;
            updateSafetyHearts();
            updateCameraViewsData();

            flightEtaString = calcRealTimeETA(selectedDuration);
            setTxt('fly-eta-badge', flightEtaString);
            setTxt('cockpit-eta', flightEtaString);
            setTxt('cabin-eta', flightEtaString);

            document.getElementById('fly-mini-svg').innerHTML = getAircraftSVG(selectedAircraft, 45);
            setTxt('fly-route-text', `${originAirport.code} ➔ ${destAirport.code}`);
            setTxt('fly-sub-info', `${selectedAircraft.split(' ')[1] || selectedAircraft} • ${selectedSeat} • ${selectedFocus.icon} ${selectedFocus.label}`);

            totalFlightSeconds = selectedDuration * 60;
            remainingSeconds = totalFlightSeconds;

            if (planeMarker) map.removeLayer(planeMarker);
            planeMarker = L.marker(originAirport.coords, { icon: createCustomAircraftMapIcon(), zIndexOffset: 1000 }).addTo(map);

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
            isFlying = false;
            playCabinDingDong();
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
            setTxt('safety-hearts', '❤️'.repeat(left) + '🖤'.repeat(MAX_VIOLATIONS - left));
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
            isPausedByViolation = true;
            violationCount++;
            updateSafetyHearts();
            if (violationCount >= MAX_VIOLATIONS) {
                isFlying = false;
                clearInterval(flightInterval);
                stopAlarmLoop();
                document.getElementById('turbulence-modal').classList.add('hidden');
                document.getElementById('turbulence-modal').classList.remove('flex');
                document.getElementById('crash-modal').classList.remove('hidden');
                document.getElementById('crash-modal').classList.add('flex');
                playCockpitAlarmBeep();
                return;
            }
            setTxt('violation-count-text', `${violationCount} / ${MAX_VIOLATIONS}`);
            document.getElementById('turbulence-modal').classList.remove('hidden');
            document.getElementById('turbulence-modal').classList.add('flex');
            playCockpitAlarmBeep();
            if (alarmInterval) clearInterval(alarmInterval);
            alarmInterval = setInterval(playCockpitAlarmBeep, 900);
        }

        function stopAlarmLoop() {
            if (alarmInterval) { clearInterval(alarmInterval); alarmInterval = null; }
        }
        function resumeFromTurbulence() {
            stopAlarmLoop();
            isPausedByViolation = false;
            document.getElementById('turbulence-modal').classList.add('hidden');
            document.getElementById('turbulence-modal').classList.remove('flex');
        }
        function closeCrashModal() {
            document.getElementById('crash-modal').classList.add('hidden');
            document.getElementById('crash-modal').classList.remove('flex');
            abortFlight();
        }

        document.addEventListener('visibilitychange', () => {
            if (document.hidden) triggerTurbulenceViolation();
        });

        function updateFlightTick() {
            const hrs = Math.floor(remainingSeconds / 3600);
            const mins = Math.floor((remainingSeconds % 3600) / 60);
            const secs = remainingSeconds % 60;
            const timeFormatted = hrs > 0
                ? `${hrs}:${mins<10?'0'+mins:mins}:${secs<10?'0'+secs:secs}`
                : `${mins<10?'0'+mins:mins}:${secs<10?'0'+secs:secs}`;

            setTxt('countdown-timer', timeFormatted);
            setTxt('cockpit-timer-display', timeFormatted);
            setTxt('cabin-timer-display', timeFormatted);

            currentFlightProgress = (totalFlightSeconds - remainingSeconds) / totalFlightSeconds;
            document.getElementById('flight-progress').style.width = `${currentFlightProgress * 100}%`;

            const distLeft = Math.max(0, Math.round(currentDistance * (1 - currentFlightProgress)));
            setTxt('fly-dist-left', distLeft);
            setTxt('cockpit-dist-display', `${distLeft} KM`);
            setTxt('cabin-dist-display', distLeft);

            const lat = originAirport.coords[0] + (destAirport.coords[0] - originAirport.coords[0]) * currentFlightProgress;
            const lng = originAirport.coords[1] + (destAirport.coords[1] - originAirport.coords[1]) * currentFlightProgress;
            if (planeMarker) planeMarker.setLatLng([lat, lng]);
        }

        function centerOnPlane() {
            setCameraView('map');
            const curLat = originAirport.coords[0] + (destAirport.coords[0] - originAirport.coords[0]) * currentFlightProgress;
            const curLng = originAirport.coords[1] + (destAirport.coords[1] - originAirport.coords[1]) * currentFlightProgress;
            if (is2DMapActive && planeMarker) map.flyTo(planeMarker.getLatLng(), 7, { duration: 1.2 });
            else {
                targetRot.y = (curLng + 90) * (Math.PI / 180);
                targetRot.x = curLat * (Math.PI / 180) * 0.75;
            }
        }

        function abortFlight() {
            isFlying = false;
            isPausedByViolation = false;
            stopAlarmLoop();
            if (flightInterval) clearInterval(flightInterval);
            if (planeMarker) map.removeLayer(planeMarker);
            setCameraView('map');
            document.getElementById('screen-flying').classList.add('hidden');
            document.getElementById('screen-booking').classList.remove('hidden');
            document.getElementById('toggle-booking-btn').classList.remove('hidden');
            updateBookingUI();
        }

        // ================= 10. CHATBOT AI ĐA NGÔN NGỮ & MEDIA =================
        function toggleChatbotWindow() {
            const win = document.getElementById('chatbot-window');
            win.classList.toggle('hidden');
            win.classList.toggle('flex');
        }

        function getCurrentTimeStr() {
            const now = new Date();
            return `${String(now.getHours()).padStart(2,'0')}:${String(now.getMinutes()).padStart(2,'0')}`;
        }

        function sendQuickChat(text) {
            document.getElementById('chat-input').value = text;
            sendChatMessage();
        }

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
                return `您好 <b>${profile.name}</b>！<br>目前您有 <b>${pending.length} 項待辦任務</b>。您可以點擊右側萬年曆選擇日期與重複週期（每週、每月同日或自訂週期），系統將自動為您安排專注航班！`;
            }
            if (currentLang === 'en') {
                return `Hello <b>${profile.name}</b>!<br>You currently have <b>${pending.length} pending tasks</b>. Pick any date on the monthly calendar and set your custom recurrence!`;
            }
            return `Chào <b>${profile.name}</b>!<br>Hiện bạn có <b>${pending.length} nhiệm vụ</b> đang chờ. Bạn có thể bấm chọn trực tiếp ngày trên tờ Lịch Tháng (có cả Âm lịch & Thứ) và chọn chu kỳ lặp lại tùy ý nhé!`;
        }

        function resetChat() {
            const profile = appState.members[currentMemberKey];
            const botAvatar = document.getElementById('bot-launcher-img').src;
            let welcome = `Xin chào <b>${profile.name}</b>! 🙋‍♀️<br>Đã tích hợp Lịch Vạn Niên (Thứ/Ngày/Tháng/Năm + Âm lịch), Chu kỳ lặp lại tùy chọn và 3 ngôn ngữ (VI / EN / 繁體)!`;
            if (currentLang === 'zh') welcome = `您好 <b>${profile.name}</b>！🙋‍♀️<br>我是您的 AI 學習助理。系統已全面支援繁體中文、國農曆月曆與自訂重複週期！`;
            else if (currentLang === 'en') welcome = `Hello <b>${profile.name}</b>! 🙋‍♀️<br>Full English interface, Monthly Calendar with Lunar dates & Custom Recurrence are ready!`;

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
            if (p.paused) {
                p.play().then(() => {
                    eq.classList.remove('hidden');
                    eq.classList.add('flex');
                    txt.innerText = "Playing";
                }).catch(() => {});
            } else {
                p.pause();
                eq.classList.add('hidden');
                eq.classList.remove('flex');
                txt.innerText = "🎵 Lofi";
            }
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
                    lastOut = output[i];
                    output[i] *= 0.15;
                }
                cabinNoiseNode = audioCtx.createBufferSource();
                cabinNoiseNode.buffer = noiseBuffer;
                cabinNoiseNode.loop = true;
                cabinNoiseNode.connect(audioCtx.destination);
                cabinNoiseNode.start(0);
            } else if (cabinNoiseNode) {
                cabinNoiseNode.stop();
                cabinNoiseNode.disconnect();
                cabinNoiseNode = null;
            }
        }

        function openMediaModal() {
            document.getElementById('media-modal').classList.remove('hidden');
            document.getElementById('media-modal').classList.add('flex');
        }
        function closeMediaModal() {
            document.getElementById('media-modal').classList.add('hidden');
            document.getElementById('media-modal').classList.remove('flex');
        }
        function handleLocalAudio(input) {
            if (input.files && input.files[0]) {
                const url = URL.createObjectURL(input.files[0]);
                const p = document.getElementById('lofi-player');
                p.src = url;
                p.play();
                document.getElementById('eq-icon').classList.remove('hidden');
                document.getElementById('eq-icon').classList.add('flex');
            }
        }
        function applyCustomMedia() {
            const aUrl = document.getElementById('audio-url-input').value.trim();
            if (aUrl) {
                const p = document.getElementById('lofi-player');
                p.src = aUrl;
                p.play();
            }
            closeMediaModal();
        }

        // Khởi chạy toàn bộ Hệ thống
        document.getElementById('member-select').value = currentMemberKey;
        initThreeGlobe();
        updateRealTimeClock();
        initAirportDropdowns();
        syncEnvironmentWithRealTime();
        updateSlotDurationPreview();
        onRouteChange();
        setAppLanguage('vi');
    </script>
</body>
</html>
"""

components.html(app_html, height=800, scrolling=False)
