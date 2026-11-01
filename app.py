import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="StudyHub & Flight Sim - Real-Time",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Khóa chặt iframe khớp 100% với chiều cao màn hình thực tế của mọi Laptop/Điện thoại
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
            background-color: #060913 !important;
        }
    </style>
""", unsafe_allow_html=True)

app_html = """
<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
    <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@500;700;800&display=swap" rel="stylesheet">
    <style>
        * { box-sizing: border-box; }
        body { font-family: 'Plus Jakarta Sans', sans-serif; background: #060913; color: white; margin: 0; padding: 0; width: 100vw; height: 100vh; overflow: hidden; user-select: none; }
        .mono { font-family: 'JetBrains Mono', monospace; }
        #map { position: absolute; inset: 0; z-index: 1; background: #060913; transition: filter 0.8s ease; }

        .map-night-filter { filter: brightness(0.45) contrast(1.35) saturate(0.8) hue-rotate(195deg); }
        .map-sunset-filter { filter: brightness(0.75) contrast(1.15) sepia(0.35) hue-rotate(-15deg); }
        .map-rain-filter { filter: brightness(0.55) contrast(1.2) saturate(0.6); }

        .glass-panel {
            background: rgba(13, 19, 33, 0.92);
            backdrop-filter: blur(22px);
            -webkit-backdrop-filter: blur(22px);
            border: 1px solid rgba(255, 255, 255, 0.15);
        }

        .dash-card {
            background: linear-gradient(145deg, #0f172a 0%, #0b1120 100%);
            border: 1px solid rgba(255, 255, 255, 0.1);
            box-shadow: 0 12px 32px rgba(0, 0, 0, 0.45);
        }

        .focus-popover {
            background: rgba(24, 35, 58, 0.98);
            backdrop-filter: blur(28px);
            border: 1px solid rgba(147, 197, 253, 0.35);
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

        .ticket-cutout-left { position: absolute; left: -14px; top: 66%; width: 28px; height: 28px; background: #060913; border-radius: 50%; }
        .ticket-cutout-right { position: absolute; right: -14px; top: 66%; width: 28px; height: 28px; background: #060913; border-radius: 50%; }

        @keyframes pulse-bar { 0%, 100% { height: 4px; } 50% { height: 15px; } }
        .eq-bar { width: 3px; background: #38bdf8; border-radius: 2px; animation: pulse-bar 0.9s infinite ease-in-out; }
        .eq-bar:nth-child(2) { animation-delay: 0.2s; }
        .eq-bar:nth-child(3) { animation-delay: 0.4s; }

        @keyframes strobe-blink { 0%, 85%, 100% { opacity: 0.15; } 90%, 95% { opacity: 1; filter: drop-shadow(0 0 8px #ffffff); } }
        .strobe-light { animation: strobe-blink 1.5s infinite; }

        @keyframes radar-pulse { 0% { transform: scale(0.4); opacity: 0.85; } 100% { transform: scale(2.4); opacity: 0; } }
        .radar-ring { animation: radar-pulse 2.2s infinite ease-out; }

        @keyframes cloud-move { 0% { transform: translateX(110%); } 100% { transform: translateX(-120%); } }
        .cloud-anim-1 { animation: cloud-move 18s linear infinite; }
        .cloud-anim-2 { animation: cloud-move 26s linear infinite; animation-delay: -9s; }
        .cloud-anim-3 { animation: cloud-move 14s linear infinite; animation-delay: -4s; }

        @keyframes hud-sway { 0%, 100% { transform: rotate(-1.5deg) translateY(0px); } 50% { transform: rotate(1.5deg) translateY(4px); } }
        .hud-horizon { animation: hud-sway 7s ease-in-out infinite; }

        @keyframes rain-fall { 0% { background-position: 0px 0px; } 100% { background-position: -150px 500px; } }
        .rain-overlay {
            background-image: repeating-linear-gradient(105deg, transparent 0px, transparent 18px, rgba(186, 230, 253, 0.3) 19px, transparent 20px);
            background-size: 200px 200px;
            animation: rain-fall 0.6s linear infinite;
        }

        @keyframes red-alert { 0%, 100% { background: rgba(153, 27, 27, 0.94); } 50% { background: rgba(220, 38, 38, 0.98); } }
        .turbulence-alert { animation: red-alert 0.7s infinite; backdrop-filter: blur(16px); }

        @keyframes bot-glow {
            0%, 100% { box-shadow: 0 0 15px rgba(212, 163, 73, 0.6), 0 0 30px rgba(212, 163, 73, 0.3); transform: translateY(0px); }
            50% { box-shadow: 0 0 25px rgba(234, 179, 8, 0.9), 0 0 45px rgba(212, 163, 73, 0.5); transform: translateY(-3px); }
        }
        .bot-launcher-glow { animation: bot-glow 3s infinite ease-in-out; }

        .dragging-card { opacity: 0.45; border: 2px dashed #38bdf8 !important; }
        ::-webkit-scrollbar { width: 5px; height: 5px; }
        ::-webkit-scrollbar-thumb { background: rgba(255,255,255,0.25); border-radius: 10px; }
        .leaflet-control-attribution { display: none !important; }
    </style>
</head>
<body class="relative w-screen h-screen overflow-hidden bg-[#060913]">

    <!-- AUDIO LOFI -->
    <audio id="lofi-player" loop crossorigin="anonymous">
        <source id="lofi-source" src="https://cdn.pixabay.com/download/audio/2022/05/27/audio_1808fbf07a.mp3" type="audio/mpeg">
    </audio>

    <!-- ================= THANH ĐIỀU HƯỚNG CHÍNH + ĐỒNG HỒ THỜI GIAN THỰC ================= -->
    <header class="fixed top-0 left-0 right-0 h-14 z-40 bg-[#090e1a]/95 backdrop-blur-xl border-b border-white/10 px-3 sm:px-5 flex items-center justify-between gap-2">
        <!-- Logo + Chọn Thành viên + Đồng hồ Thời gian thực -->
        <div class="flex items-center gap-2.5">
            <div class="flex items-center gap-2">
                <div class="w-8 h-8 rounded-xl bg-gradient-to-br from-blue-500 to-cyan-400 flex items-center justify-center text-black font-black text-base shadow">✈️</div>
                <div class="hidden xl:block">
                    <div class="text-[11px] font-extrabold tracking-wider text-white">STUDYHUB & FLIGHT SIM</div>
                    <div class="text-[9px] text-emerald-400" id="save-status-indicator">● Tự động lưu dữ liệu</div>
                </div>
            </div>

            <!-- Chọn Thành viên (Chỉ hiển thị đúng Tên) -->
            <div class="bg-slate-900 border border-white/15 px-2.5 py-1 rounded-xl flex items-center gap-1.5">
                <span class="text-xs">👤</span>
                <div>
                    <div class="text-[8px] text-amber-400 font-bold uppercase tracking-wider leading-none">Thành viên</div>
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

            <!-- ĐỒNG HỒ THỜI GIAN THỰC (REAL-TIME CLOCK) -->
            <div class="hidden sm:flex items-center gap-2 bg-slate-900/90 border border-cyan-500/30 px-3 py-1 rounded-xl">
                <span class="w-2 h-2 rounded-full bg-emerald-400 animate-ping"></span>
                <div>
                    <div id="realtime-clock" class="mono text-xs font-extrabold text-cyan-300 leading-none">00:00:00</div>
                    <div id="realtime-date" class="text-[9px] text-slate-400 font-semibold leading-none mt-0.5">--/--/----</div>
                </div>
            </div>
        </div>

        <!-- Chuyển Đổi 2 Giao Diện Riêng Biệt -->
        <div class="bg-slate-900/90 p-1 rounded-xl border border-white/10 flex items-center gap-1">
            <button id="nav-btn-dashboard" onclick="switchPage('dashboard')" class="px-3 py-1.5 rounded-lg text-xs font-extrabold bg-gradient-to-r from-blue-600 to-cyan-500 text-white shadow transition flex items-center gap-1.5">
                <span>📊 Bảng Điều Khiển Học Tập</span>
                <span id="nav-pending-badge" class="bg-black/30 text-white text-[10px] px-1.5 rounded-full">0</span>
            </button>
            <button id="nav-btn-flight" onclick="switchPage('flight')" class="px-3 py-1.5 rounded-lg text-xs font-extrabold text-slate-400 hover:text-white transition flex items-center gap-1.5">
                <span>✈️ Chuyến Bay Tập Trung</span>
            </button>
        </div>

        <!-- Nhạc Lofi & Cài đặt -->
        <div class="flex items-center gap-1.5">
            <button onclick="toggleLofi()" class="bg-slate-900 hover:bg-slate-800 border border-white/10 px-2.5 py-1.5 rounded-xl flex items-center gap-1.5 text-xs font-bold text-slate-200 transition">
                <div id="eq-icon" class="hidden items-end gap-[2px] h-3.5">
                    <div class="eq-bar"></div><div class="eq-bar"></div><div class="eq-bar"></div>
                </div>
                <span id="lofi-btn-text">🎵 Nhạc Lofi</span>
            </button>
            <button onclick="openMediaModal()" class="bg-slate-900 hover:bg-slate-800 border border-cyan-500/30 px-2.5 py-1.5 rounded-xl text-xs font-bold text-cyan-400 transition">
                ⚙️ Âm thanh / Bot
            </button>
        </div>
    </header>

    <!-- ========================================================================================= -->
    <!-- TRANG 1: BẢNG ĐIỀU KHIỂN HỌC TẬP, TO-DO LIST & THỜI KHÓA BIỂU CÁ NHÂN                    -->
    <!-- ========================================================================================= -->
    <main id="page-dashboard" class="fixed inset-x-0 top-14 bottom-0 z-30 bg-[#060913] overflow-y-auto px-4 sm:px-6 py-5">
        <div class="max-w-7xl mx-auto space-y-5 pb-20">

            <!-- CẢNH BÁO DEADLINE KHẨN CẤP -->
            <div id="deadline-banner" class="hidden bg-gradient-to-r from-red-600/90 via-orange-600/90 to-amber-600/90 rounded-2xl p-3.5 shadow-xl border border-red-300/30 items-center justify-between gap-4">
                <div class="flex items-center gap-3">
                    <span class="text-xl animate-bounce">⏰</span>
                    <div>
                        <div class="text-[9px] font-black uppercase tracking-widest bg-black/30 px-2 py-0.5 rounded inline-block">Nhắc nhở Gần tới Deadline</div>
                        <div id="deadline-banner-text" class="text-xs sm:text-sm font-extrabold text-white mt-0.5"></div>
                    </div>
                </div>
                <button onclick="startFocusFromTopTask()" class="bg-white text-red-700 hover:bg-yellow-100 font-black text-xs px-3.5 py-2 rounded-xl shadow shrink-0">
                    🛫 Bay tập trung ngay
                </button>
            </div>

            <!-- 4 THẺ THỐNG KÊ KPI -->
            <div class="grid grid-cols-2 lg:grid-cols-4 gap-3.5">
                <div class="dash-card rounded-2xl p-3.5 flex items-center justify-between">
                    <div>
                        <div class="text-[11px] text-slate-400 font-semibold">Hồ sơ thành viên</div>
                        <div id="stat-member-name" class="text-base font-black text-amber-400 mt-0.5">Hữu Đại</div>
                        <div class="text-[10px] text-slate-500">Lưu tự động trên máy</div>
                    </div>
                    <div class="w-10 h-10 rounded-xl bg-amber-500/10 border border-amber-500/20 flex items-center justify-center text-lg">👤</div>
                </div>

                <div class="dash-card rounded-2xl p-3.5 flex items-center justify-between">
                    <div>
                        <div class="text-[11px] text-slate-400 font-semibold">Công việc đang chờ</div>
                        <div id="stat-pending-count" class="text-xl font-black text-white mt-0.5 mono">0</div>
                        <div class="text-[10px] text-cyan-400">Cần hoàn thành</div>
                    </div>
                    <div class="w-10 h-10 rounded-xl bg-cyan-500/10 border border-cyan-500/20 flex items-center justify-center text-lg">📋</div>
                </div>

                <div class="dash-card rounded-2xl p-3.5 flex items-center justify-between">
                    <div>
                        <div class="text-[11px] text-slate-400 font-semibold">Đã hoàn thành (✓)</div>
                        <div id="stat-done-count" class="text-xl font-black text-emerald-400 mt-0.5 mono">0</div>
                        <div id="stat-done-percent" class="text-[10px] text-emerald-500">Tiến độ: 0%</div>
                    </div>
                    <div class="w-10 h-10 rounded-xl bg-emerald-500/10 border border-emerald-500/20 flex items-center justify-center text-lg">✅</div>
                </div>

                <div class="dash-card rounded-2xl p-3.5 flex items-center justify-between">
                    <div>
                        <div class="text-[11px] text-slate-400 font-semibold">Dặm bay tích lũy</div>
                        <div id="stat-miles-count" class="text-lg font-black text-blue-400 mt-0.5 mono">0 km</div>
                        <div id="stat-flights-count" class="text-[10px] text-slate-400">Đã hạ cánh: 0 chuyến</div>
                    </div>
                    <div class="w-10 h-10 rounded-xl bg-blue-500/10 border border-blue-500/20 flex items-center justify-center text-lg">🛂</div>
                </div>
            </div>

            <!-- KHU VỰC AI ĐỀ XUẤT "HÔM NAY NÊN HỌC GÌ?" -->
            <div class="grid grid-cols-1 lg:grid-cols-12 gap-4">
                <div class="lg:col-span-8 bg-gradient-to-br from-blue-950/85 via-slate-900 to-slate-900 border border-cyan-500/30 rounded-3xl p-4 sm:p-5 shadow-xl flex flex-col justify-between">
                    <div class="flex flex-wrap items-center justify-between gap-2 mb-2.5">
                        <div class="flex items-center gap-2">
                            <span class="bg-cyan-400 text-black font-black text-[10px] px-2.5 py-0.5 rounded-full uppercase tracking-wider">💡 Hôm nay nên học gì? (AI Đề xuất)</span>
                            <span class="text-xs text-slate-400">Tự động gán chặng bay theo khoảng cách</span>
                        </div>
                        <button onclick="sendStudyReminderAlert()" class="bg-white/10 hover:bg-white/15 text-amber-300 border border-amber-400/30 px-3 py-1 rounded-xl text-xs font-bold transition">
                            🔔 Nhắc nhở học tập
                        </button>
                    </div>
                    <div id="ai-today-suggestion" class="bg-black/40 border border-white/10 rounded-2xl p-3.5"></div>
                </div>

                <div class="lg:col-span-4 dash-card rounded-3xl p-4 sm:p-5 flex flex-col justify-between">
                    <div>
                        <h3 class="text-sm font-extrabold text-white mb-1">⚡ Điều phối Lịch AI Thông Minh</h3>
                        <p class="text-xs text-slate-400 leading-relaxed">
                            Sắp xếp thứ tự ưu tiên theo Deadline hoặc dời toàn bộ ca học khi bạn có việc đột xuất.
                        </p>
                    </div>
                    <div class="space-y-2 mt-3">
                        <button onclick="aiSortTasks()" class="w-full bg-gradient-to-r from-amber-500 to-yellow-500 hover:opacity-95 text-black font-black py-2 px-4 rounded-xl text-xs shadow transition">
                            🤖 AI Sắp xếp Thứ tự Ưu tiên
                        </button>
                        <button onclick="handleSuddenScheduleChange()" class="w-full bg-slate-800 hover:bg-slate-700 text-cyan-300 border border-cyan-500/30 font-bold py-2 px-4 rounded-xl text-xs transition">
                            🌪️ Có lịch đột xuất (Tự động dời ca)
                        </button>
                    </div>
                </div>
            </div>

            <!-- CỘT TRÁI: TO-DO LIST KÉO THẢ | CỘT PHẢI: THỜI KHÓA BIỂU CÁ NHÂN -->
            <div class="grid grid-cols-1 lg:grid-cols-12 gap-5">
                <!-- CỘT TRÁI (7 PHẦN) -->
                <div class="lg:col-span-7 dash-card rounded-3xl p-4 sm:p-5 flex flex-col">
                    <div class="flex flex-wrap items-center justify-between gap-2 mb-3">
                        <div>
                            <h2 class="text-sm sm:text-base font-extrabold text-white flex items-center gap-2">
                                <span>✅ Danh Sách Nhiệm Vụ & Chặng Bay</span>
                                <span class="text-[10px] bg-blue-500/20 text-blue-300 px-2 py-0.5 rounded-lg border border-blue-400/30">Kéo thả ↕️</span>
                            </h2>
                            <p class="text-[11px] text-slate-400">Thời gian học được tính tự động từ khoảng cách (km) của chặng bay</p>
                        </div>

                        <div class="flex bg-slate-900 p-1 rounded-xl border border-white/10 text-xs font-bold">
                            <button id="filter-all" onclick="setTaskFilter('all')" class="px-2.5 py-1 rounded-lg bg-blue-600 text-white">Tất cả</button>
                            <button id="filter-pending" onclick="setTaskFilter('pending')" class="px-2.5 py-1 rounded-lg text-slate-400 hover:text-white">Đang làm</button>
                            <button id="filter-done" onclick="setTaskFilter('done')" class="px-2.5 py-1 rounded-lg text-slate-400 hover:text-white">Đã xong ✓</button>
                        </div>
                    </div>

                    <!-- Form Thêm Công Việc (Chọn Điểm đến để tự tính thời gian học theo khoảng cách) -->
                    <div class="bg-slate-900/90 border border-white/15 rounded-2xl p-3.5 mb-4 space-y-2.5">
                        <div class="text-xs font-bold text-cyan-400">+ Thêm công việc mới (Thời gian học tự tính theo khoảng cách bay từ SGN):</div>
                        <div class="grid grid-cols-1 sm:grid-cols-12 gap-2">
                            <input type="text" id="quick-task-title" onkeydown="if(event.key==='Enter') addNewTask()" placeholder="Nhập tên công việc (VD: Tạo app, Ôn thi...)" class="sm:col-span-6 bg-slate-800 text-white text-xs px-3 py-2 rounded-xl border border-white/10 focus:outline-none focus:border-cyan-400" />
                            <div class="sm:col-span-3 flex items-center bg-slate-800 rounded-xl border border-white/10 px-2.5">
                                <span class="text-[10px] text-amber-300 font-bold mr-1.5 shrink-0">Hạn (Giờ):</span>
                                <input type="number" id="quick-task-hours" value="24" min="1" max="720" class="w-full bg-transparent text-white text-xs py-2 focus:outline-none font-bold" />
                            </div>
                            <select id="quick-task-importance" class="sm:col-span-3 bg-slate-800 text-amber-300 text-xs px-2 py-2 rounded-xl border border-white/10 font-bold focus:outline-none">
                                <option value="5">⭐⭐⭐⭐⭐ (Rất gấp)</option>
                                <option value="4" selected>⭐⭐⭐⭐ (Quan trọng)</option>
                                <option value="3">⭐⭐⭐ (Bình thường)</option>
                                <option value="2">⭐⭐ (Nhẹ nhàng)</option>
                            </select>
                        </div>
                        <div class="grid grid-cols-1 sm:grid-cols-12 gap-2 items-center">
                            <div class="sm:col-span-4 flex items-center bg-slate-800 rounded-xl border border-white/10 px-2.5 py-1.5">
                                <span class="text-[10px] text-slate-400 font-bold mr-1.5">Ca học:</span>
                                <input type="text" id="quick-task-slot" value="19:30" class="w-full bg-transparent text-white text-xs focus:outline-none font-mono" />
                            </div>
                            <div class="sm:col-span-5 flex items-center bg-slate-800 rounded-xl border border-white/10 px-2.5 py-1.5">
                                <span class="text-[10px] text-cyan-300 font-bold mr-1.5 shrink-0">Bay tới:</span>
                                <select id="quick-task-dest" class="w-full bg-transparent text-white text-xs font-bold focus:outline-none"></select>
                            </div>
                            <button onclick="addNewTask()" class="sm:col-span-3 bg-gradient-to-r from-blue-600 to-cyan-500 hover:opacity-95 text-white font-extrabold py-2 px-3 rounded-xl text-xs shadow-lg transition">
                                + Lưu Việc
                            </button>
                        </div>
                    </div>

                    <div id="todo-drag-list" class="space-y-2 flex-1"></div>
                </div>

                <!-- CỘT PHẢI (5 PHẦN): THỜI KHÓA BIỂU CÁ NHÂN -->
                <div class="lg:col-span-5 dash-card rounded-3xl p-4 sm:p-5 flex flex-col">
                    <div class="mb-3">
                        <h2 class="text-sm sm:text-base font-extrabold text-white flex items-center gap-2">
                            <span>🗓️ Thời Khóa Biểu Cá Nhân</span>
                            <span id="timetable-owner-badge" class="text-xs text-amber-400 font-black"></span>
                        </h2>
                        <p class="text-[11px] text-slate-400">Tự thêm hoặc xóa lịch học cố định / giờ trống của riêng bạn</p>
                    </div>

                    <div class="grid grid-cols-7 gap-1 mb-3" id="day-tabs-container"></div>

                    <div class="bg-slate-900/90 border border-white/15 rounded-2xl p-3 mb-3 space-y-2">
                        <div class="text-xs font-bold text-emerald-400">+ Thêm khung giờ vào ngày <span id="add-slot-day-label">T2</span>:</div>
                        <div class="grid grid-cols-1 sm:grid-cols-2 gap-2">
                            <input type="text" id="new-slot-time" placeholder="Giờ (VD: 07:30 - 11:00)" class="bg-slate-800 text-white text-xs px-3 py-1.5 rounded-xl border border-white/10 focus:outline-none" />
                            <select id="new-slot-type" class="bg-slate-800 text-white text-xs px-2.5 py-1.5 rounded-xl border border-white/10 font-bold focus:outline-none">
                                <option value="free">🟢 Giờ trống (Dành tự học)</option>
                                <option value="busy">🔴 Lịch học trên trường / Bận</option>
                            </select>
                        </div>
                        <div class="flex gap-2">
                            <input type="text" id="new-slot-subject" onkeydown="if(event.key==='Enter') saveNewTimetableSlot()" placeholder="Tên môn học hoặc ghi chú..." class="flex-1 bg-slate-800 text-white text-xs px-3 py-1.5 rounded-xl border border-white/10 focus:outline-none" />
                            <button onclick="saveNewTimetableSlot()" class="bg-emerald-600 hover:bg-emerald-500 text-white font-extrabold px-3.5 py-1.5 rounded-xl text-xs shrink-0 shadow">
                                + Thêm
                            </button>
                        </div>
                    </div>

                    <div id="timetable-slots-list" class="space-y-2 flex-1"></div>
                </div>
            </div>
        </div>
    </main>

    <!-- ========================================================================================= -->
    <!-- TRANG 2: TRẠM BAY TẬP TRUNG, 4 GÓC NHÌN CAMERA & TỰ ĐỘNG TÍNH GIỜ THEO KHOẢNG CÁCH        -->
    <!-- ========================================================================================= -->
    <section id="page-flight" class="fixed inset-x-0 top-14 bottom-0 z-20 hidden overflow-hidden">
        <!-- GÓC NHÌN 1: BẢN ĐỒ VỆ TINH RADAR -->
        <div id="map"></div>

        <!-- THANH CHỌN 4 GÓC NHÌN CAMERA & CHẾ ĐỘ NGÀY/ĐÊM THEO THỜI GIAN THỰC -->
        <div id="flight-top-hud" class="fixed top-16 left-1/2 -translate-x-1/2 z-30 w-[96%] max-w-4xl flex flex-wrap items-center justify-between gap-2 pointer-events-none">
            <div class="glass-panel p-1 rounded-2xl flex items-center gap-1 pointer-events-auto shadow-2xl border border-cyan-400/30">
                <button id="cam-btn-map" onclick="setCameraView('map')" class="px-2.5 py-1.5 rounded-xl text-[11px] font-extrabold bg-cyan-500 text-black shadow transition">
                    🗺️ Toàn Bản Đồ
                </button>
                <button id="cam-btn-cockpit" onclick="setCameraView('cockpit')" class="px-2.5 py-1.5 rounded-xl text-[11px] font-extrabold text-slate-300 hover:text-white transition">
                    👨‍✈️ Buồng Lái Phi Công
                </button>
                <button id="cam-btn-cabin" onclick="setCameraView('cabin')" class="px-2.5 py-1.5 rounded-xl text-[11px] font-extrabold text-slate-300 hover:text-white transition">
                    💺 Trong Khoang Cabin
                </button>
                <button id="cam-btn-window" onclick="setCameraView('window')" class="px-2.5 py-1.5 rounded-xl text-[11px] font-extrabold text-slate-300 hover:text-white transition">
                    🪟 Qua Cửa Sổ
                </button>
            </div>

            <div class="glass-panel p-1 rounded-2xl flex items-center gap-1 pointer-events-auto shadow-2xl border border-amber-400/30">
                <button id="env-btn-auto" onclick="syncEnvironmentWithRealTime()" class="px-2.5 py-1.5 rounded-xl text-[11px] font-bold bg-emerald-400 text-black">
                    🕒 Theo giờ thực
                </button>
                <button id="env-btn-day" onclick="setFlightEnvironment('day')" class="px-2 py-1.5 rounded-xl text-[11px] font-bold text-slate-300 hover:text-white">
                    ☀️ Ngày
                </button>
                <button id="env-btn-sunset" onclick="setFlightEnvironment('sunset')" class="px-2 py-1.5 rounded-xl text-[11px] font-bold text-slate-300 hover:text-white">
                    🌅 Hoàng hôn
                </button>
                <button id="env-btn-night" onclick="setFlightEnvironment('night')" class="px-2 py-1.5 rounded-xl text-[11px] font-bold text-slate-300 hover:text-white">
                    🌙 Bay Đêm
                </button>
                <button id="env-btn-rain" onclick="setFlightEnvironment('rain')" class="px-2 py-1.5 rounded-xl text-[11px] font-bold text-slate-300 hover:text-white">
                    🌧️ Mưa Đêm
                </button>
            </div>
        </div>

        <!-- ================= GÓC NHÌN 2: BUỒNG LÁI PHI CÔNG (COCKPIT HUD VIEW) ================= -->
        <div id="view-cockpit" class="fixed inset-x-0 top-14 bottom-0 z-20 hidden flex-col justify-between overflow-hidden">
            <div id="cockpit-sky-bg" class="absolute inset-0 bg-gradient-to-b from-[#040b1a] via-[#0c2249] to-[#1e3a8a] transition-all duration-700">
                <div id="cockpit-stars" class="absolute inset-0 opacity-90" style="background-image: radial-gradient(white 1px, transparent 1px), radial-gradient(rgba(255,255,255,0.7) 1.5px, transparent 1.5px); background-size: 55px 55px, 95px 95px;"></div>
                <div class="cloud-anim-1 absolute top-1/3 w-96 h-24 bg-white/10 blur-2xl rounded-full"></div>
                <div class="cloud-anim-2 absolute top-1/2 w-[500px] h-28 bg-cyan-300/10 blur-3xl rounded-full"></div>
                <div id="cockpit-rain-layer" class="rain-overlay absolute inset-0 hidden pointer-events-none"></div>
            </div>

            <div class="relative z-10 flex-1 flex items-center justify-center pointer-events-none mt-10">
                <div class="absolute inset-y-0 left-1/2 -translate-x-1/2 w-4 bg-gradient-to-r from-slate-950 via-slate-800 to-slate-950 border-x border-white/10"></div>

                <!-- Màn hình HUD -->
                <div class="w-[320px] sm:w-[440px] h-[230px] sm:h-[260px] border-2 border-emerald-400/50 rounded-3xl bg-emerald-950/15 backdrop-blur-[1px] p-4 flex flex-col justify-between shadow-[0_0_50px_rgba(16,185,129,0.15)]">
                    <div class="flex justify-between items-center text-[11px] font-mono font-bold text-emerald-400 border-b border-emerald-400/30 pb-1">
                        <span>SPD: <b id="hud-speed">840 KM/H</b></span>
                        <span class="bg-emerald-400/20 px-2 py-0.5 rounded border border-emerald-400/40">HDG <b id="hud-heading">045°</b></span>
                        <span>ALT: <b id="hud-alt">36,000 FT</b></span>
                    </div>

                    <div class="relative flex-1 flex items-center justify-center overflow-hidden my-1">
                        <div class="hud-horizon w-52 flex flex-col items-center space-y-2.5">
                            <div class="w-28 border-b border-dashed border-emerald-400/60 text-[9px] font-mono text-emerald-400 flex justify-between"><span>+10</span><span>+10</span></div>
                            <div class="w-44 border-b-2 border-emerald-400 text-[10px] font-mono text-emerald-300 flex justify-between"><span>0</span><span>PITCH</span><span>0</span></div>
                            <div class="w-28 border-b border-dashed border-emerald-400/60 text-[9px] font-mono text-emerald-400 flex justify-between"><span>-10</span><span>-10</span></div>
                        </div>
                        <div class="absolute text-emerald-300 font-mono font-black text-base">─ ✛ ─</div>
                    </div>

                    <div class="flex justify-between items-center text-[10px] font-mono text-emerald-300 border-t border-emerald-400/30 pt-1">
                        <span id="hud-aircraft-name">AIRBUS A321NEO</span>
                        <span id="hud-route-code">SGN ➔ DAD</span>
                    </div>
                </div>
            </div>

            <!-- Táp-lô Buồng lái -->
            <div class="relative z-10 h-44 bg-gradient-to-t from-[#05070e] via-[#0d1322] to-[#1a243b] border-t-4 border-slate-700/80 px-4 py-2.5 shadow-2xl">
                <div class="max-w-3xl mx-auto grid grid-cols-3 gap-3 h-24">
                    <div class="bg-[#060a12] border border-slate-700 rounded-xl p-2 flex flex-col justify-between font-mono">
                        <div class="text-[9px] text-cyan-400 font-bold flex justify-between"><span>PFD</span><span class="text-emerald-400">AP1+FD</span></div>
                        <div class="flex items-center justify-center"><div id="cockpit-plane-svg-preview" class="w-10 h-10"></div></div>
                        <div class="text-[9px] text-slate-400 flex justify-between"><span id="cockpit-real-clock">00:00</span><span>ETA <b id="cockpit-eta">--:--</b></span></div>
                    </div>

                    <div class="bg-[#060a12] border border-cyan-500/40 rounded-xl p-2 flex flex-col items-center justify-center font-mono">
                        <div class="text-[8px] text-amber-400 uppercase font-bold">DISTANCE TIMER</div>
                        <div id="cockpit-timer-display" class="text-xl sm:text-2xl font-extrabold text-white">56:00</div>
                        <div id="cockpit-task-display" class="text-[9px] text-cyan-300 truncate max-w-[140px]">💻 Work</div>
                    </div>

                    <div class="bg-[#060a12] border border-slate-700 rounded-xl p-2 flex flex-col justify-between font-mono relative overflow-hidden">
                        <div class="text-[9px] text-emerald-400 font-bold flex justify-between"><span>RADAR</span><span id="cockpit-dist-display">610 KM</span></div>
                        <div class="w-11 h-11 rounded-full border border-emerald-500/40 mx-auto flex items-center justify-center relative">
                            <div class="radar-ring absolute inset-0 rounded-full border border-emerald-400"></div>
                            <span class="text-[10px]">✈️</span>
                        </div>
                        <div class="text-[8px] text-slate-400 text-center">WX + TCAS ON</div>
                    </div>
                </div>
            </div>
        </div>

        <!-- ================= GÓC NHÌN 3: TRONG KHOANG CABIN (CABIN INTERIOR VIEW) ================= -->
        <div id="view-cabin" class="fixed inset-x-0 top-14 bottom-0 z-20 hidden flex-col items-center justify-center bg-gradient-to-b from-[#131129] via-[#0e172a] to-[#060913] p-4 overflow-hidden">
            <div id="cabin-ceiling-glow" class="absolute top-0 inset-x-0 h-32 bg-gradient-to-b from-purple-500/30 via-cyan-500/15 to-transparent blur-2xl pointer-events-none transition-all duration-700"></div>

            <div class="relative z-10 flex items-center gap-2 mb-3">
                <div class="bg-slate-900/90 border border-white/15 px-3 py-1 rounded-full flex items-center gap-2 text-[11px]">
                    <span class="text-amber-400 font-bold">🔔 FASTEN SEATBELT</span>
                    <span class="text-slate-600">|</span>
                    <span class="text-cyan-300 font-mono" id="cabin-real-clock">00:00:00</span>
                </div>
                <button onclick="cycleCabinMoodLight()" class="bg-white/10 hover:bg-white/20 border border-white/20 px-3 py-1 rounded-full text-[11px] font-bold text-cyan-300">
                    🌈 Đổi đèn LED Cabin
                </button>
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
                            <div class="text-[10px] text-slate-400 uppercase font-bold">Mục tiêu phiên bay</div>
                            <div id="cabin-task-title" class="text-sm font-extrabold text-white mt-0.5 truncate">💻 Work</div>
                            <div class="text-[11px] text-emerald-400 mt-1">👤 <b id="cabin-passenger-name">Hữu Đại</b></div>
                            <div class="text-[10px] text-slate-400 font-mono mt-1">Hạ cánh dự kiến: <b id="cabin-eta" class="text-amber-300">--:--</b></div>
                        </div>

                        <div class="bg-slate-900/90 border border-white/10 rounded-xl p-2.5 text-center">
                            <div class="text-[9px] text-slate-400 uppercase">Thời gian bay còn lại</div>
                            <div id="cabin-timer-display" class="text-2xl font-black text-cyan-400 mono">56:00</div>
                            <div class="text-[10px] text-amber-300">Còn <span id="cabin-dist-display">610</span> km</div>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- ================= GÓC NHÌN 4: QUA CỬA SỔ MÁY BAY (WINDOW SEAT VIEW) ================= -->
        <div id="view-window" class="fixed inset-x-0 top-14 bottom-0 z-20 hidden flex-col items-center justify-center bg-[#090d18] p-4 overflow-hidden">
            <div class="relative z-20 flex items-center gap-3 mb-2">
                <button onclick="toggleWindowShade()" class="glass-panel px-3.5 py-1 rounded-full text-xs font-extrabold text-amber-300 hover:text-white border border-amber-400/30">
                    🪟 Kéo Rèm Cửa Sổ Lên / Xuống
                </button>
            </div>

            <div class="relative w-[280px] sm:w-[330px] h-[360px] sm:h-[400px] rounded-[150px] border-[16px] border-[#1e293b] shadow-[inset_0_0_40px_rgba(0,0,0,0.9),0_25px_70px_rgba(0,0,0,0.95)] overflow-hidden bg-gradient-to-b from-[#040b1d] via-[#0f2557] to-[#1e3a8a] mb-20" id="window-sky-container">
                <div id="window-stars" class="absolute inset-0 opacity-90" style="background-image: radial-gradient(white 1.2px, transparent 1.2px), radial-gradient(rgba(255,255,255,0.6) 1px, transparent 1px); background-size: 45px 45px, 80px 80px;"></div>
                <div id="window-celestial" class="absolute top-10 right-12 w-11 h-11 rounded-full bg-yellow-100 shadow-[0_0_35px_#fef08a]"></div>
                <div class="cloud-anim-1 absolute top-36 w-64 h-14 bg-white/20 blur-xl rounded-full"></div>
                <div class="cloud-anim-3 absolute bottom-24 w-72 h-16 bg-white/15 blur-xl rounded-full"></div>
                <div id="window-city-lights" class="absolute bottom-0 inset-x-0 h-14 bg-gradient-to-t from-amber-500/25 via-orange-500/10 to-transparent"></div>

                <!-- Cánh máy bay nhìn từ cửa sổ -->
                <div class="absolute bottom-10 right-0 w-[240px] h-[125px] pointer-events-none">
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

        <!-- Nút thu gọn bảng đặt vé -->
        <button id="toggle-booking-btn" onclick="toggleBookingCardSize()" class="fixed bottom-3 left-3 z-30 glass-panel px-3 py-1.5 rounded-xl text-[11px] font-extrabold text-cyan-300 hover:text-white shadow-lg border border-cyan-500/30">
            🔽 Thu gọn bảng
        </button>

        <!-- MÀN HÌNH 1 TRONG TRẠM BAY: BẢNG ĐẶT VÉ TỰ ĐỘNG TÍNH THỜI GIAN HỌC THEO KHOẢNG CÁCH -->
        <div id="screen-booking" class="fixed bottom-3 left-1/2 -translate-x-1/2 z-30 w-[95%] max-w-md glass-panel rounded-3xl p-3.5 shadow-2xl transition-all duration-300">
            <!-- Hàng 1: Mô hình Tàu bay + Quãng đường + Thời gian tự tính -->
            <div class="flex items-center justify-between gap-2 mb-2.5 pb-2 border-b border-white/10">
                <div class="flex items-center gap-2.5">
                    <div id="booking-plane-svg-box" class="w-10 h-10 rounded-xl bg-slate-900 border border-cyan-400/30 flex items-center justify-center p-1 shrink-0"></div>
                    <div>
                        <div class="flex items-center gap-1.5">
                            <span id="badge-origin" class="bg-cyan-400 text-black font-black text-[10px] px-1.5 py-0.5 rounded">SGN</span>
                            <span class="text-xs text-slate-400">➔</span>
                            <span id="badge-dest" class="bg-yellow-400 text-black font-black text-[10px] px-1.5 py-0.5 rounded">DAD</span>
                            <span id="badge-dist" class="text-[11px] font-mono text-cyan-300 font-bold ml-1">610 km</span>
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

            <!-- Hàng 2: Chọn Điểm Đi & Điểm Đến -->
            <div class="grid grid-cols-11 gap-1.5 items-center bg-slate-900/90 p-2 rounded-2xl border border-white/10 mb-2.5">
                <div class="col-span-5">
                    <div class="text-[9px] text-slate-400 uppercase font-bold mb-0.5">Điểm khởi hành</div>
                    <select id="origin-select" onchange="onRouteChange()" class="w-full bg-slate-800 text-white font-bold text-[11px] px-2 py-1.5 rounded-lg border border-white/10 focus:outline-none cursor-pointer"></select>
                </div>
                <div class="col-span-1 flex justify-center pt-3">
                    <button onclick="swapRoute()" class="w-7 h-7 rounded-full bg-slate-800 hover:bg-blue-600 text-cyan-400 hover:text-white font-bold text-xs flex items-center justify-center transition border border-white/10">⇄</button>
                </div>
                <div class="col-span-5">
                    <div class="text-[9px] text-yellow-400 uppercase font-bold mb-0.5">Điểm hạ cánh</div>
                    <select id="dest-select" onchange="onRouteChange()" class="w-full bg-slate-800 text-white font-bold text-[11px] px-2 py-1.5 rounded-lg border border-yellow-400/40 focus:outline-none cursor-pointer"></select>
                </div>
            </div>

            <!-- Hàng 3: Bảng Thời Gian Học Tự Động Theo Khoảng Cách & Giờ Thực Tế -->
            <div class="bg-blue-950/50 border border-cyan-400/30 rounded-2xl p-2.5 mb-2.5 flex items-center justify-between">
                <div>
                    <div class="text-[9px] text-cyan-300 font-bold uppercase tracking-wider">⏱️ Thời gian học (Tính theo khoảng cách)</div>
                    <div class="flex items-baseline gap-2 mt-0.5">
                        <span id="auto-calc-duration-text" class="text-base font-black text-yellow-400 mono">56 phút</span>
                        <span id="auto-calc-speed-text" class="text-[10px] text-slate-300">(610 km • 840 km/h)</span>
                    </div>
                </div>
                <div class="text-right font-mono">
                    <div class="text-[9px] text-slate-400">Hạ cánh dự kiến (ETA)</div>
                    <div id="booking-realtime-eta" class="text-xs font-extrabold text-emerald-400">--:--</div>
                </div>
            </div>

            <div class="flex gap-2">
                <button onclick="randomRoute()" class="bg-slate-800 hover:bg-slate-700 text-cyan-300 font-bold px-3 py-2.5 rounded-2xl text-xs border border-white/10 shrink-0" title="Đổi chặng ngẫu nhiên">
                    🎲 Đổi chặng
                </button>
                <button onclick="goToSeatSelection()" class="flex-1 bg-gradient-to-r from-blue-600 to-cyan-500 hover:opacity-95 text-white font-extrabold py-2.5 rounded-2xl shadow-lg shadow-blue-600/30 transition flex items-center justify-center gap-1.5 text-xs uppercase tracking-wider">
                    <span>Chọn Ghế & Bắt Đầu Tập Trung</span>
                    <span>➔</span>
                </button>
            </div>
        </div>

        <!-- MÀN HÌNH 2 TRONG TRẠM BAY: CHỌN GHẾ NGỒI -->
        <div id="screen-seat" class="fixed inset-x-0 top-14 bottom-0 z-30 bg-[#070b14]/95 backdrop-blur-xl hidden flex-col items-center justify-between py-3 px-4">
            <div class="w-full max-w-md flex items-center justify-between">
                <button onclick="backToBooking()" class="bg-slate-800 hover:bg-slate-700 text-slate-200 px-3 py-1.5 rounded-xl text-xs font-bold">‹ Đổi chặng bay</button>
                <div class="text-center">
                    <div id="seat-header-aircraft" class="text-[10px] text-cyan-400 font-extrabold uppercase tracking-widest">AIRBUS A321NEO</div>
                    <div id="seat-header-route" class="text-xs font-extrabold text-white">SGN ➔ DAD • 56 phút</div>
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

            <!-- POPUP "What do you want to focus?" -->
            <div id="focus-popover-backdrop" class="fixed inset-0 z-40 bg-black/65 backdrop-blur-sm hidden items-center justify-center p-4">
                <div class="focus-popover w-full max-w-[350px] rounded-[26px] p-5 text-white">
                    <div class="flex justify-between items-center mb-1">
                        <span class="text-xs font-bold text-blue-300">Seat: <span id="pop-seat-code" class="mono text-white">06A</span></span>
                        <button onclick="closeFocusPopover()" class="text-slate-400 hover:text-white text-sm font-bold">✕</button>
                    </div>
                    <h3 class="text-sm font-extrabold text-white mb-3">Bạn muốn tập trung làm gì trên chuyến bay này?</h3>

                    <div class="flex flex-wrap gap-1.5 mb-3" id="focus-pills-container"></div>

                    <div id="custom-focus-box" class="mb-3">
                        <label class="block text-[10px] text-slate-300 font-bold mb-1">Tên công việc / môn học cụ thể:</label>
                        <input type="text" id="custom-focus-input" placeholder="Nhập mục tiêu (VD: Tạo app, Giải đề...)" class="w-full bg-slate-900/90 text-xs text-white px-3 py-2 rounded-xl border border-blue-400/40 focus:outline-none" />
                    </div>

                    <div class="bg-red-500/15 border border-red-400/30 p-2.5 rounded-2xl flex items-center justify-between mb-3.5">
                        <div>
                            <div class="text-xs font-extrabold text-red-200">🔒 Khóa Kỷ Luật (Strict Mode)</div>
                            <div class="text-[10px] text-slate-300">Báo động đỏ nếu rời khỏi màn hình học</div>
                        </div>
                        <input type="checkbox" id="strict-mode-toggle" checked class="w-4 h-4 accent-red-500 cursor-pointer" />
                    </div>

                    <button onclick="confirmSeatAndFocus()" class="w-full bg-gradient-to-r from-blue-600 to-cyan-500 hover:opacity-95 text-white font-extrabold py-3 rounded-2xl text-xs shadow-lg">
                        Xác nhận Ghế & Xuất Vé Máy Bay ➔
                    </button>
                </div>
            </div>

            <div class="w-full max-w-md flex items-center justify-between px-2">
                <div class="text-xs text-slate-400">Chạm vào ghế bất kỳ hoặc bấm Tiếp tục</div>
                <button onclick="showBoardingPass()" class="bg-blue-600 hover:bg-blue-500 text-white font-extrabold px-5 py-2 rounded-xl text-xs shadow-lg">Tiếp tục ➔</button>
            </div>
        </div>

        <!-- MÀN HÌNH 3 TRONG TRẠM BAY: VÉ BOARDING PASS THỜI GIAN THỰC -->
        <div id="screen-ticket" class="fixed inset-x-0 top-14 bottom-0 z-40 bg-black/85 backdrop-blur-md hidden items-center justify-center p-4">
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
                                <div class="text-[9px] text-slate-400 uppercase">Hành khách</div>
                                <div id="tk-passenger" class="text-sm font-black text-amber-300 uppercase">HỮU ĐẠI</div>
                            </div>
                            <div class="text-right">
                                <div class="text-[9px] text-slate-400 uppercase">Giờ thực tế (STD ➔ ETA)</div>
                                <div id="tk-realtime-span" class="text-xs font-extrabold text-emerald-400 mono">14:45 ➔ 15:41</div>
                            </div>
                        </div>

                        <div class="flex justify-between items-center my-3">
                            <div>
                                <div id="tk-origin-code" class="text-3xl font-black text-white">SGN</div>
                                <div id="tk-origin-name" class="text-[11px] text-slate-400">TP.HCM</div>
                            </div>
                            <div class="flex flex-col items-center">
                                <div id="tk-plane-svg" class="w-8 h-8"></div>
                                <span id="tk-duration" class="text-xs font-extrabold text-yellow-400 mt-0.5">56 phút</span>
                            </div>
                            <div class="text-right">
                                <div id="tk-dest-code" class="text-3xl font-black text-yellow-400">DAD</div>
                                <div id="tk-dest-name" class="text-[11px] text-slate-400">Đà Nẵng</div>
                            </div>
                        </div>

                        <div class="grid grid-cols-3 gap-2 pt-3 border-t border-white/10 text-xs mb-4">
                            <div>
                                <div class="text-slate-500 text-[9px] uppercase">Ghế ngồi</div>
                                <div id="tk-seat" class="font-extrabold text-cyan-400 mt-0.5 mono">06A</div>
                            </div>
                            <div>
                                <div class="text-slate-500 text-[9px] uppercase">Khoảng cách</div>
                                <div id="tk-dist" class="font-bold text-white mt-0.5">610 km</div>
                            </div>
                            <div class="text-right">
                                <div class="text-slate-500 text-[9px] uppercase">Mục tiêu</div>
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
                    <button onclick="backToSeatFromTicket()" class="w-1/3 bg-slate-800 hover:bg-slate-700 text-slate-300 font-bold py-3 rounded-2xl text-xs">‹ Đổi ghế</button>
                    <button onclick="startFlight()" class="w-2/3 bg-gradient-to-r from-emerald-500 to-cyan-500 hover:opacity-95 text-black font-black py-3 rounded-2xl shadow-xl text-xs uppercase tracking-wider">
                        🛫 Cất Cánh Bắt Đầu Học
                    </button>
                </div>
            </div>
        </div>

        <!-- MÀN HÌNH 4 TRONG TRẠM BAY: ĐANG BAY & ĐẾM NGƯỢC THEO KHOẢNG CÁCH THỰC -->
        <div id="screen-flying" class="fixed bottom-3 left-1/2 -translate-x-1/2 z-30 w-[95%] max-w-lg glass-panel rounded-3xl p-3.5 shadow-2xl hidden">
            <div class="flex items-center justify-between border-b border-white/10 pb-2 mb-2">
                <div class="flex items-center gap-2.5">
                    <div id="fly-mini-svg" class="w-9 h-9 rounded-xl bg-slate-900 border border-cyan-400/40 p-1 flex items-center justify-center"></div>
                    <div>
                        <div class="text-xs font-extrabold text-white" id="fly-route-text">TP.HCM ➔ Đà Nẵng</div>
                        <div class="text-[10px] text-cyan-400 font-semibold" id="fly-sub-info">Airbus A321neo • Ghế 06A</div>
                    </div>
                </div>
                <div class="text-right">
                    <div class="text-[9px] text-slate-400 font-mono">Hạ cánh lúc <b id="fly-eta-badge" class="text-amber-300">--:--</b></div>
                    <div id="safety-hearts" class="text-xs tracking-widest mt-0.5">❤️❤️❤️</div>
                </div>
            </div>

            <div class="flex items-end justify-between">
                <div>
                    <div class="text-[9px] uppercase tracking-widest text-slate-400 flex items-center gap-2">
                        <span>Thời gian bay còn lại</span>
                        <span id="telemetry-live-badge" class="text-[9px] text-emerald-400 font-mono">● 840 KM/H</span>
                    </div>
                    <div id="countdown-timer" class="mono text-2xl sm:text-3xl font-extrabold text-white tracking-tight">56:00</div>
                </div>
                <div class="text-right">
                    <div class="text-[11px] text-slate-300 font-semibold mb-1">Còn <span id="fly-dist-left" class="text-yellow-400 font-bold">610</span> km</div>
                    <div class="flex gap-1.5">
                        <button onclick="centerOnPlane()" class="bg-slate-800 hover:bg-slate-700 text-xs px-2.5 py-1.5 rounded-xl text-slate-200 border border-white/10 font-bold" title="Theo dõi máy bay">🎯</button>
                        <button onclick="completeFlightEarly()" class="bg-emerald-500/20 hover:bg-emerald-500/30 text-emerald-300 border border-emerald-500/30 px-2.5 py-1.5 rounded-xl text-xs font-bold">✓ Xong sớm</button>
                        <button onclick="abortFlight()" class="bg-red-500/20 hover:bg-red-500/30 text-red-300 border border-red-500/30 px-2.5 py-1.5 rounded-xl text-xs font-bold">Hủy</button>
                    </div>
                </div>
            </div>

            <div class="w-full bg-slate-800 h-2 rounded-full overflow-hidden mt-2.5">
                <div id="flight-progress" class="bg-gradient-to-r from-blue-500 via-cyan-400 to-yellow-400 h-full w-0 transition-all duration-500"></div>
            </div>
        </div>
    </section>

    <!-- ================= MODAL GIẢI THÍCH "TẠI SAO LẠI CÓ LỊCH NÀY?" ================= -->
    <div id="why-schedule-modal" class="fixed inset-0 z-50 bg-black/75 backdrop-blur-md hidden items-center justify-center p-4">
        <div class="glass-panel w-full max-w-md rounded-3xl p-5 shadow-2xl border border-cyan-400/40">
            <div class="flex justify-between items-center mb-3">
                <h3 class="text-sm font-extrabold text-white">🧠 Tại sao AI xếp lịch & chặng bay này?</h3>
                <button onclick="closeWhyModal()" class="text-slate-400 hover:text-white font-bold">✕</button>
            </div>
            <div id="why-modal-content" class="space-y-2.5 text-xs text-slate-200"></div>
            <button onclick="closeWhyModal()" class="mt-4 w-full bg-gradient-to-r from-blue-600 to-cyan-500 text-white font-extrabold py-2.5 rounded-xl text-xs">Đã hiểu</button>
        </div>
    </div>

    <!-- ================= CẢNH BÁO ĐỎ STRICT MODE KHI CHUYỂN TAB ================= -->
    <div id="turbulence-modal" class="fixed inset-0 z-50 turbulence-alert hidden flex-col items-center justify-center p-6 text-center">
        <div class="text-5xl mb-2 animate-bounce">🚨</div>
        <h2 class="text-xl sm:text-2xl font-black text-white uppercase mb-2">CẢNH BÁO: BẠN ĐÃ RỜI KHỎI BUỒNG LÁI TẬP TRUNG!</h2>
        <p class="text-xs sm:text-sm text-red-100 max-w-md mb-4">Đồng hồ tập trung đã bị <b>TẠM DỪNG</b> vì bạn vừa chuyển sang cửa sổ khác!</p>
        <div class="bg-black/50 border border-red-300/30 rounded-2xl p-3.5 w-full max-w-xs mb-5">
            <div class="text-[11px] text-red-200 uppercase font-bold">Số lần vi phạm kỷ luật</div>
            <div id="violation-count-text" class="text-xl font-black text-yellow-400 mono">1 / 3 LẦN</div>
        </div>
        <button onclick="resumeFromTurbulence()" class="bg-white hover:bg-yellow-300 text-red-900 font-black px-6 py-3.5 rounded-2xl shadow-2xl text-xs uppercase">
            🔒 Quay lại Học tiếp ngay
        </button>
    </div>

    <div id="crash-modal" class="fixed inset-0 z-50 bg-black/95 backdrop-blur-xl hidden flex-col items-center justify-center p-6 text-center">
        <div class="text-5xl mb-2">💥</div>
        <h2 class="text-xl font-black text-red-500 uppercase mb-2">CHUYẾN BAY BỊ HỦY DO MẤT TẬP TRUNG QUÁ 3 LẦN</h2>
        <button onclick="closeCrashModal()" class="mt-4 bg-red-600 hover:bg-red-500 text-white font-extrabold px-6 py-3 rounded-2xl text-xs uppercase">Quay lại</button>
    </div>

    <!-- MODAL TÙY CHỈNH ÂM THANH & BOT -->
    <div id="media-modal" class="fixed inset-0 z-50 bg-black/75 backdrop-blur-md hidden items-center justify-center p-4">
        <div class="glass-panel w-full max-w-md rounded-3xl p-5 shadow-2xl">
            <div class="flex justify-between items-center mb-3">
                <h3 class="text-sm font-extrabold text-white">🎧 Tùy Chỉnh Âm Thanh & Giao Diện</h3>
                <button onclick="closeMediaModal()" class="text-slate-400 hover:text-white text-lg font-bold">✕</button>
            </div>
            <div class="space-y-3 text-xs">
                <div class="bg-slate-900/90 p-3 rounded-2xl border border-white/10">
                    <label class="font-bold text-cyan-400 block mb-1">1. Chọn file nhạc Lofi từ máy (.mp3, .wav):</label>
                    <input type="file" accept="audio/*" onchange="handleLocalAudio(this)" class="w-full text-slate-300 file:mr-2 file:py-1 file:px-3 file:rounded-xl file:border-0 file:font-bold file:bg-blue-600 file:text-white cursor-pointer mb-1.5" />
                    <input type="text" id="audio-url-input" placeholder="Hoặc dán link MP3..." class="w-full bg-slate-800 text-white px-3 py-1.5 rounded-xl border border-white/10" />
                </div>

                <div class="bg-slate-900/90 p-3 rounded-2xl border border-white/10 flex items-center justify-between">
                    <div>
                        <div class="font-bold text-white">🛫 Tiếng động cơ máy bay (Cabin White Noise)</div>
                        <div class="text-[10px] text-slate-400">Giúp tập trung sâu như ngồi trên máy bay thật</div>
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

    <!-- ================= CHATBOT AI VÀNG KIM GÓC DƯỚI PHẢI ================= -->
    <div id="chatbot-launcher" onclick="toggleChatbotWindow()" class="fixed bottom-3 right-3 z-40 w-13 h-13 rounded-full bg-white p-1 cursor-pointer bot-launcher-glow flex items-center justify-center border-2 border-[#d4a349]" style="width:52px;height:52px;">
        <img id="bot-launcher-img" src="https://cdn-icons-png.flaticon.com/512/4712/4712109.png" class="w-full h-full rounded-full object-cover bg-gradient-to-b from-yellow-300 to-amber-500 p-1" />
        <span class="absolute -top-0.5 -right-0.5 w-3 h-3 bg-emerald-500 border-2 border-white rounded-full"></span>
    </div>

    <div id="chatbot-window" class="fixed bottom-20 right-4 z-50 w-[330px] sm:w-[355px] h-[440px] bg-[#f8f9fa] text-slate-800 rounded-2xl shadow-2xl border border-[#d4a349]/50 hidden flex-col overflow-hidden">
        <div class="bg-[#d4a349] text-white px-4 py-2.5 flex items-center justify-between shadow">
            <div class="flex items-center gap-2">
                <div class="w-7 h-7 rounded-full bg-white p-0.5 shadow">
                    <img id="bot-header-img" src="https://cdn-icons-png.flaticon.com/512/4712/4712109.png" class="w-full h-full rounded-full object-cover bg-amber-400" />
                </div>
                <span class="font-bold text-xs">Trợ lý Học tập AI</span>
            </div>
            <div class="flex items-center gap-3 text-white">
                <button onclick="resetChat()" title="Làm mới" class="text-xs font-bold">↺</button>
                <button onclick="toggleChatbotWindow()" class="text-base font-bold leading-none">✕</button>
            </div>
        </div>

        <div id="chat-messages" class="flex-1 p-3 overflow-y-auto space-y-2.5 bg-[#f7f8fc]"></div>

        <div class="px-2.5 py-1.5 bg-white border-t border-slate-100 flex gap-1.5 overflow-x-auto">
            <button onclick="sendQuickChat('Hôm nay mình nên học gì?')" class="shrink-0 bg-amber-50 hover:bg-amber-100 text-[#b07d2b] border border-[#d4a349]/40 text-[10px] font-semibold px-2 py-1 rounded-full">💡 Hôm nay học gì?</button>
            <button onclick="sendQuickChat('Kiểm tra công việc chưa xong')" class="shrink-0 bg-amber-50 hover:bg-amber-100 text-[#b07d2b] border border-[#d4a349]/40 text-[10px] font-semibold px-2 py-1 rounded-full">📋 Việc đang làm</button>
            <button onclick="sendQuickChat('Mình có lịch đột xuất')" class="shrink-0 bg-amber-50 hover:bg-amber-100 text-[#b07d2b] border border-[#d4a349]/40 text-[10px] font-semibold px-2 py-1 rounded-full">🌪️ Dời lịch</button>
        </div>

        <div class="p-2 bg-white border-t border-slate-200 flex items-center gap-2">
            <input type="text" id="chat-input" onkeydown="if(event.key==='Enter') sendChatMessage()" placeholder="Nhập tin nhắn..." class="flex-1 text-xs text-slate-800 px-2 py-1 focus:outline-none" />
            <button onclick="sendChatMessage()" class="w-7 h-7 rounded-full bg-[#d4a349] hover:bg-[#c29138] text-white flex items-center justify-center shadow text-xs">➤</button>
        </div>
    </div>

    <script>
        // ================= 1. KHAI BÁO TOÀN BỘ BIẾN TRẠNG THÁI Ở ĐẦU FILE (CHỐNG LỖI) =================
        const AIRPORTS = [
            // 22 Sân bay Việt Nam
            { code: "SGN", name: "TP.HCM (Tân Sơn Nhất)", group: "VN", coords: [10.8188, 106.6519] },
            { code: "HAN", name: "Hà Nội (Nội Bài)", group: "VN", coords: [21.2212, 105.8072] },
            { code: "DAD", name: "Đà Nẵng", group: "VN", coords: [16.0439, 108.1994] },
            { code: "CXR", name: "Cam Ranh (Khánh Hòa)", group: "VN", coords: [11.9982, 109.2194] },
            { code: "UIH", name: "Phù Cát (Quy Nhơn)", group: "VN", coords: [13.9550, 109.0422] },
            { code: "LTH", name: "Long Thành (Đồng Nai)", group: "VN", coords: [10.7850, 107.0650] },
            { code: "PQC", name: "Phú Quốc (Kiên Giang)", group: "VN", coords: [10.1698, 103.9931] },
            { code: "DLI", name: "Đà Lạt (Liên Khương)", group: "VN", coords: [11.7500, 108.3667] },
            { code: "HPH", name: "Hải Phòng (Cát Bi)", group: "VN", coords: [20.8194, 106.7250] },
            { code: "VII", name: "Vinh (Nghệ An)", group: "VN", coords: [18.7376, 105.6708] },
            { code: "HUI", name: "Huế (Phú Bài)", group: "VN", coords: [16.4015, 107.7026] },
            { code: "VCA", name: "Cần Thơ", group: "VN", coords: [10.0851, 105.7119] },
            { code: "VDH", name: "Đồng Hới (Quảng Bình)", group: "VN", coords: [17.5150, 106.5905] },
            { code: "THD", name: "Thanh Hóa (Thọ Xuân)", group: "VN", coords: [19.9017, 105.4678] },
            { code: "VDO", name: "Vân Đồn (Quảng Ninh)", group: "VN", coords: [21.1178, 107.4142] },
            { code: "VCL", name: "Chu Lai (Quảng Nam)", group: "VN", coords: [15.4061, 108.7056] },
            { code: "TBB", name: "Tuy Hòa (Phú Yên)", group: "VN", coords: [13.0494, 109.3336] },
            { code: "BMV", name: "Buôn Ma Thuột (Đắk Lắk)", group: "VN", coords: [12.6683, 108.1200] },
            { code: "PXU", name: "Pleiku (Gia Lai)", group: "VN", coords: [14.0045, 108.0172] },
            { code: "VCS", name: "Côn Đảo (Bà Rịa - VT)", group: "VN", coords: [8.7325, 106.6336] },
            { code: "DIN", name: "Điện Biên Phủ", group: "VN", coords: [21.3975, 103.0078] },
            { code: "CAH", name: "Cà Mau", group: "VN", coords: [9.1756, 105.1794] },
            // 12 Sân bay Quốc tế
            { code: "BKK", name: "Bangkok (Thái Lan)", group: "INT", coords: [13.6900, 100.7501] },
            { code: "SIN", name: "Singapore (Changi)", group: "INT", coords: [1.3644, 103.9915] },
            { code: "KUL", name: "Kuala Lumpur (Malaysia)", group: "INT", coords: [2.7456, 101.7072] },
            { code: "TPE", name: "Đài Bắc (Đài Loan)", group: "INT", coords: [25.0797, 121.2342] },
            { code: "HKG", name: "Hong Kong", group: "INT", coords: [22.3080, 113.9185] },
            { code: "ICN", name: "Seoul Incheon (Hàn Quốc)", group: "INT", coords: [37.4602, 126.4407] },
            { code: "HND", name: "Tokyo Haneda (Nhật Bản)", group: "INT", coords: [35.5494, 139.7798] },
            { code: "MNL", name: "Manila (Philippines)", group: "INT", coords: [14.5086, 121.0194] },
            { code: "PEK", name: "Bắc Kinh (Trung Quốc)", group: "INT", coords: [40.0799, 116.6031] },
            { code: "SYD", name: "Sydney (Úc)", group: "INT", coords: [-33.9399, 151.1753] },
            { code: "CDG", name: "Paris (Pháp)", group: "INT", coords: [49.0097, 2.5479] },
            { code: "JFK", name: "New York (Mỹ)", group: "INT", coords: [40.6413, -73.7781] }
        ];

        const FOCUS_MODES = [
            { id: "focus", label: "Focus", icon: "⚛️", color: "bg-slate-600/90 border-slate-400 text-white" },
            { id: "work", label: "Work", icon: "💻", color: "bg-blue-600 border-blue-300 text-white" },
            { id: "meditate", label: "Meditate", icon: "🧘", color: "bg-indigo-500 border-indigo-300 text-white" },
            { id: "read", label: "Read", icon: "📖", color: "bg-teal-600 border-teal-300 text-white" },
            { id: "exercise", label: "Exercise", icon: "🏃", color: "bg-sky-500 border-sky-300 text-white" }
        ];

        const DAYS_OF_WEEK = ["T2", "T3", "T4", "T5", "T6", "T7", "CN"];
        let selectedDay = "T2";
        let currentTaskFilter = "all";
        let activeTaskIdForFlight = null;

        let originAirport = AIRPORTS[0]; // SGN
        let destAirport = AIRPORTS[2];   // DAD
        let selectedAircraft = "Airbus A321neo";
        let currentDistance = 610;
        let selectedDuration = 56; // Tự động tính từ khoảng cách
        let selectedSeat = "06A";
        let selectedFocus = FOCUS_MODES[1];
        let isBookingCollapsed = false;

        let isFlying = false, strictModeEnabled = true, isPausedByViolation = false, violationCount = 0;
        const MAX_VIOLATIONS = 3;
        let alarmInterval = null, flightInterval = null, audioCtx = null, cabinNoiseNode = null;
        let remainingSeconds = 56 * 60, totalFlightSeconds = 56 * 60;
        let flightEtaString = "--:--";

        let currentCamView = "map";
        let currentEnvMode = "day";
        let isShadeClosed = false;
        let cabinMoodIdx = 0;

        // ================= 2. CÔNG THỨC TÍNH THỜI GIAN HỌC DỰA VÀO KHOẢNG CÁCH & VẬN TỐC MÁY BAY =================
        function getAircraftSpecs(aircraftType) {
            if (aircraftType.includes("787")) return { speedKmh: 910, altFt: "39,000 FT", taxiMins: 12 };
            if (aircraftType.includes("A350")) return { speedKmh: 905, altFt: "40,000 FT", taxiMins: 12 };
            if (aircraftType.includes("ATR")) return { speedKmh: 510, altFt: "22,000 FT", taxiMins: 8 };
            return { speedKmh: 840, altFt: "36,000 FT", taxiMins: 12 }; // Airbus A321neo
        }

        function calcDistanceKm(coord1, coord2) {
            const R = 6371;
            const dLat = (coord2[0] - coord1[0]) * Math.PI / 180;
            const dLon = (coord2[1] - coord1[1]) * Math.PI / 180;
            const a = Math.sin(dLat/2) * Math.sin(dLat/2) +
                      Math.cos(coord1[0]*Math.PI/180) * Math.cos(coord2[0]*Math.PI/180) *
                      Math.sin(dLon/2) * Math.sin(dLon/2);
            return Math.max(25, Math.round(R * 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a))));
        }

        // Tính tự động số phút học dựa vào Khoảng cách (km) và Vận tốc tàu bay
        function calcStudyDurationFromDistance(distKm, aircraftType) {
            const specs = getAircraftSpecs(aircraftType);
            const airMinutes = (distKm / specs.speedKmh) * 60;
            return Math.max(10, Math.round(airMinutes + specs.taxiMins));
        }

        function formatDurationLabel(mins) {
            if (mins < 60) return `${mins} phút`;
            const h = Math.floor(mins / 60);
            const m = mins % 60;
            return m > 0 ? `${h}h ${m}p (${mins} phút)` : `${h} giờ (${mins} phút)`;
        }

        // Tính giờ hạ cánh thực tế (ETA) = Giờ hiện tại + số phút bay
        function calcRealTimeETA(durationMins) {
            const now = new Date();
            const eta = new Date(now.getTime() + durationMins * 60000);
            return `${String(eta.getHours()).padStart(2,'0')}:${String(eta.getMinutes()).padStart(2,'0')}`;
        }

        // ================= 3. ĐỒNG HỒ THỜI GIAN THỰC (REAL-TIME ENGINE) =================
        function updateRealTimeClock() {
            const now = new Date();
            const hh = String(now.getHours()).padStart(2, '0');
            const mm = String(now.getMinutes()).padStart(2, '0');
            const ss = String(now.getSeconds()).padStart(2, '0');
            const dayNames = ["Chủ Nhật", "Thứ 2", "Thứ 3", "Thứ 4", "Thứ 5", "Thứ 6", "Thứ 7"];
            const dateStr = `${dayNames[now.getDay()]}, ${String(now.getDate()).padStart(2,'0')}/${String(now.getMonth()+1).padStart(2,'0')}/${now.getFullYear()}`;

            const clockEl = document.getElementById('realtime-clock');
            const dateEl = document.getElementById('realtime-date');
            if (clockEl) clockEl.innerText = `${hh}:${mm}:${ss}`;
            if (dateEl) dateEl.innerText = dateStr;

            const cClock = document.getElementById('cockpit-real-clock');
            const cbClock = document.getElementById('cabin-real-clock');
            if (cClock) cClock.innerText = `${hh}:${mm}:${ss}`;
            if (cbClock) cbClock.innerText = `${hh}:${mm}:${ss}`;

            if (!isFlying) {
                const etaStr = calcRealTimeETA(selectedDuration);
                const etaEl = document.getElementById('booking-realtime-eta');
                if (etaEl) etaEl.innerText = `${hh}:${mm} ➔ ${etaStr}`;
            }
        }
        setInterval(updateRealTimeClock, 1000);

        function syncEnvironmentWithRealTime() {
            const hour = new Date().getHours();
            if (hour >= 6 && hour < 16) setFlightEnvironment('day', true);
            else if (hour >= 16 && hour < 18) setFlightEnvironment('sunset', true);
            else setFlightEnvironment('night', true);
        }

        // ================= 4. HÀM VẼ 4 MÔ HÌNH MÁY BAY VECTOR SVG =================
        function getAircraftSVG(aircraftType, headingDeg = 0) {
            if (aircraftType.includes("787")) {
                return `
                <svg viewBox="0 0 100 100" style="transform: rotate(${headingDeg}deg);" class="w-full h-full drop-shadow-[0_6px_12px_rgba(0,0,0,0.85)]">
                    <line x1="36" y1="62" x2="36" y2="95" stroke="rgba(255,255,255,0.35)" stroke-width="2" stroke-dasharray="3,3"/>
                    <line x1="64" y1="62" x2="64" y2="95" stroke="rgba(255,255,255,0.35)" stroke-width="2" stroke-dasharray="3,3"/>
                    <rect x="32" y="46" width="7" height="14" rx="3" fill="#eab308" stroke="#fef08a" stroke-width="1"/>
                    <rect x="61" y="46" width="7" height="14" rx="3" fill="#eab308" stroke="#fef08a" stroke-width="1"/>
                    <path d="M50 34 L94 62 L98 68 L88 67 L55 52 L45 52 L12 67 L2 68 L6 62 Z" fill="#f8fafc" stroke="#eab308" stroke-width="1.5"/>
                    <path d="M50 76 L72 90 L70 94 L53 86 L47 86 L30 94 L28 90 Z" fill="#eab308"/>
                    <path d="M50 6 C55 6 57 18 57 45 L55 86 L50 95 L45 86 L43 45 C43 18 45 6 50 6 Z" fill="#ffffff" stroke="#cbd5e1" stroke-width="1"/>
                    <path d="M46 14 Q50 10 54 14 Q50 16 46 14 Z" fill="#0284c7"/>
                    <circle cx="5" cy="64" r="3" fill="#ef4444" class="strobe-light"/>
                    <circle cx="95" cy="64" r="3" fill="#22c55e" class="strobe-light"/>
                </svg>`;
            } else if (aircraftType.includes("A350")) {
                return `
                <svg viewBox="0 0 100 100" style="transform: rotate(${headingDeg}deg);" class="w-full h-full drop-shadow-[0_6px_12px_rgba(0,0,0,0.85)]">
                    <line x1="35" y1="60" x2="35" y2="95" stroke="rgba(255,255,255,0.35)" stroke-width="2" stroke-dasharray="3,3"/>
                    <line x1="65" y1="60" x2="65" y2="95" stroke="rgba(255,255,255,0.35)" stroke-width="2" stroke-dasharray="3,3"/>
                    <rect x="31" y="45" width="7" height="14" rx="3" fill="#ec4899"/>
                    <rect x="62" y="45" width="7" height="14" rx="3" fill="#ec4899"/>
                    <path d="M50 35 L92 58 L96 66 L89 64 L56 51 L44 51 L11 64 L4 66 L8 58 Z" fill="#f1f5f9" stroke="#ec4899" stroke-width="1.5"/>
                    <path d="M50 76 L72 89 L70 93 L50 86 L30 93 L28 89 Z" fill="#ec4899"/>
                    <path d="M50 5 C55 5 57 18 57 46 L55 87 L50 96 L45 87 L43 46 C43 18 45 5 50 5 Z" fill="#ffffff"/>
                    <path d="M44 13 Q50 8 56 13 Q56 17 50 15 Q44 17 44 13 Z" fill="#0f172a"/>
                    <circle cx="6" cy="62" r="3" fill="#ef4444" class="strobe-light"/>
                    <circle cx="94" cy="62" r="3" fill="#22c55e" class="strobe-light"/>
                </svg>`;
            } else if (aircraftType.includes("ATR")) {
                return `
                <svg viewBox="0 0 100 100" style="transform: rotate(${headingDeg}deg);" class="w-full h-full drop-shadow-[0_6px_12px_rgba(0,0,0,0.85)]">
                    <rect x="8" y="40" width="84" height="11" rx="4" fill="#e2e8f0" stroke="#10b981" stroke-width="1.5"/>
                    <rect x="29" y="34" width="6" height="16" rx="2" fill="#10b981"/>
                    <rect x="65" y="34" width="6" height="16" rx="2" fill="#10b981"/>
                    <circle cx="32" cy="32" r="7" fill="rgba(56,189,248,0.35)" stroke="#ffffff" stroke-width="1.5" stroke-dasharray="4,3"/>
                    <circle cx="68" cy="32" r="7" fill="rgba(56,189,248,0.35)" stroke="#ffffff" stroke-width="1.5" stroke-dasharray="4,3"/>
                    <rect x="33" y="83" width="34" height="7" rx="3" fill="#10b981"/>
                    <path d="M50 10 C54 10 55 20 55 46 L54 85 L50 93 L46 85 L45 46 C45 20 46 10 50 10 Z" fill="#ffffff"/>
                    <path d="M46 16 Q50 13 54 16 Z" fill="#0f172a"/>
                    <circle cx="10" cy="45" r="3" fill="#ef4444" class="strobe-light"/>
                    <circle cx="90" cy="45" r="3" fill="#22c55e" class="strobe-light"/>
                </svg>`;
            }
            return `
            <svg viewBox="0 0 100 100" style="transform: rotate(${headingDeg}deg);" class="w-full h-full drop-shadow-[0_6px_12px_rgba(0,0,0,0.85)]">
                <line x1="36" y1="58" x2="36" y2="94" stroke="rgba(56,189,248,0.4)" stroke-width="2" stroke-dasharray="3,3"/>
                <line x1="64" y1="58" x2="64" y2="94" stroke="rgba(56,189,248,0.4)" stroke-width="2" stroke-dasharray="3,3"/>
                <rect x="33" y="44" width="6" height="12" rx="2.5" fill="#06b6d4"/>
                <rect x="61" y="44" width="6" height="12" rx="2.5" fill="#06b6d4"/>
                <path d="M50 36 L90 56 L93 63 L87 61 L55 50 L45 50 L13 61 L7 63 L10 56 Z" fill="#f8fafc" stroke="#06b6d4" stroke-width="1.5"/>
                <path d="M50 76 L70 88 L68 92 L50 85 L32 92 L30 88 Z" fill="#06b6d4"/>
                <path d="M50 7 C54 7 56 18 56 46 L54 86 L50 95 L46 86 L44 46 C44 18 46 7 50 7 Z" fill="#ffffff"/>
                <path d="M46 14 Q50 11 54 14 Z" fill="#0284c7"/>
                <circle cx="9" cy="59" r="3" fill="#ef4444" class="strobe-light"/>
                <circle cx="91" cy="59" r="3" fill="#22c55e" class="strobe-light"/>
            </svg>`;
        }

        function calcBearingDeg(coord1, coord2) {
            const lat1 = coord1[0] * Math.PI / 180;
            const lat2 = coord2[0] * Math.PI / 180;
            const dLon = (coord2[1] - coord1[1]) * Math.PI / 180;
            const y = Math.sin(dLon) * Math.cos(lat2);
            const x = Math.cos(lat1) * Math.sin(lat2) - Math.sin(lat1) * Math.cos(lat2) * Math.cos(dLon);
            const brng = Math.atan2(y, x) * 180 / Math.PI;
            return Math.round((brng + 360) % 360);
        }

        // ================= 5. LƯU TRỮ DỮ LIỆU VĨNH VIỄN CHO 6 THÀNH VIÊN =================
        function createEmptyTimetable() {
            return { "T2": [], "T3": [], "T4": [], "T5": [], "T6": [], "T7": [], "CN": [] };
        }

        const INITIAL_CLEAN_DB = {
            lastMember: "huudai",
            members: {
                huudai:    { name: "Hữu Đại",    seat: "06A", miles: 0, flights: 0, tasks: [], timetable: createEmptyTimetable() },
                quangminh: { name: "Quang Minh", seat: "06A", miles: 0, flights: 0, tasks: [], timetable: createEmptyTimetable() },
                khanhthi:  { name: "Khánh Thi",  seat: "04F", miles: 0, flights: 0, tasks: [], timetable: createEmptyTimetable() },
                minhchau:  { name: "Minh Châu",  seat: "05A", miles: 0, flights: 0, tasks: [], timetable: createEmptyTimetable() },
                uyennhi:   { name: "Uyên Nhi",   seat: "03C", miles: 0, flights: 0, tasks: [], timetable: createEmptyTimetable() },
                vanhoang:  { name: "Văn Hoàng",  seat: "07F", miles: 0, flights: 0, tasks: [], timetable: createEmptyTimetable() }
            }
        };

        const STORAGE_KEY = "studyhub_focus_flight_clean_v3";
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
                if (ind) ind.innerHTML = `<span class="text-cyan-400">● Đã lưu lúc ${getCurrentTimeStr()}</span>`;
            } catch (e) {}
        }

        loadPersistentState();
        let currentMemberKey = appState.lastMember || "huudai";

        // ================= 6. KHỞI TẠO BẢN ĐỒ VỆ TINH LEAFLET =================
        const map = L.map('map', { zoomControl: false }).setView([14.0, 108.0], 5);
        L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}', { maxZoom: 18 }).addTo(map);
        L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/Reference/World_Boundaries_and_Places/MapServer/tile/{z}/{y}/{x}', { maxZoom: 18 }).addTo(map);

        let routeLine = null, originMarker = null, destMarker = null, planeMarker = null;

        function createAirportBadge(code, isDest) {
            const cls = isDest ? 'bg-yellow-400 text-black' : 'bg-cyan-400 text-black';
            return L.divIcon({
                className: 'badge-icon',
                html: `<div class="${cls} font-black text-[11px] px-2 py-0.5 rounded-md shadow-xl border border-black/40 flex items-center gap-1 whitespace-nowrap">✈️ ${code}</div>`,
                iconSize: [56, 24],
                iconAnchor: [28, 12]
            });
        }

        function createCustomAircraftMapIcon() {
            const brng = calcBearingDeg(originAirport.coords, destAirport.coords);
            const svgHtml = getAircraftSVG(selectedAircraft, brng);
            return L.divIcon({
                className: 'custom-plane-leaflet-icon',
                html: `
                    <div class="relative w-16 h-16 flex items-center justify-center">
                        <div class="radar-ring absolute inset-1 rounded-full border-2 border-cyan-400/70"></div>
                        <div class="w-14 h-14 relative z-10">${svgHtml}</div>
                    </div>
                `,
                iconSize: [64, 64],
                iconAnchor: [32, 32]
            });
        }

        // ================= 7. CHUYỂN ĐỔI GÓC NHÌN CAMERA & BẦU TRỜI THỜI GIAN THỰC =================
        function setCameraView(view) {
            currentCamView = view;
            ['map', 'cockpit', 'cabin', 'window'].forEach(v => {
                const btn = document.getElementById('cam-btn-' + v);
                if (btn) {
                    btn.className = (v === view)
                        ? "px-2.5 py-1.5 rounded-xl text-[11px] font-extrabold bg-cyan-500 text-black shadow transition"
                        : "px-2.5 py-1.5 rounded-xl text-[11px] font-extrabold text-slate-300 hover:text-white transition";
                }
            });

            document.getElementById('view-cockpit').classList.toggle('hidden', view !== 'cockpit');
            document.getElementById('view-cockpit').classList.toggle('flex', view === 'cockpit');

            document.getElementById('view-cabin').classList.toggle('hidden', view !== 'cabin');
            document.getElementById('view-cabin').classList.toggle('flex', view === 'cabin');

            document.getElementById('view-window').classList.toggle('hidden', view !== 'window');
            document.getElementById('view-window').classList.toggle('flex', view === 'window');

            updateCameraViewsData();
        }

        function setFlightEnvironment(mode, isAuto = false) {
            currentEnvMode = mode;
            ['auto', 'day', 'sunset', 'night', 'rain'].forEach(m => {
                const btn = document.getElementById('env-btn-' + m);
                if (btn) {
                    const active = (isAuto && m === 'auto') || (!isAuto && m === mode);
                    btn.className = active
                        ? "px-2.5 py-1.5 rounded-xl text-[11px] font-bold bg-amber-400 text-black shadow"
                        : "px-2 py-1.5 rounded-xl text-[11px] font-bold text-slate-300 hover:text-white";
                }
            });

            const mapEl = document.getElementById('map');
            mapEl.className = "";
            if (mode === 'night') mapEl.classList.add('map-night-filter');
            if (mode === 'sunset') mapEl.classList.add('map-sunset-filter');
            if (mode === 'rain') mapEl.classList.add('map-rain-filter');

            const cSky = document.getElementById('cockpit-sky-bg');
            const wSky = document.getElementById('window-sky-container');
            const cStars = document.getElementById('cockpit-stars');
            const wStars = document.getElementById('window-stars');
            const cRain = document.getElementById('cockpit-rain-layer');
            const wRain = document.getElementById('window-rain-layer');
            const celestial = document.getElementById('window-celestial');

            cRain.classList.toggle('hidden', mode !== 'rain');
            wRain.classList.toggle('hidden', mode !== 'rain');

            if (mode === 'day') {
                cSky.className = "absolute inset-0 bg-gradient-to-b from-sky-500 via-blue-400 to-sky-200 transition-all duration-700";
                wSky.style.background = "linear-gradient(180deg, #0284c7 0%, #38bdf8 55%, #bae6fd 100%)";
                cStars.style.opacity = "0"; wStars.style.opacity = "0";
                celestial.className = "absolute top-10 right-12 w-12 h-12 rounded-full bg-yellow-300 shadow-[0_0_50px_#fde047]";
            } else if (mode === 'sunset') {
                cSky.className = "absolute inset-0 bg-gradient-to-b from-[#1e1b4b] via-[#be185d] to-[#f97316] transition-all duration-700";
                wSky.style.background = "linear-gradient(180deg, #1e1b4b 0%, #9d174d 45%, #f97316 85%, #fde047 100%)";
                cStars.style.opacity = "0.35"; wStars.style.opacity = "0.35";
                celestial.className = "absolute top-24 right-12 w-14 h-14 rounded-full bg-orange-400 shadow-[0_0_60px_#fb923c]";
            } else if (mode === 'night') {
                cSky.className = "absolute inset-0 bg-gradient-to-b from-[#020617] via-[#090d1e] to-[#111827] transition-all duration-700";
                wSky.style.background = "linear-gradient(180deg, #02040a 0%, #070d1f 65%, #1e1b4b 100%)";
                cStars.style.opacity = "1"; wStars.style.opacity = "1";
                celestial.className = "absolute top-10 right-12 w-10 h-10 rounded-full bg-slate-100 shadow-[0_0_30px_#e2e8f0]";
            } else if (mode === 'rain') {
                cSky.className = "absolute inset-0 bg-gradient-to-b from-slate-950 via-slate-800 to-slate-900 transition-all duration-700";
                wSky.style.background = "linear-gradient(180deg, #090d16 0%, #1e293b 65%, #0f172a 100%)";
                cStars.style.opacity = "0.15"; wStars.style.opacity = "0.15";
                celestial.className = "hidden";
            }
        }

        function toggleWindowShade() {
            isShadeClosed = !isShadeClosed;
            document.getElementById('window-shade-panel').style.height = isShadeClosed ? "88%" : "0%";
        }

        function cycleCabinMoodLight() {
            const moods = [
                "from-purple-500/35 via-cyan-500/15 to-transparent",
                "from-amber-500/35 via-pink-500/15 to-transparent",
                "from-emerald-500/35 via-blue-500/15 to-transparent",
                "from-blue-600/40 via-indigo-900/20 to-transparent"
            ];
            cabinMoodIdx = (cabinMoodIdx + 1) % moods.length;
            document.getElementById('cabin-ceiling-glow').className = `absolute top-0 inset-x-0 h-36 bg-gradient-to-b ${moods[cabinMoodIdx]} blur-2xl pointer-events-none transition-all duration-700`;
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
            document.getElementById('cabin-aircraft-label').innerText = selectedAircraft;
            document.getElementById('cabin-route-label').innerText = `${originAirport.code} ➔ ${destAirport.code}`;
            document.getElementById('cabin-task-title').innerText = `${selectedFocus.icon} ${selectedFocus.label}`;
            document.getElementById('cabin-passenger-name').innerText = profile.name;
        }

        // ================= 8. CHUYỂN ĐỔI 2 TRANG (DASHBOARD <-> CHUYẾN BAY) =================
        function switchPage(page) {
            const pageDash = document.getElementById('page-dashboard');
            const pageFlight = document.getElementById('page-flight');
            const btnDash = document.getElementById('nav-btn-dashboard');
            const btnFlight = document.getElementById('nav-btn-flight');

            if (page === 'flight') {
                pageDash.classList.add('hidden');
                pageFlight.classList.remove('hidden');
                btnFlight.className = "px-3 py-1.5 rounded-lg text-xs font-extrabold bg-gradient-to-r from-blue-600 to-cyan-500 text-white shadow transition flex items-center gap-1.5";
                btnDash.className = "px-3 py-1.5 rounded-lg text-xs font-extrabold text-slate-400 hover:text-white transition flex items-center gap-1.5";
                setTimeout(() => {
                    map.invalidateSize();
                    updateBookingUI();
                }, 120);
            } else {
                pageFlight.classList.add('hidden');
                pageDash.classList.remove('hidden');
                btnDash.className = "px-3 py-1.5 rounded-lg text-xs font-extrabold bg-gradient-to-r from-blue-600 to-cyan-500 text-white shadow transition flex items-center gap-1.5";
                btnFlight.className = "px-3 py-1.5 rounded-lg text-xs font-extrabold text-slate-400 hover:text-white transition flex items-center gap-1.5";
                renderDashboard();
            }
        }

        function switchMemberProfile() {
            currentMemberKey = document.getElementById('member-select').value;
            appState.lastMember = currentMemberKey;
            savePersistentState();
            renderDashboard();
            resetChat();
        }

        // ================= 9. QUẢN LÝ CÔNG VIỆC (TÍNH GIỜ THEO KHOẢNG CÁCH) & THỜI KHÓA BIỂU =================
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
            const slot = document.getElementById('quick-task-slot').value.trim() || "19:30";
            const destCode = document.getElementById('quick-task-dest').value || "DAD";

            const targetAirport = AIRPORTS.find(a => a.code === destCode) || AIRPORTS[2];
            const distKm = calcDistanceKm(AIRPORTS[0].coords, targetAirport.coords);
            const autoMins = calcStudyDurationFromDistance(distKm, selectedAircraft);

            const profile = appState.members[currentMemberKey];
            profile.tasks.unshift({
                id: Date.now(),
                title,
                hoursLeft: hours,
                importance: imp,
                slot,
                destCode: targetAirport.code,
                distKm: distKm,
                duration: autoMins,
                done: false
            });

            titleInput.value = '';
            savePersistentState();
            renderDashboard();
        }

        function toggleTaskDone(taskId) {
            const profile = appState.members[currentMemberKey];
            const task = profile.tasks.find(t => t.id === taskId);
            if (task) {
                task.done = !task.done;
                savePersistentState();
                renderDashboard();
            }
        }

        function deleteTask(taskId) {
            const profile = appState.members[currentMemberKey];
            profile.tasks = profile.tasks.filter(t => t.id !== taskId);
            savePersistentState();
            renderDashboard();
        }

        function saveNewTimetableSlot() {
            const timeInput = document.getElementById('new-slot-time');
            const subjInput = document.getElementById('new-slot-subject');
            const typeInput = document.getElementById('new-slot-type');

            const time = timeInput.value.trim() || "19:00 - 21:00";
            const subject = subjInput.value.trim();
            if (!subject) { subjInput.focus(); return; }
            const type = typeInput.value;

            const profile = appState.members[currentMemberKey];
            if (!profile.timetable[selectedDay]) profile.timetable[selectedDay] = [];
            profile.timetable[selectedDay].push({ time, subject, type });

            timeInput.value = '';
            subjInput.value = '';
            savePersistentState();
            renderDashboard();
        }

        function removeTimetableSlot(idx) {
            const profile = appState.members[currentMemberKey];
            if (profile.timetable[selectedDay]) {
                profile.timetable[selectedDay].splice(idx, 1);
                savePersistentState();
                renderDashboard();
            }
        }

        function renderDashboard() {
            const profile = appState.members[currentMemberKey];
            const allTasks = profile.tasks || [];
            const pendingTasks = allTasks.filter(t => !t.done);
            const doneTasks = allTasks.filter(t => t.done);
            const daySlots = (profile.timetable && profile.timetable[selectedDay]) ? profile.timetable[selectedDay] : [];

            document.getElementById('stat-member-name').innerText = profile.name;
            document.getElementById('stat-pending-count').innerText = pendingTasks.length;
            document.getElementById('stat-done-count').innerText = doneTasks.length;
            document.getElementById('nav-pending-badge').innerText = pendingTasks.length;
            const pct = allTasks.length > 0 ? Math.round((doneTasks.length / allTasks.length) * 100) : 0;
            document.getElementById('stat-done-percent').innerText = `Tiến độ: ${pct}% (${doneTasks.length}/${allTasks.length})`;
            document.getElementById('stat-miles-count').innerText = `${profile.miles || 0} km`;
            document.getElementById('stat-flights-count').innerText = `Đã hạ cánh: ${profile.flights || 0} chuyến`;
            document.getElementById('timetable-owner-badge').innerText = `(${profile.name})`;
            document.getElementById('add-slot-day-label').innerText = selectedDay;

            const urgentTasks = pendingTasks.filter(t => t.hoursLeft <= 24);
            const banner = document.getElementById('deadline-banner');
            if (urgentTasks.length > 0) {
                banner.classList.remove('hidden');
                banner.classList.add('flex');
                document.getElementById('deadline-banner-text').innerText = 
                    `${profile.name} có ${urgentTasks.length} công việc sắp tới hạn: "${urgentTasks[0].title}" (còn ${urgentTasks[0].hoursLeft} giờ)!`;
            } else {
                banner.classList.add('hidden');
                banner.classList.remove('flex');
            }

            const aiBox = document.getElementById('ai-today-suggestion');
            if (pendingTasks.length > 0) {
                const sorted = [...pendingTasks].sort((a, b) => calcPriorityScore(b) - calcPriorityScore(a));
                const top = sorted[0];
                const dCode = top.destCode || "DAD";
                const dKm = top.distKm || 610;

                aiBox.innerHTML = `
                    <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
                        <div>
                            <div class="flex flex-wrap items-center gap-2 mb-1">
                                <span class="bg-amber-400 text-black text-[10px] font-black px-2 py-0.5 rounded">ƯU TIÊN SỐ 1 • ĐIỂM AI: ${calcPriorityScore(top)}</span>
                                <span class="text-xs font-bold text-red-300">⏳ Hạn còn: ${top.hoursLeft} giờ</span>
                                <span class="text-xs text-amber-300">${'⭐'.repeat(top.importance)}</span>
                            </div>
                            <div class="text-sm sm:text-base font-extrabold text-white">${top.title}</div>
                            <div class="text-xs text-cyan-300 mt-1">
                                ✈️ Chặng SGN ➔ <b>${dCode} (${dKm} km)</b> • Thời gian bay tự tính: <b>${top.duration} phút</b>
                            </div>
                        </div>
                        <div class="flex sm:flex-col gap-2 shrink-0">
                            <button onclick="startFlightFromTask(${top.id})" class="bg-gradient-to-r from-emerald-500 to-cyan-500 hover:opacity-95 text-black font-black px-4 py-2 rounded-xl text-xs shadow-lg whitespace-nowrap">
                                🛫 Bay ngay (${top.duration}p)
                            </button>
                            <button onclick="openWhyModal(${top.id})" class="bg-white/10 hover:bg-white/20 text-white font-bold px-3 py-1.5 rounded-xl text-[11px] whitespace-nowrap">
                                ❓ Tại sao có lịch này?
                            </button>
                        </div>
                    </div>
                `;
            } else if (allTasks.length > 0 && pendingTasks.length === 0) {
                aiBox.innerHTML = `<div class="text-xs text-emerald-400 font-bold py-1.5">🎉 Xuất sắc! ${profile.name} đã hoàn thành toàn bộ ${allTasks.length} công việc!</div>`;
            } else {
                aiBox.innerHTML = `<div class="text-xs text-slate-400 py-1.5">Danh sách của <b>${profile.name}</b> đang trống. Hãy nhập công việc bên dưới hoặc bấm sang tab <b>✈️ Chuyến Bay Tập Trung</b> để bay ngay!</div>`;
            }

            const listEl = document.getElementById('todo-drag-list');
            listEl.innerHTML = '';

            let filteredTasks = allTasks;
            if (currentTaskFilter === 'pending') filteredTasks = pendingTasks;
            if (currentTaskFilter === 'done') filteredTasks = doneTasks;

            if (filteredTasks.length === 0) {
                listEl.innerHTML = `
                    <div class="text-center py-8 bg-slate-900/40 rounded-2xl border border-dashed border-white/10">
                        <div class="text-xl mb-1">📝</div>
                        <div class="text-xs font-bold text-slate-300">Chưa có nhiệm vụ nào ở mục này</div>
                    </div>
                `;
            } else {
                filteredTasks.forEach((task) => {
                    const realIdx = allTasks.findIndex(t => t.id === task.id);
                    const score = calcPriorityScore(task);
                    const isUrgent = !task.done && task.hoursLeft <= 24;
                    const dCode = task.destCode || "DAD";
                    const dKm = task.distKm || 610;

                    const card = document.createElement('div');
                    card.draggable = true;
                    card.dataset.index = realIdx;
                    card.className = `p-3 rounded-2xl border transition cursor-grab active:cursor-grabbing flex flex-col sm:flex-row sm:items-center justify-between gap-2.5 ${
                        task.done 
                        ? 'bg-emerald-950/20 border-emerald-500/30' 
                        : (isUrgent ? 'bg-slate-900/95 border-red-400/40 shadow-md' : 'bg-slate-900/90 border-white/10 hover:border-cyan-400/40')
                    }`;

                    card.addEventListener('dragstart', handleDragStart);
                    card.addEventListener('dragover', handleDragOver);
                    card.addEventListener('drop', handleDrop);
                    card.addEventListener('dragend', handleDragEnd);

                    card.innerHTML = `
                        <div class="flex items-start gap-2.5">
                            <button onclick="toggleTaskDone(${task.id})" title="Đánh dấu hoàn thành" class="mt-0.5 w-6 h-6 rounded-full border-2 flex items-center justify-center font-black text-xs transition shrink-0 ${
                                task.done 
                                ? 'bg-emerald-500 border-emerald-400 text-black shadow-lg shadow-emerald-500/30' 
                                : 'bg-slate-800 border-slate-500 text-transparent hover:border-emerald-400'
                            }">✓</button>

                            <div>
                                <div class="flex flex-wrap items-center gap-1.5 mb-1">
                                    ${task.done 
                                        ? `<span class="text-[10px] font-black bg-emerald-500/20 text-emerald-300 border border-emerald-500/30 px-2 py-0.5 rounded">✅ ĐÃ XONG</span>` 
                                        : `<span class="text-[10px] font-black px-2 py-0.5 rounded ${isUrgent ? 'bg-red-500/25 text-red-300 border border-red-400/30' : 'bg-blue-500/20 text-blue-300'}">⏳ Hạn: ${task.hoursLeft}h</span>`
                                    }
                                    <span class="text-[10px] font-bold text-amber-300">${'⭐'.repeat(task.importance)}</span>
                                    <span class="text-[10px] font-mono bg-white/10 text-cyan-300 px-2 py-0.5 rounded">✈️ SGN➔${dCode} (${dKm}km = ${task.duration}p)</span>
                                </div>
                                <div class="text-xs sm:text-sm font-extrabold ${task.done ? 'line-through text-slate-400' : 'text-white'}">${task.title}</div>
                            </div>
                        </div>

                        <div class="flex items-center gap-1.5 shrink-0 self-end sm:self-center">
                            <button onclick="openWhyModal(${task.id})" class="bg-slate-800 hover:bg-slate-700 text-cyan-300 border border-cyan-500/30 px-2 py-1 rounded-xl text-[11px] font-bold">
                                ❓ Tại sao?
                            </button>
                            ${!task.done ? `
                                <button onclick="startFlightFromTask(${task.id})" class="bg-blue-600 hover:bg-blue-500 text-white px-2.5 py-1 rounded-xl text-[11px] font-extrabold shadow">
                                    🛫 Bay (${task.duration}p)
                                </button>
                            ` : ''}
                            <button onclick="deleteTask(${task.id})" class="bg-red-500/15 hover:bg-red-500/30 text-red-300 px-2 py-1 rounded-xl text-xs font-bold">🗑️</button>
                        </div>
                    `;
                    listEl.appendChild(card);
                });
            }

            const dayTabs = document.getElementById('day-tabs-container');
            dayTabs.innerHTML = '';
            DAYS_OF_WEEK.forEach(d => {
                const count = (profile.timetable && profile.timetable[d]) ? profile.timetable[d].length : 0;
                const active = d === selectedDay;
                const btn = document.createElement('button');
                btn.className = `py-1.5 rounded-xl text-xs font-extrabold transition border flex flex-col items-center ${
                    active ? 'bg-amber-400 text-black border-amber-300 shadow' : 'bg-slate-900 text-slate-400 border-white/10 hover:text-white'
                }`;
                btn.innerHTML = `<span>${d}</span><span class="text-[9px] ${active ? 'text-black/70' : 'text-slate-500'}">${count}</span>`;
                btn.onclick = () => { selectedDay = d; renderDashboard(); };
                dayTabs.appendChild(btn);
            });

            const slotsList = document.getElementById('timetable-slots-list');
            slotsList.innerHTML = '';
            if (daySlots.length === 0) {
                slotsList.innerHTML = `
                    <div class="text-center py-6 bg-slate-900/40 rounded-2xl border border-dashed border-white/10">
                        <div class="text-xs font-bold text-slate-300">Ngày ${selectedDay} chưa có lịch nào</div>
                    </div>
                `;
            } else {
                daySlots.forEach((s, sIdx) => {
                    const isFree = s.type === 'free';
                    const el = document.createElement('div');
                    el.className = `p-3 rounded-2xl border flex items-center justify-between gap-2 ${
                        isFree ? 'bg-emerald-950/30 border-emerald-400/30' : 'bg-slate-900/90 border-white/10'
                    }`;
                    el.innerHTML = `
                        <div>
                            <div class="flex items-center gap-2">
                                <span class="text-[10px] font-mono font-extrabold px-2 py-0.5 rounded ${isFree ? 'bg-emerald-400 text-black' : 'bg-slate-700 text-slate-200'}">${s.time}</span>
                                <span class="text-[10px] font-bold ${isFree ? 'text-emerald-300' : 'text-red-300'}">${isFree ? '🟢 Giờ trống' : '🔴 Bận học'}</span>
                            </div>
                            <div class="text-xs font-bold text-white mt-1">${s.subject}</div>
                        </div>
                        <button onclick="removeTimetableSlot(${sIdx})" class="bg-red-500/15 hover:bg-red-500/30 text-red-300 px-2 py-1 rounded-xl text-xs font-bold">🗑️</button>
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
            if (profile.tasks.length === 0) { alert("Hãy thêm công việc trước khi sắp xếp!"); return; }
            profile.tasks.sort((a, b) => {
                if (a.done !== b.done) return a.done ? 1 : -1;
                return calcPriorityScore(b) - calcPriorityScore(a);
            });
            savePersistentState();
            renderDashboard();
            alert(`🤖 AI đã sắp xếp lại danh sách của ${profile.name} theo Độ quan trọng và Thời hạn Deadline!`);
        }

        function handleSuddenScheduleChange() {
            const profile = appState.members[currentMemberKey];
            const pending = profile.tasks.filter(t => !t.done);
            if (pending.length === 0) { alert("Hiện không có công việc nào đang chờ!"); return; }
            const backupSlots = ["20:30 (Tối dự phòng)", "21:30 (Ca khuya)", "08:00 (Sáng mai)"];
            pending.forEach((t, i) => { t.slot = backupSlots[i % backupSlots.length]; });
            savePersistentState();
            renderDashboard();
            alert(`🌪️ Đã tự động dời ${pending.length} công việc của ${profile.name} sang khung giờ trống dự phòng!`);
        }

        function openWhyModal(taskId) {
            const profile = appState.members[currentMemberKey];
            const task = profile.tasks.find(t => t.id === taskId);
            if (!task) return;
            const score = calcPriorityScore(task);
            const dCode = task.destCode || "DAD";
            const dKm = task.distKm || 610;

            document.getElementById('why-modal-content').innerHTML = `
                <div class="bg-slate-900 p-3 rounded-2xl border border-white/10">
                    <div class="text-sm font-extrabold text-white">${task.title}</div>
                    <div class="text-xs text-amber-300 font-mono mt-0.5">Điểm ưu tiên AI: <b>${score} điểm</b></div>
                </div>
                <div class="space-y-2">
                    <div class="bg-red-500/15 border border-red-400/30 p-2.5 rounded-2xl">
                        <div class="font-extrabold text-red-300">1. ⏳ Thời hạn (Deadline): Còn ${task.hoursLeft} giờ</div>
                    </div>
                    <div class="bg-amber-500/15 border border-amber-400/30 p-2.5 rounded-2xl">
                        <div class="font-extrabold text-amber-300">2. ⭐ Độ quan trọng: ${task.importance}/5 Sao</div>
                    </div>
                    <div class="bg-cyan-500/15 border border-cyan-400/30 p-2.5 rounded-2xl">
                        <div class="font-extrabold text-cyan-300">3. ✈️ Thời gian học tự tính theo Khoảng cách:</div>
                        <div class="text-[11px] text-slate-300 mt-0.5">Chặng SGN ➔ ${dCode} dài <b>${dKm} km</b> nên hệ thống tự động thiết lập phiên học kéo dài <b>${task.duration} phút</b>.</div>
                    </div>
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
            const pending = profile.tasks.filter(t => !t.done);
            if (pending.length === 0) alert(`🔔 ${profile.name} đã hoàn thành hết công việc!`);
            else alert(`🔔 Nhắc học (${profile.name}): Hãy hoàn thành "${pending[0].title}" (${pending[0].duration} phút)!`);
        }

        function startFocusFromTopTask() {
            const profile = appState.members[currentMemberKey];
            const pending = profile.tasks.filter(t => !t.done).sort((a,b) => calcPriorityScore(b) - calcPriorityScore(a));
            if (pending[0]) startFlightFromTask(pending[0].id);
        }

        function startFlightFromTask(taskId) {
            const profile = appState.members[currentMemberKey];
            const task = profile.tasks.find(t => t.id === taskId);
            if (!task) return;

            activeTaskIdForFlight = task.id;
            originAirport = AIRPORTS[0];
            destAirport = AIRPORTS.find(a => a.code === task.destCode) || AIRPORTS[2];
            document.getElementById('origin-select').value = originAirport.code;
            document.getElementById('dest-select').value = destAirport.code;

            selectedFocus = { id: 'custom', label: task.title, icon: '🎯', color: 'bg-cyan-600 border-cyan-300 text-white' };
            document.getElementById('custom-focus-input').value = task.title;

            onRouteChange();
            switchPage('flight');
            goToSeatSelection();
        }

        // ================= 10. LOGIC TRẠM BAY & TỰ ĐỘNG TÍNH THỜI GIAN THEO KHOẢNG CÁCH =================
        function toggleBookingCardSize() {
            const card = document.getElementById('screen-booking');
            const btn = document.getElementById('toggle-booking-btn');
            isBookingCollapsed = !isBookingCollapsed;
            if (isBookingCollapsed) {
                card.classList.add('translate-y-[130%]');
                btn.innerText = "🔼 Mở bảng đặt vé";
            } else {
                card.classList.remove('translate-y-[130%]');
                btn.innerText = "🔽 Thu gọn bảng";
            }
        }

        function initAirportDropdowns() {
            const oSel = document.getElementById('origin-select');
            const dSel = document.getElementById('dest-select');
            const qSel = document.getElementById('quick-task-dest');

            const vnAirports = AIRPORTS.filter(a => a.group === 'VN');
            const intAirports = AIRPORTS.filter(a => a.group === 'INT');

            const buildOptions = (withTimeHint = false) => {
                let html = `<optgroup label="🇻🇳 Sân bay Việt Nam (22 sân bay)" class="bg-slate-900">`;
                vnAirports.forEach(a => {
                    const dist = calcDistanceKm(AIRPORTS[0].coords, a.coords);
                    const mins = calcStudyDurationFromDistance(dist, "Airbus A321neo");
                    html += `<option value="${a.code}">${a.code} - ${a.name} ${withTimeHint ? `(~${mins}p)` : ''}</option>`;
                });
                html += `</optgroup><optgroup label="🌏 Khu vực & Quốc tế (12 sân bay)" class="bg-slate-900">`;
                intAirports.forEach(a => {
                    const dist = calcDistanceKm(AIRPORTS[0].coords, a.coords);
                    const mins = calcStudyDurationFromDistance(dist, "Airbus A321neo");
                    html += `<option value="${a.code}">${a.code} - ${a.name} ${withTimeHint ? `(~${mins}p)` : ''}</option>`;
                });
                html += `</optgroup>`;
                return html;
            };

            oSel.innerHTML = buildOptions(false);
            dSel.innerHTML = buildOptions(false);
            qSel.innerHTML = buildOptions(true);

            oSel.value = originAirport.code;
            dSel.value = destAirport.code;
            qSel.value = "DAD";
        }

        function onRouteChange() {
            const oCode = document.getElementById('origin-select').value;
            const dCode = document.getElementById('dest-select').value;
            if (oCode === dCode) {
                const alt = AIRPORTS.find(a => a.code !== oCode);
                document.getElementById('dest-select').value = alt.code;
            }
            originAirport = AIRPORTS.find(a => a.code === document.getElementById('origin-select').value);
            destAirport = AIRPORTS.find(a => a.code === document.getElementById('dest-select').value);

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

        function randomRoute() {
            const randDest = AIRPORTS.filter(a => a.code !== originAirport.code);
            destAirport = randDest[Math.floor(Math.random() * randDest.length)];
            document.getElementById('dest-select').value = destAirport.code;
            onRouteChange();
        }

        function updateAircraft() {
            selectedAircraft = document.getElementById('aircraft-select').value;
            selectedDuration = calcStudyDurationFromDistance(currentDistance, selectedAircraft);
            updateBookingUI();
            if (isFlying && planeMarker) {
                planeMarker.setIcon(createCustomAircraftMapIcon());
            }
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
            const hh = String(now.getHours()).padStart(2, '0');
            const mm = String(now.getMinutes()).padStart(2, '0');
            document.getElementById('booking-realtime-eta').innerText = `${hh}:${mm} ➔ ${calcRealTimeETA(selectedDuration)}`;

            if (routeLine) map.removeLayer(routeLine);
            if (originMarker) map.removeLayer(originMarker);
            if (destMarker) map.removeLayer(destMarker);

            originMarker = L.marker(originAirport.coords, { icon: createAirportBadge(originAirport.code, false) }).addTo(map);
            destMarker = L.marker(destAirport.coords, { icon: createAirportBadge(destAirport.code, true) }).addTo(map);

            routeLine = L.polyline([originAirport.coords, destAirport.coords], {
                color: '#38bdf8', weight: 3.5, dashArray: '8, 8', opacity: 0.95
            }).addTo(map);

            map.fitBounds(routeLine.getBounds(), { padding: [70, 70] });
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
                        if (isSelected) style = 'bg-[#3b82f6] border-blue-200 text-white shadow-lg shadow-blue-500/50 scale-105';

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
                pill.className = `px-3 py-1.5 rounded-full text-xs font-bold flex items-center gap-1.5 border transition ${
                    active ? mode.color + ' scale-105 shadow-md' : 'bg-slate-800/80 border-white/10 text-slate-300 hover:bg-slate-700'
                }`;
                pill.innerHTML = `<span>${mode.icon}</span><span>${mode.label}</span>`;
                pill.onclick = () => {
                    selectedFocus = mode;
                    renderFocusPills();
                    renderSeats();
                };
                container.appendChild(pill);
            });
        }

        function openFocusPopover(seatCode) {
            selectedSeat = seatCode;
            appState.members[currentMemberKey].seat = seatCode;
            savePersistentState();
            document.getElementById('seat-selected-badge').innerText = seatCode;
            document.getElementById('pop-seat-code').innerText = seatCode;
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
            document.getElementById('seat-header-aircraft').innerText = selectedAircraft;
            document.getElementById('seat-header-route').innerText = `${originAirport.code} ➔ ${destAirport.code} (${currentDistance} km • ${selectedDuration} phút)`;
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

            document.getElementById('tk-aircraft').innerText = selectedAircraft;
            document.getElementById('tk-passenger').innerText = profile.name;
            document.getElementById('tk-realtime-span').innerText = `${stdStr} ➔ ${flightEtaString}`;
            document.getElementById('tk-strict-badge').innerText = strictModeEnabled ? "🔒 STRICT LOCK ON" : "🔓 FREE MODE";
            document.getElementById('tk-origin-code').innerText = originAirport.code;
            document.getElementById('tk-origin-name').innerText = originAirport.name.split(' (')[0];
            document.getElementById('tk-dest-code').innerText = destAirport.code;
            document.getElementById('tk-dest-name').innerText = destAirport.name.split(' (')[0];
            document.getElementById('tk-duration').innerText = `${selectedDuration} phút`;
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

        function playCabinDingDong() {
            try {
                if (!audioCtx) audioCtx = new (window.AudioContext || window.webkitAudioContext)();
                const now = audioCtx.currentTime;
                const osc1 = audioCtx.createOscillator();
                const osc2 = audioCtx.createOscillator();
                const gain = audioCtx.createGain();
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
            const profile = appState.members[currentMemberKey];
            const specs = getAircraftSpecs(selectedAircraft);

            document.getElementById('screen-ticket').classList.add('hidden');
            document.getElementById('screen-ticket').classList.remove('flex');
            document.getElementById('screen-flying').classList.remove('hidden');

            playCabinDingDong();
            const player = document.getElementById('lofi-player');
            if (player.paused) toggleLofi();

            isFlying = true;
            isPausedByViolation = false;
            violationCount = 0;
            updateSafetyHearts();
            updateCameraViewsData();

            flightEtaString = calcRealTimeETA(selectedDuration);
            document.getElementById('fly-eta-badge').innerText = flightEtaString;
            document.getElementById('cockpit-eta').innerText = flightEtaString;
            document.getElementById('cabin-eta').innerText = flightEtaString;
            document.getElementById('telemetry-live-badge').innerText = `● ${specs.speedKmh} KM/H • ${specs.altFt}`;

            document.getElementById('fly-mini-svg').innerHTML = getAircraftSVG(selectedAircraft, 45);
            document.getElementById('fly-route-text').innerText = `${originAirport.name.split(' (')[0]} ➔ ${destAirport.name.split(' (')[0]}`;
            document.getElementById('fly-sub-info').innerText = `${selectedAircraft} • Ghế ${selectedSeat} • ${selectedFocus.icon} ${selectedFocus.label}`;

            totalFlightSeconds = selectedDuration * 60;
            remainingSeconds = totalFlightSeconds;

            if (planeMarker) map.removeLayer(planeMarker);
            planeMarker = L.marker(originAirport.coords, { icon: createCustomAircraftMapIcon(), zIndexOffset: 1000 }).addTo(map);
            map.flyTo(originAirport.coords, 7, { duration: 1.8 });

            updateFlightTick();
            if (flightInterval) clearInterval(flightInterval);
            flightInterval = setInterval(() => {
                if (isPausedByViolation) return;
                remainingSeconds--;
                if (remainingSeconds <= 0) {
                    finishFlightSuccessfully();
                } else {
                    updateFlightTick();
                }
            }, 1000);
        }

        function completeFlightEarly() {
            finishFlightSuccessfully();
        }

        function finishFlightSuccessfully() {
            if (flightInterval) clearInterval(flightInterval);
            isFlying = false;
            playCabinDingDong();
            const profile = appState.members[currentMemberKey];

            profile.miles = (profile.miles || 0) + currentDistance;
            profile.flights = (profile.flights || 0) + 1;

            if (activeTaskIdForFlight) {
                const task = profile.tasks.find(t => t.id === activeTaskIdForFlight);
                if (task) task.done = true;
                activeTaskIdForFlight = null;
            }
            savePersistentState();

            alert(`🎉 Chuyến bay ${selectedAircraft} (${originAirport.code} ➔ ${destAirport.code}) đã hạ cánh an toàn!\n+ Cộng thêm ${currentDistance} km vào hồ sơ của ${profile.name}!`);
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
                const osc = audioCtx.createOscillator();
                const gain = audioCtx.createGain();
                osc.type = 'sawtooth';
                osc.frequency.setValueAtTime(880, audioCtx.currentTime);
                osc.frequency.setValueAtTime(440, audioCtx.currentTime + 0.18);
                gain.gain.setValueAtTime(0.2, audioCtx.currentTime);
                osc.connect(gain);
                gain.connect(audioCtx.destination);
                osc.start();
                osc.stop(audioCtx.currentTime + 0.35);
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

            document.getElementById('violation-count-text').innerText = `${violationCount} / ${MAX_VIOLATIONS} LẦN`;
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

            document.getElementById('countdown-timer').innerText = timeFormatted;
            document.getElementById('cockpit-timer-display').innerText = timeFormatted;
            document.getElementById('cabin-timer-display').innerText = timeFormatted;

            const progress = (totalFlightSeconds - remainingSeconds) / totalFlightSeconds;
            document.getElementById('flight-progress').style.width = `${progress * 100}%`;

            const distLeft = Math.max(0, Math.round(currentDistance * (1 - progress)));
            document.getElementById('fly-dist-left').innerText = distLeft;
            document.getElementById('cockpit-dist-display').innerText = `${distLeft} KM`;
            document.getElementById('cabin-dist-display').innerText = distLeft;

            const lat = originAirport.coords[0] + (destAirport.coords[0] - originAirport.coords[0]) * progress;
            const lng = originAirport.coords[1] + (destAirport.coords[1] - originAirport.coords[1]) * progress;
            if (planeMarker) planeMarker.setLatLng([lat, lng]);
        }

        function centerOnPlane() {
            setCameraView('map');
            if (planeMarker) map.flyTo(planeMarker.getLatLng(), 8, { duration: 1.2 });
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

        // ================= 11. CHATBOT AI & MEDIA =================
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
            box.innerHTML += `
                <div class="flex flex-col items-end">
                    <div class="bg-[#d4a349] text-white font-semibold text-xs px-3.5 py-2 rounded-2xl rounded-tr-sm shadow-sm max-w-[82%]">${text}</div>
                    <span class="text-[9px] text-slate-400 mt-0.5">${getCurrentTimeStr()}</span>
                </div>
            `;
            box.scrollTop = box.scrollHeight;

            setTimeout(() => {
                const reply = generateSmartBotReply(text);
                const botAvatar = document.getElementById('bot-launcher-img').src;
                box.innerHTML += `
                    <div class="flex items-start gap-2">
                        <img src="${botAvatar}" class="w-7 h-7 rounded-full bg-amber-400 p-0.5 border border-[#d4a349] shrink-0 mt-1 object-cover" />
                        <div class="max-w-[84%]">
                            <div class="bg-[#fae5be] p-1 rounded-2xl rounded-tl-sm shadow-sm">
                                <div class="bg-white rounded-xl p-2.5 text-xs text-slate-800 leading-relaxed">${reply}</div>
                            </div>
                            <span class="text-[9px] text-slate-400 mt-0.5 block">${getCurrentTimeStr()}</span>
                        </div>
                    </div>
                `;
                box.scrollTop = box.scrollHeight;
            }, 250);
        }

        function generateSmartBotReply(q) {
            const lower = q.toLowerCase();
            const profile = appState.members[currentMemberKey];
            const pending = profile.tasks.filter(t => !t.done).sort((a,b) => calcPriorityScore(b) - calcPriorityScore(a));
            const done = profile.tasks.filter(t => t.done);

            if (lower.includes('hôm nay') || lower.includes('học gì')) {
                if (pending.length === 0) return `Chào <b>${profile.name}</b>! Hiện danh sách của bạn đang trống. Hãy thêm công việc mới hoặc chọn chuyến bay để bắt đầu học nhé!`;
                return `Chào <b>${profile.name}</b>! Bạn nên ưu tiên làm ngay:<br>• <b>${pending[0].title}</b> (Bay ${pending[0].duration} phút theo khoảng cách ${pending[0].distKm} km).`;
            }
            if (lower.includes('việc') || lower.includes('chưa xong') || lower.includes('tiến độ')) {
                return `📊 Tiến độ của <b>${profile.name}</b>:<br>• Đang cần làm: <b>${pending.length} việc</b><br>• Đã hoàn thành (✓): <b>${done.length} việc</b><br>• Tổng dặm bay: <b>${profile.miles || 0} km</b>.`;
            }
            if (lower.includes('đột xuất') || lower.includes('dời lịch')) {
                handleSuddenScheduleChange();
                return `🌪️ Mình đã tự động dời các ca học chưa xong của <b>${profile.name}</b> sang khung giờ dự phòng rồi nhé!`;
            }
            return `Xin chào <b>${profile.name}</b>! Thời gian học hiện đã được tính tự động hoàn toàn theo khoảng cách (km) giữa 2 sân bay và giờ thực tế.`;
        }

        function resetChat() {
            const profile = appState.members[currentMemberKey];
            const botAvatar = document.getElementById('bot-launcher-img').src;
            document.getElementById('chat-messages').innerHTML = `
                <div class="flex flex-col items-end">
                    <div class="bg-[#d4a349] text-white font-semibold text-xs px-3.5 py-1.5 rounded-2xl rounded-tr-sm shadow-sm">Bắt đầu</div>
                    <span class="text-[9px] text-slate-400 mt-0.5">${getCurrentTimeStr()}</span>
                </div>
                <div class="flex items-start gap-2">
                    <img src="${botAvatar}" class="w-7 h-7 rounded-full bg-amber-400 p-0.5 border border-[#d4a349] shrink-0 mt-1 object-cover" />
                    <div>
                        <div class="bg-[#fae5be] p-1 rounded-2xl rounded-tl-sm shadow-sm">
                            <div class="bg-white rounded-xl p-2.5 text-xs text-slate-800 leading-relaxed">
                                Xin chào <b>${profile.name}</b>! 🙋‍♀️<br>Thời gian học hiện được tính tự động theo khoảng cách bay và đồng hồ thời gian thực!
                            </div>
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
                    eq.classList.remove('hidden'); eq.classList.add('flex');
                    txt.innerText = "Đang phát";
                }).catch(() => {});
            } else {
                p.pause();
                eq.classList.add('hidden'); eq.classList.remove('flex');
                txt.innerText = "🎵 Nhạc Lofi";
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
                p.src = url; p.play();
                document.getElementById('eq-icon').classList.remove('hidden');
                document.getElementById('eq-icon').classList.add('flex');
                document.getElementById('lofi-btn-text').innerText = "Nhạc riêng";
            }
        }
        function applyCustomMedia() {
            const aUrl = document.getElementById('audio-url-input').value.trim();
            if (aUrl) {
                const p = document.getElementById('lofi-player');
                p.src = aUrl; p.play();
            }
            closeMediaModal();
        }

        // Khởi chạy ứng dụng
        document.getElementById('member-select').value = currentMemberKey;
        updateRealTimeClock();
        initAirportDropdowns();
        syncEnvironmentWithRealTime();
        onRouteChange();
        renderDashboard();
        resetChat();
    </script>
</body>
</html>
"""

components.html(app_html, height=800, scrolling=False)
