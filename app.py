import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="StudyHub & Focus Flight Simulator - Group 4",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
    <style>
        #MainMenu {visibility: hidden;}
        header {visibility: hidden;}
        footer {visibility: hidden;}
        .block-container { padding: 0rem !important; max-width: 100% !important; }
        iframe { border: none !important; width: 100vw !important; height: 100vh !important; display: block !important; }
        body { margin: 0; padding: 0; overflow: hidden; background-color: #060913; }
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
        body { font-family: 'Plus Jakarta Sans', sans-serif; background: #060913; color: white; margin: 0; overflow: hidden; user-select: none; }
        .mono { font-family: 'JetBrains Mono', monospace; }
        #map { position: absolute; inset: 0; z-index: 1; background: #060913; transition: filter 0.8s ease; }

        /* Bộ lọc Bản đồ khi bay qua đêm / hoàng hôn */
        .map-night-filter { filter: brightness(0.48) contrast(1.35) saturate(0.8) hue-rotate(195deg); }
        .map-sunset-filter { filter: brightness(0.78) contrast(1.15) sepia(0.35) hue-rotate(-15deg); }
        .map-rain-filter { filter: brightness(0.55) contrast(1.2) saturate(0.6); }

        .glass-panel {
            background: rgba(13, 19, 33, 0.90);
            backdrop-filter: blur(22px);
            -webkit-backdrop-filter: blur(22px);
            border: 1px solid rgba(255, 255, 255, 0.14);
        }

        .dash-card {
            background: linear-gradient(145deg, #0f172a 0%, #0b1120 100%);
            border: 1px solid rgba(255, 255, 255, 0.09);
            box-shadow: 0 12px 32px rgba(0, 0, 0, 0.4);
        }

        .focus-popover {
            background: rgba(24, 35, 58, 0.97);
            backdrop-filter: blur(28px);
            border: 1px solid rgba(147, 197, 253, 0.3);
            box-shadow: 0 25px 60px rgba(0, 0, 0, 0.85);
        }

        .fuselage {
            border-top-left-radius: 170px 260px;
            border-top-right-radius: 170px 260px;
            border-left: 3px solid rgba(56, 189, 248, 0.3);
            border-right: 3px solid rgba(56, 189, 248, 0.3);
            border-top: 3px solid rgba(56, 189, 248, 0.45);
            background: linear-gradient(180deg, rgba(20, 29, 47, 0.96) 0%, rgba(10, 14, 24, 0.98) 100%);
            box-shadow: inset 0 15px 40px rgba(56, 189, 248, 0.06), 0 20px 60px rgba(0,0,0,0.85);
        }

        .seat-box { transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1); }
        .seat-box:hover { transform: scale(1.07); }

        .ticket-cutout-left { position: absolute; left: -14px; top: 66%; width: 28px; height: 28px; background: #060913; border-radius: 50%; }
        .ticket-cutout-right { position: absolute; right: -14px; top: 66%; width: 28px; height: 28px; background: #060913; border-radius: 50%; }

        /* Sóng nhạc Lofi */
        @keyframes pulse-bar { 0%, 100% { height: 4px; } 50% { height: 15px; } }
        .eq-bar { width: 3px; background: #38bdf8; border-radius: 2px; animation: pulse-bar 0.9s infinite ease-in-out; }
        .eq-bar:nth-child(2) { animation-delay: 0.2s; }
        .eq-bar:nth-child(3) { animation-delay: 0.4s; }

        /* Đèn nháy cánh máy bay (Strobe & Nav lights) */
        @keyframes strobe-blink { 0%, 85%, 100% { opacity: 0.15; } 90%, 95% { opacity: 1; filter: drop-shadow(0 0 8px #ffffff); } }
        .strobe-light { animation: strobe-blink 1.6s infinite; }

        /* Cánh quạt máy bay ATR-72 quay tít */
        @keyframes prop-spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }
        .prop-blade { transform-origin: center; animation: prop-spin 0.15s linear infinite; }

        /* Vòng quét Radar quanh máy bay */
        @keyframes radar-pulse { 0% { transform: scale(0.4); opacity: 0.85; } 100% { transform: scale(2.4); opacity: 0; } }
        .radar-ring { animation: radar-pulse 2.4s infinite ease-out; }

        /* Mây trôi & Sao đêm ở góc nhìn Cửa sổ / Buồng lái */
        @keyframes cloud-move { 0% { transform: translateX(110%); } 100% { transform: translateX(-120%); } }
        .cloud-anim-1 { animation: cloud-move 18s linear infinite; }
        .cloud-anim-2 { animation: cloud-move 26s linear infinite; animation-delay: -9s; }
        .cloud-anim-3 { animation: cloud-move 14s linear infinite; animation-delay: -4s; }

        /* Nghiêng nhẹ đường chân trời buồng lái */
        @keyframes hud-sway { 0%, 100% { transform: rotate(-1.5deg) translateY(0px); } 50% { transform: rotate(1.5deg) translateY(4px); } }
        .hud-horizon { animation: hud-sway 7s ease-in-out infinite; }

        /* Mưa rơi trên kính */
        @keyframes rain-fall { 0% { background-position: 0px 0px; } 100% { background-position: -150px 500px; } }
        .rain-overlay {
            background-image: repeating-linear-gradient(105deg, transparent 0px, transparent 18px, rgba(186, 230, 253, 0.28) 19px, transparent 20px);
            background-size: 200px 200px;
            animation: rain-fall 0.65s linear infinite;
        }

        /* Cảnh báo đỏ Strict Mode */
        @keyframes red-alert { 0%, 100% { background: rgba(153, 27, 27, 0.92); } 50% { background: rgba(220, 38, 38, 0.98); } }
        .turbulence-alert { animation: red-alert 0.7s infinite; backdrop-filter: blur(16px); }

        /* Chatbot Vàng Kim */
        @keyframes bot-glow {
            0%, 100% { box-shadow: 0 0 15px rgba(212, 163, 73, 0.6), 0 0 30px rgba(212, 163, 73, 0.3); transform: translateY(0px); }
            50% { box-shadow: 0 0 25px rgba(234, 179, 8, 0.9), 0 0 45px rgba(212, 163, 73, 0.5); transform: translateY(-4px); }
        }
        .bot-launcher-glow { animation: bot-glow 3s infinite ease-in-out; }

        .dragging-card { opacity: 0.45; border: 2px dashed #38bdf8 !important; }
        ::-webkit-scrollbar { width: 6px; height: 6px; }
        ::-webkit-scrollbar-thumb { background: rgba(255,255,255,0.2); border-radius: 10px; }
        .leaflet-control-attribution { display: none !important; }
    </style>
</head>
<body class="relative w-screen h-screen bg-[#060913]">

    <!-- AUDIO LOFI -->
    <audio id="lofi-player" loop crossorigin="anonymous">
        <source id="lofi-source" src="https://cdn.pixabay.com/download/audio/2022/05/27/audio_1808fbf07a.mp3" type="audio/mpeg">
    </audio>

    <!-- ================= THANH ĐIỀU HƯỚNG CHÍNH (TOP NAVIGATION BAR) ================= -->
    <header class="fixed top-0 left-0 right-0 h-16 z-40 bg-[#090e1a]/95 backdrop-blur-xl border-b border-white/10 px-4 sm:px-6 flex items-center justify-between gap-2">
        <!-- Logo & Hồ sơ thành viên (CHỈ GHI TÊN) -->
        <div class="flex items-center gap-3">
            <div class="flex items-center gap-2.5">
                <div class="w-9 h-9 rounded-xl bg-gradient-to-br from-blue-500 to-cyan-400 flex items-center justify-center text-black font-black text-lg shadow">✈️</div>
                <div class="hidden md:block">
                    <div class="text-xs font-extrabold tracking-wider text-white">STUDYHUB & FLIGHT SIM</div>
                    <div class="text-[10px] text-emerald-400 flex items-center gap-1" id="save-status-indicator">
                        <span>● Tự động lưu dữ liệu</span>
                    </div>
                </div>
            </div>

            <!-- Chọn Hồ sơ Thành viên (Chỉ hiển thị đúng Tên) -->
            <div class="bg-slate-900 border border-white/15 px-3 py-1.5 rounded-xl flex items-center gap-2">
                <span class="text-xs">👤</span>
                <div>
                    <div class="text-[9px] text-amber-400 font-bold uppercase tracking-wider leading-none">Thành viên</div>
                    <select id="member-select" onchange="switchMemberProfile()" class="bg-transparent text-white font-extrabold text-xs focus:outline-none cursor-pointer pr-1 mt-0.5">
                        <option value="huudai" class="bg-slate-900">Hữu Đại</option>
                        <option value="quangminh" class="bg-slate-900">Quang Minh</option>
                        <option value="khanhthi" class="bg-slate-900">Khánh Thi</option>
                        <option value="minhchau" class="bg-slate-900">Minh Châu</option>
                        <option value="uyennhi" class="bg-slate-900">Uyên Nhi</option>
                        <option value="vanhoang" class="bg-slate-900">Văn Hoàng</option>
                    </select>
                </div>
            </div>
        </div>

        <!-- Cụm Chuyển Đổi 2 Trang Độc Lập -->
        <div class="bg-slate-900/90 p-1 rounded-2xl border border-white/10 flex items-center gap-1">
            <button id="nav-btn-dashboard" onclick="switchPage('dashboard')" class="px-4 py-2 rounded-xl text-xs font-extrabold bg-gradient-to-r from-blue-600 to-cyan-500 text-white shadow transition flex items-center gap-1.5">
                <span>📊 Bảng Điều Khiển Học Tập</span>
                <span id="nav-pending-badge" class="bg-black/30 text-white text-[10px] px-1.5 py-0.2 rounded-full">0</span>
            </button>
            <button id="nav-btn-flight" onclick="switchPage('flight')" class="px-4 py-2 rounded-xl text-xs font-extrabold text-slate-400 hover:text-white transition flex items-center gap-1.5">
                <span>✈️ Chuyến Bay Tập Trung</span>
            </button>
        </div>

        <!-- Cụm Nhạc Lofi & Tùy chỉnh -->
        <div class="flex items-center gap-2">
            <button onclick="toggleLofi()" class="bg-slate-900 hover:bg-slate-800 border border-white/10 px-3 py-2 rounded-xl flex items-center gap-2 text-xs font-bold text-slate-200 transition">
                <div id="eq-icon" class="hidden items-end gap-[2px] h-4">
                    <div class="eq-bar"></div><div class="eq-bar"></div><div class="eq-bar"></div>
                </div>
                <span id="lofi-btn-text">🎵 Nhạc Lofi</span>
            </button>
            <button onclick="openMediaModal()" class="bg-slate-900 hover:bg-slate-800 border border-cyan-500/30 px-3 py-2 rounded-xl text-xs font-bold text-cyan-400 transition">
                ⚙️ Âm thanh / Bot
            </button>
        </div>
    </header>

    <!-- ========================================================================================= -->
    <!-- TRANG 1 (MẶC ĐỊNH): BẢNG ĐIỀU KHIỂN HỌC TẬP, TO-DO LIST & THỜI KHÓA BIỂU RIÊNG BIỆT     -->
    <!-- ========================================================================================= -->
    <main id="page-dashboard" class="fixed inset-0 top-16 z-30 bg-[#060913] overflow-y-auto px-4 sm:px-8 py-6">
        <div class="max-w-7xl mx-auto space-y-6 pb-20">

            <!-- CẢNH BÁO DEADLINE KHẨN CẤP -->
            <div id="deadline-banner" class="hidden bg-gradient-to-r from-red-600/90 via-orange-600/90 to-amber-600/90 rounded-2xl p-4 shadow-xl border border-red-300/30 items-center justify-between gap-4">
                <div class="flex items-center gap-3">
                    <span class="text-2xl animate-bounce">⏰</span>
                    <div>
                        <div class="text-[10px] font-black uppercase tracking-widest bg-black/30 px-2 py-0.5 rounded inline-block mb-0.5">Nhắc nhở Gần tới Deadline</div>
                        <div id="deadline-banner-text" class="text-sm font-extrabold text-white"></div>
                    </div>
                </div>
                <button onclick="startFocusFromTopTask()" class="bg-white text-red-700 hover:bg-yellow-100 font-black text-xs px-4 py-2.5 rounded-xl shadow shrink-0">
                    🛫 Bay tập trung ngay
                </button>
            </div>

            <!-- HÀNG THỐNG KÊ TỔNG QUAN (4 THẺ KPI) -->
            <div class="grid grid-cols-2 lg:grid-cols-4 gap-4">
                <div class="dash-card rounded-2xl p-4 flex items-center justify-between">
                    <div>
                        <div class="text-[11px] text-slate-400 font-semibold">Thành viên đang chọn</div>
                        <div id="stat-member-name" class="text-lg font-black text-amber-400 mt-1">Hữu Đại</div>
                        <div class="text-[10px] text-slate-500 mt-0.5">Dữ liệu lưu vĩnh viễn</div>
                    </div>
                    <div class="w-11 h-11 rounded-2xl bg-amber-500/10 border border-amber-500/20 flex items-center justify-center text-xl">👤</div>
                </div>

                <div class="dash-card rounded-2xl p-4 flex items-center justify-between">
                    <div>
                        <div class="text-[11px] text-slate-400 font-semibold">Công việc đang chờ</div>
                        <div id="stat-pending-count" class="text-2xl font-black text-white mt-1 mono">0</div>
                        <div class="text-[10px] text-cyan-400 mt-0.5">Cần hoàn thành</div>
                    </div>
                    <div class="w-11 h-11 rounded-2xl bg-cyan-500/10 border border-cyan-500/20 flex items-center justify-center text-xl">📋</div>
                </div>

                <div class="dash-card rounded-2xl p-4 flex items-center justify-between">
                    <div>
                        <div class="text-[11px] text-slate-400 font-semibold">Đã hoàn thành (✓)</div>
                        <div id="stat-done-count" class="text-2xl font-black text-emerald-400 mt-1 mono">0</div>
                        <div id="stat-done-percent" class="text-[10px] text-emerald-500 mt-0.5">Tiến độ: 0%</div>
                    </div>
                    <div class="w-11 h-11 rounded-2xl bg-emerald-500/10 border border-emerald-500/20 flex items-center justify-center text-xl">✅</div>
                </div>

                <div class="dash-card rounded-2xl p-4 flex items-center justify-between">
                    <div>
                        <div class="text-[11px] text-slate-400 font-semibold">Dặm bay & Chuyến bay</div>
                        <div id="stat-miles-count" class="text-xl font-black text-blue-400 mt-1 mono">0 km</div>
                        <div id="stat-flights-count" class="text-[10px] text-slate-400 mt-0.5">Đã hạ cánh: 0 chuyến</div>
                    </div>
                    <div class="w-11 h-11 rounded-2xl bg-blue-500/10 border border-blue-500/20 flex items-center justify-center text-xl">🛂</div>
                </div>
            </div>

            <!-- KHU VỰC AI ĐỀ XUẤT: "HÔM NAY NÊN HỌC GÌ?" & ĐIỀU PHỐI LỊCH -->
            <div class="grid grid-cols-1 lg:grid-cols-12 gap-4">
                <div class="lg:col-span-8 bg-gradient-to-br from-blue-950/85 via-slate-900 to-slate-900 border border-cyan-500/30 rounded-3xl p-5 shadow-xl flex flex-col justify-between">
                    <div class="flex flex-wrap items-center justify-between gap-2 mb-3">
                        <div class="flex items-center gap-2">
                            <span class="bg-cyan-400 text-black font-black text-[10px] px-2.5 py-1 rounded-full uppercase tracking-wider">💡 Hôm nay nên học gì? (AI Đề xuất)</span>
                            <span class="text-xs text-slate-400">Tự động phân tích từ Deadline & Thời khóa biểu</span>
                        </div>
                        <button onclick="sendStudyReminderAlert()" class="bg-white/10 hover:bg-white/15 text-amber-300 border border-amber-400/30 px-3 py-1.5 rounded-xl text-xs font-bold transition">
                            🔔 Bật thông báo nhắc học
                        </button>
                    </div>

                    <div id="ai-today-suggestion" class="bg-black/40 border border-white/10 rounded-2xl p-4"></div>
                </div>

                <div class="lg:col-span-4 dash-card rounded-3xl p-5 flex flex-col justify-between">
                    <div>
                        <h3 class="text-sm font-extrabold text-white flex items-center gap-2 mb-1">
                            <span>⚡ Điều phối Lịch AI Thông Minh</span>
                        </h3>
                        <p class="text-xs text-slate-400 leading-relaxed">
                            Sắp xếp thứ tự ưu tiên tự động theo Deadline hoặc dời toàn bộ ca học khi bạn có lịch bận đột xuất.
                        </p>
                    </div>
                    <div class="space-y-2.5 mt-4">
                        <button onclick="aiSortTasks()" class="w-full bg-gradient-to-r from-amber-500 to-yellow-500 hover:opacity-95 text-black font-black py-2.5 px-4 rounded-xl text-xs shadow transition flex items-center justify-center gap-2">
                            <span>🤖 AI Sắp xếp Thứ tự Ưu tiên</span>
                        </button>
                        <button onclick="handleSuddenScheduleChange()" class="w-full bg-slate-800 hover:bg-slate-700 text-cyan-300 border border-cyan-500/30 font-bold py-2.5 px-4 rounded-xl text-xs transition flex items-center justify-center gap-2">
                            <span>🌪️ Có lịch đột xuất (Tự động dời ca)</span>
                        </button>
                    </div>
                </div>
            </div>

            <!-- KHU VỰC CHÍNH: CỘT TRÁI (TO-DO LIST KÉO THẢ) | CỘT PHẢI (THỜI KHÓA BIỂU CÁ NHÂN) -->
            <div class="grid grid-cols-1 lg:grid-cols-12 gap-6">

                <!-- CỘT TRÁI (7 PHẦN): TO-DO LIST & DEADLINE -->
                <div class="lg:col-span-7 dash-card rounded-3xl p-5 flex flex-col">
                    <div class="flex flex-wrap items-center justify-between gap-2 mb-4">
                        <div>
                            <h2 class="text-base font-extrabold text-white flex items-center gap-2">
                                <span>✅ Danh Sách Nhiệm Vụ & Deadline</span>
                                <span class="text-[10px] bg-blue-500/20 text-blue-300 px-2 py-0.5 rounded-lg border border-blue-400/30 font-semibold">Kéo thả ↕️</span>
                            </h2>
                            <p class="text-xs text-slate-400 mt-0.5">Nhấn vào vòng tròn <b>✓</b> để đánh dấu hoàn thành — thông tin được giữ lại vĩnh viễn</p>
                        </div>

                        <div class="flex bg-slate-900 p-1 rounded-xl border border-white/10 text-xs font-bold">
                            <button id="filter-all" onclick="setTaskFilter('all')" class="px-3 py-1 rounded-lg bg-blue-600 text-white">Tất cả</button>
                            <button id="filter-pending" onclick="setTaskFilter('pending')" class="px-3 py-1 rounded-lg text-slate-400 hover:text-white">Đang làm</button>
                            <button id="filter-done" onclick="setTaskFilter('done')" class="px-3 py-1 rounded-lg text-slate-400 hover:text-white">Đã xong ✓</button>
                        </div>
                    </div>

                    <!-- Form Thêm Nhiệm Vụ Trực Tiếp -->
                    <div class="bg-slate-900/90 border border-white/15 rounded-2xl p-3.5 mb-4 space-y-3">
                        <div class="text-xs font-bold text-cyan-400">+ Thêm công việc / bài tập mới:</div>
                        <div class="grid grid-cols-1 sm:grid-cols-12 gap-2.5">
                            <input type="text" id="quick-task-title" onkeydown="if(event.key==='Enter') addNewTask()" placeholder="Nhập tên công việc (VD: Tạo app, Ôn thi...)" class="sm:col-span-6 bg-slate-800 text-white text-xs px-3.5 py-2.5 rounded-xl border border-white/10 focus:outline-none focus:border-cyan-400" />
                            <div class="sm:col-span-3 flex items-center bg-slate-800 rounded-xl border border-white/10 px-2.5">
                                <span class="text-[10px] text-amber-300 font-bold mr-1.5 shrink-0">Hạn (Giờ):</span>
                                <input type="number" id="quick-task-hours" value="24" min="1" max="720" class="w-full bg-transparent text-white text-xs py-2 focus:outline-none font-bold" />
                            </div>
                            <select id="quick-task-importance" class="sm:col-span-3 bg-slate-800 text-amber-300 text-xs px-2.5 py-2.5 rounded-xl border border-white/10 font-bold focus:outline-none">
                                <option value="5">⭐⭐⭐⭐⭐ (Rất gấp)</option>
                                <option value="4" selected>⭐⭐⭐⭐ (Quan trọng)</option>
                                <option value="3">⭐⭐⭐ (Bình thường)</option>
                                <option value="2">⭐⭐ (Nhẹ nhàng)</option>
                            </select>
                        </div>
                        <div class="grid grid-cols-1 sm:grid-cols-12 gap-2.5 items-center">
                            <div class="sm:col-span-4 flex items-center bg-slate-800 rounded-xl border border-white/10 px-3 py-2">
                                <span class="text-[10px] text-slate-400 font-bold mr-2">Ca học:</span>
                                <input type="text" id="quick-task-slot" value="19:30 - 20:15" class="w-full bg-transparent text-white text-xs focus:outline-none font-mono" />
                            </div>
                            <div class="sm:col-span-4 flex items-center bg-slate-800 rounded-xl border border-white/10 px-3 py-2">
                                <span class="text-[10px] text-slate-400 font-bold mr-2">Thời lượng:</span>
                                <select id="quick-task-duration" class="w-full bg-transparent text-cyan-300 text-xs font-bold focus:outline-none">
                                    <option value="15" class="bg-slate-900">15 phút</option>
                                    <option value="25" class="bg-slate-900">25 phút</option>
                                    <option value="35" selected class="bg-slate-900">35 phút</option>
                                    <option value="45" class="bg-slate-900">45 phút</option>
                                    <option value="60" class="bg-slate-900">60 phút</option>
                                    <option value="90" class="bg-slate-900">90 phút</option>
                                </select>
                            </div>
                            <button onclick="addNewTask()" class="sm:col-span-4 bg-gradient-to-r from-blue-600 to-cyan-500 hover:opacity-95 text-white font-extrabold py-2.5 px-4 rounded-xl text-xs shadow-lg transition">
                                + Lưu Nhiệm Vụ
                            </button>
                        </div>
                    </div>

                    <div id="todo-drag-list" class="space-y-2.5 flex-1"></div>
                </div>

                <!-- CỘT PHẢI (5 PHẦN): THỜI KHÓA BIỂU CÁ NHÂN (TỰ THÊM / XÓA) -->
                <div class="lg:col-span-5 dash-card rounded-3xl p-5 flex flex-col">
                    <div class="flex items-center justify-between mb-3">
                        <div>
                            <h2 class="text-base font-extrabold text-white flex items-center gap-2">
                                <span>🗓️ Thời Khóa Biểu Cá Nhân</span>
                                <span id="timetable-owner-badge" class="text-xs text-amber-400 font-black"></span>
                            </h2>
                            <p class="text-xs text-slate-400 mt-0.5">Tự thêm hoặc xóa ca học / khung giờ trống của riêng bạn</p>
                        </div>
                    </div>

                    <div class="grid grid-cols-7 gap-1.5 mb-4" id="day-tabs-container"></div>

                    <div class="bg-slate-900/90 border border-white/15 rounded-2xl p-3.5 mb-4 space-y-2.5">
                        <div class="text-xs font-bold text-emerald-400">+ Thêm khung giờ vào ngày <span id="add-slot-day-label">T2</span>:</div>
                        <div class="grid grid-cols-1 sm:grid-cols-2 gap-2">
                            <input type="text" id="new-slot-time" placeholder="Giờ (VD: 07:30 - 11:00)" class="bg-slate-800 text-white text-xs px-3 py-2 rounded-xl border border-white/10 focus:outline-none" />
                            <select id="new-slot-type" class="bg-slate-800 text-white text-xs px-3 py-2 rounded-xl border border-white/10 font-bold focus:outline-none">
                                <option value="free">🟢 Giờ trống (Dành tự học)</option>
                                <option value="busy">🔴 Lịch học trên trường / Bận</option>
                            </select>
                        </div>
                        <div class="flex gap-2">
                            <input type="text" id="new-slot-subject" onkeydown="if(event.key==='Enter') saveNewTimetableSlot()" placeholder="Tên môn học hoặc ghi chú..." class="flex-1 bg-slate-800 text-white text-xs px-3 py-2 rounded-xl border border-white/10 focus:outline-none" />
                            <button onclick="saveNewTimetableSlot()" class="bg-emerald-600 hover:bg-emerald-500 text-white font-extrabold px-4 py-2 rounded-xl text-xs shrink-0 shadow">
                                + Thêm Lịch
                            </button>
                        </div>
                    </div>

                    <div id="timetable-slots-list" class="space-y-2.5 flex-1"></div>
                </div>

            </div>
        </div>
    </main>

    <!-- ========================================================================================= -->
    <!-- TRANG 2 (RIÊNG BIỆT): TRẠM BAY TẬP TRUNG, 4 GÓC NHÌN CAMERA & BAY XUYÊN ĐÊM              -->
    <!-- ========================================================================================= -->
    <section id="page-flight" class="fixed inset-0 top-16 z-20 hidden">
        <!-- GÓC NHÌN 1: BẢN ĐỒ VỆ TINH RADAR -->
        <div id="map"></div>

        <!-- THANH ĐIỀU KHIỂN 4 GÓC NHÌN CAMERA & CHẾ ĐỘ NGÀY/ĐÊM/MƯA (Hiện khi đang bay hoặc xem trước) -->
        <div id="flight-top-hud" class="fixed top-20 left-1/2 -translate-x-1/2 z-35 w-[96%] max-w-4xl flex flex-wrap items-center justify-between gap-2 pointer-events-none">
            <!-- Bộ chuyển 4 Góc nhìn Camera -->
            <div class="glass-panel p-1 rounded-2xl flex items-center gap-1 pointer-events-auto shadow-2xl border border-cyan-400/30">
                <button id="cam-btn-map" onclick="setCameraView('map')" class="px-3 py-1.5 rounded-xl text-[11px] font-extrabold bg-cyan-500 text-black shadow transition">
                    🗺️ Toàn Bản Đồ
                </button>
                <button id="cam-btn-cockpit" onclick="setCameraView('cockpit')" class="px-3 py-1.5 rounded-xl text-[11px] font-extrabold text-slate-300 hover:text-white transition">
                    👨‍✈️ Buồng Lái Phi Công
                </button>
                <button id="cam-btn-cabin" onclick="setCameraView('cabin')" class="px-3 py-1.5 rounded-xl text-[11px] font-extrabold text-slate-300 hover:text-white transition">
                    💺 Trong Khoang Cabin
                </button>
                <button id="cam-btn-window" onclick="setCameraView('window')" class="px-3 py-1.5 rounded-xl text-[11px] font-extrabold text-slate-300 hover:text-white transition">
                    🪟 Qua Cửa Sổ
                </button>
            </div>

            <!-- Bộ chuyển Thời gian Bay: Ngày / Hoàng hôn / Bay Đêm / Mưa Đêm -->
            <div class="glass-panel p-1 rounded-2xl flex items-center gap-1 pointer-events-auto shadow-2xl border border-amber-400/30">
                <button id="env-btn-day" onclick="setFlightEnvironment('day')" class="px-2.5 py-1.5 rounded-xl text-[11px] font-bold bg-amber-400 text-black">
                    ☀️ Ngày
                </button>
                <button id="env-btn-sunset" onclick="setFlightEnvironment('sunset')" class="px-2.5 py-1.5 rounded-xl text-[11px] font-bold text-slate-300 hover:text-white">
                    🌅 Hoàng hôn
                </button>
                <button id="env-btn-night" onclick="setFlightEnvironment('night')" class="px-2.5 py-1.5 rounded-xl text-[11px] font-bold text-slate-300 hover:text-white">
                    🌙 Bay Đêm
                </button>
                <button id="env-btn-rain" onclick="setFlightEnvironment('rain')" class="px-2.5 py-1.5 rounded-xl text-[11px] font-bold text-slate-300 hover:text-white">
                    🌧️ Mưa Đêm
                </button>
            </div>
        </div>

        <!-- ================= GÓC NHÌN 2: BUỒNG LÁI PHI CÔNG (COCKPIT HUD VIEW) ================= -->
        <div id="view-cockpit" class="fixed inset-0 top-16 z-25 hidden flex-col justify-between overflow-hidden">
            <!-- Bầu trời phía trước mũi máy bay -->
            <div id="cockpit-sky-bg" class="absolute inset-0 bg-gradient-to-b from-[#040b1a] via-[#0c2249] to-[#1e3a8a] transition-all duration-700">
                <!-- Các ngôi sao khi bay đêm -->
                <div id="cockpit-stars" class="absolute inset-0 opacity-90" style="background-image: radial-gradient(white 1px, transparent 1px), radial-gradient(rgba(255,255,255,0.7) 1.5px, transparent 1.5px); background-size: 55px 55px, 95px 95px; background-position: 0 0, 25px 25px;"></div>
                <!-- Đám mây lướt qua -->
                <div class="cloud-anim-1 absolute top-1/3 w-96 h-24 bg-white/10 blur-2xl rounded-full"></div>
                <div class="cloud-anim-2 absolute top-1/2 w-[500px] h-28 bg-cyan-300/10 blur-3xl rounded-full"></div>
                <!-- Hiệu ứng mưa trên kính chắn gió buồng lái -->
                <div id="cockpit-rain-layer" class="rain-overlay absolute inset-0 hidden pointer-events-none"></div>
            </div>

            <!-- Kính chắn gió & Màn hình HUD xanh lá của Cơ trưởng -->
            <div class="relative z-10 flex-1 flex items-center justify-center pointer-events-none mt-10">
                <!-- Khung cột chia đôi kính chắn gió buồng lái -->
                <div class="absolute inset-y-0 left-1/2 -translate-x-1/2 w-5 bg-gradient-to-r from-slate-950 via-slate-800 to-slate-950 border-x border-white/10"></div>

                <!-- Màn hình HUD (Head-Up Display) phát sáng xanh lá -->
                <div class="w-[340px] sm:w-[460px] h-[270px] sm:h-[310px] border-2 border-emerald-400/50 rounded-3xl bg-emerald-950/10 backdrop-blur-[1px] p-4 flex flex-col justify-between shadow-[0_0_50px_rgba(16,185,129,0.15)]">
                    <!-- Thanh La bàn số phía trên -->
                    <div class="flex justify-between items-center text-[11px] font-mono font-bold text-emerald-400 border-b border-emerald-400/30 pb-1.5">
                        <span>SPD: <b id="hud-speed">845 KM/H</b></span>
                        <span class="bg-emerald-400/20 px-2 py-0.5 rounded border border-emerald-400/40">HDG <b id="hud-heading">045°</b></span>
                        <span>ALT: <b id="hud-alt">36,000 FT</b></span>
                    </div>

                    <!-- Đường chân trời nhân tạo (Artificial Horizon) nghiêng nhẹ -->
                    <div class="relative flex-1 flex items-center justify-center overflow-hidden my-2">
                        <div class="hud-horizon w-56 flex flex-col items-center space-y-3">
                            <div class="w-32 border-b border-dashed border-emerald-400/60 text-[9px] font-mono text-emerald-400 flex justify-between"><span>+10</span><span>+10</span></div>
                            <div class="w-48 border-b-2 border-emerald-400 text-[10px] font-mono text-emerald-300 flex justify-between"><span>0</span><span>PITCH</span><span>0</span></div>
                            <div class="w-32 border-b border-dashed border-emerald-400/60 text-[9px] font-mono text-emerald-400 flex justify-between"><span>-10</span><span>-10</span></div>
                        </div>
                        <!-- Tâm ngắm máy bay cố định -->
                        <div class="absolute text-emerald-300 font-mono font-black text-lg">─ ✛ ─</div>
                    </div>

                    <!-- Thông tin Tác vụ & Máy bay trên HUD -->
                    <div class="flex justify-between items-center text-[10px] font-mono text-emerald-300 border-t border-emerald-400/30 pt-1.5">
                        <span id="hud-aircraft-name">AIRBUS A321NEO • AUTOPILOT ON</span>
                        <span id="hud-route-code">SGN ➔ DAD</span>
                    </div>
                </div>
            </div>

            <!-- Bảng táp-lô Buồng lái phía dưới (Cockpit Glare-shield & Màn hình PFD/ND) -->
            <div class="relative z-10 h-52 bg-gradient-to-t from-[#05070e] via-[#0d1322] to-[#1a243b] border-t-4 border-slate-700/80 px-6 py-3 shadow-2xl">
                <div class="max-w-4xl mx-auto grid grid-cols-3 gap-4 h-full pb-20">
                    <!-- Màn hình PFD Trái -->
                    <div class="bg-[#060a12] border-2 border-slate-700 rounded-xl p-2.5 flex flex-col justify-between font-mono">
                        <div class="text-[10px] text-cyan-400 font-bold flex justify-between"><span>PFD • MACH 0.79</span><span class="text-emerald-400">AP1 + FD</span></div>
                        <div class="flex items-center justify-center my-auto">
                            <div id="cockpit-plane-svg-preview" class="w-12 h-12"></div>
                        </div>
                        <div class="text-[10px] text-slate-400 flex justify-between"><span>TAT -24°C</span><span>SAT -54°C</span></div>
                    </div>

                    <!-- Màn hình ECAM Giữa: Đồng hồ Tập trung -->
                    <div class="bg-[#060a12] border-2 border-cyan-500/40 rounded-xl p-2.5 flex flex-col items-center justify-center font-mono">
                        <div class="text-[9px] text-amber-400 uppercase font-bold">FOCUS MISSION TIMER</div>
                        <div id="cockpit-timer-display" class="text-2xl sm:text-3xl font-extrabold text-white tracking-wider">35:00</div>
                        <div id="cockpit-task-display" class="text-[10px] text-cyan-300 truncate max-w-[180px]">💻 Work</div>
                    </div>

                    <!-- Màn hình Radar ND Phải -->
                    <div class="bg-[#060a12] border-2 border-slate-700 rounded-xl p-2.5 flex flex-col justify-between font-mono relative overflow-hidden">
                        <div class="text-[10px] text-emerald-400 font-bold flex justify-between"><span>NAV RADAR</span><span id="cockpit-dist-display">610 KM</span></div>
                        <div class="w-16 h-16 rounded-full border border-emerald-500/40 mx-auto my-auto flex items-center justify-center relative">
                            <div class="radar-ring absolute inset-0 rounded-full border border-emerald-400"></div>
                            <span class="text-xs">✈️</span>
                        </div>
                        <div class="text-[9px] text-slate-400 text-center">TCAS TA/RA • WX ON</div>
                    </div>
                </div>
            </div>
        </div>

        <!-- ================= GÓC NHÌN 3: TRONG KHOANG CABIN (CABIN INTERIOR VIEW) ================= -->
        <div id="view-cabin" class="fixed inset-0 top-16 z-25 hidden flex-col items-center justify-center bg-gradient-to-b from-[#131129] via-[#0e172a] to-[#060913] p-4 overflow-hidden">
            <!-- Đèn LED trần khoang máy bay (Mood Lighting) -->
            <div id="cabin-ceiling-glow" class="absolute top-0 inset-x-0 h-32 bg-gradient-to-b from-purple-500/30 via-cyan-500/15 to-transparent blur-2xl pointer-events-none transition-all duration-700"></div>

            <!-- Thanh tín hiệu Fasten Seatbelt & Nút đổi màu đèn trần Cabin -->
            <div class="relative z-10 flex flex-wrap items-center justify-center gap-3 mb-4 mt-8">
                <div class="bg-slate-900/90 border border-white/15 px-3.5 py-1.5 rounded-full flex items-center gap-3 text-xs">
                    <span class="text-amber-400 font-bold flex items-center gap-1">🔔 FASTEN SEATBELT</span>
                    <span class="text-slate-600">|</span>
                    <span class="text-red-400 font-bold flex items-center gap-1">🚭 NO DISTRACTION</span>
                </div>
                <button onclick="cycleCabinMoodLight()" class="bg-white/10 hover:bg-white/20 border border-white/20 px-3 py-1.5 rounded-full text-xs font-bold text-cyan-300 transition">
                    🌈 Đổi màu đèn LED Cabin
                </button>
            </div>

            <!-- Lưng ghế phía trước & Màn hình Giải trí IFE (In-Flight Entertainment) -->
            <div class="relative z-10 w-full max-w-xl bg-gradient-to-b from-[#1e293b] to-[#0f172a] border-4 border-slate-700/80 rounded-t-[48px] rounded-b-3xl p-5 sm:p-6 shadow-2xl mb-16">
                <!-- Gối tựa đầu ghế trước -->
                <div class="w-48 h-8 bg-slate-800 border border-white/10 rounded-b-2xl mx-auto -mt-6 mb-4 flex items-center justify-center text-[10px] font-extrabold text-amber-300 tracking-widest uppercase">
                    SEAT <span id="cabin-seat-label" class="ml-1">06A</span>
                </div>

                <!-- Màn hình cảm ứng IFE sau lưng ghế -->
                <div class="bg-[#060a14] border-4 border-slate-950 rounded-2xl p-4 sm:p-5 shadow-inner relative overflow-hidden">
                    <div class="flex items-center justify-between border-b border-white/10 pb-3 mb-3">
                        <div class="flex items-center gap-2">
                            <span class="bg-blue-600 text-white text-[10px] font-black px-2 py-0.5 rounded">IFE ENTERTAINMENT</span>
                            <span id="cabin-aircraft-label" class="text-xs font-bold text-cyan-400 mono">Airbus A321neo</span>
                        </div>
                        <div id="cabin-route-label" class="text-xs font-extrabold text-yellow-400 mono">SGN ➔ DAD</div>
                    </div>

                    <div class="grid grid-cols-1 sm:grid-cols-2 gap-4 items-center">
                        <div>
                            <div class="text-[10px] text-slate-400 uppercase font-bold">Nhiệm vụ đang tập trung</div>
                            <div id="cabin-task-title" class="text-sm sm:text-base font-extrabold text-white mt-0.5">💻 Work</div>
                            <div class="text-[11px] text-emerald-400 mt-1">👤 Hành khách: <b id="cabin-passenger-name">Hữu Đại</b></div>
                            <div class="mt-3 flex items-center gap-2 text-[11px] text-slate-300 font-mono">
                                <span>🏔️ 36,000 FT</span>
                                <span>•</span>
                                <span>💨 845 KM/H</span>
                            </div>
                        </div>

                        <div class="bg-slate-900/90 border border-white/10 rounded-2xl p-3 text-center">
                            <div class="text-[10px] text-slate-400 uppercase">Thời gian hạ cánh</div>
                            <div id="cabin-timer-display" class="text-3xl font-black text-cyan-400 mono my-0.5">35:00</div>
                            <div class="text-[10px] text-amber-300">Còn <span id="cabin-dist-display">610</span> km</div>
                        </div>
                    </div>
                </div>

                <!-- Bàn ăn gấp gọn dưới màn hình -->
                <div class="mt-4 h-7 bg-slate-800/90 border border-white/10 rounded-xl flex items-center justify-between px-4 text-[10px] text-slate-400 font-bold">
                    <span>☕ TRAY TABLE LOCKED</span>
                    <span>🎧 LOFI AUDIO CHANNEL ACTIVE</span>
                </div>
            </div>
        </div>

        <!-- ================= GÓC NHÌN 4: QUA CỬA SỔ MÁY BAY (WINDOW SEAT VIEW) ================= -->
        <div id="view-window" class="fixed inset-0 top-16 z-25 hidden flex-col items-center justify-center bg-[#090d18] p-4 overflow-hidden">
            <!-- Nút Kéo Rèm Cửa Sổ -->
            <div class="relative z-20 flex items-center gap-3 mb-3 mt-6">
                <button onclick="toggleWindowShade()" class="glass-panel px-4 py-1.5 rounded-full text-xs font-extrabold text-amber-300 hover:text-white border border-amber-400/30 transition">
                    🪟 Kéo Rèm Cửa Sổ Lên / Xuống
                </button>
            </div>

            <!-- Khung Cửa Sổ Bầu Dục Máy Bay Thực Tế -->
            <div class="relative w-[310px] sm:w-[370px] h-[430px] sm:h-[470px] rounded-[160px] border-[18px] border-[#1e293b] shadow-[inset_0_0_40px_rgba(0,0,0,0.9),0_25px_70px_rgba(0,0,0,0.95)] overflow-hidden bg-gradient-to-b from-[#040b1d] via-[#0f2557] to-[#1e3a8a] mb-16" id="window-sky-container">
                <!-- Sao đêm ngoài cửa sổ -->
                <div id="window-stars" class="absolute inset-0 opacity-90" style="background-image: radial-gradient(white 1.2px, transparent 1.2px), radial-gradient(rgba(255,255,255,0.6) 1px, transparent 1px); background-size: 45px 45px, 80px 80px;"></div>

                <!-- Mặt trăng / Mặt trời ngoài cửa sổ -->
                <div id="window-celestial" class="absolute top-12 right-14 w-12 h-12 rounded-full bg-yellow-100 shadow-[0_0_35px_#fef08a]"></div>

                <!-- Đám mây trôi qua cánh máy bay -->
                <div class="cloud-anim-1 absolute top-44 w-72 h-16 bg-white/20 blur-xl rounded-full"></div>
                <div class="cloud-anim-3 absolute bottom-28 w-80 h-20 bg-white/15 blur-xl rounded-full"></div>

                <!-- Ánh đèn thành phố ban đêm phía dưới mặt đất -->
                <div id="window-city-lights" class="absolute bottom-0 inset-x-0 h-16 bg-gradient-to-t from-amber-500/25 via-orange-500/10 to-transparent"></div>

                <!-- CÁNH MÁY BAY & ĐỘNG CƠ NHÌN TỪ CỬA SỔ -->
                <div class="absolute bottom-14 right-0 w-[270px] h-[140px] pointer-events-none">
                    <svg viewBox="0 0 300 160" class="w-full h-full drop-shadow-2xl">
                        <!-- Động cơ phản lực dưới cánh -->
                        <ellipse cx="145" cy="112" rx="34" ry="18" fill="#334155" stroke="#64748b" stroke-width="2"/>
                        <ellipse cx="115" cy="112" rx="8" ry="15" fill="#0f172a" stroke="#38bdf8" stroke-width="1.5"/>
                        <!-- Thân cánh máy bay nghiêng ra xa -->
                        <polygon points="300,35 35,95 55,112 300,98" fill="#cbd5e1" stroke="#94a3b8" stroke-width="2"/>
                        <!-- Đầu cánh Sharklet / Winglet -->
                        <polygon points="35,95 15,62 28,60 55,112" fill="#0ea5e9"/>
                        <!-- Đèn nháy đỏ đầu cánh (Strobe Light) -->
                        <circle cx="22" cy="62" r="5" fill="#ef4444" class="strobe-light"/>
                    </svg>
                </div>

                <!-- Lớp mưa trên kính cửa sổ -->
                <div id="window-rain-layer" class="rain-overlay absolute inset-0 hidden pointer-events-none"></div>

                <!-- Rèm cửa sổ kéo xuống -->
                <div id="window-shade-panel" class="absolute inset-x-0 top-0 h-0 bg-gradient-to-b from-slate-800 to-slate-900 border-b-4 border-slate-600 transition-all duration-500 flex items-end justify-center pb-2 overflow-hidden">
                    <div class="w-12 h-1.5 rounded-full bg-slate-400"></div>
                </div>
            </div>
        </div>

        <!-- Nút thu gọn / mở rộng bảng chọn chuyến bay -->
        <button id="toggle-booking-btn" onclick="toggleBookingCardSize()" class="fixed bottom-4 left-4 z-30 glass-panel px-3.5 py-2 rounded-xl text-xs font-extrabold text-cyan-300 hover:text-white shadow-lg border border-cyan-500/30">
            🔽 Thu gọn bảng đặt vé
        </button>

        <!-- MÀN HÌNH 1 TRONG TRẠM BAY: BẢNG ĐẶT VÉ NHỎ GỌN (COMPACT DOCK) -->
        <div id="screen-booking" class="fixed bottom-4 left-1/2 -translate-x-1/2 z-30 w-[94%] max-w-md glass-panel rounded-3xl p-4 shadow-2xl transition-all duration-300">
            <div class="flex items-center justify-between gap-2 mb-3 pb-2.5 border-b border-white/10">
                <div class="flex items-center gap-2.5">
                    <!-- Xem trước Mô hình SVG của loại máy bay đang chọn -->
                    <div id="booking-plane-svg-box" class="w-11 h-11 rounded-xl bg-slate-900 border border-cyan-400/30 flex items-center justify-center p-1 shrink-0"></div>
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

                <select id="aircraft-select" onchange="updateAircraft()" class="bg-slate-800 text-cyan-300 text-[11px] font-bold px-2.5 py-1.5 rounded-xl border border-cyan-500/30 focus:outline-none cursor-pointer">
                    <option value="Airbus A321neo">🛩️ Airbus A321neo</option>
                    <option value="Boeing 787-9">✈️ Boeing 787-9</option>
                    <option value="Airbus A350-900">🛫 Airbus A350-900</option>
                    <option value="ATR 72-600">⚙️ ATR 72-600 (Cánh quạt)</option>
                </select>
            </div>

            <!-- Chọn Điểm Đi & Điểm Đến (34 Sân bay) -->
            <div class="grid grid-cols-11 gap-1.5 items-center bg-slate-900/90 p-2.5 rounded-2xl border border-white/10 mb-3">
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

            <div class="flex items-center justify-between mb-1.5">
                <span class="text-[11px] text-slate-300 font-semibold">Thời gian tập trung:</span>
                <button onclick="randomRoute()" class="text-[11px] text-cyan-400 font-bold hover:underline">🎲 Random sân bay</button>
            </div>

            <div class="grid grid-cols-6 gap-1.5 mb-3">
                <button onclick="setDuration(15)" id="dur-15" class="dur-btn bg-slate-800 py-1.5 rounded-xl text-xs font-bold text-slate-300 border border-transparent">15m</button>
                <button onclick="setDuration(25)" id="dur-25" class="dur-btn bg-slate-800 py-1.5 rounded-xl text-xs font-bold text-slate-300 border border-transparent">25m</button>
                <button onclick="setDuration(35)" id="dur-35" class="dur-btn bg-blue-600/30 border-blue-400 text-blue-300 py-1.5 rounded-xl text-xs font-bold border">35m</button>
                <button onclick="setDuration(45)" id="dur-45" class="dur-btn bg-slate-800 py-1.5 rounded-xl text-xs font-bold text-slate-300 border border-transparent">45m</button>
                <button onclick="setDuration(60)" id="dur-60" class="dur-btn bg-slate-800 py-1.5 rounded-xl text-xs font-bold text-slate-300 border border-transparent">60m</button>
                <button onclick="setDuration(90)" id="dur-90" class="dur-btn bg-slate-800 py-1.5 rounded-xl text-xs font-bold text-slate-300 border border-transparent">90m</button>
            </div>

            <button onclick="goToSeatSelection()" class="w-full bg-gradient-to-r from-blue-600 to-cyan-500 hover:opacity-95 text-white font-extrabold py-3 rounded-2xl shadow-lg shadow-blue-600/30 transition flex items-center justify-center gap-2 text-xs uppercase tracking-wider">
                <span>Book Now • Chọn Ghế & Chế Độ Học</span>
                <span>➔</span>
            </button>
        </div>

        <!-- MÀN HÌNH 2 TRONG TRẠM BAY: CHỌN GHẾ NGỒI -->
        <div id="screen-seat" class="fixed inset-0 top-16 z-35 bg-[#070b14]/95 backdrop-blur-xl hidden flex-col items-center justify-between py-4 px-4">
            <div class="w-full max-w-md flex items-center justify-between">
                <button onclick="backToBooking()" class="bg-slate-800 hover:bg-slate-700 text-slate-200 px-3.5 py-2 rounded-xl text-xs font-bold">‹ Quay lại</button>
                <div class="text-center">
                    <div id="seat-header-aircraft" class="text-[10px] text-cyan-400 font-extrabold uppercase tracking-widest">AIRBUS A321NEO</div>
                    <div id="seat-header-route" class="text-sm font-extrabold text-white mt-0.5">SGN ➔ DAD • 35m</div>
                </div>
                <span id="seat-selected-badge" class="bg-blue-600/30 border border-blue-400 text-blue-200 text-xs font-mono font-bold px-2.5 py-1 rounded-lg">06A</span>
            </div>

            <div class="relative w-full max-w-[330px] h-[64vh] fuselage flex flex-col items-center pt-10 pb-8 px-6 overflow-y-auto my-1">
                <div class="w-32 h-6 border-b border-slate-700/80 mb-4 flex items-center justify-center text-[10px] font-mono text-slate-500 tracking-widest uppercase">Cockpit</div>
                <div class="grid grid-cols-5 w-full text-center text-xs font-extrabold text-slate-400 mb-2 px-1">
                    <div>A</div><div>C</div><div></div><div>D</div><div>F</div>
                </div>
                <div id="seat-grid" class="w-full space-y-2 pb-6"></div>
            </div>

            <!-- POPUP "What do you want to focus?" -->
            <div id="focus-popover-backdrop" class="fixed inset-0 z-40 bg-black/60 backdrop-blur-sm hidden items-center justify-center p-4">
                <div class="focus-popover w-full max-w-[360px] rounded-[28px] p-5 text-white">
                    <div class="flex justify-between items-center mb-1">
                        <span class="text-xs font-bold text-blue-300">Seat: <span id="pop-seat-code" class="mono text-white">06A</span></span>
                        <button onclick="closeFocusPopover()" class="text-slate-400 hover:text-white text-sm font-bold">✕</button>
                    </div>
                    <h3 class="text-base font-extrabold text-white mb-3">What do you want to focus?</h3>

                    <div class="flex flex-wrap gap-2 mb-3" id="focus-pills-container"></div>

                    <div id="custom-focus-box" class="mb-3">
                        <label class="block text-[10px] text-slate-300 font-bold mb-1">Nhiệm vụ trong chuyến bay này:</label>
                        <input type="text" id="custom-focus-input" placeholder="Nhập tên công việc (VD: Tạo app, Học bài...)" class="w-full bg-slate-900/90 text-xs text-white px-3.5 py-2.5 rounded-xl border border-blue-400/40 focus:outline-none" />
                    </div>

                    <div class="bg-red-500/15 border border-red-400/30 p-3 rounded-2xl flex items-center justify-between mb-4">
                        <div>
                            <div class="text-xs font-extrabold text-red-200">🔒 Khóa Kỷ Luật (Strict Mode)</div>
                            <div class="text-[10px] text-slate-300">Báo động đỏ nếu tự ý chuyển sang Tab khác</div>
                        </div>
                        <input type="checkbox" id="strict-mode-toggle" checked class="w-5 h-5 accent-red-500 cursor-pointer" />
                    </div>

                    <button onclick="confirmSeatAndFocus()" class="w-full bg-blue-500 hover:bg-blue-400 text-white font-extrabold py-3 rounded-2xl text-xs shadow-lg">
                        Xác nhận & Xuất Vé Máy Bay ➔
                    </button>
                </div>
            </div>

            <div class="w-full max-w-md flex items-center justify-between px-2">
                <div class="text-xs text-slate-400">Chạm vào ghế bất kỳ để chọn mục tiêu</div>
                <button onclick="showBoardingPass()" class="bg-blue-600 hover:bg-blue-500 text-white font-extrabold px-5 py-2 rounded-xl text-xs shadow-lg">Tiếp tục ➔</button>
            </div>
        </div>

        <!-- MÀN HÌNH 3 TRONG TRẠM BAY: VÉ BOARDING PASS -->
        <div id="screen-ticket" class="fixed inset-0 top-16 z-40 bg-black/85 backdrop-blur-md hidden items-center justify-center p-4">
            <div class="w-full max-w-sm flex flex-col items-center">
                <div class="w-full bg-[#121723] border border-white/15 rounded-3xl overflow-hidden shadow-2xl relative">
                    <div class="ticket-cutout-left"></div>
                    <div class="ticket-cutout-right"></div>

                    <div class="bg-gradient-to-r from-blue-600 to-cyan-500 px-6 py-3 flex justify-between items-center">
                        <span class="text-xs font-black tracking-widest uppercase text-white">BOARDING PASS</span>
                        <span id="tk-aircraft" class="text-[11px] font-mono font-bold bg-black/25 text-white px-2 py-0.5 rounded">Airbus A321neo</span>
                    </div>

                    <div class="p-6">
                        <div class="flex justify-between items-start mb-4">
                            <div>
                                <div class="text-[10px] text-slate-400 uppercase">Hành khách</div>
                                <div id="tk-passenger" class="text-base font-black text-amber-300 uppercase">HỮU ĐẠI</div>
                            </div>
                            <div class="text-right">
                                <div class="text-[10px] text-slate-400 uppercase">Chế độ kỷ luật</div>
                                <div id="tk-strict-badge" class="text-[11px] font-extrabold text-red-400">🔒 STRICT LOCK ON</div>
                            </div>
                        </div>

                        <div class="flex justify-between items-center my-4">
                            <div>
                                <div id="tk-origin-code" class="text-4xl font-black text-white">SGN</div>
                                <div id="tk-origin-name" class="text-xs text-slate-400 mt-0.5">TP.HCM</div>
                            </div>
                            <div class="flex flex-col items-center">
                                <div id="tk-plane-svg" class="w-9 h-9"></div>
                                <span id="tk-duration" class="text-xs font-extrabold text-yellow-400 mt-0.5">35m</span>
                            </div>
                            <div class="text-right">
                                <div id="tk-dest-code" class="text-4xl font-black text-yellow-400">DAD</div>
                                <div id="tk-dest-name" class="text-xs text-slate-400 mt-0.5">Đà Nẵng</div>
                            </div>
                        </div>

                        <div class="grid grid-cols-3 gap-2 pt-4 border-t border-white/10 text-xs mb-5">
                            <div>
                                <div class="text-slate-500 text-[10px] uppercase">Ghế ngồi</div>
                                <div id="tk-seat" class="font-extrabold text-cyan-400 mt-0.5 mono">06A</div>
                            </div>
                            <div>
                                <div class="text-slate-500 text-[10px] uppercase">Quãng đường</div>
                                <div id="tk-dist" class="font-bold text-white mt-0.5">610 km</div>
                            </div>
                            <div class="text-right">
                                <div class="text-slate-500 text-[10px] uppercase">Mục tiêu</div>
                                <div id="tk-focus" class="font-extrabold text-blue-300 mt-0.5 truncate">💻 Work</div>
                            </div>
                        </div>

                        <div class="border-b-2 border-dashed border-slate-700/80 my-4"></div>
                        <div class="flex flex-col items-center mt-3">
                            <div class="mono text-[10px] tracking-[0.35em] text-cyan-400 font-bold">CLEARED FOR TAKEOFF</div>
                        </div>
                    </div>
                </div>

                <div class="flex gap-2 w-full mt-4">
                    <button onclick="backToSeatFromTicket()" class="w-1/3 bg-slate-800 hover:bg-slate-700 text-slate-300 font-bold py-3.5 rounded-2xl text-xs">‹ Đổi ghế</button>
                    <button onclick="startFlight()" class="w-2/3 bg-gradient-to-r from-blue-600 to-cyan-500 hover:opacity-95 text-white font-extrabold py-3.5 rounded-2xl shadow-xl text-xs uppercase tracking-wider">
                        🛫 Cất Cánh Bắt Đầu Học
                    </button>
                </div>
            </div>
        </div>

        <!-- MÀN HÌNH 4 TRONG TRẠM BAY: THANH TELEMETRY & ĐỒNG HỒ ĐẾM NGƯỢC KHI ĐANG BAY -->
        <div id="screen-flying" class="fixed bottom-4 left-1/2 -translate-x-1/2 z-30 w-[95%] max-w-lg glass-panel rounded-3xl p-4 shadow-2xl hidden">
            <div class="flex items-center justify-between border-b border-white/10 pb-2.5 mb-2.5">
                <div class="flex items-center gap-2.5">
                    <div id="fly-mini-svg" class="w-9 h-9 rounded-xl bg-slate-900 border border-cyan-400/40 p-1 flex items-center justify-center"></div>
                    <div>
                        <div class="text-xs font-extrabold text-white" id="fly-route-text">TP.HCM ➔ Đà Nẵng</div>
                        <div class="text-[11px] text-cyan-400 font-semibold" id="fly-sub-info">Airbus A321neo • Ghế 06A</div>
                    </div>
                </div>
                <div class="text-right">
                    <div class="text-[9px] text-slate-400 uppercase font-bold">An toàn bay</div>
                    <div id="safety-hearts" class="text-xs tracking-widest">❤️❤️❤️</div>
                </div>
            </div>

            <div class="flex items-end justify-between">
                <div>
                    <div class="text-[10px] uppercase tracking-widest text-slate-400 flex items-center gap-2">
                        <span>Thời gian còn lại</span>
                        <span id="telemetry-live-badge" class="text-[9px] text-emerald-400 font-mono">● 845 KM/H • 36,000 FT</span>
                    </div>
                    <div id="countdown-timer" class="mono text-3xl font-extrabold text-white tracking-tight">35:00</div>
                </div>
                <div class="text-right">
                    <div class="text-[11px] text-slate-300 font-semibold mb-1">Còn <span id="fly-dist-left" class="text-yellow-400 font-bold">610</span> km</div>
                    <div class="flex gap-1.5">
                        <button onclick="centerOnPlane()" class="bg-slate-800 hover:bg-slate-700 text-xs px-2.5 py-1.5 rounded-xl text-slate-200 border border-white/10 font-bold" title="Tâm máy bay">🎯</button>
                        <button onclick="completeFlightEarly()" class="bg-emerald-500/20 hover:bg-emerald-500/30 text-emerald-300 border border-emerald-500/30 px-3 py-1.5 rounded-xl text-xs font-bold">✓ Xong sớm</button>
                        <button onclick="abortFlight()" class="bg-red-500/20 hover:bg-red-500/30 text-red-300 border border-red-500/30 px-3 py-1.5 rounded-xl text-xs font-bold">Hủy</button>
                    </div>
                </div>
            </div>

            <div class="w-full bg-slate-800 h-2 rounded-full overflow-hidden mt-3">
                <div id="flight-progress" class="bg-gradient-to-r from-blue-500 via-cyan-400 to-yellow-400 h-full w-0 transition-all duration-500"></div>
            </div>
        </div>
    </section>

    <!-- ================= MODAL GIẢI THÍCH "TẠI SAO LẠI CÓ LỊCH NÀY?" ================= -->
    <div id="why-schedule-modal" class="fixed inset-0 z-50 bg-black/75 backdrop-blur-md hidden items-center justify-center p-4">
        <div class="glass-panel w-full max-w-md rounded-3xl p-6 shadow-2xl border border-cyan-400/40">
            <div class="flex justify-between items-center mb-3">
                <h3 class="text-base font-extrabold text-white">🧠 Tại sao AI lại xếp ưu tiên lịch này?</h3>
                <button onclick="closeWhyModal()" class="text-slate-400 hover:text-white font-bold">✕</button>
            </div>
            <div id="why-modal-content" class="space-y-3 text-xs text-slate-200"></div>
            <button onclick="closeWhyModal()" class="mt-5 w-full bg-gradient-to-r from-blue-600 to-cyan-500 text-white font-extrabold py-3 rounded-xl text-xs">Đã hiểu</button>
        </div>
    </div>

    <!-- ================= CẢNH BÁO ĐỎ STRICT MODE KHI CHUYỂN TAB ================= -->
    <div id="turbulence-modal" class="fixed inset-0 z-50 turbulence-alert hidden flex-col items-center justify-center p-6 text-center">
        <div class="text-6xl mb-3 animate-bounce">🚨</div>
        <h2 class="text-2xl sm:text-3xl font-black text-white uppercase mb-2">CẢNH BÁO: BẠN ĐÃ RỜI KHỎI BUỒNG LÁI TẬP TRUNG!</h2>
        <p class="text-sm text-red-100 max-w-md mb-5">Đồng hồ tập trung đã bị <b>TẠM DỪNG</b> vì bạn vừa chuyển sang cửa sổ khác!</p>
        <div class="bg-black/50 border border-red-300/30 rounded-2xl p-4 w-full max-w-sm mb-6">
            <div class="text-xs text-red-200 uppercase font-bold mb-1">Số lần vi phạm kỷ luật</div>
            <div id="violation-count-text" class="text-2xl font-black text-yellow-400 mono">1 / 3 LẦN</div>
        </div>
        <button onclick="resumeFromTurbulence()" class="bg-white hover:bg-yellow-300 text-red-900 font-black px-8 py-4 rounded-2xl shadow-2xl text-sm uppercase">
            🔒 Quay lại Học tiếp ngay
        </button>
    </div>

    <div id="crash-modal" class="fixed inset-0 z-50 bg-black/95 backdrop-blur-xl hidden flex-col items-center justify-center p-6 text-center">
        <div class="text-6xl mb-3">💥</div>
        <h2 class="text-2xl font-black text-red-500 uppercase mb-2">CHUYẾN BAY BỊ HỦY DO MẤT TẬP TRUNG QUÁ 3 LẦN</h2>
        <button onclick="closeCrashModal()" class="mt-4 bg-red-600 hover:bg-red-500 text-white font-extrabold px-6 py-3.5 rounded-2xl text-xs uppercase">Quay lại</button>
    </div>

    <!-- MODAL TÙY CHỈNH NHẠC LOFI & BOT -->
    <div id="media-modal" class="fixed inset-0 z-50 bg-black/75 backdrop-blur-md hidden items-center justify-center p-4">
        <div class="glass-panel w-full max-w-md rounded-3xl p-6 shadow-2xl">
            <div class="flex justify-between items-center mb-4">
                <h3 class="text-base font-extrabold text-white">🎧 Tùy Chỉnh Âm Thanh & Giao Diện</h3>
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
                        <div class="text-[10px] text-slate-400">Giúp tập trung sâu như trên máy bay thật</div>
                    </div>
                    <input type="checkbox" onchange="toggleCabinNoise(this.checked)" class="w-5 h-5 accent-cyan-400 cursor-pointer" />
                </div>

                <div class="bg-slate-900/90 p-3 rounded-2xl border border-amber-400/30">
                    <label class="font-bold text-amber-300 block mb-1">2. Đổi ảnh đại diện Chatbot AI:</label>
                    <input type="file" accept="image/*" onchange="handleBotAvatarUpload(this)" class="w-full text-slate-300 file:mr-2 file:py-1 file:px-3 file:rounded-xl file:border-0 file:font-bold file:bg-amber-500 file:text-black cursor-pointer" />
                </div>
            </div>
            <button onclick="applyCustomMedia()" class="mt-4 w-full bg-gradient-to-r from-blue-600 to-cyan-500 text-white font-extrabold py-3 rounded-xl text-xs">Lưu & Đóng</button>
        </div>
    </div>

    <!-- ================= CHATBOT AI VÀNG KIM GÓC DƯỚI PHẢI ================= -->
    <div id="chatbot-launcher" onclick="toggleChatbotWindow()" class="fixed bottom-5 right-5 z-40 w-14 h-14 rounded-full bg-white p-1 cursor-pointer bot-launcher-glow flex items-center justify-center border-2 border-[#d4a349]">
        <img id="bot-launcher-img" src="https://cdn-icons-png.flaticon.com/512/4712/4712109.png" class="w-full h-full rounded-full object-cover bg-gradient-to-b from-yellow-300 to-amber-500 p-1" />
        <span class="absolute -top-0.5 -right-0.5 w-3.5 h-3.5 bg-emerald-500 border-2 border-white rounded-full"></span>
    </div>

    <div id="chatbot-window" class="fixed bottom-22 right-5 z-50 w-[340px] sm:w-[365px] h-[480px] bg-[#f8f9fa] text-slate-800 rounded-2xl shadow-2xl border border-[#d4a349]/50 hidden flex-col overflow-hidden">
        <div class="bg-[#d4a349] text-white px-4 py-3 flex items-center justify-between shadow">
            <div class="flex items-center gap-2.5">
                <div class="w-8 h-8 rounded-full bg-white p-0.5 shadow">
                    <img id="bot-header-img" src="https://cdn-icons-png.flaticon.com/512/4712/4712109.png" class="w-full h-full rounded-full object-cover bg-amber-400" />
                </div>
                <span class="font-bold text-sm">Trợ lý Học tập AI</span>
            </div>
            <div class="flex items-center gap-3 text-white">
                <button onclick="resetChat()" title="Làm mới" class="text-sm font-bold">↺</button>
                <button onclick="toggleChatbotWindow()" class="text-lg font-bold leading-none">✕</button>
            </div>
        </div>

        <div id="chat-messages" class="flex-1 p-3.5 overflow-y-auto space-y-3 bg-[#f7f8fc]"></div>

        <div class="px-3 py-2 bg-white border-t border-slate-100 flex gap-1.5 overflow-x-auto">
            <button onclick="sendQuickChat('Hôm nay mình nên học gì?')" class="shrink-0 bg-amber-50 hover:bg-amber-100 text-[#b07d2b] border border-[#d4a349]/40 text-[11px] font-semibold px-2.5 py-1 rounded-full">💡 Hôm nay học gì?</button>
            <button onclick="sendQuickChat('Kiểm tra công việc chưa xong')" class="shrink-0 bg-amber-50 hover:bg-amber-100 text-[#b07d2b] border border-[#d4a349]/40 text-[11px] font-semibold px-2.5 py-1 rounded-full">📋 Việc đang làm</button>
            <button onclick="sendQuickChat('Mình có lịch đột xuất')" class="shrink-0 bg-amber-50 hover:bg-amber-100 text-[#b07d2b] border border-[#d4a349]/40 text-[11px] font-semibold px-2.5 py-1 rounded-full">🌪️ Dời lịch đột xuất</button>
        </div>

        <div class="p-2.5 bg-white border-t border-slate-200 flex items-center gap-2">
            <input type="text" id="chat-input" onkeydown="if(event.key==='Enter') sendChatMessage()" placeholder="Nhập tin nhắn..." class="flex-1 text-xs text-slate-800 px-2 py-1.5 focus:outline-none" />
            <button onclick="sendChatMessage()" class="w-8 h-8 rounded-full bg-[#d4a349] hover:bg-[#c29138] text-white flex items-center justify-center shadow">➤</button>
        </div>
    </div>

    <script>
        // ================= 1. HÀM VẼ 4 MÔ HÌNH MÁY BAY VECTOR SVG RIÊNG BIỆT =================
        function getAircraftSVG(aircraftType, headingDeg = 0) {
            if (aircraftType.includes("787")) {
                // BOEING 787-9 DREAMLINER: Cánh cong vút Raked Wingtips, thân rộng, màu vàng Gold & Trắng
                return `
                <svg viewBox="0 0 100 100" style="transform: rotate(${headingDeg}deg);" class="w-full h-full drop-shadow-[0_6px_12px_rgba(0,0,0,0.85)]">
                    <!-- Vệt khói trắng động cơ -->
                    <line x1="36" y1="62" x2="36" y2="95" stroke="rgba(255,255,255,0.35)" stroke-width="2" stroke-dasharray="3,3"/>
                    <line x1="64" y1="62" x2="64" y2="95" stroke="rgba(255,255,255,0.35)" stroke-width="2" stroke-dasharray="3,3"/>
                    <!-- 2 Động cơ GEnx lớn -->
                    <rect x="32" y="46" width="7" height="14" rx="3" fill="#eab308" stroke="#fef08a" stroke-width="1"/>
                    <rect x="61" y="46" width="7" height="14" rx="3" fill="#eab308" stroke="#fef08a" stroke-width="1"/>
                    <!-- Cánh cong vút Dreamliner -->
                    <path d="M50 34 L94 62 L98 68 L88 67 L55 52 L45 52 L12 67 L2 68 L6 62 Z" fill="#f8fafc" stroke="#eab308" stroke-width="1.5"/>
                    <!-- Cánh đuôi -->
                    <path d="M50 76 L72 90 L70 94 L53 86 L47 86 L30 94 L28 90 Z" fill="#eab308"/>
                    <!-- Thân máy bay rộng -->
                    <path d="M50 6 C55 6 57 18 57 45 L55 86 L50 95 L45 86 L43 45 C43 18 45 6 50 6 Z" fill="#ffffff" stroke="#cbd5e1" stroke-width="1"/>
                    <!-- Kính buồng lái Dreamliner -->
                    <path d="M46 14 Q50 10 54 14 Q50 16 46 14 Z" fill="#0284c7"/>
                    <!-- Đèn nháy đầu cánh -->
                    <circle cx="5" cy="64" r="3" fill="#ef4444" class="strobe-light"/>
                    <circle cx="95" cy="64" r="3" fill="#22c55e" class="strobe-light"/>
                </svg>`;
            } else if (aircraftType.includes("A350")) {
                // AIRBUS A350-900: Kính đen Raccoon Mask, đầu cánh Winglets tím/hồng hiện đại
                return `
                <svg viewBox="0 0 100 100" style="transform: rotate(${headingDeg}deg);" class="w-full h-full drop-shadow-[0_6px_12px_rgba(0,0,0,0.85)]">
                    <line x1="35" y1="60" x2="35" y2="95" stroke="rgba(255,255,255,0.35)" stroke-width="2" stroke-dasharray="3,3"/>
                    <line x1="65" y1="60" x2="65" y2="95" stroke="rgba(255,255,255,0.35)" stroke-width="2" stroke-dasharray="3,3"/>
                    <rect x="31" y="45" width="7" height="14" rx="3" fill="#ec4899"/>
                    <rect x="62" y="45" width="7" height="14" rx="3" fill="#ec4899"/>
                    <path d="M50 35 L92 58 L96 66 L89 64 L56 51 L44 51 L11 64 L4 66 L8 58 Z" fill="#f1f5f9" stroke="#ec4899" stroke-width="1.5"/>
                    <path d="M50 76 L72 89 L70 93 L50 86 L30 93 L28 89 Z" fill="#ec4899"/>
                    <path d="M50 5 C55 5 57 18 57 46 L55 87 L50 96 L45 87 L43 46 C43 18 45 5 50 5 Z" fill="#ffffff"/>
                    <!-- Kính đen Raccoon Mask đặc trưng A350 -->
                    <path d="M44 13 Q50 8 56 13 Q56 17 50 15 Q44 17 44 13 Z" fill="#0f172a"/>
                    <circle cx="6" cy="62" r="3" fill="#ef4444" class="strobe-light"/>
                    <circle cx="94" cy="62" r="3" fill="#22c55e" class="strobe-light"/>
                </svg>`;
            } else if (aircraftType.includes("ATR")) {
                // ATR 72-600: Máy bay Cánh thẳng + 2 Cánh quạt Tuabin quay tít
                return `
                <svg viewBox="0 0 100 100" style="transform: rotate(${headingDeg}deg);" class="w-full h-full drop-shadow-[0_6px_12px_rgba(0,0,0,0.85)]">
                    <!-- Cánh thẳng ngang vai -->
                    <rect x="8" y="40" width="84" height="11" rx="4" fill="#e2e8f0" stroke="#10b981" stroke-width="1.5"/>
                    <!-- Động cơ Tuabin cánh quạt -->
                    <rect x="29" y="34" width="6" height="16" rx="2" fill="#10b981"/>
                    <rect x="65" y="34" width="6" height="16" rx="2" fill="#10b981"/>
                    <!-- 2 Cánh quạt xoay tròn -->
                    <circle cx="32" cy="32" r="7" fill="rgba(56,189,248,0.35)" stroke="#ffffff" stroke-width="1.5" stroke-dasharray="4,3"/>
                    <circle cx="68" cy="32" r="7" fill="rgba(56,189,248,0.35)" stroke="#ffffff" stroke-width="1.5" stroke-dasharray="4,3"/>
                    <!-- Đuôi chữ T -->
                    <rect x="33" y="83" width="34" height="7" rx="3" fill="#10b981"/>
                    <!-- Thân ATR -->
                    <path d="M50 10 C54 10 55 20 55 46 L54 85 L50 93 L46 85 L45 46 C45 20 46 10 50 10 Z" fill="#ffffff"/>
                    <path d="M46 16 Q50 13 54 16 Z" fill="#0f172a"/>
                    <circle cx="10" cy="45" r="3" fill="#ef4444" class="strobe-light"/>
                    <circle cx="90" cy="45" r="3" fill="#22c55e" class="strobe-light"/>
                </svg>`;
            }
            // MẶC ĐỊNH: AIRBUS A321NEO (Sharklets xanh Cyan hiện đại)
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

        // Tính góc hướng mũi máy bay (Bearing) từ Sân bay đi -> Sân bay đến
        function calcBearingDeg(coord1, coord2) {
            const lat1 = coord1[0] * Math.PI / 180;
            const lat2 = coord2[0] * Math.PI / 180;
            const dLon = (coord2[1] - coord1[1]) * Math.PI / 180;
            const y = Math.sin(dLon) * Math.cos(lat2);
            const x = Math.cos(lat1) * Math.sin(lat2) - Math.sin(lat1) * Math.cos(lat2) * Math.cos(dLon);
            const brng = Math.atan2(y, x) * 180 / Math.PI;
            return Math.round((brng + 360) % 360);
        }

        // ================= 2. DANH SÁCH 34 SÂN BAY (22 VIỆT NAM + 12 QUỐC TẾ) =================
        const AIRPORTS = [
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

        // ================= 3. KHỞI TẠO HỒ SƠ TRỐNG 100% & LƯU TRỮ VĨNH VIỄN =================
        const DAYS_OF_WEEK = ["T2", "T3", "T4", "T5", "T6", "T7", "CN"];
        let selectedDay = "T2";
        let currentTaskFilter = "all";
        let activeTaskIdForFlight = null;

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

        // ================= 4. CHUYỂN ĐỔI GÓC NHÌN CAMERA & CHẾ ĐỘ NGÀY/ĐÊM/MƯA =================
        let currentCamView = "map";
        let currentEnvMode = "day";
        let isShadeClosed = false;
        let cabinMoodIdx = 0;

        function setCameraView(view) {
            currentCamView = view;
            const views = ['map', 'cockpit', 'cabin', 'window'];
            views.forEach(v => {
                const btn = document.getElementById('cam-btn-' + v);
                if (btn) {
                    btn.className = (v === view)
                        ? "px-3 py-1.5 rounded-xl text-[11px] font-extrabold bg-cyan-500 text-black shadow transition"
                        : "px-3 py-1.5 rounded-xl text-[11px] font-extrabold text-slate-300 hover:text-white transition";
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

        function setFlightEnvironment(mode) {
            currentEnvMode = mode;
            ['day', 'sunset', 'night', 'rain'].forEach(m => {
                const btn = document.getElementById('env-btn-' + m);
                if (btn) {
                    btn.className = (m === mode)
                        ? "px-2.5 py-1.5 rounded-xl text-[11px] font-bold bg-amber-400 text-black shadow"
                        : "px-2.5 py-1.5 rounded-xl text-[11px] font-bold text-slate-300 hover:text-white";
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
                cStars.style.opacity = "0";
                wStars.style.opacity = "0";
                celestial.className = "absolute top-12 right-14 w-14 h-14 rounded-full bg-yellow-300 shadow-[0_0_50px_#fde047]";
            } else if (mode === 'sunset') {
                cSky.className = "absolute inset-0 bg-gradient-to-b from-[#1e1b4b] via-[#be185d] to-[#f97316] transition-all duration-700";
                wSky.style.background = "linear-gradient(180deg, #1e1b4b 0%, #9d174d 45%, #f97316 85%, #fde047 100%)";
                cStars.style.opacity = "0.35";
                wStars.style.opacity = "0.35";
                celestial.className = "absolute top-28 right-14 w-16 h-16 rounded-full bg-orange-400 shadow-[0_0_60px_#fb923c]";
            } else if (mode === 'night') {
                cSky.className = "absolute inset-0 bg-gradient-to-b from-[#020617] via-[#090d1e] to-[#111827] transition-all duration-700";
                wSky.style.background = "linear-gradient(180deg, #02040a 0%, #070d1f 65%, #1e1b4b 100%)";
                cStars.style.opacity = "1";
                wStars.style.opacity = "1";
                celestial.className = "absolute top-12 right-14 w-11 h-11 rounded-full bg-slate-100 shadow-[0_0_30px_#e2e8f0]";
            } else if (mode === 'rain') {
                cSky.className = "absolute inset-0 bg-gradient-to-b from-slate-950 via-slate-800 to-slate-900 transition-all duration-700";
                wSky.style.background = "linear-gradient(180deg, #090d16 0%, #1e293b 65%, #0f172a 100%)";
                cStars.style.opacity = "0.15";
                wStars.style.opacity = "0.15";
                celestial.className = "hidden";
            }
        }

        function toggleWindowShade() {
            isShadeClosed = !isShadeClosed;
            const shade = document.getElementById('window-shade-panel');
            shade.style.height = isShadeClosed ? "88%" : "0%";
        }

        function cycleCabinMoodLight() {
            const moods = [
                "from-purple-500/35 via-cyan-500/15 to-transparent",
                "from-amber-500/35 via-pink-500/15 to-transparent",
                "from-emerald-500/35 via-blue-500/15 to-transparent",
                "from-blue-600/40 via-indigo-900/20 to-transparent"
            ];
            cabinMoodIdx = (cabinMoodIdx + 1) % moods.length;
            document.getElementById('cabin-ceiling-glow').className = `absolute top-0 inset-x-0 h-40 bg-gradient-to-b ${moods[cabinMoodIdx]} blur-2xl pointer-events-none transition-all duration-700`;
        }

        function updateCameraViewsData() {
            const profile = appState.members[currentMemberKey];
            const brng = calcBearingDeg(originAirport.coords, destAirport.coords);
            const speed = selectedAircraft.includes("ATR") ? "510 KM/H" : "860 KM/H";
            const alt = selectedAircraft.includes("ATR") ? "22,000 FT" : "36,000 FT";

            document.getElementById('hud-speed').innerText = speed;
            document.getElementById('hud-heading').innerText = `${brng}°`;
            document.getElementById('hud-alt').innerText = alt;
            document.getElementById('hud-aircraft-name').innerText = `${selectedAircraft.toUpperCase()} • AP ON`;
            document.getElementById('hud-route-code').innerText = `${originAirport.code} ➔ ${destAirport.code}`;
            document.getElementById('cockpit-plane-svg-preview').innerHTML = getAircraftSVG(selectedAircraft, 0);
            document.getElementById('cockpit-task-display').innerText = `${selectedFocus.icon} ${selectedFocus.label}`;

            document.getElementById('cabin-seat-label').innerText = selectedSeat;
            document.getElementById('cabin-aircraft-label').innerText = selectedAircraft;
            document.getElementById('cabin-route-label').innerText = `${originAirport.code} ➔ ${destAirport.code}`;
            document.getElementById('cabin-task-title').innerText = `${selectedFocus.icon} ${selectedFocus.label}`;
            document.getElementById('cabin-passenger-name').innerText = profile.name;
        }

        // ================= 5. CHUYỂN TRANG (DASHBOARD HỌC TẬP <-> TRẠM BAY) =================
        function switchPage(page) {
            const pageDash = document.getElementById('page-dashboard');
            const pageFlight = document.getElementById('page-flight');
            const btnDash = document.getElementById('nav-btn-dashboard');
            const btnFlight = document.getElementById('nav-btn-flight');

            if (page === 'flight') {
                pageDash.classList.add('hidden');
                pageFlight.classList.remove('hidden');
                btnFlight.className = "px-4 py-2 rounded-xl text-xs font-extrabold bg-gradient-to-r from-blue-600 to-cyan-500 text-white shadow transition flex items-center gap-1.5";
                btnDash.className = "px-4 py-2 rounded-xl text-xs font-extrabold text-slate-400 hover:text-white transition flex items-center gap-1.5";
                setTimeout(() => {
                    map.invalidateSize();
                    updateBookingUI();
                }, 150);
            } else {
                pageFlight.classList.add('hidden');
                pageDash.classList.remove('hidden');
                btnDash.className = "px-4 py-2 rounded-xl text-xs font-extrabold bg-gradient-to-r from-blue-600 to-cyan-500 text-white shadow transition flex items-center gap-1.5";
                btnFlight.className = "px-4 py-2 rounded-xl text-xs font-extrabold text-slate-400 hover:text-white transition flex items-center gap-1.5";
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

        // ================= 6. QUẢN LÝ CÔNG VIỆC, HOÀN THÀNH (✓) & THỜI KHÓA BIỂU =================
        function calcPriorityScore(task) {
            const urgency = Math.max(5, 100 - task.hoursLeft * 1.4);
            return Math.round(task.importance * 18 + urgency * 0.6);
        }

        function setTaskFilter(filter) {
            currentTaskFilter = filter;
            ['all', 'pending', 'done'].forEach(f => {
                const el = document.getElementById('filter-' + f);
                el.className = (f === filter) ? "px-3 py-1 rounded-lg bg-blue-600 text-white" : "px-3 py-1 rounded-lg text-slate-400 hover:text-white";
            });
            renderDashboard();
        }

        function addNewTask() {
            const titleInput = document.getElementById('quick-task-title');
            const title = titleInput.value.trim();
            if (!title) { titleInput.focus(); return; }
            const hours = parseInt(document.getElementById('quick-task-hours').value) || 24;
            const imp = parseInt(document.getElementById('quick-task-importance').value) || 4;
            const slot = document.getElementById('quick-task-slot').value.trim() || "19:30 - 20:15";
            const dur = parseInt(document.getElementById('quick-task-duration').value) || 35;

            const profile = appState.members[currentMemberKey];
            profile.tasks.unshift({
                id: Date.now(), title, hoursLeft: hours, importance: imp, slot, duration: dur, done: false
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
                const freeSlots = daySlots.filter(s => s.type === 'free');
                const suggestedSlot = freeSlots.length > 0 ? freeSlots[0].time : top.slot;

                aiBox.innerHTML = `
                    <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
                        <div>
                            <div class="flex flex-wrap items-center gap-2 mb-1">
                                <span class="bg-amber-400 text-black text-[10px] font-black px-2 py-0.5 rounded">ƯU TIÊN SỐ 1 • ĐIỂM AI: ${calcPriorityScore(top)}</span>
                                <span class="text-xs font-bold text-red-300">⏳ Hạn còn: ${top.hoursLeft} giờ</span>
                                <span class="text-xs text-amber-300">${'⭐'.repeat(top.importance)}</span>
                            </div>
                            <div class="text-base font-extrabold text-white">${top.title}</div>
                            <div class="text-xs text-cyan-300 mt-1">
                                🕒 Khung giờ đề xuất: <b>${suggestedSlot}</b> • Thời lượng tập trung: <b>${top.duration} phút</b>
                            </div>
                        </div>
                        <div class="flex sm:flex-col gap-2 shrink-0">
                            <button onclick="startFlightFromTask(${top.id})" class="bg-gradient-to-r from-emerald-500 to-cyan-500 hover:opacity-95 text-black font-black px-4 py-2.5 rounded-xl text-xs shadow-lg whitespace-nowrap">
                                🛫 Bay tập trung (${top.duration}p)
                            </button>
                            <button onclick="openWhyModal(${top.id})" class="bg-white/10 hover:bg-white/20 text-white font-bold px-3 py-1.5 rounded-xl text-[11px] whitespace-nowrap">
                                ❓ Tại sao có lịch này?
                            </button>
                        </div>
                    </div>
                `;
            } else if (allTasks.length > 0 && pendingTasks.length === 0) {
                aiBox.innerHTML = `<div class="text-xs text-emerald-400 font-bold py-2">🎉 Xuất sắc! ${profile.name} đã hoàn thành toàn bộ ${allTasks.length} công việc!</div>`;
            } else {
                aiBox.innerHTML = `<div class="text-xs text-slate-400 py-2">Danh sách công việc của <b>${profile.name}</b> đang trống. Hãy nhập công việc ở khung bên dưới để AI gợi ý lịch trình!</div>`;
            }

            const listEl = document.getElementById('todo-drag-list');
            listEl.innerHTML = '';

            let filteredTasks = allTasks;
            if (currentTaskFilter === 'pending') filteredTasks = pendingTasks;
            if (currentTaskFilter === 'done') filteredTasks = doneTasks;

            if (filteredTasks.length === 0) {
                listEl.innerHTML = `
                    <div class="text-center py-10 bg-slate-900/40 rounded-2xl border border-dashed border-white/10">
                        <div class="text-2xl mb-1">📝</div>
                        <div class="text-xs font-bold text-slate-300">Chưa có nhiệm vụ nào ở mục này</div>
                        <div class="text-[11px] text-slate-500 mt-0.5">Hãy thêm công việc mới ở thanh phía trên — dữ liệu sẽ được giữ lại tự động!</div>
                    </div>
                `;
            } else {
                filteredTasks.forEach((task) => {
                    const realIdx = allTasks.findIndex(t => t.id === task.id);
                    const score = calcPriorityScore(task);
                    const isUrgent = !task.done && task.hoursLeft <= 24;

                    const card = document.createElement('div');
                    card.draggable = true;
                    card.dataset.index = realIdx;
                    card.className = `p-3.5 rounded-2xl border transition cursor-grab active:cursor-grabbing flex flex-col sm:flex-row sm:items-center justify-between gap-3 ${
                        task.done 
                        ? 'bg-emerald-950/20 border-emerald-500/30' 
                        : (isUrgent ? 'bg-slate-900/95 border-red-400/40 shadow-md' : 'bg-slate-900/90 border-white/10 hover:border-cyan-400/40')
                    }`;

                    card.addEventListener('dragstart', handleDragStart);
                    card.addEventListener('dragover', handleDragOver);
                    card.addEventListener('drop', handleDrop);
                    card.addEventListener('dragend', handleDragEnd);

                    card.innerHTML = `
                        <div class="flex items-start gap-3">
                            <button onclick="toggleTaskDone(${task.id})" title="Đánh dấu hoàn thành" class="mt-0.5 w-6 h-6 rounded-full border-2 flex items-center justify-center font-black text-xs transition shrink-0 ${
                                task.done 
                                ? 'bg-emerald-500 border-emerald-400 text-black shadow-lg shadow-emerald-500/30' 
                                : 'bg-slate-800 border-slate-500 text-transparent hover:border-emerald-400'
                            }">✓</button>

                            <div>
                                <div class="flex flex-wrap items-center gap-1.5 mb-1">
                                    ${task.done 
                                        ? `<span class="text-[10px] font-black bg-emerald-500/20 text-emerald-300 border border-emerald-500/30 px-2 py-0.5 rounded">✅ ĐÃ HOÀN THÀNH</span>` 
                                        : `<span class="text-[10px] font-black px-2 py-0.5 rounded ${isUrgent ? 'bg-red-500/25 text-red-300 border border-red-400/30' : 'bg-blue-500/20 text-blue-300'}">⏳ Hạn: ${task.hoursLeft}h</span>`
                                    }
                                    <span class="text-[10px] font-bold text-amber-300">${'⭐'.repeat(task.importance)}</span>
                                    <span class="text-[10px] font-mono bg-white/10 text-cyan-300 px-2 py-0.5 rounded">🕒 ${task.slot}</span>
                                    <span class="text-[10px] font-mono text-slate-400">Điểm AI: ${score}</span>
                                </div>
                                <div class="text-sm font-extrabold ${task.done ? 'line-through text-slate-400' : 'text-white'}">${task.title}</div>
                            </div>
                        </div>

                        <div class="flex items-center gap-1.5 shrink-0 self-end sm:self-center">
                            <button onclick="openWhyModal(${task.id})" class="bg-slate-800 hover:bg-slate-700 text-cyan-300 border border-cyan-500/30 px-2.5 py-1.5 rounded-xl text-[11px] font-bold">
                                ❓ Tại sao?
                            </button>
                            ${!task.done ? `
                                <button onclick="startFlightFromTask(${task.id})" class="bg-blue-600 hover:bg-blue-500 text-white px-3 py-1.5 rounded-xl text-[11px] font-extrabold shadow">
                                    🛫 Bay (${task.duration}p)
                                </button>
                            ` : ''}
                            <button onclick="deleteTask(${task.id})" title="Xóa nhiệm vụ" class="bg-red-500/15 hover:bg-red-500/30 text-red-300 px-2.5 py-1.5 rounded-xl text-xs font-bold">
                                🗑️
                            </button>
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
                btn.className = `py-2 rounded-xl text-xs font-extrabold transition border flex flex-col items-center ${
                    active ? 'bg-amber-400 text-black border-amber-300 shadow' : 'bg-slate-900 text-slate-400 border-white/10 hover:text-white'
                }`;
                btn.innerHTML = `<span>${d}</span><span class="text-[9px] ${active ? 'text-black/70' : 'text-slate-500'}">${count} ca</span>`;
                btn.onclick = () => { selectedDay = d; renderDashboard(); };
                dayTabs.appendChild(btn);
            });

            const slotsList = document.getElementById('timetable-slots-list');
            slotsList.innerHTML = '';
            if (daySlots.length === 0) {
                slotsList.innerHTML = `
                    <div class="text-center py-8 bg-slate-900/40 rounded-2xl border border-dashed border-white/10">
                        <div class="text-2xl mb-1">🗓️</div>
                        <div class="text-xs font-bold text-slate-300">Ngày ${selectedDay} chưa có lịch nào</div>
                        <div class="text-[11px] text-slate-500 mt-0.5">Hãy tự thêm ca học hoặc giờ trống của bạn ở khung phía trên!</div>
                    </div>
                `;
            } else {
                daySlots.forEach((s, sIdx) => {
                    const isFree = s.type === 'free';
                    const el = document.createElement('div');
                    el.className = `p-3.5 rounded-2xl border flex items-center justify-between gap-2 ${
                        isFree ? 'bg-emerald-950/30 border-emerald-400/30' : 'bg-slate-900/90 border-white/10'
                    }`;
                    el.innerHTML = `
                        <div>
                            <div class="flex items-center gap-2">
                                <span class="text-[10px] font-mono font-extrabold px-2 py-0.5 rounded ${isFree ? 'bg-emerald-400 text-black' : 'bg-slate-700 text-slate-200'}">
                                    ${s.time}
                                </span>
                                <span class="text-[10px] font-bold ${isFree ? 'text-emerald-300' : 'text-red-300'}">
                                    ${isFree ? '🟢 Giờ trống tự học' : '🔴 Lịch học / Bận'}
                                </span>
                            </div>
                            <div class="text-xs font-bold text-white mt-1.5">${s.subject}</div>
                        </div>
                        <button onclick="removeTimetableSlot(${sIdx})" title="Xóa lịch này" class="bg-red-500/15 hover:bg-red-500/30 text-red-300 px-2.5 py-1.5 rounded-xl text-xs font-bold">
                            🗑️
                        </button>
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
            if (profile.tasks.length === 0) {
                alert("Hãy thêm công việc vào danh sách trước khi sắp xếp!");
                return;
            }
            profile.tasks.sort((a, b) => {
                if (a.done !== b.done) return a.done ? 1 : -1;
                return calcPriorityScore(b) - calcPriorityScore(a);
            });
            savePersistentState();
            renderDashboard();
            alert(`🤖 AI đã sắp xếp lại danh sách công việc của ${profile.name} theo Độ quan trọng và Thời hạn Deadline!`);
        }

        function handleSuddenScheduleChange() {
            const profile = appState.members[currentMemberKey];
            const pending = profile.tasks.filter(t => !t.done);
            if (pending.length === 0) {
                alert("Hiện không có công việc nào đang chờ để dời lịch!");
                return;
            }
            const backupSlots = ["20:30 - 21:15 (Ca tối dự phòng)", "21:30 - 22:15 (Ca khuya linh hoạt)", "08:00 - 08:45 (Sáng mai)"];
            pending.forEach((t, i) => { t.slot = backupSlots[i % backupSlots.length]; });
            savePersistentState();
            renderDashboard();
            alert(`🌪️ Đã cập nhật lịch đột xuất! AI đã tự động dời ${pending.length} công việc của ${profile.name} sang khung giờ trống dự phòng.`);
        }

        function openWhyModal(taskId) {
            const profile = appState.members[currentMemberKey];
            const task = profile.tasks.find(t => t.id === taskId);
            if (!task) return;
            const score = calcPriorityScore(task);
            const daySlots = (profile.timetable && profile.timetable[selectedDay]) ? profile.timetable[selectedDay] : [];
            const freeSlots = daySlots.filter(s => s.type === 'free');
            const freeText = freeSlots.length > 0 ? freeSlots.map(s => s.time).join(', ') : task.slot;

            document.getElementById('why-modal-content').innerHTML = `
                <div class="bg-slate-900 p-3.5 rounded-2xl border border-white/10">
                    <div class="text-[10px] text-cyan-400 font-bold uppercase">Công việc phân tích</div>
                    <div class="text-sm font-extrabold text-white mt-0.5">${task.title}</div>
                    <div class="text-xs text-amber-300 font-mono mt-1">Điểm ưu tiên AI: <b>${score} điểm</b></div>
                </div>
                <div class="space-y-2.5">
                    <div class="bg-red-500/15 border border-red-400/30 p-3 rounded-2xl">
                        <div class="font-extrabold text-red-300">1. ⏳ Thời hạn (Deadline): Còn ${task.hoursLeft} giờ</div>
                        <div class="text-[11px] text-slate-300 mt-0.5">
                            ${task.hoursLeft <= 24 ? 'Thời gian còn dưới 24 giờ nên được xếp vào nhóm Khẩn cấp cần làm ngay.' : 'Cần hoàn thành sớm để tránh dồn việc sát hạn.'}
                        </div>
                    </div>
                    <div class="bg-amber-500/15 border border-amber-400/30 p-3 rounded-2xl">
                        <div class="font-extrabold text-amber-300">2. ⭐ Mức độ Quan trọng: ${task.importance}/5 Sao</div>
                        <div class="text-[11px] text-slate-300 mt-0.5">Đóng góp ${task.importance * 18} điểm vào thứ tự ưu tiên học tập hôm nay.</div>
                    </div>
                    <div class="bg-emerald-500/15 border border-emerald-400/30 p-3 rounded-2xl">
                        <div class="font-extrabold text-emerald-300">3. 🕒 Khung giờ trống phù hợp:</div>
                        <div class="text-[11px] text-slate-300 mt-0.5">Phù hợp để bay tập trung <b>${task.duration} phút</b> vào khung giờ <b>${freeText}</b> của ${profile.name}.</div>
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
            if (pending.length === 0) {
                alert(`🔔 Thông báo (${profile.name}): Bạn chưa có công việc nào đang chờ hoặc đã hoàn thành hết!`);
            } else {
                alert(`🔔 Nhắc học (${profile.name}): Đừng quên hoàn thành "${pending[0].title}" (${pending[0].duration} phút - Ca ${pending[0].slot}) nhé!`);
            }
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
            selectedDuration = task.duration;
            setDuration(task.duration);
            selectedFocus = { id: 'custom', label: task.title, icon: '🎯', color: 'bg-cyan-600 border-cyan-300 text-white' };
            document.getElementById('custom-focus-input').value = task.title;

            switchPage('flight');
            goToSeatSelection();
        }

        // ================= 7. TRẠM BAY TẬP TRUNG, MÔ HÌNH MÁY BAY & BẢN ĐỒ =================
        let originAirport = AIRPORTS[0]; // SGN
        let destAirport = AIRPORTS[2];   // DAD
        let selectedDuration = 35;
        let currentDistance = 610;
        let selectedAircraft = "Airbus A321neo";
        let selectedSeat = "06A";
        let selectedFocus = FOCUS_MODES[1];
        let isBookingCollapsed = false;

        let isFlying = false, strictModeEnabled = true, isPausedByViolation = false, violationCount = 0;
        const MAX_VIOLATIONS = 3;
        let alarmInterval = null, flightInterval = null;
        let remainingSeconds = 35 * 60, totalFlightSeconds = 35 * 60;

        const map = L.map('map', { zoomControl: false }).setView([14.0, 108.0], 6);
        L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}', { maxZoom: 18 }).addTo(map);
        L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/Reference/World_Boundaries_and_Places/MapServer/tile/{z}/{y}/{x}', { maxZoom: 18 }).addTo(map);

        let routeLine = null, originMarker = null, destMarker = null, planeMarker = null;

        function toggleBookingCardSize() {
            const card = document.getElementById('screen-booking');
            const btn = document.getElementById('toggle-booking-btn');
            isBookingCollapsed = !isBookingCollapsed;
            if (isBookingCollapsed) {
                card.classList.add('translate-y-[120%]');
                btn.innerText = "🔼 Mở bảng đặt vé";
            } else {
                card.classList.remove('translate-y-[120%]');
                btn.innerText = "🔽 Thu gọn bảng đặt vé";
            }
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

        function createAirportBadge(code, isDest) {
            const cls = isDest ? 'bg-yellow-400 text-black' : 'bg-cyan-400 text-black';
            return L.divIcon({
                className: 'badge-icon',
                html: `<div class="${cls} font-black text-[11px] px-2 py-0.5 rounded-md shadow-xl border border-black/40 flex items-center gap-1 whitespace-nowrap">✈️ ${code}</div>`,
                iconSize: [56, 24],
                iconAnchor: [28, 12]
            });
        }

        // Tạo Marker Máy Bay trên bản đồ bằng chính mô hình SVG của dòng máy bay đó + Vòng Radar
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

        function initAirportDropdowns() {
            const oSel = document.getElementById('origin-select');
            const dSel = document.getElementById('dest-select');

            const vnAirports = AIRPORTS.filter(a => a.group === 'VN');
            const intAirports = AIRPORTS.filter(a => a.group === 'INT');

            const buildOptions = () => {
                let html = `<optgroup label="🇻🇳 Sân bay Việt Nam (22 sân bay)" class="bg-slate-900">`;
                vnAirports.forEach(a => { html += `<option value="${a.code}">${a.code} - ${a.name}</option>`; });
                html += `</optgroup><optgroup label="🌏 Khu vực & Quốc tế (12 sân bay)" class="bg-slate-900">`;
                intAirports.forEach(a => { html += `<option value="${a.code}">${a.code} - ${a.name}</option>`; });
                html += `</optgroup>`;
                return html;
            };

            oSel.innerHTML = buildOptions();
            dSel.innerHTML = buildOptions();
            oSel.value = originAirport.code;
            dSel.value = destAirport.code;
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
            document.getElementById('booking-plane-svg-box').innerHTML = getAircraftSVG(selectedAircraft, 45);
            if (isFlying && planeMarker) {
                planeMarker.setIcon(createCustomAircraftMapIcon());
            }
            updateCameraViewsData();
        }

        function setDuration(mins) {
            selectedDuration = mins;
            document.querySelectorAll('.dur-btn').forEach(b => {
                b.className = "dur-btn bg-slate-800 py-1.5 rounded-xl text-xs font-bold text-slate-300 border border-transparent";
            });
            const activeBtn = document.getElementById('dur-' + mins);
            if (activeBtn) activeBtn.className = "dur-btn bg-blue-600/30 border-blue-400 text-blue-300 py-1.5 rounded-xl text-xs font-bold border";
        }

        function updateBookingUI() {
            document.getElementById('booking-plane-svg-box').innerHTML = getAircraftSVG(selectedAircraft, 45);
            document.getElementById('badge-origin').innerText = originAirport.code;
            document.getElementById('badge-dest').innerText = destAirport.code;
            document.getElementById('badge-dist').innerText = `${currentDistance} km`;
            document.getElementById('banner-dest-title').innerText = `${originAirport.name.split(' (')[0]} ➔ ${destAirport.name}`;

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

                        btn.className = `seat-box h-10 rounded-xl font-bold text-xs flex items-center justify-center border ${style}`;
                        btn.innerHTML = isSelected ? `<span class="text-base">${selectedFocus.icon}</span>` : '';
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
                pill.className = `px-3.5 py-2 rounded-full text-xs font-bold flex items-center gap-1.5 border transition ${
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
            document.getElementById('seat-header-route').innerText = `${originAirport.code} ➔ ${destAirport.code} • ${selectedDuration}m`;
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

            document.getElementById('tk-aircraft').innerText = selectedAircraft;
            document.getElementById('tk-passenger').innerText = profile.name;
            document.getElementById('tk-strict-badge').innerText = strictModeEnabled ? "🔒 STRICT LOCK ON" : "🔓 FREE MODE";
            document.getElementById('tk-origin-code').innerText = originAirport.code;
            document.getElementById('tk-origin-name').innerText = originAirport.name.split(' (')[0];
            document.getElementById('tk-dest-code').innerText = destAirport.code;
            document.getElementById('tk-dest-name').innerText = destAirport.name.split(' (')[0];
            document.getElementById('tk-duration').innerText = selectedDuration + 'm';
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

        function requestAppFullscreen() {
            const elem = document.documentElement;
            if (elem.requestFullscreen) elem.requestFullscreen().catch(() => {});
        }

        // Tiếng chuông Ding-Dong trên khoang máy bay khi cất cánh
        let audioCtx = null, cabinNoiseNode = null;
        function playCabinDingDong() {
            try {
                if (!audioCtx) audioCtx = new (window.AudioContext || window.webkitAudioContext)();
                const now = audioCtx.currentTime;
                const osc1 = audioCtx.createOscillator();
                const osc2 = audioCtx.createOscillator();
                const gain = audioCtx.createGain();
                osc1.frequency.setValueAtTime(659.25, now); // Nốt Mi (E5)
                osc2.frequency.setValueAtTime(523.25, now + 0.35); // Nốt Đô (C5)
                gain.gain.setValueAtTime(0.18, now);
                gain.gain.exponentialRampToValueAtTime(0.001, now + 1.2);
                osc1.connect(gain); osc2.connect(gain); gain.connect(audioCtx.destination);
                osc1.start(now); osc1.stop(now + 0.35);
                osc2.start(now + 0.35); osc2.stop(now + 1.2);
            } catch (e) {}
        }

        function startFlight() {
            const profile = appState.members[currentMemberKey];
            document.getElementById('screen-ticket').classList.add('hidden');
            document.getElementById('screen-ticket').classList.remove('flex');
            document.getElementById('screen-flying').classList.remove('hidden');

            playCabinDingDong();
            if (strictModeEnabled) requestAppFullscreen();

            const player = document.getElementById('lofi-player');
            if (player.paused) toggleLofi();

            isFlying = true;
            isPausedByViolation = false;
            violationCount = 0;
            updateSafetyHearts();
            updateCameraViewsData();

            document.getElementById('fly-mini-svg').innerHTML = getAircraftSVG(selectedAircraft, 45);
            document.getElementById('fly-route-text').innerText = `${originAirport.name.split(' (')[0]} ➔ ${destAirport.name.split(' (')[0]}`;
            document.getElementById('fly-sub-info').innerText = `${selectedAircraft} • Ghế ${selectedSeat} • ${selectedFocus.icon} ${selectedFocus.label}`;

            totalFlightSeconds = selectedDuration * 60;
            remainingSeconds = totalFlightSeconds;

            if (planeMarker) map.removeLayer(planeMarker);
            planeMarker = L.marker(originAirport.coords, { icon: createCustomAircraftMapIcon(), zIndexOffset: 1000 }).addTo(map);
            map.flyTo(originAirport.coords, 9, { duration: 2 });

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
            requestAppFullscreen();
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
            const mins = Math.floor(remainingSeconds / 60);
            const secs = remainingSeconds % 60;
            const timeFormatted = `${mins<10?'0'+mins:mins}:${secs<10?'0'+secs:secs}`;

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
            if (planeMarker) map.flyTo(planeMarker.getLatLng(), 10, { duration: 1.5 });
        }

        function abortFlight() {
            isFlying = false;
            isPausedByViolation = false;
            stopAlarmLoop();
            if (flightInterval) clearInterval(flightInterval);
            if (planeMarker) map.removeLayer(planeMarker);
            if (document.fullscreenElement && document.exitFullscreen) {
                document.exitFullscreen().catch(() => {});
            }
            setCameraView('map');
            document.getElementById('screen-flying').classList.add('hidden');
            document.getElementById('screen-booking').classList.remove('hidden');
            document.getElementById('toggle-booking-btn').classList.remove('hidden');
            updateBookingUI();
        }

        // ================= 8. CHATBOT AI & MEDIA =================
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
                    <div class="bg-[#d4a349] text-white font-semibold text-xs px-4 py-2 rounded-2xl rounded-tr-sm shadow-sm max-w-[82%]">${text}</div>
                    <span class="text-[10px] text-slate-400 mt-1">${getCurrentTimeStr()}</span>
                </div>
            `;
            box.scrollTop = box.scrollHeight;

            setTimeout(() => {
                const reply = generateSmartBotReply(text);
                const botAvatar = document.getElementById('bot-launcher-img').src;
                box.innerHTML += `
                    <div class="flex items-start gap-2">
                        <img src="${botAvatar}" class="w-8 h-8 rounded-full bg-amber-400 p-0.5 border border-[#d4a349] shrink-0 mt-1 object-cover" />
                        <div class="max-w-[84%]">
                            <div class="bg-[#fae5be] p-1.5 rounded-2xl rounded-tl-sm shadow-sm">
                                <div class="bg-white rounded-xl p-3 text-xs text-slate-800 leading-relaxed">${reply}</div>
                            </div>
                            <span class="text-[10px] text-slate-400 mt-1 block">${getCurrentTimeStr()}</span>
                        </div>
                    </div>
                `;
                box.scrollTop = box.scrollHeight;
            }, 300);
        }

        function generateSmartBotReply(q) {
            const lower = q.toLowerCase();
            const profile = appState.members[currentMemberKey];
            const pending = profile.tasks.filter(t => !t.done).sort((a,b) => calcPriorityScore(b) - calcPriorityScore(a));
            const done = profile.tasks.filter(t => t.done);

            if (lower.includes('hôm nay') || lower.includes('học gì')) {
                if (pending.length === 0) return `Chào <b>${profile.name}</b>! Hiện danh sách của bạn chưa có công việc nào đang chờ. Hãy thêm công việc mới trên Bảng điều khiển nhé!`;
                return `Chào <b>${profile.name}</b>! Theo phân tích AI, bạn nên ưu tiên làm ngay:<br>• <b>${pending[0].title}</b> (Hạn còn ${pending[0].hoursLeft}h, Ca ${pending[0].slot}).`;
            }
            if (lower.includes('việc') || lower.includes('chưa xong') || lower.includes('tiến độ')) {
                return `📊 Tiến độ của <b>${profile.name}</b>:<br>• Đang cần làm: <b>${pending.length} việc</b><br>• Đã hoàn thành (✓): <b>${done.length} việc</b><br>• Tổng dặm bay: <b>${profile.miles || 0} km</b>.`;
            }
            if (lower.includes('đột xuất') || lower.includes('dời lịch')) {
                handleSuddenScheduleChange();
                return `🌪️ Mình đã tự động dời các ca học chưa xong của <b>${profile.name}</b> sang khung giờ dự phòng rồi nhé!`;
            }
            return `Xin chào <b>${profile.name}</b>! Bạn có thể thử trải nghiệm 4 góc nhìn máy bay (Bản đồ, Buồng lái phi công, Khoang Cabin, Cửa sổ) và chế độ Bay qua đêm ở mục Chuyến Bay Tập Trung nhé!`;
        }

        function resetChat() {
            const profile = appState.members[currentMemberKey];
            const botAvatar = document.getElementById('bot-launcher-img').src;
            document.getElementById('chat-messages').innerHTML = `
                <div class="flex flex-col items-end">
                    <div class="bg-[#d4a349] text-white font-semibold text-xs px-4 py-2 rounded-2xl rounded-tr-sm shadow-sm">Bắt đầu</div>
                    <span class="text-[10px] text-slate-400 mt-1">${getCurrentTimeStr()}</span>
                </div>
                <div class="flex items-start gap-2">
                    <img src="${botAvatar}" class="w-8 h-8 rounded-full bg-amber-400 p-0.5 border border-[#d4a349] shrink-0 mt-1 object-cover" />
                    <div>
                        <div class="bg-[#fae5be] p-1.5 rounded-2xl rounded-tl-sm shadow-sm">
                            <div class="bg-white rounded-xl p-3 text-xs text-slate-800 leading-relaxed">
                                Xin chào <b>${profile.name}</b>! 🙋‍♀️<br>Mình là trợ lý AI học tập. Mọi công việc và thời khóa biểu bạn thêm đều được lưu giữ tự động!
                            </div>
                        </div>
                        <span class="text-[10px] text-slate-400 mt-1 block">${getCurrentTimeStr()}</span>
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

        // Khởi chạy ban đầu
        document.getElementById('member-select').value = currentMemberKey;
        initAirportDropdowns();
        onRouteChange();
        renderDashboard();
        resetChat();
    </script>
</body>
</html>
"""

components.html(app_html, height=940, scrolling=False)
