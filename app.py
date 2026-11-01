import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Focus Flight & AI Study Planner - Group 4",
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
        body { margin: 0; padding: 0; overflow: hidden; background-color: #060911; }
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
        body { font-family: 'Plus Jakarta Sans', sans-serif; background: #060911; color: white; margin: 0; overflow: hidden; user-select: none; }
        .mono { font-family: 'JetBrains Mono', monospace; }
        #map { position: absolute; inset: 0; z-index: 1; background: #060911; }

        .glass-panel {
            background: rgba(14, 19, 32, 0.90);
            backdrop-filter: blur(24px);
            -webkit-backdrop-filter: blur(24px);
            border: 1px solid rgba(255, 255, 255, 0.14);
        }

        .focus-popover {
            background: rgba(32, 45, 72, 0.96);
            backdrop-filter: blur(28px);
            border: 1px solid rgba(147, 197, 253, 0.25);
            box-shadow: 0 25px 60px rgba(0, 0, 0, 0.8);
        }

        .fuselage {
            border-top-left-radius: 170px 260px;
            border-top-right-radius: 170px 260px;
            border-left: 3px solid rgba(148, 163, 184, 0.25);
            border-right: 3px solid rgba(148, 163, 184, 0.25);
            border-top: 3px solid rgba(148, 163, 184, 0.35);
            background: linear-gradient(180deg, rgba(22, 30, 46, 0.96) 0%, rgba(11, 15, 25, 0.98) 100%);
            box-shadow: inset 0 15px 40px rgba(255,255,255,0.04), 0 20px 60px rgba(0,0,0,0.8);
        }

        .seat-box { transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1); }
        .seat-box:hover { transform: scale(1.06); }

        .ticket-cutout-left { position: absolute; left: -14px; top: 66%; width: 28px; height: 28px; background: #060911; border-radius: 50%; }
        .ticket-cutout-right { position: absolute; right: -14px; top: 66%; width: 28px; height: 28px; background: #060911; border-radius: 50%; }

        @keyframes pulse-bar { 0%, 100% { height: 4px; } 50% { height: 15px; } }
        .eq-bar { width: 3px; background: #38bdf8; border-radius: 2px; animation: pulse-bar 0.9s infinite ease-in-out; }
        .eq-bar:nth-child(2) { animation-delay: 0.2s; }
        .eq-bar:nth-child(3) { animation-delay: 0.4s; }

        @keyframes red-alert {
            0%, 100% { background: rgba(153, 27, 27, 0.90); }
            50% { background: rgba(220, 38, 38, 0.96); }
        }
        .turbulence-alert { animation: red-alert 0.7s infinite; backdrop-filter: blur(16px); }

        /* Hiệu ứng viền vàng phát sáng cho Chatbot giống ảnh mẫu */
        @keyframes bot-glow {
            0%, 100% { box-shadow: 0 0 15px rgba(212, 163, 73, 0.6), 0 0 30px rgba(212, 163, 73, 0.3); transform: translateY(0px); }
            50% { box-shadow: 0 0 25px rgba(234, 179, 8, 0.9), 0 0 45px rgba(212, 163, 73, 0.5); transform: translateY(-4px); }
        }
        .bot-launcher-glow {
            animation: bot-glow 3s infinite ease-in-out;
        }

        .dragging-card {
            opacity: 0.45;
            border: 2px dashed #38bdf8 !important;
            transform: scale(0.98);
        }

        ::-webkit-scrollbar { width: 5px; height: 5px; }
        ::-webkit-scrollbar-thumb { background: rgba(255,255,255,0.22); border-radius: 10px; }
        .leaflet-control-attribution { display: none !important; }
    </style>
</head>
<body class="relative w-screen h-screen" id="app-root">

    <!-- BẢN ĐỒ VỆ TINH NỀN -->
    <div id="map"></div>

    <!-- AUDIO LOFI -->
    <audio id="lofi-player" loop crossorigin="anonymous">
        <source id="lofi-source" src="https://cdn.pixabay.com/download/audio/2022/05/27/audio_1808fbf07a.mp3" type="audio/mpeg">
    </audio>

    <!-- ================= BANNER NHẮC NHỞ DEADLINE KHẨN CẤP (TOP VOTED #1 - COUNT: 6) ================= -->
    <div id="deadline-toast" class="fixed top-20 left-1/2 -translate-x-1/2 z-40 w-[92%] max-w-xl bg-gradient-to-r from-amber-500/95 via-orange-500/95 to-red-500/95 backdrop-blur-md text-white px-4 py-2.5 rounded-2xl shadow-2xl border border-yellow-200/40 flex items-center justify-between transition-all duration-300">
        <div class="flex items-center gap-2.5">
            <span class="text-xl animate-bounce">🔔</span>
            <div class="text-xs">
                <span class="font-black uppercase tracking-wider bg-black/25 px-1.5 py-0.5 rounded mr-1">Nhắc nhở Deadline</span>
                <span id="deadline-toast-text" class="font-bold">Bạn có nhiệm vụ sắp đến hạn trong hôm nay!</span>
            </div>
        </div>
        <div class="flex items-center gap-2">
            <button onclick="switchMainTab('planner')" class="bg-white text-orange-700 font-extrabold text-[11px] px-2.5 py-1 rounded-lg shadow hover:bg-yellow-50 whitespace-nowrap">Xem & Bay ngay</button>
            <button onclick="document.getElementById('deadline-toast').classList.add('hidden')" class="text-white/80 hover:text-white font-bold text-sm px-1">✕</button>
        </div>
    </div>

    <!-- ================= THANH TOP BAR & CHUYỂN ĐỔI 6 THÀNH VIÊN NHÓM ================= -->
    <div class="fixed top-3.5 left-4 right-4 z-30 flex flex-wrap justify-between items-center gap-2 pointer-events-none">
        <!-- Cụm trái: Logo + Chọn Thành Viên Cá Nhân Hóa -->
        <div class="flex items-center gap-2 pointer-events-auto">
            <div class="glass-panel px-3.5 py-2 rounded-2xl flex items-center gap-2.5 shadow-xl">
                <div class="w-8 h-8 rounded-xl bg-gradient-to-br from-blue-500 to-cyan-400 flex items-center justify-center text-black font-black text-base shadow">✈️</div>
                <div class="hidden sm:block">
                    <div class="text-[11px] font-extrabold tracking-wider text-white flex items-center gap-1.5">
                        FOCUS FLIGHT G4
                        <span id="top-aircraft-tag" class="bg-cyan-500/20 text-cyan-300 text-[9px] px-1.5 py-0.5 rounded font-mono">A321neo</span>
                    </div>
                    <div class="text-[10px] text-slate-400">Tân Sơn Nhất (SGN) ➔ Quê hương</div>
                </div>
            </div>

            <!-- Bộ chọn 6 Thành viên nhóm (Mỗi người 1 Thời khóa biểu & Deadline riêng) -->
            <div class="glass-panel px-3 py-1.5 rounded-2xl flex items-center gap-2 shadow-xl border border-amber-400/30">
                <span class="text-sm">👤</span>
                <div>
                    <div class="text-[9px] text-amber-300 font-bold uppercase tracking-wider">Hồ sơ thành viên (6 người)</div>
                    <select id="member-select" onchange="switchMemberProfile()" class="bg-transparent text-white font-extrabold text-xs focus:outline-none cursor-pointer pr-1">
                        <option value="quangminh" class="bg-slate-900">Quang Minh (Đà Nẵng/SGN)</option>
                        <option value="huudai" class="bg-slate-900">Hữu Đại (Cam Ranh - CXR)</option>
                        <option value="khanhthi" class="bg-slate-900">Khánh Thi (Đà Nẵng - DAD)</option>
                        <option value="minhchau" class="bg-slate-900">Minh Châu (Quy Nhơn - UIH)</option>
                        <option value="uyennhi" class="bg-slate-900">Uyên Nhi (Long Thành - LTH)</option>
                        <option value="vanhoang" class="bg-slate-900">Văn Hoàng (Đà Lạt - DLI)</option>
                    </select>
                </div>
            </div>
        </div>

        <!-- Cụm giữa: Chuyển đổi giữa Trạm Bay & Lịch Học AI Thông Minh -->
        <div class="glass-panel p-1 rounded-2xl flex items-center gap-1 shadow-xl pointer-events-auto border border-cyan-500/30">
            <button id="tab-btn-flight" onclick="switchMainTab('flight')" class="px-3.5 py-2 rounded-xl text-xs font-extrabold bg-gradient-to-r from-blue-600 to-cyan-500 text-white shadow transition flex items-center gap-1.5">
                <span>🛫 Trạm Bay Focus</span>
            </button>
            <button id="tab-btn-planner" onclick="switchMainTab('planner')" class="px-3.5 py-2 rounded-xl text-xs font-extrabold text-slate-300 hover:text-white transition flex items-center gap-1.5 relative">
                <span>📅 Lịch Học AI & To-Do</span>
                <span id="urgent-count-badge" class="bg-red-500 text-white text-[10px] font-black px-1.5 py-0.2 rounded-full">2</span>
            </button>
        </div>

        <!-- Cụm phải: Nhạc Lofi & Cài đặt Media -->
        <div class="flex items-center gap-2 pointer-events-auto">
            <button onclick="toggleLofi()" class="glass-panel px-3 py-2 rounded-2xl flex items-center gap-2 text-xs font-bold text-slate-200 hover:text-white transition shadow-xl">
                <div id="eq-icon" class="hidden items-end gap-[2px] h-4">
                    <div class="eq-bar"></div><div class="eq-bar"></div><div class="eq-bar"></div>
                </div>
                <span id="lofi-btn-text">🎵 Lofi</span>
            </button>
            <button onclick="openMediaModal()" class="glass-panel px-3 py-2 rounded-2xl text-xs font-bold text-cyan-400 hover:bg-slate-800 transition shadow-xl border border-cyan-500/30">
                ⚙️ Nhạc / Ảnh
            </button>
        </div>
    </div>

    <!-- ================= GIAO DIỆN LỊCH HỌC AI, TO-DO KÉO THẢ & THỜI KHÓA BIỂU CÁ NHÂN ================= -->
    <div id="screen-planner" class="fixed inset-0 z-25 bg-[#060911]/90 backdrop-blur-xl hidden flex-col pt-20 pb-6 px-4 overflow-y-auto">
        <div class="w-full max-w-6xl mx-auto space-y-4">

            <!-- HÀNG 1: GỢI Ý "HÔM NAY NÊN HỌC GÌ?" (COUNT: 6) + NÚT BÁO LỊCH ĐỘT XUẤT (COUNT: 4) -->
            <div class="grid grid-cols-1 lg:grid-cols-3 gap-4">
                <!-- Card Hôm nay nên học gì -->
                <div class="lg:col-span-2 bg-gradient-to-r from-blue-950/90 via-indigo-950/90 to-slate-900/90 border border-cyan-400/40 rounded-3xl p-5 shadow-2xl relative overflow-hidden">
                    <div class="flex flex-wrap items-center justify-between gap-2 mb-2">
                        <div class="flex items-center gap-2">
                            <span class="bg-emerald-400 text-black font-black text-[10px] px-2.5 py-0.5 rounded-full uppercase tracking-wider">🌟 Hôm nay nên học gì? (AI Đề xuất)</span>
                            <span id="today-member-tag" class="text-xs font-bold text-cyan-300">Hồ sơ: Quang Minh</span>
                        </div>
                        <button onclick="triggerDesktopNotification()" class="bg-white/10 hover:bg-white/20 text-xs font-bold text-amber-300 px-3 py-1 rounded-xl border border-amber-300/30 transition">
                            🔔 Gửi thông báo nhắc học
                        </button>
                    </div>

                    <div id="today-recommendation-box" class="mt-2 flex flex-col sm:flex-row sm:items-center justify-between gap-4 bg-black/35 p-4 rounded-2xl border border-white/10">
                        <!-- Render tự động bằng JS -->
                    </div>
                </div>

                <!-- Card Thao tác thông minh: Sắp xếp AI & Báo lịch đột xuất -->
                <div class="glass-panel rounded-3xl p-5 flex flex-col justify-between border border-white/15">
                    <div>
                        <div class="text-xs font-extrabold uppercase tracking-wider text-amber-400 mb-1">⚡ Điều phối Lịch thông minh</div>
                        <p class="text-[11px] text-slate-300 leading-relaxed">
                            AI tự động tính điểm ưu tiên theo <b>Độ quan trọng</b> & <b>Thời gian tới Deadline</b>, hoặc tự dời ca học khi bạn có lịch bận đột xuất.
                        </p>
                    </div>
                    <div class="space-y-2 mt-3">
                        <button onclick="aiSortTasks()" class="w-full bg-gradient-to-r from-amber-500 to-yellow-500 hover:opacity-95 text-black font-black py-2.5 px-4 rounded-xl text-xs shadow-lg flex items-center justify-center gap-2 transition">
                            <span>🤖 AI Sắp xếp Thứ tự Ưu tiên</span>
                        </button>
                        <button onclick="handleSuddenScheduleChange()" class="w-full bg-slate-800 hover:bg-slate-700 text-cyan-300 border border-cyan-500/30 font-bold py-2.5 px-4 rounded-xl text-xs flex items-center justify-center gap-2 transition">
                            <span>🌪️ Có lịch đột xuất (Tự dời sang giờ trống)</span>
                        </button>
                    </div>
                </div>
            </div>

            <!-- HÀNG 2: CỘT TRÁI (TO-DO LIST KÉO THẢ & DEADLINE) + CỘT PHẢI (THỜI KHÓA BIỂU CÁ NHÂN HÓA) -->
            <div class="grid grid-cols-1 lg:grid-cols-12 gap-4">
                
                <!-- CỘT TRÁI (7 PHẦN): TO-DO LIST KÉO THẢ LINH HOẠT + NÚT "TẠI SAO LẠI CÓ LỊCH NÀY?" -->
                <div class="lg:col-span-7 glass-panel rounded-3xl p-5 border border-white/15 flex flex-col">
                    <div class="flex flex-wrap items-center justify-between gap-2 mb-3">
                        <div>
                            <h3 class="text-sm font-extrabold text-white flex items-center gap-2">
                                📋 To-Do List & Deadline Kéo Thả Linh Hoạt
                                <span class="text-[10px] bg-blue-500/20 text-blue-300 px-2 py-0.5 rounded-lg border border-blue-400/30">Giữ chuột để kéo thả ↕️</span>
                            </h3>
                            <p class="text-[11px] text-slate-400 mt-0.5">Bấm vào <b>"❓ Tại sao có lịch này?"</b> trên từng nhiệm vụ để xem giải thích từ AI</p>
                        </div>
                        <button onclick="openAddTaskModal()" class="bg-blue-600 hover:bg-blue-500 text-white font-extrabold text-xs px-3.5 py-2 rounded-xl shadow">
                            + Thêm Nhiệm Vụ / Deadline
                        </button>
                    </div>

                    <!-- Danh sách kéo thả -->
                    <div id="todo-drag-list" class="space-y-2.5 max-h-[46vh] overflow-y-auto pr-1">
                        <!-- Render bằng JS -->
                    </div>
                </div>

                <!-- CỘT PHẢI (5 PHẦN): THỜI KHÓA BIỂU CÁ NHÂN CỦA THÀNH VIÊN ĐANG CHỌN -->
                <div class="lg:col-span-5 glass-panel rounded-3xl p-5 border border-white/15 flex flex-col">
                    <div class="flex items-center justify-between mb-3">
                        <div>
                            <h3 class="text-sm font-extrabold text-white flex items-center gap-1.5">
                                🗓️ Thời Khóa Biểu Cá Nhân
                                <span id="timetable-owner-badge" class="text-xs text-amber-300 font-black">(Quang Minh)</span>
                            </h3>
                            <p class="text-[11px] text-slate-400 mt-0.5">Mỗi thành viên trong nhóm có lịch học & giờ trống riêng</p>
                        </div>
                        <button onclick="openAddSlotModal()" class="bg-emerald-600 hover:bg-emerald-500 text-white font-extrabold text-xs px-3 py-2 rounded-xl shadow">
                            + Thêm Ca Học / Giờ Trống
                        </button>
                    </div>

                    <!-- Chọn Thứ trong tuần -->
                    <div class="grid grid-cols-7 gap-1 mb-3" id="day-tabs-container">
                        <!-- Thứ 2 -> CN -->
                    </div>

                    <!-- Danh sách các khung giờ trong ngày của thành viên -->
                    <div id="timetable-slots-list" class="space-y-2 max-h-[40vh] overflow-y-auto pr-1">
                        <!-- Render bằng JS -->
                    </div>
                </div>

            </div>
        </div>
    </div>

    <!-- ================= MODAL GIẢI THÍCH "TẠI SAO LẠI CÓ LỊCH NÀY?" (COUNT: 4) ================= -->
    <div id="why-schedule-modal" class="fixed inset-0 z-50 bg-black/75 backdrop-blur-md hidden items-center justify-center p-4">
        <div class="glass-panel w-full max-w-md rounded-3xl p-6 shadow-2xl border border-cyan-400/40">
            <div class="flex justify-between items-center mb-3">
                <div class="flex items-center gap-2">
                    <span class="text-xl">🧠</span>
                    <h3 class="text-base font-extrabold text-white">Tại sao AI lại xếp lịch học này?</h3>
                </div>
                <button onclick="closeWhyModal()" class="text-slate-400 hover:text-white font-bold">✕</button>
            </div>
            <div id="why-modal-content" class="space-y-3 text-xs text-slate-200">
                <!-- Render chi tiết 3 yếu tố: Thời hạn, Độ quan trọng, Thời gian trống -->
            </div>
            <button onclick="closeWhyModal()" class="mt-5 w-full bg-gradient-to-r from-blue-600 to-cyan-500 text-white font-extrabold py-3 rounded-xl text-xs">
                Đã hiểu lý do sắp xếp
            </button>
        </div>
    </div>

    <!-- ================= MODAL THÊM TASK / DEADLINE MỚI ================= -->
    <div id="add-task-modal" class="fixed inset-0 z-50 bg-black/75 backdrop-blur-md hidden items-center justify-center p-4">
        <div class="glass-panel w-full max-w-md rounded-3xl p-6 shadow-2xl border border-white/15">
            <div class="flex justify-between items-center mb-4">
                <h3 class="text-base font-extrabold text-white">➕ Thêm Nhiệm Vụ & Deadline Mới</h3>
                <button onclick="closeAddTaskModal()" class="text-slate-400 hover:text-white font-bold">✕</button>
            </div>
            <div class="space-y-3 text-xs">
                <div>
                    <label class="font-bold text-slate-300 block mb-1">Tên bài tập / Môn học:</label>
                    <input type="text" id="new-task-title" placeholder="VD: Hoàn thiện báo cáo Đồ án Tự động hóa..." class="w-full bg-slate-900 text-white px-3.5 py-2.5 rounded-xl border border-white/15" />
                </div>
                <div class="grid grid-cols-2 gap-3">
                    <div>
                        <label class="font-bold text-amber-300 block mb-1">Thời hạn (Còn mấy giờ?):</label>
                        <input type="number" id="new-task-hours" value="18" min="1" max="720" class="w-full bg-slate-900 text-white px-3.5 py-2.5 rounded-xl border border-white/15" />
                    </div>
                    <div>
                        <label class="font-bold text-cyan-300 block mb-1">Độ quan trọng (1 - 5 sao):</label>
                        <select id="new-task-importance" class="w-full bg-slate-900 text-white px-3 py-2.5 rounded-xl border border-white/15">
                            <option value="5">⭐⭐⭐⭐⭐ (5 - Rất gấp/Quan trọng)</option>
                            <option value="4">⭐⭐⭐⭐ (4 - Quan trọng)</option>
                            <option value="3">⭐⭐⭐ (3 - Vừa phải)</option>
                            <option value="2">⭐⭐ (2 - Bổ trợ)</option>
                        </select>
                    </div>
                </div>
                <div class="grid grid-cols-2 gap-3">
                    <div>
                        <label class="font-bold text-slate-300 block mb-1">Thời lượng cần học (Phút):</label>
                        <select id="new-task-duration" class="w-full bg-slate-900 text-white px-3 py-2.5 rounded-xl border border-white/15">
                            <option value="25">25 phút</option>
                            <option value="35" selected>35 phút</option>
                            <option value="45">45 phút</option>
                            <option value="60">60 phút</option>
                        </select>
                    </div>
                    <div>
                        <label class="font-bold text-slate-300 block mb-1">Khung giờ dự kiến:</label>
                        <input type="text" id="new-task-slot" value="19:30 - 20:15" class="w-full bg-slate-900 text-white px-3.5 py-2.5 rounded-xl border border-white/15" />
                    </div>
                </div>
            </div>
            <button onclick="saveNewTask()" class="mt-5 w-full bg-blue-600 hover:bg-blue-500 text-white font-extrabold py-3 rounded-xl text-xs">
                Lưu vào Lịch Cá Nhân
            </button>
        </div>
    </div>

    <!-- ================= MODAL THÊM CA HỌC / GIỜ TRỐNG VÀO THỜI KHÓA BIỂU ================= -->
    <div id="add-slot-modal" class="fixed inset-0 z-50 bg-black/75 backdrop-blur-md hidden items-center justify-center p-4">
        <div class="glass-panel w-full max-w-md rounded-3xl p-6 shadow-2xl border border-white/15">
            <div class="flex justify-between items-center mb-4">
                <h3 class="text-base font-extrabold text-white">🗓️ Thêm Lịch Học / Khung Giờ Trống</h3>
                <button onclick="closeAddSlotModal()" class="text-slate-400 hover:text-white font-bold">✕</button>
            </div>
            <div class="space-y-3 text-xs">
                <div>
                    <label class="font-bold text-slate-300 block mb-1">Khung giờ (VD: 07:30 - 11:00 hoặc 14:00 - 16:00):</label>
                    <input type="text" id="new-slot-time" placeholder="14:00 - 16:00" class="w-full bg-slate-900 text-white px-3.5 py-2.5 rounded-xl border border-white/15" />
                </div>
                <div>
                    <label class="font-bold text-slate-300 block mb-1">Nội dung ca học / Trạng thái:</label>
                    <input type="text" id="new-slot-subject" placeholder="VD: Trống lịch - Dành tự học hoặc Học trên trường" class="w-full bg-slate-900 text-white px-3.5 py-2.5 rounded-xl border border-white/15" />
                </div>
                <div>
                    <label class="font-bold text-slate-300 block mb-1">Loại khung giờ:</label>
                    <select id="new-slot-type" class="w-full bg-slate-900 text-white px-3 py-2.5 rounded-xl border border-white/15">
                        <option value="free">🟢 Giờ trống (AI có thể xếp lịch bay học tập)</option>
                        <option value="busy">🔴 Lịch học trên trường / Bận cố định</option>
                    </select>
                </div>
            </div>
            <button onclick="saveNewTimetableSlot()" class="mt-5 w-full bg-emerald-600 hover:bg-emerald-500 text-white font-extrabold py-3 rounded-xl text-xs">
                Thêm vào Thời Khóa Biểu
            </button>
        </div>
    </div>

    <!-- ================= CẢNH BÁO ĐỎ STRICT MODE KHI CHUYỂN TAB ================= -->
    <div id="turbulence-modal" class="fixed inset-0 z-[999] turbulence-alert hidden flex-col items-center justify-center p-6 text-center">
        <div class="text-6xl mb-3 animate-bounce">🚨</div>
        <div class="bg-black/40 border border-white/30 px-4 py-1 rounded-full text-xs font-mono font-bold uppercase tracking-widest text-yellow-300 mb-2">
            COCKPIT MASTER WARNING • TURBULENCE DETECTED
        </div>
        <h2 class="text-2xl sm:text-3xl font-black text-white uppercase tracking-wide mb-2">
            CẢNH BÁO: BẠN ĐÃ RỜI KHỎI CHUYẾN BAY!
        </h2>
        <p class="text-sm text-red-100 max-w-md mb-5">
            Hệ thống phát hiện bạn vừa chuyển sang Tab/Ứng dụng khác. Đồng hồ tập trung đã bị <b>ĐÓNG BĂNG</b>!
        </p>
        <div class="bg-black/50 border border-red-300/30 rounded-2xl p-4 w-full max-w-sm mb-6">
            <div class="text-xs text-red-200 uppercase font-bold mb-1">Số lần vi phạm kỷ luật bay</div>
            <div id="violation-count-text" class="text-2xl font-black text-yellow-400 mono">1 / 3 LẦN</div>
        </div>
        <button onclick="resumeFromTurbulence()" class="bg-white hover:bg-yellow-300 text-red-900 font-black px-8 py-4 rounded-2xl shadow-2xl text-sm uppercase tracking-wider">
            🔒 Quay lại Buồng lái & Tiếp tục Học
        </button>
    </div>

    <div id="crash-modal" class="fixed inset-0 z-[999] bg-black/95 backdrop-blur-xl hidden flex-col items-center justify-center p-6 text-center">
        <div class="text-6xl mb-3">💥</div>
        <h2 class="text-2xl font-black text-red-500 uppercase mb-2">CHUYẾN BAY ĐÃ BỊ HỦY BỎ (FLIGHT FAILED)</h2>
        <p class="text-xs text-slate-300 max-w-sm mb-6">Bạn đã rời khỏi màn hình tập trung quá 3 lần cho phép.</p>
        <button onclick="closeCrashModal()" class="bg-red-600 hover:bg-red-500 text-white font-extrabold px-6 py-3.5 rounded-2xl text-xs uppercase">Đặt lại chuyến bay mới</button>
    </div>

    <!-- MODAL THÊM NHẠC LOFI, ẢNH NỀN & AVATAR CHATBOT -->
    <div id="media-modal" class="fixed inset-0 z-50 bg-black/75 backdrop-blur-md hidden items-center justify-center p-4">
        <div class="glass-panel w-full max-w-md rounded-3xl p-6 shadow-2xl">
            <div class="flex justify-between items-center mb-4">
                <h3 class="text-base font-extrabold text-white">🎧 Trạm Tùy Chỉnh Nhạc, Ảnh & Avatar Bot</h3>
                <button onclick="closeMediaModal()" class="text-slate-400 hover:text-white text-lg font-bold">✕</button>
            </div>
            <div class="space-y-3 text-xs">
                <div class="bg-slate-900/90 p-3 rounded-2xl border border-white/10">
                    <label class="font-bold text-cyan-400 block mb-1">1. Tải nhạc Lofi từ máy (.mp3, .wav):</label>
                    <input type="file" accept="audio/*" onchange="handleLocalAudio(this)" class="w-full text-slate-300 file:mr-2 file:py-1 file:px-3 file:rounded-xl file:border-0 file:font-bold file:bg-blue-600 file:text-white cursor-pointer mb-1.5" />
                    <input type="text" id="audio-url-input" placeholder="Hoặc dán link MP3..." class="w-full bg-slate-800 text-white px-3 py-1.5 rounded-xl border border-white/10" />
                </div>

                <div class="bg-slate-900/90 p-3 rounded-2xl border border-white/10 flex items-center justify-between">
                    <div>
                        <div class="font-bold text-white">🛫 Tiếng động cơ Cabin A321 (White Noise)</div>
                        <div class="text-[10px] text-slate-400">Tăng khả năng tập trung sâu</div>
                    </div>
                    <input type="checkbox" onchange="toggleCabinNoise(this.checked)" class="w-5 h-5 accent-cyan-400 cursor-pointer" />
                </div>

                <div class="bg-slate-900/90 p-3 rounded-2xl border border-white/10">
                    <label class="font-bold text-yellow-400 block mb-1">2. Đổi ảnh nền Sân bay:</label>
                    <input type="file" accept="image/*" onchange="handleLocalImage(this)" class="w-full text-slate-300 file:mr-2 file:py-1 file:px-3 file:rounded-xl file:border-0 file:font-bold file:bg-yellow-500 file:text-black cursor-pointer" />
                </div>

                <div class="bg-slate-900/90 p-3 rounded-2xl border border-amber-400/30">
                    <label class="font-bold text-amber-300 block mb-1">3. Đổi hình đại diện Chatbot AI góc phải:</label>
                    <input type="file" accept="image/*" onchange="handleBotAvatarUpload(this)" class="w-full text-slate-300 file:mr-2 file:py-1 file:px-3 file:rounded-xl file:border-0 file:font-bold file:bg-amber-500 file:text-black cursor-pointer" />
                </div>
            </div>
            <button onclick="applyCustomMedia()" class="mt-4 w-full bg-gradient-to-r from-blue-600 to-cyan-500 text-white font-extrabold py-3 rounded-xl text-xs">Lưu & Đóng</button>
        </div>
    </div>

    <!-- ================= MÀN HÌNH 1: ĐẶT VÉ MÁY BAY (BOOKING) ================= -->
    <div id="screen-booking" class="fixed bottom-5 left-1/2 -translate-x-1/2 z-20 w-[94%] max-w-lg glass-panel rounded-3xl p-5 shadow-2xl">
        <div class="relative w-full h-28 rounded-2xl overflow-hidden mb-3.5 border border-white/10">
            <img id="dest-banner-img" src="" class="w-full h-full object-cover opacity-85 transition-all duration-500" />
            <div class="absolute inset-0 bg-gradient-to-t from-[#060911] via-[#060911]/40 to-transparent"></div>
            <div class="absolute top-2.5 left-3 flex items-center gap-1.5">
                <span id="badge-origin" class="bg-cyan-400 text-black font-black text-[10px] px-2 py-0.5 rounded-md">✈️ SGN</span>
                <span class="text-white text-xs font-bold">➔</span>
                <span id="badge-dest" class="bg-yellow-400 text-black font-black text-[10px] px-2 py-0.5 rounded-md">✈️ CXR</span>
                <span id="badge-dist" class="bg-black/60 text-slate-200 text-[10px] font-mono px-2 py-0.5 rounded-md border border-white/15">320 km</span>
            </div>
            <div class="absolute bottom-2.5 left-3 right-3 flex justify-between items-end">
                <div>
                    <div id="banner-region-tag" class="text-[10px] text-cyan-300 font-bold uppercase tracking-wider"></div>
                    <div id="banner-dest-title" class="text-base font-extrabold text-white"></div>
                </div>
                <select id="aircraft-select" onchange="updateAircraft()" class="bg-white/15 backdrop-blur-md text-white text-[11px] font-bold px-2.5 py-1 rounded-lg border border-white/20 focus:outline-none cursor-pointer">
                    <option value="Airbus A321neo" class="bg-slate-900">🛩️ Airbus A321neo</option>
                    <option value="Boeing 787-9" class="bg-slate-900">🛩️ Boeing 787-9</option>
                    <option value="Airbus A350-900" class="bg-slate-900">🛩️ Airbus A350-900</option>
                    <option value="ATR 72-600" class="bg-slate-900">🛩️ ATR 72-600</option>
                </select>
            </div>
        </div>

        <div class="grid grid-cols-11 gap-2 items-center bg-slate-900/90 p-3 rounded-2xl border border-white/10 mb-3">
            <div class="col-span-5">
                <div class="text-[10px] text-slate-400 uppercase font-bold mb-1">Điểm khởi hành</div>
                <select id="origin-select" onchange="onRouteChange()" class="w-full bg-slate-800 text-white font-extrabold text-xs px-2.5 py-2 rounded-xl border border-white/10 focus:outline-none cursor-pointer"></select>
            </div>
            <div class="col-span-1 flex justify-center pt-4">
                <button onclick="swapRoute()" class="w-8 h-8 rounded-full bg-slate-800 hover:bg-blue-600 text-cyan-400 hover:text-white font-bold text-sm flex items-center justify-center transition border border-white/10">⇄</button>
            </div>
            <div class="col-span-5">
                <div class="text-[10px] text-yellow-400 uppercase font-bold mb-1">Điểm hạ cánh</div>
                <select id="dest-select" onchange="onRouteChange()" class="w-full bg-slate-800 text-white font-extrabold text-xs px-2.5 py-2 rounded-xl border border-yellow-400/40 focus:outline-none cursor-pointer"></select>
            </div>
        </div>

        <div class="flex items-center justify-between mb-1.5">
            <span class="text-[11px] text-slate-400 font-semibold">Thời gian tập trung (Phút):</span>
            <button onclick="randomRoute()" class="text-[11px] text-cyan-400 font-bold hover:underline">🎲 Random chuyến bay</button>
        </div>

        <div class="grid grid-cols-6 gap-1.5 mb-3.5">
            <button onclick="setDuration(15)" id="dur-15" class="dur-btn bg-slate-800 py-2 rounded-xl text-xs font-bold text-slate-300 border border-transparent">15m</button>
            <button onclick="setDuration(25)" id="dur-25" class="dur-btn bg-slate-800 py-2 rounded-xl text-xs font-bold text-slate-300 border border-transparent">25m</button>
            <button onclick="setDuration(35)" id="dur-35" class="dur-btn bg-blue-600/30 border-blue-400 text-blue-300 py-2 rounded-xl text-xs font-bold border">35m</button>
            <button onclick="setDuration(45)" id="dur-45" class="dur-btn bg-slate-800 py-2 rounded-xl text-xs font-bold text-slate-300 border border-transparent">45m</button>
            <button onclick="setDuration(60)" id="dur-60" class="dur-btn bg-slate-800 py-2 rounded-xl text-xs font-bold text-slate-300 border border-transparent">60m</button>
            <button onclick="setDuration(90)" id="dur-90" class="dur-btn bg-slate-800 py-2 rounded-xl text-xs font-bold text-slate-300 border border-transparent">90m</button>
        </div>

        <button onclick="goToSeatSelection()" class="w-full bg-gradient-to-r from-blue-600 to-cyan-500 hover:opacity-95 text-white font-extrabold py-3.5 rounded-2xl shadow-lg shadow-blue-600/30 transition flex items-center justify-center gap-2 text-sm">
            <span>Book Now • Chọn Ghế & Chế Độ Tập Trung</span>
            <span>➔</span>
        </button>
    </div>

    <!-- ================= MÀN HÌNH 2: SƠ ĐỒ GHẾ & POPUP FOCUS ================= -->
    <div id="screen-seat" class="fixed inset-0 z-30 bg-[#070b14]/95 backdrop-blur-xl hidden flex-col items-center justify-between py-5 px-4">
        <div class="w-full max-w-md flex items-center justify-between mt-12">
            <button onclick="backToBooking()" class="bg-slate-800/80 hover:bg-slate-700 text-slate-200 px-3.5 py-2 rounded-xl text-xs font-bold">‹ Quay lại</button>
            <div class="text-center">
                <div id="seat-header-aircraft" class="text-[10px] text-cyan-400 font-extrabold uppercase tracking-widest">AIRBUS A321NEO</div>
                <div id="seat-header-route" class="text-sm font-extrabold text-white mt-0.5">SGN ➔ CXR • 35m</div>
            </div>
            <div class="w-16 text-right">
                <span id="seat-selected-badge" class="bg-blue-600/30 border border-blue-400 text-blue-200 text-xs font-mono font-bold px-2.5 py-1 rounded-lg">06A</span>
            </div>
        </div>

        <div class="relative w-full max-w-[340px] h-[66vh] fuselage flex flex-col items-center pt-12 pb-8 px-6 overflow-y-auto my-2">
            <div class="w-32 h-6 border-b border-slate-700/80 mb-5 flex items-center justify-center text-[10px] font-mono text-slate-500 tracking-widest uppercase">Cockpit</div>
            <div class="grid grid-cols-5 w-full text-center text-xs font-extrabold text-slate-400 mb-3 px-1">
                <div>A</div><div>C</div><div></div><div>D</div><div>F</div>
            </div>
            <div id="seat-grid" class="w-full space-y-2.5 pb-8"></div>
        </div>

        <!-- POPUP "What do you want to focus?" -->
        <div id="focus-popover-backdrop" class="fixed inset-0 z-40 bg-black/50 backdrop-blur-[2px] hidden items-center justify-center p-4">
            <div class="focus-popover w-full max-w-[360px] rounded-[28px] p-5 text-white">
                <div class="flex justify-between items-center mb-1">
                    <span class="text-xs font-bold text-blue-300/90">Seat: <span id="pop-seat-code" class="mono text-white">06A</span></span>
                    <button onclick="closeFocusPopover()" class="text-slate-400 hover:text-white text-sm font-bold">✕</button>
                </div>
                <h3 class="text-base font-extrabold text-white mb-3.5">What do you want to focus?</h3>

                <div class="flex flex-wrap gap-2 mb-3.5" id="focus-pills-container"></div>

                <div id="custom-focus-box" class="hidden mb-3">
                    <input type="text" id="custom-focus-input" placeholder="Nhập mục tiêu riêng (VD: Đồ án, Giải tích...)" class="w-full bg-slate-900/90 text-xs text-white px-3.5 py-2.5 rounded-xl border border-blue-400/40 focus:outline-none" />
                </div>

                <div class="bg-slate-900/60 p-3 rounded-2xl border border-white/10 mb-3">
                    <label class="block text-[10px] uppercase tracking-wider text-slate-400 font-bold mb-1">Hành khách (Theo hồ sơ đang chọn):</label>
                    <input type="text" id="passenger-name-input" value="QUANG MINH" class="w-full bg-transparent text-xs font-extrabold text-amber-300 focus:outline-none uppercase" />
                </div>

                <div class="bg-red-500/15 border border-red-400/30 p-3 rounded-2xl flex items-center justify-between mb-4">
                    <div>
                        <div class="text-xs font-extrabold text-red-200">🔒 Khóa Kỷ Luật (Strict Mode)</div>
                        <div class="text-[10px] text-slate-300">Tự bung Fullscreen & Báo động nếu chuyển tab</div>
                    </div>
                    <input type="checkbox" id="strict-mode-toggle" checked class="w-5 h-5 accent-red-500 cursor-pointer" />
                </div>

                <button onclick="confirmSeatAndFocus()" class="w-full bg-blue-500 hover:bg-blue-400 text-white font-extrabold py-3 rounded-2xl text-xs shadow-lg">
                    Xác nhận Ghế & Xuất Vé Boarding Pass ➔
                </button>
            </div>
        </div>

        <div class="w-full max-w-md flex items-center justify-between px-2">
            <div class="text-xs text-slate-400">Chạm vào ghế bất kỳ để chọn chế độ tập trung</div>
            <button onclick="showBoardingPass()" class="bg-blue-600 hover:bg-blue-500 text-white font-extrabold px-5 py-2.5 rounded-xl text-xs shadow-lg">Tiếp tục ➔</button>
        </div>
    </div>

    <!-- ================= MÀN HÌNH 3: VÉ MÁY BAY (BOARDING PASS) ================= -->
    <div id="screen-ticket" class="fixed inset-0 z-40 bg-black/85 backdrop-blur-md hidden items-center justify-center p-4">
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
                            <div class="text-[10px] text-slate-400 uppercase">Passenger</div>
                            <div id="tk-passenger" class="text-base font-black text-amber-300 uppercase">QUANG MINH</div>
                        </div>
                        <div class="text-right">
                            <div class="text-[10px] text-slate-400 uppercase">Discipline Mode</div>
                            <div id="tk-strict-badge" class="text-[11px] font-extrabold text-red-400">🔒 STRICT LOCK ON</div>
                        </div>
                    </div>

                    <div class="flex justify-between items-center my-4">
                        <div>
                            <div id="tk-origin-code" class="text-4xl font-black text-white">SGN</div>
                            <div id="tk-origin-name" class="text-xs text-slate-400 mt-0.5">Sài Gòn</div>
                        </div>
                        <div class="flex flex-col items-center">
                            <span class="text-cyan-400 text-xl">✈️</span>
                            <span id="tk-duration" class="text-xs font-extrabold text-yellow-400 mt-0.5">35m</span>
                        </div>
                        <div class="text-right">
                            <div id="tk-dest-code" class="text-4xl font-black text-yellow-400">CXR</div>
                            <div id="tk-dest-name" class="text-xs text-slate-400 mt-0.5">Cam Ranh</div>
                        </div>
                    </div>

                    <div class="grid grid-cols-3 gap-2 pt-4 border-t border-white/10 text-xs mb-5">
                        <div>
                            <div class="text-slate-500 text-[10px] uppercase">Seat</div>
                            <div id="tk-seat" class="font-extrabold text-cyan-400 mt-0.5 mono">06A</div>
                        </div>
                        <div>
                            <div class="text-slate-500 text-[10px] uppercase">Distance</div>
                            <div id="tk-dist" class="font-bold text-white mt-0.5">320 km</div>
                        </div>
                        <div class="text-right">
                            <div class="text-slate-500 text-[10px] uppercase">Focus Mode</div>
                            <div id="tk-focus" class="font-extrabold text-blue-300 mt-0.5 truncate">💻 Work</div>
                        </div>
                    </div>

                    <div class="border-b-2 border-dashed border-slate-700/80 my-4"></div>

                    <div class="flex flex-col items-center mt-4">
                        <div class="w-full h-12 flex items-center justify-between gap-[2px] px-2">
                            <script>
                                for(let i=0; i<45; i++) {
                                    let w = [1, 2, 3, 4][Math.floor(Math.random()*4)];
                                    document.write(`<div style="width:${w*2}px" class="h-full bg-blue-400/85 rounded-full"></div>`);
                                }
                            </script>
                        </div>
                        <div class="mono text-[10px] tracking-[0.35em] text-slate-400 mt-2">GROUP4-FOCUS-PASS</div>
                    </div>
                </div>
            </div>

            <div class="flex gap-2 w-full mt-5">
                <button onclick="backToSeatFromTicket()" class="w-1/3 bg-slate-800 hover:bg-slate-700 text-slate-300 font-bold py-4 rounded-2xl text-xs">‹ Đổi ghế</button>
                <button onclick="startFlight()" class="w-2/3 bg-gradient-to-r from-blue-600 to-cyan-500 hover:opacity-95 text-white font-extrabold py-4 rounded-2xl shadow-xl text-xs uppercase tracking-wider">
                    🛫 Boarding & Khóa Màn Hình
                </button>
            </div>
        </div>
    </div>

    <!-- ================= MÀN HÌNH 4: ĐANG BAY TRÊN BẢN ĐỒ VỆ TINH ================= -->
    <div id="screen-flying" class="fixed bottom-5 left-1/2 -translate-x-1/2 z-20 w-[94%] max-w-lg glass-panel rounded-3xl p-5 shadow-2xl hidden">
        <div class="flex items-center justify-between border-b border-white/10 pb-3 mb-3">
            <div class="flex items-center gap-3">
                <span class="px-2.5 py-1.5 rounded-xl bg-yellow-400 text-black font-black text-xs mono" id="fly-badge">CXR</span>
                <div>
                    <div class="text-xs font-extrabold text-white" id="fly-route-text">Sài Gòn ➔ Cam Ranh</div>
                    <div class="text-[11px] text-cyan-400 font-semibold mt-0.5" id="fly-sub-info">💻 Work • Ghế 06A • QUANG MINH</div>
                </div>
            </div>
            <div class="text-right">
                <div class="text-[10px] text-slate-400 uppercase font-bold">An toàn bay</div>
                <div id="safety-hearts" class="text-xs tracking-widest">❤️❤️❤️</div>
            </div>
        </div>

        <div class="flex items-end justify-between">
            <div>
                <div class="text-[10px] uppercase tracking-widest text-slate-400 flex items-center gap-1.5">
                    <span>Time Remaining</span>
                    <span id="strict-live-pill" class="bg-red-500/20 text-red-300 border border-red-500/30 px-1.5 py-0.2 rounded text-[9px] font-bold">🔒 KHÓA TAB</span>
                </div>
                <div id="countdown-timer" class="mono text-4xl font-extrabold text-white tracking-tight mt-0.5">35:00</div>
            </div>
            <div class="text-right">
                <div class="text-xs text-slate-300 font-semibold mb-1.5">Còn <span id="fly-dist-left" class="text-yellow-400 font-bold">320</span> km</div>
                <div class="flex gap-1.5">
                    <button onclick="centerOnPlane()" class="bg-slate-800 hover:bg-slate-700 text-xs px-3 py-2 rounded-xl text-slate-200 border border-white/10 font-bold">🎯</button>
                    <button onclick="abortFlight()" class="bg-red-500/20 hover:bg-red-500/30 text-red-300 border border-red-500/30 px-3.5 py-2 rounded-xl text-xs font-bold transition">Hạ cánh khẩn cấp</button>
                </div>
            </div>
        </div>

        <div class="w-full bg-slate-800 h-2.5 rounded-full overflow-hidden mt-4">
            <div id="flight-progress" class="bg-gradient-to-r from-blue-500 via-cyan-400 to-yellow-400 h-full w-0 transition-all duration-500"></div>
        </div>
    </div>

    <!-- ================= TRỢ LÝ CHATBOT AI VÀNG KIM (GIỐNG HỆT ẢNH MẪU SAMI) ================= -->
    <!-- Nút tròn Robot Vàng Kim ở góc dưới bên phải -->
    <div id="chatbot-launcher" onclick="toggleChatbotWindow()" class="fixed bottom-5 right-5 z-50 w-16 h-16 rounded-full bg-white p-1 cursor-pointer bot-launcher-glow flex items-center justify-center border-2 border-[#d4a349]">
        <img id="bot-launcher-img" src="https://cdn-icons-png.flaticon.com/512/4712/4712109.png" class="w-full h-full rounded-full object-cover bg-gradient-to-b from-yellow-300 to-amber-500 p-1" />
        <span class="absolute -top-1 -right-1 w-4 h-4 bg-emerald-500 border-2 border-white rounded-full"></span>
    </div>

    <!-- Cửa sổ Chat Vàng Kim chuẩn giao diện mẫu -->
    <div id="chatbot-window" class="fixed bottom-24 right-5 z-50 w-[350px] sm:w-[375px] h-[510px] bg-[#f8f9fa] text-slate-800 rounded-2xl shadow-2xl border border-[#d4a349]/50 hidden flex-col overflow-hidden">
        <!-- Header màu vàng đồng (#d4a349) -->
        <div class="bg-[#d4a349] text-white px-4 py-3 flex items-center justify-between shadow">
            <div class="flex items-center gap-2.5">
                <div class="w-9 h-9 rounded-full bg-white p-0.5 shadow">
                    <img id="bot-header-img" src="https://cdn-icons-png.flaticon.com/512/4712/4712109.png" class="w-full h-full rounded-full object-cover bg-amber-400" />
                </div>
                <span class="font-bold text-sm tracking-wide">Chat cùng Trợ lý AI G4</span>
            </div>
            <div class="flex items-center gap-3 text-white/90">
                <button onclick="resetChat()" title="Làm mới đoạn chat" class="hover:text-white text-sm font-bold">↺</button>
                <button onclick="toggleChatbotWindow()" class="hover:text-white text-lg font-bold leading-none">✕</button>
            </div>
        </div>

        <!-- Nội dung tin nhắn -->
        <div id="chat-messages" class="flex-1 p-4 overflow-y-auto space-y-3 bg-[#f7f8fc]">
            <!-- Nút "Bắt đầu" bên phải như ảnh -->
            <div class="flex flex-col items-end">
                <div class="bg-[#d4a349] text-white font-semibold text-xs px-5 py-2.5 rounded-2xl rounded-tr-sm shadow-sm">
                    Bắt đầu
                </div>
                <span class="text-[10px] text-slate-400 mt-1">13:47</span>
            </div>

            <!-- Tin nhắn chào của Sami Bot bên trái có viền vàng kem (#f6e0b5) -->
            <div class="flex items-start gap-2">
                <img id="bot-msg-img" src="https://cdn-icons-png.flaticon.com/512/4712/4712109.png" class="w-8 h-8 rounded-full bg-amber-400 p-0.5 border border-[#d4a349] shrink-0 mt-1" />
                <div>
                    <div class="bg-[#fae5be] p-1.5 rounded-2xl rounded-tl-sm shadow-sm">
                        <div class="bg-white rounded-xl p-3 text-xs text-slate-800 leading-relaxed">
                            Xin chào, 🙋‍♀️<br>
                            Mình là <b>Sami</b> trợ lý AI của <b>FOCUS FLIGHT G4</b>.<br>
                            Hôm nay Mình có thể giúp gì được cho <b id="bot-greet-name">Quang Minh</b>?
                        </div>
                    </div>
                    <span class="text-[10px] text-slate-400 mt-1 block">13:47</span>
                </div>
            </div>
        </div>

        <!-- Các nút gợi ý hỏi nhanh -->
        <div class="px-3 py-2 bg-white border-t border-slate-100 flex gap-1.5 overflow-x-auto">
            <button onclick="sendQuickChat('Hôm nay mình nên học gì?')" class="shrink-0 bg-amber-50 hover:bg-amber-100 text-[#b07d2b] border border-[#d4a349]/40 text-[11px] font-semibold px-2.5 py-1 rounded-full">💡 Hôm nay học gì?</button>
            <button onclick="sendQuickChat('Kiểm tra deadline sắp tới')" class="shrink-0 bg-amber-50 hover:bg-amber-100 text-[#b07d2b] border border-[#d4a349]/40 text-[11px] font-semibold px-2.5 py-1 rounded-full">⏰ Deadline gấp</button>
            <button onclick="sendQuickChat('Tại sao xếp lịch này?')" class="shrink-0 bg-amber-50 hover:bg-amber-100 text-[#b07d2b] border border-[#d4a349]/40 text-[11px] font-semibold px-2.5 py-1 rounded-full">❓ Giải thích lịch</button>
            <button onclick="sendQuickChat('Mình có lịch đột xuất')" class="shrink-0 bg-amber-50 hover:bg-amber-100 text-[#b07d2b] border border-[#d4a349]/40 text-[11px] font-semibold px-2.5 py-1 rounded-full">🌪️ Dời lịch đột xuất</button>
        </div>

        <!-- Ô nhập tin nhắn dưới cùng giống hệt ảnh -->
        <div class="p-3 bg-white border-t border-slate-200 flex items-center gap-2">
            <button onclick="switchMainTab('planner')" class="text-[#d4a349] hover:opacity-80 font-bold text-lg px-1" title="Mở bảng Lịch học">☰</button>
            <input type="text" id="chat-input" onkeydown="if(event.key==='Enter') sendChatMessage()" placeholder="Nhập tin nhắn" class="flex-1 text-xs text-slate-800 placeholder-slate-400 focus:outline-none px-2 py-1.5" />
            <button onclick="sendChatMessage()" class="w-9 h-9 rounded-full bg-[#d4a349] hover:bg-[#c29138] text-white flex items-center justify-center shadow transition">
                ➤
            </button>
        </div>
    </div>

    <script>
        // ================= 1. DỮ LIỆU SÂN BAY & CẤU HÌNH CHUYẾN BAY =================
        const AIRPORTS = [
            { code: "SGN", name: "Sài Gòn (Tân Sơn Nhất)", region: "📍 TP. Hồ Chí Minh", coords: [10.8188, 106.6519], img: "https://images.unsplash.com/photo-1583417319070-4a69db38a482?w=900&q=80" },
            { code: "DAD", name: "Đà Nẵng (Quảng Nam)", region: "✨ Quê hương Quảng Nam - Đà Nẵng", coords: [16.0439, 108.1994], img: "https://images.unsplash.com/photo-1559592413-7cec4d0cae2b?w=900&q=80" },
            { code: "CXR", name: "Cam Ranh (Khánh Hòa)", region: "🏖️ Quê hương Diên Khánh - Khánh Hòa", coords: [11.9982, 109.2194], img: "https://images.unsplash.com/photo-1582297121287-75905c10640d?w=900&q=80" },
            { code: "UIH", name: "Phù Cát (Quy Nhơn)", region: "🌊 Quê hương Quy Nhơn - Bình Định", coords: [13.9550, 109.0422], img: "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=900&q=80" },
            { code: "LTH", name: "Long Thành (Đồng Nai)", region: "🛫 Quê hương Đồng Nai", coords: [10.7850, 107.0650], img: "https://images.unsplash.com/photo-1436491865332-7a61a109cc05?w=900&q=80" },
            { code: "DLI", name: "Đà Lạt (Liên Khương)", region: "🌲 Cao nguyên Lâm Đồng", coords: [11.7500, 108.3667], img: "https://images.unsplash.com/photo-1509316975850-ff9c5deb0cd9?w=900&q=80" },
            { code: "HAN", name: "Hà Nội (Nội Bài)", region: "🏛️ Thủ đô Hà Nội", coords: [21.2212, 105.8072], img: "https://images.unsplash.com/photo-1509030450996-dd1a26dda07a?w=900&q=80" },
            { code: "HPH", name: "Hải Phòng (Cát Bi)", region: "⚓ Thành phố Cảng Hải Phòng", coords: [20.8194, 106.7250], img: "https://images.unsplash.com/photo-1540959733332-eab4deabeeaf?w=900&q=80" },
            { code: "VII", name: "TP. Vinh (Nghệ An)", region: "🌾 Miền Trung Nghệ An", coords: [18.7376, 105.6708], img: "https://images.unsplash.com/photo-1506744038136-46273834b3fb?w=900&q=80" },
            { code: "PQC", name: "Phú Quốc (Kiên Giang)", region: "🏝️ Đảo Ngọc Phú Quốc", coords: [10.1698, 103.9931], img: "https://images.unsplash.com/photo-1540202404-a2f29016b523?w=900&q=80" }
        ];

        const FOCUS_MODES = [
            { id: "focus", label: "Focus", icon: "⚛️", color: "bg-slate-600/90 border-slate-400 text-white" },
            { id: "work", label: "Work", icon: "💻", color: "bg-blue-600 border-blue-300 text-white" },
            { id: "meditate", label: "Meditate", icon: "🧘", color: "bg-indigo-500 border-indigo-300 text-white" },
            { id: "read", label: "Read", icon: "📖", color: "bg-teal-600 border-teal-300 text-white" },
            { id: "exercise", label: "Exercise", icon: "🏃", color: "bg-sky-500 border-sky-300 text-white" }
        ];

        // ================= 2. DỮ LIỆU CÁ NHÂN HÓA CHO 6 THÀNH VIÊN NHÓM G4 =================
        const DAYS_OF_WEEK = ["T2", "T3", "T4", "T5", "T6", "T7", "CN"];
        let selectedDay = "T2";

        const DEFAULT_MEMBERS_DB = {
            quangminh: {
                name: "QUANG MINH",
                preferredDest: "DAD",
                seat: "06A",
                tasks: [
                    { id: 101, title: "Hoàn thiện Web App Streamlit Đồ án TACN1", hoursLeft: 14, importance: 5, duration: 45, slot: "19:30 - 20:15", done: false },
                    { id: 102, title: "Ôn luyện IELTS Speaking & Listening Band 6.0", hoursLeft: 36, importance: 4, duration: 35, slot: "14:00 - 14:35", done: false },
                    { id: 103, title: "Mô phỏng mạch Vi điều khiển STM32 & PLC", hoursLeft: 60, importance: 4, duration: 45, slot: "20:30 - 21:15", done: false }
                ],
                timetable: {
                    "T2": [
                        { time: "07:30 - 11:00", subject: "Học Lý thuyết Điều khiển tự động trên trường", type: "busy" },
                        { time: "14:00 - 16:00", subject: "Khung giờ trống - Tự học IELTS / Code", type: "free" },
                        { time: "19:30 - 21:30", subject: "Khung giờ trống - Làm Đồ án nhóm G4", type: "free" }
                    ],
                    "T3": [
                        { time: "08:00 - 11:30", subject: "Thực hành PLC & Mạng công nghiệp", type: "busy" },
                        { time: "15:00 - 17:30", subject: "Khung giờ trống - Tự học tại nhà", type: "free" }
                    ],
                    "T4": [{ time: "18:30 - 21:00", subject: "Khung giờ trống buổi tối", type: "free" }],
                    "T5": [{ time: "13:30 - 16:30", subject: "Khung giờ trống chiều Thứ 5", type: "free" }],
                    "T6": [{ time: "19:00 - 21:30", subject: "Khung giờ trống tối Thứ 6", type: "free" }],
                    "T7": [{ time: "09:00 - 11:30", subject: "Khung giờ trống cuối tuần", type: "free" }],
                    "CN": [{ time: "19:30 - 21:30", subject: "Họp nhóm G4 & Tổng kết tuần", type: "free" }]
                }
            },
            huudai: {
                name: "HỮU ĐẠI",
                preferredDest: "CXR",
                seat: "02A",
                tasks: [
                    { id: 201, title: "Thiết kế Slide thuyết trình Dự án G4", hoursLeft: 16, importance: 5, duration: 35, slot: "20:00 - 20:35", done: false },
                    { id: 202, title: "Tổng hợp bảng khảo sát Google Sheets 44 câu", hoursLeft: 28, importance: 4, duration: 25, slot: "15:00 - 15:25", done: false }
                ],
                timetable: {
                    "T2": [
                        { time: "08:00 - 11:30", subject: "Ca học sáng trên giảng đường", type: "busy" },
                        { time: "15:00 - 17:00", subject: "Khung giờ trống chiều", type: "free" },
                        { time: "20:00 - 22:00", subject: "Khung giờ trống tối - Làm dự án", type: "free" }
                    ],
                    "T3": [{ time: "19:00 - 21:00", subject: "Khung giờ trống buổi tối", type: "free" }],
                    "T4": [{ time: "14:00 - 16:30", subject: "Khung giờ trống chiều", type: "free" }],
                    "T5": [{ time: "19:30 - 21:30", subject: "Khung giờ trống tối", type: "free" }],
                    "T6": [{ time: "15:00 - 17:00", subject: "Khung giờ trống chiều", type: "free" }],
                    "T7": [{ time: "09:00 - 11:00", subject: "Ôn tập cuối tuần", type: "free" }],
                    "CN": [{ time: "19:30 - 21:30", subject: "Họp nhóm G4", type: "free" }]
                }
            },
            khanhthi: {
                name: "KHÁNH THI",
                preferredDest: "DAD",
                seat: "04F",
                tasks: [
                    { id: 301, title: "Soạn kịch bản thuyết trình phần Giải pháp AI", hoursLeft: 18, importance: 5, duration: 45, slot: "19:00 - 19:45", done: false },
                    { id: 302, title: "Đọc tài liệu môn Tâm lý học ứng dụng", hoursLeft: 48, importance: 3, duration: 35, slot: "14:30 - 15:05", done: false }
                ],
                timetable: {
                    "T2": [
                        { time: "13:00 - 16:00", subject: "Học ca chiều tại trường", type: "busy" },
                        { time: "19:00 - 21:30", subject: "Khung giờ trống tối - Tự học", type: "free" }
                    ],
                    "T3": [{ time: "08:30 - 10:30", subject: "Khung giờ trống sáng", type: "free" }],
                    "T4": [{ time: "19:00 - 21:00", subject: "Khung giờ trống tối", type: "free" }],
                    "T5": [{ time: "14:00 - 16:00", subject: "Khung giờ trống chiều", type: "free" }],
                    "T6": [{ time: "19:00 - 21:00", subject: "Khung giờ trống tối", type: "free" }],
                    "T7": [{ time: "14:00 - 16:00", subject: "Khung giờ trống thứ 7", type: "free" }],
                    "CN": [{ time: "19:30 - 21:30", subject: "Họp nhóm G4", type: "free" }]
                }
            },
            minhchau: {
                name: "MINH CHÂU",
                preferredDest: "UIH",
                seat: "05A",
                tasks: [
                    { id: 401, title: "Chuẩn bị Demo tính năng Chatbot & Voice AI", hoursLeft: 12, importance: 5, duration: 35, slot: "18:30 - 19:05", done: false },
                    { id: 402, title: "Làm bài tập nhóm môn Chuyên ngành", hoursLeft: 40, importance: 4, duration: 35, slot: "20:00 - 20:35", done: false }
                ],
                timetable: {
                    "T2": [
                        { time: "07:30 - 11:00", subject: "Học trên trường ca sáng", type: "busy" },
                        { time: "18:30 - 21:00", subject: "Khung giờ trống tối - Học bài", type: "free" }
                    ],
                    "T3": [{ time: "14:00 - 16:30", subject: "Khung giờ trống chiều", type: "free" }],
                    "T4": [{ time: "19:00 - 21:00", subject: "Khung giờ trống tối", type: "free" }],
                    "T5": [{ time: "15:00 - 17:00", subject: "Khung giờ trống chiều", type: "free" }],
                    "T6": [{ time: "19:30 - 21:30", subject: "Khung giờ trống tối", type: "free" }],
                    "T7": [{ time: "09:00 - 11:00", subject: "Khung giờ trống sáng", type: "free" }],
                    "CN": [{ time: "19:30 - 21:30", subject: "Họp nhóm G4", type: "free" }]
                }
            },
            uyennhi: {
                name: "UYÊN NHI",
                preferredDest: "LTH",
                seat: "03C",
                tasks: [
                    { id: 501, title: "Kiểm thử giao diện To-do kéo thả & Báo cáo", hoursLeft: 20, importance: 5, duration: 25, slot: "20:00 - 20:25", done: false },
                    { id: 502, title: "Ôn tập từ vựng tiếng Anh học thuật", hoursLeft: 52, importance: 3, duration: 25, slot: "15:30 - 15:55", done: false }
                ],
                timetable: {
                    "T2": [
                        { time: "08:00 - 11:00", subject: "Lịch học cố định buổi sáng", type: "busy" },
                        { time: "15:00 - 17:00", subject: "Khung giờ trống chiều", type: "free" },
                        { time: "20:00 - 21:30", subject: "Khung giờ trống tối", type: "free" }
                    ],
                    "T3": [{ time: "19:00 - 21:00", subject: "Khung giờ trống tối", type: "free" }],
                    "T4": [{ time: "14:00 - 16:00", subject: "Khung giờ trống chiều", type: "free" }],
                    "T5": [{ time: "19:00 - 21:00", subject: "Khung giờ trống tối", type: "free" }],
                    "T6": [{ time: "14:00 - 16:00", subject: "Khung giờ trống chiều", type: "free" }],
                    "T7": [{ time: "09:00 - 11:00", subject: "Khung giờ trống sáng", type: "free" }],
                    "CN": [{ time: "19:30 - 21:30", subject: "Họp nhóm G4", type: "free" }]
                }
            },
            vanhoang: {
                name: "VĂN HOÀNG",
                preferredDest: "DLI",
                seat: "07F",
                tasks: [
                    { id: 601, title: "Tổng hợp số liệu & Kiểm tra logic nhắc Deadline", hoursLeft: 15, importance: 5, duration: 35, slot: "19:30 - 20:05", done: false },
                    { id: 602, title: "Luyện đề trắc nghiệm môn cơ sở ngành", hoursLeft: 45, importance: 4, duration: 35, slot: "14:00 - 14:35", done: false }
                ],
                timetable: {
                    "T2": [
                        { time: "13:00 - 16:30", subject: "Lịch học thực hành chiều", type: "busy" },
                        { time: "19:30 - 22:00", subject: "Khung giờ trống tối - Tự học", type: "free" }
                    ],
                    "T3": [{ time: "08:30 - 11:00", subject: "Khung giờ trống sáng", type: "free" }],
                    "T4": [{ time: "19:00 - 21:30", subject: "Khung giờ trống tối", type: "free" }],
                    "T5": [{ time: "14:00 - 16:30", subject: "Khung giờ trống chiều", type: "free" }],
                    "T6": [{ time: "19:00 - 21:00", subject: "Khung giờ trống tối", type: "free" }],
                    "T7": [{ time: "09:00 - 11:00", subject: "Khung giờ trống sáng", type: "free" }],
                    "CN": [{ time: "19:30 - 21:30", subject: "Họp nhóm G4", type: "free" }]
                }
            }
        };

        // Load dữ liệu từ LocalStorage hoặc khởi tạo mặc định
        let membersDB = DEFAULT_MEMBERS_DB;
        try {
            const saved = localStorage.getItem('focus_flight_g4_db_v1');
            if (saved) membersDB = JSON.parse(saved);
        } catch (e) {}

        function saveDB() {
            try { localStorage.setItem('focus_flight_g4_db_v1', JSON.stringify(membersDB)); } catch (e) {}
        }

        let currentMemberKey = "quangminh";
        let originAirport = AIRPORTS[0]; // SGN
        let destAirport = AIRPORTS[1];   // DAD
        let selectedDuration = 35;
        let currentDistance = 610;
        let selectedAircraft = "Airbus A321neo";
        let selectedSeat = "06A";
        let selectedFocus = FOCUS_MODES[1];
        let passengerName = "QUANG MINH";

        let isFlying = false, strictModeEnabled = true, isPausedByViolation = false, violationCount = 0;
        const MAX_VIOLATIONS = 3;
        let alarmInterval = null, flightInterval = null;
        let remainingSeconds = 35 * 60, totalFlightSeconds = 35 * 60;

        // ================= 3. BẢN ĐỒ VỆ TINH LEAFLET =================
        const map = L.map('map', { zoomControl: false }).setView([13.0, 108.0], 6);
        L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}', { maxZoom: 18 }).addTo(map);
        L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/Reference/World_Boundaries_and_Places/MapServer/tile/{z}/{y}/{x}', { maxZoom: 18 }).addTo(map);

        let routeLine = null, originMarker = null, destMarker = null, planeMarker = null;

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

        // ================= 4. CHUYỂN ĐỔI HỒ SƠ 6 THÀNH VIÊN & CÁC TAB =================
        function switchMainTab(tab) {
            const btnFlight = document.getElementById('tab-btn-flight');
            const btnPlanner = document.getElementById('tab-btn-planner');
            const plannerScreen = document.getElementById('screen-planner');

            if (tab === 'planner') {
                plannerScreen.classList.remove('hidden');
                plannerScreen.classList.add('flex');
                btnPlanner.className = "px-3.5 py-2 rounded-xl text-xs font-extrabold bg-gradient-to-r from-blue-600 to-cyan-500 text-white shadow transition flex items-center gap-1.5 relative";
                btnFlight.className = "px-3.5 py-2 rounded-xl text-xs font-extrabold text-slate-300 hover:text-white transition flex items-center gap-1.5";
                renderPlannerDashboard();
            } else {
                plannerScreen.classList.add('hidden');
                plannerScreen.classList.remove('flex');
                btnFlight.className = "px-3.5 py-2 rounded-xl text-xs font-extrabold bg-gradient-to-r from-blue-600 to-cyan-500 text-white shadow transition flex items-center gap-1.5";
                btnPlanner.className = "px-3.5 py-2 rounded-xl text-xs font-extrabold text-slate-300 hover:text-white transition flex items-center gap-1.5 relative";
            }
        }

        function switchMemberProfile() {
            currentMemberKey = document.getElementById('member-select').value;
            const profile = membersDB[currentMemberKey];
            passengerName = profile.name;
            selectedSeat = profile.seat || "06A";
            document.getElementById('passenger-name-input').value = passengerName;
            document.getElementById('bot-greet-name').innerText = passengerName;

            // Đổi sân bay đích về đúng quê hương của thành viên đó
            const prefAirport = AIRPORTS.find(a => a.code === profile.preferredDest);
            if (prefAirport) {
                destAirport = prefAirport;
                document.getElementById('dest-select').value = destAirport.code;
                onRouteChange();
            }

            renderPlannerDashboard();
            checkUrgentDeadlinesBanner();
        }

        // Tính điểm ưu tiên AI (Importance * 22 + Độ gấp của Deadline)
        function calcPriorityScore(task) {
            const urgency = Math.max(5, 100 - task.hoursLeft * 1.4);
            return Math.round(task.importance * 18 + urgency * 0.6);
        }

        function checkUrgentDeadlinesBanner() {
            const profile = membersDB[currentMemberKey];
            const urgentTasks = profile.tasks.filter(t => !t.done && t.hoursLeft <= 24);
            document.getElementById('urgent-count-badge').innerText = urgentTasks.length;

            const toast = document.getElementById('deadline-toast');
            if (urgentTasks.length > 0) {
                toast.classList.remove('hidden');
                document.getElementById('deadline-toast-text').innerText = 
                    `${profile.name} ơi! Nhiệm vụ "${urgentTasks[0].title}" chỉ còn ${urgentTasks[0].hoursLeft} giờ nữa là tới hạn!`;
            }
        }

        // ================= 5. RENDER BẢNG KẾ HOẠCH AI, KÉO THẢ & THỜI KHÓA BIỂU =================
        function renderPlannerDashboard() {
            const profile = membersDB[currentMemberKey];
            document.getElementById('today-member-tag').innerText = `Hồ sơ: ${profile.name}`;
            document.getElementById('timetable-owner-badge').innerText = `(${profile.name})`;

            // 1. Tìm công việc ưu tiên số 1 cho mục "Hôm nay nên học gì?"
            const activeTasks = profile.tasks.filter(t => !t.done);
            const sorted = [...activeTasks].sort((a, b) => calcPriorityScore(b) - calcPriorityScore(a));
            const topTask = sorted[0];

            const recBox = document.getElementById('today-recommendation-box');
            if (topTask) {
                const freeSlots = (profile.timetable[selectedDay] || []).filter(s => s.type === 'free');
                const matchedSlot = freeSlots.length > 0 ? freeSlots[0].time : topTask.slot;
                recBox.innerHTML = `
                    <div>
                        <div class="flex items-center gap-2 mb-1">
                            <span class="bg-red-500 text-white text-[10px] font-black px-2 py-0.5 rounded">ƯU TIÊN #1 • ĐIỂM AI: ${calcPriorityScore(topTask)}</span>
                            <span class="text-xs text-amber-300 font-bold">⏰ Còn ${topTask.hoursLeft} giờ tới hạn</span>
                        </div>
                        <div class="text-sm sm:text-base font-extrabold text-white">${topTask.title}</div>
                        <div class="text-xs text-cyan-300 mt-1">
                            🕒 Khung giờ trống đề xuất: <b>${matchedSlot}</b> • Thời lượng bay: <b>${topTask.duration} phút</b>
                        </div>
                    </div>
                    <div class="flex sm:flex-col gap-2 shrink-0">
                        <button onclick="startFlightFromTask(${topTask.id})" class="bg-gradient-to-r from-emerald-500 to-cyan-500 hover:opacity-95 text-black font-black px-4 py-2.5 rounded-xl text-xs shadow-lg whitespace-nowrap">
                            🛫 Bay ngay (${topTask.duration}p)
                        </button>
                        <button onclick="openWhyModal(${topTask.id})" class="bg-white/10 hover:bg-white/20 text-white font-bold px-3 py-1.5 rounded-xl text-[11px] whitespace-nowrap">
                            ❓ Tại sao có lịch này?
                        </button>
                    </div>
                `;
            } else {
                recBox.innerHTML = `<div class="text-xs text-emerald-300 font-bold">🎉 Tuyệt vời! ${profile.name} đã hoàn thành toàn bộ nhiệm vụ hôm nay!</div>`;
            }

            // 2. Render danh sách To-do kéo thả (Drag and Drop)
            const listEl = document.getElementById('todo-drag-list');
            listEl.innerHTML = '';
            profile.tasks.forEach((task, idx) => {
                const score = calcPriorityScore(task);
                const isUrgent = task.hoursLeft <= 20;
                const item = document.createElement('div');
                item.draggable = true;
                item.dataset.index = idx;
                item.className = `p-3.5 rounded-2xl border transition cursor-grab active:cursor-grabbing flex flex-col sm:flex-row sm:items-center justify-between gap-3 ${
                    task.done ? 'bg-slate-900/40 border-white/5 opacity-55' : (isUrgent ? 'bg-slate-900/95 border-red-400/40 shadow-md' : 'bg-slate-900/85 border-white/10 hover:border-cyan-400/40')
                }`;

                // Sự kiện kéo thả HTML5
                item.addEventListener('dragstart', handleDragStart);
                item.addEventListener('dragover', handleDragOver);
                item.addEventListener('drop', handleDrop);
                item.addEventListener('dragend', handleDragEnd);

                item.innerHTML = `
                    <div class="flex items-start gap-3">
                        <input type="checkbox" ${task.done ? 'checked' : ''} onchange="toggleTaskDone(${task.id})" class="mt-1 w-4 h-4 accent-emerald-400 cursor-pointer" />
                        <div>
                            <div class="flex flex-wrap items-center gap-1.5 mb-1">
                                <span class="text-[10px] font-black px-2 py-0.5 rounded ${isUrgent ? 'bg-red-500/25 text-red-300 border border-red-400/30' : 'bg-blue-500/20 text-blue-300'}">
                                    ⏳ Hạn: ${task.hoursLeft}h
                                </span>
                                <span class="text-[10px] font-bold text-amber-300">${'⭐'.repeat(task.importance)}</span>
                                <span class="text-[10px] font-mono bg-white/10 text-cyan-300 px-2 py-0.5 rounded">Ca: ${task.slot}</span>
                                <span class="text-[10px] font-mono text-slate-400">Điểm AI: ${score}</span>
                            </div>
                            <div class="text-xs sm:text-sm font-extrabold ${task.done ? 'line-through text-slate-500' : 'text-white'}">${task.title}</div>
                        </div>
                    </div>
                    <div class="flex items-center gap-1.5 shrink-0 self-end sm:self-center">
                        <button onclick="openWhyModal(${task.id})" class="bg-slate-800 hover:bg-slate-700 text-cyan-300 border border-cyan-500/30 px-2.5 py-1.5 rounded-xl text-[11px] font-bold" title="Giải thích lý do sắp xếp">
                            ❓ Tại sao?
                        </button>
                        <button onclick="startFlightFromTask(${task.id})" class="bg-blue-600 hover:bg-blue-500 text-white px-3 py-1.5 rounded-xl text-[11px] font-extrabold shadow">
                            ✈️ ${task.duration}p
                        </button>
                        <button onclick="deleteTask(${task.id})" class="text-slate-500 hover:text-red-400 px-1.5 text-xs font-bold">✕</button>
                    </div>
                `;
                listEl.appendChild(item);
            });

            // 3. Render Thứ trong tuần & Thời khóa biểu cá nhân
            const dayTabs = document.getElementById('day-tabs-container');
            dayTabs.innerHTML = '';
            DAYS_OF_WEEK.forEach(d => {
                const active = d === selectedDay;
                const btn = document.createElement('button');
                btn.className = `py-1.5 rounded-xl text-xs font-extrabold transition border ${
                    active ? 'bg-amber-400 text-black border-amber-300 shadow' : 'bg-slate-900 text-slate-400 border-white/5 hover:text-white'
                }`;
                btn.innerText = d;
                btn.onclick = () => { selectedDay = d; renderPlannerDashboard(); };
                dayTabs.appendChild(btn);
            });

            const slotsList = document.getElementById('timetable-slots-list');
            slotsList.innerHTML = '';
            const daySlots = profile.timetable[selectedDay] || [];
            if (daySlots.length === 0) {
                slotsList.innerHTML = `<div class="text-xs text-slate-400 p-4 text-center bg-slate-900/50 rounded-2xl">Chưa có ca học nào trong ngày ${selectedDay}. Bấm "+ Thêm Ca Học" để cá nhân hóa!</div>`;
            } else {
                daySlots.forEach((s, sIdx) => {
                    const isFree = s.type === 'free';
                    const el = document.createElement('div');
                    el.className = `p-3 rounded-2xl border flex items-center justify-between gap-2 ${
                        isFree ? 'bg-emerald-950/35 border-emerald-400/30' : 'bg-slate-900/90 border-white/10'
                    }`;
                    el.innerHTML = `
                        <div>
                            <div class="flex items-center gap-2">
                                <span class="text-[10px] font-mono font-extrabold px-2 py-0.5 rounded ${isFree ? 'bg-emerald-400 text-black' : 'bg-slate-700 text-slate-200'}">
                                    ${s.time}
                                </span>
                                <span class="text-[10px] font-bold ${isFree ? 'text-emerald-300' : 'text-red-300'}">
                                    ${isFree ? '🟢 Giờ trống (Khuyên bay)' : '🔴 Bận học cố định'}
                                </span>
                            </div>
                            <div class="text-xs font-bold text-white mt-1">${s.subject}</div>
                        </div>
                        <button onclick="removeTimetableSlot(${sIdx})" class="text-slate-500 hover:text-red-400 text-xs font-bold px-2">✕</button>
                    `;
                    slotsList.appendChild(el);
                });
            }
        }

        // Xử lý Kéo Thả (Drag & Drop) To-do List
        let dragStartIndex = null;
        function handleDragStart(e) {
            dragStartIndex = +this.dataset.index;
            this.classList.add('dragging-card');
        }
        function handleDragOver(e) { e.preventDefault(); }
        function handleDrop(e) {
            const dragEndIndex = +this.dataset.index;
            if (dragStartIndex === null || dragStartIndex === dragEndIndex) return;
            const tasks = membersDB[currentMemberKey].tasks;
            const [movedItem] = tasks.splice(dragStartIndex, 1);
            tasks.splice(dragEndIndex, 0, movedItem);
            saveDB();
            renderPlannerDashboard();
        }
        function handleDragEnd() { this.classList.remove('dragging-card'); }

        // Thuật toán AI tự động sắp xếp thứ tự ưu tiên (Count: 5)
        function aiSortTasks() {
            const profile = membersDB[currentMemberKey];
            profile.tasks.sort((a, b) => calcPriorityScore(b) - calcPriorityScore(a));
            saveDB();
            renderPlannerDashboard();
            alert(`🤖 AI đã sắp xếp lại danh sách của ${profile.name} dựa trên Độ quan trọng và Thời gian còn lại tới Deadline!`);
        }

        // Báo lịch đột xuất -> Tự động dời các task sang khung giờ trống kế tiếp (Count: 4)
        function handleSuddenScheduleChange() {
            const profile = membersDB[currentMemberKey];
            const backupSlots = ["20:30 - 21:15 (Ca tối dự phòng)", "21:30 - 22:05 (Ca khuya linh hoạt)", "08:00 - 08:45 (Sáng mai)"];
            profile.tasks.forEach((t, i) => {
                if (!t.done) t.slot = backupSlots[i % backupSlots.length];
            });
            saveDB();
            renderPlannerDashboard();
            alert(`🌪️ Đã cập nhật lịch đột xuất! AI đã tự động dời các nhiệm vụ chưa xong của ${profile.name} sang khung giờ trống dự phòng.`);
        }

        // Giải thích "Tại sao lại có lịch này?" (Count: 4)
        function openWhyModal(taskId) {
            const profile = membersDB[currentMemberKey];
            const task = profile.tasks.find(t => t.id === taskId);
            if (!task) return;
            const score = calcPriorityScore(task);
            const freeSlots = (profile.timetable[selectedDay] || []).filter(s => s.type === 'free');
            const freeText = freeSlots.length > 0 ? freeSlots.map(s => s.time).join(', ') : '19:30 - 21:30';

            document.getElementById('why-modal-content').innerHTML = `
                <div class="bg-slate-900/90 p-3.5 rounded-2xl border border-white/10">
                    <div class="text-[10px] text-cyan-400 font-bold uppercase">Nhiệm vụ đang phân tích</div>
                    <div class="text-sm font-extrabold text-white mt-0.5">${task.title}</div>
                    <div class="text-xs text-amber-300 font-mono mt-1">Tổng điểm ưu tiên AI: <b>${score} / 150 điểm</b></div>
                </div>
                <div class="space-y-2.5">
                    <div class="bg-red-500/15 border border-red-400/30 p-3 rounded-2xl">
                        <div class="font-extrabold text-red-300">1. ⏳ Yếu tố Thời hạn (Deadline): Còn ${task.hoursLeft} giờ</div>
                        <div class="text-[11px] text-slate-300 mt-0.5">
                            ${task.hoursLeft <= 24 ? 'Thời hạn dưới 24 giờ nên hệ thống đẩy lên mức Cấp bách để tránh trễ hạn.' : 'Thời hạn còn dư dả nhưng cần chia nhỏ vào chuyến bay hôm nay để giảm tải.'}
                        </div>
                    </div>
                    <div class="bg-amber-500/15 border border-amber-400/30 p-3 rounded-2xl">
                        <div class="font-extrabold text-amber-300">2. ⭐ Mức độ Quan trọng: ${task.importance}/5 Sao</div>
                        <div class="text-[11px] text-slate-300 mt-0.5">
                            Trọng số môn học/dự án này đóng góp ${task.importance * 18} điểm vào thuật toán sắp xếp lịch.
                        </div>
                    </div>
                    <div class="bg-emerald-500/15 border border-emerald-400/30 p-3 rounded-2xl">
                        <div class="font-extrabold text-emerald-300">3. 🕒 Khớp Thời gian trống của ${profile.name}:</div>
                        <div class="text-[11px] text-slate-300 mt-0.5">
                            Dựa trên Thời khóa biểu ngày <b>${selectedDay}</b> của ${profile.name}, bạn đang rảnh vào khung <b>${freeText}</b> nên AI xếp chuyến bay <b>${task.duration} phút</b> vào ca <b>${task.slot}</b>.
                        </div>
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

        function startFlightFromTask(taskId) {
            const profile = membersDB[currentMemberKey];
            const task = profile.tasks.find(t => t.id === taskId);
            if (!task) return;

            selectedDuration = task.duration;
            setDuration(task.duration);
            selectedFocus = { id: 'custom', label: task.title, icon: '🎯', color: 'bg-cyan-600 border-cyan-300 text-white' };
            passengerName = profile.name;

            switchMainTab('flight');
            goToSeatSelection();
        }

        function toggleTaskDone(taskId) {
            const profile = membersDB[currentMemberKey];
            const task = profile.tasks.find(t => t.id === taskId);
            if (task) task.done = !task.done;
            saveDB();
            renderPlannerDashboard();
            checkUrgentDeadlinesBanner();
        }

        function deleteTask(taskId) {
            const profile = membersDB[currentMemberKey];
            profile.tasks = profile.tasks.filter(t => t.id !== taskId);
            saveDB();
            renderPlannerDashboard();
            checkUrgentDeadlinesBanner();
        }

        function openAddTaskModal() {
            document.getElementById('add-task-modal').classList.remove('hidden');
            document.getElementById('add-task-modal').classList.add('flex');
        }
        function closeAddTaskModal() {
            document.getElementById('add-task-modal').classList.add('hidden');
            document.getElementById('add-task-modal').classList.remove('flex');
        }
        function saveNewTask() {
            const title = document.getElementById('new-task-title').value.trim();
            if (!title) return;
            const hours = parseInt(document.getElementById('new-task-hours').value) || 24;
            const imp = parseInt(document.getElementById('new-task-importance').value) || 4;
            const dur = parseInt(document.getElementById('new-task-duration').value) || 35;
            const slot = document.getElementById('new-task-slot').value.trim() || "19:30 - 20:05";

            membersDB[currentMemberKey].tasks.unshift({
                id: Date.now(), title, hoursLeft: hours, importance: imp, duration: dur, slot, done: false
            });
            saveDB();
            document.getElementById('new-task-title').value = '';
            closeAddTaskModal();
            renderPlannerDashboard();
            checkUrgentDeadlinesBanner();
        }

        function openAddSlotModal() {
            document.getElementById('add-slot-modal').classList.remove('hidden');
            document.getElementById('add-slot-modal').classList.add('flex');
        }
        function closeAddSlotModal() {
            document.getElementById('add-slot-modal').classList.add('hidden');
            document.getElementById('add-slot-modal').classList.remove('flex');
        }
        function saveNewTimetableSlot() {
            const time = document.getElementById('new-slot-time').value.trim() || "14:00 - 16:00";
            const subject = document.getElementById('new-slot-subject').value.trim() || "Khung giờ tự học";
            const type = document.getElementById('new-slot-type').value;
            if (!membersDB[currentMemberKey].timetable[selectedDay]) {
                membersDB[currentMemberKey].timetable[selectedDay] = [];
            }
            membersDB[currentMemberKey].timetable[selectedDay].push({ time, subject, type });
            saveDB();
            closeAddSlotModal();
            renderPlannerDashboard();
        }
        function removeTimetableSlot(idx) {
            membersDB[currentMemberKey].timetable[selectedDay].splice(idx, 1);
            saveDB();
            renderPlannerDashboard();
        }

        function triggerDesktopNotification() {
            const profile = membersDB[currentMemberKey];
            const top = profile.tasks.find(t => !t.done);
            const msg = top ? `🔔 Nhắc học (${profile.name}): Hôm nay bạn nên hoàn thành "${top.title}" (${top.duration} phút - Ca ${top.slot})!` : `🎉 Bạn đã hoàn thành hết lịch học hôm nay!`;
            alert(msg);
        }

        // ================= 6. CHATBOT AI SAMI VÀNG KIM (GIỐNG ẢNH MẪU) =================
        function toggleChatbotWindow() {
            const win = document.getElementById('chatbot-window');
            if (win.classList.contains('hidden')) {
                win.classList.remove('hidden');
                win.classList.add('flex');
            } else {
                win.classList.add('hidden');
                win.classList.remove('flex');
            }
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
            const timeStr = getCurrentTimeStr();

            // Render tin nhắn người dùng màu vàng đồng bên phải
            box.innerHTML += `
                <div class="flex flex-col items-end">
                    <div class="bg-[#d4a349] text-white font-semibold text-xs px-4 py-2.5 rounded-2xl rounded-tr-sm shadow-sm max-w-[80%]">
                        ${text}
                    </div>
                    <span class="text-[10px] text-slate-400 mt-1">${timeStr}</span>
                </div>
            `;
            box.scrollTop = box.scrollHeight;

            // Xử lý câu trả lời thông minh theo đúng hồ sơ thành viên đang chọn
            setTimeout(() => {
                const reply = generateSmartBotReply(text);
                const botAvatar = document.getElementById('bot-launcher-img').src;
                box.innerHTML += `
                    <div class="flex items-start gap-2">
                        <img src="${botAvatar}" class="w-8 h-8 rounded-full bg-amber-400 p-0.5 border border-[#d4a349] shrink-0 mt-1 object-cover" />
                        <div class="max-w-[82%]">
                            <div class="bg-[#fae5be] p-1.5 rounded-2xl rounded-tl-sm shadow-sm">
                                <div class="bg-white rounded-xl p-3 text-xs text-slate-800 leading-relaxed">
                                    ${reply}
                                </div>
                            </div>
                            <span class="text-[10px] text-slate-400 mt-1 block">${getCurrentTimeStr()}</span>
                        </div>
                    </div>
                `;
                box.scrollTop = box.scrollHeight;
            }, 350);
        }

        function generateSmartBotReply(q) {
            const lower = q.toLowerCase();
            const profile = membersDB[currentMemberKey];
            const activeTasks = profile.tasks.filter(t => !t.done).sort((a,b) => calcPriorityScore(b) - calcPriorityScore(a));
            const topTask = activeTasks[0];

            if (lower.includes('hôm nay') || lower.includes('học gì')) {
                if (!topTask) return `Chào <b>${profile.name}</b>! Hôm nay bạn đã hoàn thành sạch sẽ các nhiệm vụ rồi 🎉 Bạn có thể đặt một chuyến bay thư giãn đọc sách nhé!`;
                return `Chào <b>${profile.name}</b>! 🙋‍♀️ Dựa vào Thời khóa biểu của bạn, hôm nay bạn nên ưu tiên số 1 cho:<br>• <b>${topTask.title}</b><br>• Thời lượng bay: <b>${topTask.duration} phút</b> (Ca ${topTask.slot}).<br>Bấm vào tab <b>📅 Lịch Học AI</b> để cất cánh ngay nha!`;
            }
            if (lower.includes('deadline') || lower.includes('hạn') || lower.includes('gấp')) {
                const urg = activeTasks.filter(t => t.hoursLeft <= 24);
                if (urg.length === 0) return `Hiện tại <b>${profile.name}</b> không có deadline nào quá gấp dưới 24h. Bạn đang kiểm soát tiến độ rất tốt!`;
                return `⚠️ Cảnh báo cho <b>${profile.name}</b>: Bạn có <b>${urg.length} nhiệm vụ</b> sắp tới hạn dưới 24h:<br>` + urg.map(u => `• <b>${u.title}</b> (còn ${u.hoursLeft}h)`).join('<br>');
            }
            if (lower.includes('tại sao') || lower.includes('giải thích')) {
                if (!topTask) return `Lịch học được AI tính toán từ 3 yếu tố: Thời hạn (Deadline), Độ quan trọng (1-5 sao) và Khung giờ trống trong Thời khóa biểu cá nhân của từng thành viên nhóm G4.`;
                return `🧠 <b>Giải thích lịch của ${profile.name}:</b><br>Sami xếp <b>"${topTask.title}"</b> lên đầu vì:<br>1. Còn <b>${topTask.hoursLeft} giờ</b> tới hạn.<br>2. Độ quan trọng: <b>${topTask.importance}/5 sao</b>.<br>3. Khớp với khung giờ trống <b>${topTask.slot}</b> của bạn!`;
            }
            if (lower.includes('đột xuất') || lower.includes('dời lịch') || lower.includes('bận')) {
                handleSuddenScheduleChange();
                return `🌪️ Sami đã tự động dời các nhiệm vụ hôm nay của <b>${profile.name}</b> sang khung giờ trống dự phòng buổi tối rồi nhé! Bạn cứ yên tâm giải quyết việc đột xuất nha.`;
            }
            return `Cảm ơn <b>${profile.name}</b> đã nhắn cho Sami! 🤖<br>Hiện bạn đang có <b>${activeTasks.length} nhiệm vụ</b> trong danh sách và chặng bay yêu thích là <b>SGN ➔ ${profile.preferredDest}</b>. Bạn có thể hỏi mình về <i>"Hôm nay học gì?"</i>, <i>"Deadline gấp"</i> hoặc <i>"Dời lịch đột xuất"</i> nhé!`;
        }

        function resetChat() {
            const profile = membersDB[currentMemberKey];
            const botAvatar = document.getElementById('bot-launcher-img').src;
            document.getElementById('chat-messages').innerHTML = `
                <div class="flex flex-col items-end">
                    <div class="bg-[#d4a349] text-white font-semibold text-xs px-5 py-2.5 rounded-2xl rounded-tr-sm shadow-sm">Bắt đầu</div>
                    <span class="text-[10px] text-slate-400 mt-1">${getCurrentTimeStr()}</span>
                </div>
                <div class="flex items-start gap-2">
                    <img src="${botAvatar}" class="w-8 h-8 rounded-full bg-amber-400 p-0.5 border border-[#d4a349] shrink-0 mt-1 object-cover" />
                    <div>
                        <div class="bg-[#fae5be] p-1.5 rounded-2xl rounded-tl-sm shadow-sm">
                            <div class="bg-white rounded-xl p-3 text-xs text-slate-800 leading-relaxed">
                                Xin chào, 🙋‍♀️<br>Mình là <b>Sami</b> trợ lý AI của <b>FOCUS FLIGHT G4</b>.<br>Hôm nay Mình có thể giúp gì được cho <b>${profile.name}</b>?
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
                const msgImg = document.getElementById('bot-msg-img');
                if (msgImg) msgImg.src = url;
            }
        }

        // ================= 7. LOGIC ĐẶT VÉ, CHỌN GHẾ & BAY STRICT MODE =================
        function initDropdowns() {
            const oSel = document.getElementById('origin-select');
            const dSel = document.getElementById('dest-select');
            oSel.innerHTML = ''; dSel.innerHTML = '';
            AIRPORTS.forEach(a => {
                oSel.innerHTML += `<option value="${a.code}" class="bg-slate-900">${a.code} - ${a.name}</option>`;
                dSel.innerHTML += `<option value="${a.code}" class="bg-slate-900">${a.code} - ${a.name}</option>`;
            });
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
            document.getElementById('top-aircraft-tag').innerText = selectedAircraft;
        }

        function setDuration(mins) {
            selectedDuration = mins;
            document.querySelectorAll('.dur-btn').forEach(b => {
                b.className = "dur-btn bg-slate-800 py-2 rounded-xl text-xs font-bold text-slate-300 border border-transparent";
            });
            const activeBtn = document.getElementById('dur-' + mins);
            if (activeBtn) activeBtn.className = "dur-btn bg-blue-600/30 border-blue-400 text-blue-300 py-2 rounded-xl text-xs font-bold border";
        }

        function updateBookingUI() {
            document.getElementById('dest-banner-img').src = destAirport.img;
            document.getElementById('badge-origin').innerText = `✈️ ${originAirport.code}`;
            document.getElementById('badge-dest').innerText = `✈️ ${destAirport.code}`;
            document.getElementById('badge-dist').innerText = `${currentDistance} km`;
            document.getElementById('banner-region-tag').innerText = destAirport.region;
            document.getElementById('banner-dest-title').innerText = `${originAirport.code} ➔ ${destAirport.name}`;

            if (routeLine) map.removeLayer(routeLine);
            if (originMarker) map.removeLayer(originMarker);
            if (destMarker) map.removeLayer(destMarker);

            originMarker = L.marker(originAirport.coords, { icon: createAirportBadge(originAirport.code, false) }).addTo(map);
            destMarker = L.marker(destAirport.coords, { icon: createAirportBadge(destAirport.code, true) }).addTo(map);

            routeLine = L.polyline([originAirport.coords, destAirport.coords], {
                color: '#38bdf8', weight: 3.5, dashArray: '8, 8', opacity: 0.95
            }).addTo(map);

            map.fitBounds(routeLine.getBounds(), { padding: [90, 90] });
        }

        function renderSeats() {
            const grid = document.getElementById('seat-grid');
            grid.innerHTML = '';
            const cols = ['A', 'C', '', 'D', 'F'];

            for (let r = 1; r <= 12; r++) {
                const rowNum = r < 10 ? '0' + r : '' + r;
                const rowEl = document.createElement('div');
                rowEl.className = 'grid grid-cols-5 gap-2.5 items-center w-full';

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

                        btn.className = `seat-box h-11 rounded-xl font-bold text-xs flex items-center justify-center border ${style}`;
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
                pill.className = `px-4 py-2.5 rounded-full text-xs font-bold flex items-center gap-2 border transition ${
                    active ? mode.color + ' scale-105 shadow-md' : 'bg-slate-800/80 border-white/10 text-slate-300 hover:bg-slate-700'
                }`;
                pill.innerHTML = `<span>${mode.icon}</span><span>${mode.label}</span>`;
                pill.onclick = () => {
                    selectedFocus = mode;
                    document.getElementById('custom-focus-box').classList.add('hidden');
                    renderFocusPills();
                    renderSeats();
                };
                container.appendChild(pill);
            });

            const plusBtn = document.createElement('button');
            plusBtn.className = `w-9 h-9 rounded-full bg-slate-800/90 hover:bg-slate-700 border border-white/15 text-white font-bold text-base flex items-center justify-center`;
            plusBtn.innerText = '+';
            plusBtn.onclick = () => document.getElementById('custom-focus-box').classList.toggle('hidden');
            container.appendChild(plusBtn);
        }

        function openFocusPopover(seatCode) {
            selectedSeat = seatCode;
            membersDB[currentMemberKey].seat = seatCode;
            saveDB();
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
            if (customVal) selectedFocus = { id: 'custom', label: customVal, icon: '✨', color: 'bg-cyan-600 border-cyan-300 text-white' };
            const pName = document.getElementById('passenger-name-input').value.trim();
            if (pName) passengerName = pName;
            strictModeEnabled = document.getElementById('strict-mode-toggle').checked;

            closeFocusPopover();
            renderSeats();
            showBoardingPass();
        }

        function goToSeatSelection() {
            document.getElementById('seat-header-aircraft').innerText = selectedAircraft;
            document.getElementById('seat-header-route').innerText = `${originAirport.code} ➔ ${destAirport.code} • ${selectedDuration}m`;
            document.getElementById('screen-booking').classList.add('hidden');
            document.getElementById('screen-seat').classList.remove('hidden');
            document.getElementById('screen-seat').classList.add('flex');
            renderSeats();
        }

        function backToBooking() {
            document.getElementById('screen-seat').classList.add('hidden');
            document.getElementById('screen-seat').classList.remove('flex');
            document.getElementById('screen-booking').classList.remove('hidden');
        }

        function showBoardingPass() {
            strictModeEnabled = document.getElementById('strict-mode-toggle').checked;
            document.getElementById('screen-seat').classList.add('hidden');
            document.getElementById('screen-seat').classList.remove('flex');

            document.getElementById('tk-aircraft').innerText = selectedAircraft;
            document.getElementById('tk-passenger').innerText = passengerName;
            document.getElementById('tk-strict-badge').innerText = strictModeEnabled ? "🔒 STRICT LOCK ON" : "🔓 FREE MODE";
            document.getElementById('tk-Origin-code');
            document.getElementById('tk-origin-code').innerText = originAirport.code;
            document.getElementById('tk-origin-name').innerText = originAirport.name.split(' (')[0];
            document.getElementById('tk-dest-code').innerText = destAirport.code;
            document.getElementById('tk-dest-name').innerText = destAirport.name.split(' (')[0];
            document.getElementById('tk-duration').innerText = selectedDuration + 'm';
            document.getElementById('tk-seat').innerText = selectedSeat;
            document.getElementById('tk-dist').innerText = currentDistance + ' km';
            document.getElementById('tk-focus').innerText = `${selectedFocus.icon} ${selectedFocus.label}`;

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
            else if (elem.webkitRequestFullscreen) elem.webkitRequestFullscreen();
        }

        function startFlight() {
            document.getElementById('screen-ticket').classList.add('hidden');
            document.getElementById('screen-ticket').classList.remove('flex');
            document.getElementById('screen-flying').classList.remove('hidden');

            if (strictModeEnabled) requestAppFullscreen();

            const player = document.getElementById('lofi-player');
            if (player.paused) toggleLofi();

            isFlying = true;
            isPausedByViolation = false;
            violationCount = 0;
            updateSafetyHearts();

            document.getElementById('strict-live-pill').style.display = strictModeEnabled ? 'inline-block' : 'none';
            document.getElementById('fly-badge').innerText = destAirport.code;
            document.getElementById('fly-route-text').innerText = `${originAirport.name.split(' (')[0]} ➔ ${destAirport.name.split(' (')[0]}`;
            document.getElementById('fly-sub-info').innerText = `${selectedFocus.icon} ${selectedFocus.label} • Ghế ${selectedSeat} • ${passengerName}`;

            totalFlightSeconds = selectedDuration * 60;
            remainingSeconds = totalFlightSeconds;

            const planeIcon = L.divIcon({
                className: 'plane-icon',
                html: `<div class="w-10 h-10 rounded-full bg-yellow-400 text-black flex items-center justify-center shadow-2xl border-2 border-white text-xl">✈️</div>`,
                iconSize: [40, 40],
                iconAnchor: [20, 20]
            });

            if (planeMarker) map.removeLayer(planeMarker);
            planeMarker = L.marker(originAirport.coords, { icon: planeIcon, zIndexOffset: 1000 }).addTo(map);
            map.flyTo(originAirport.coords, 12, { duration: 2 });

            updateFlightTick();
            if (flightInterval) clearInterval(flightInterval);
            flightInterval = setInterval(() => {
                if (isPausedByViolation) return;
                remainingSeconds--;
                if (remainingSeconds <= 0) {
                    clearInterval(flightInterval);
                    isFlying = false;
                    alert(`🎉 Chuyến bay ${originAirport.code} ➔ ${destAirport.code} đã hạ cánh an toàn! Chúc mừng ${passengerName} đã hoàn thành phiên học tập!`);
                    abortFlight();
                } else {
                    updateFlightTick();
                }
            }, 1000);
        }

        function updateSafetyHearts() {
            const left = Math.max(0, MAX_VIOLATIONS - violationCount);
            document.getElementById('safety-hearts').innerText = '❤️'.repeat(left) + '🖤'.repeat(MAX_VIOLATIONS - left);
        }

        let audioCtx = null, cabinNoiseNode = null;

        function playCockpitAlarmBeep() {
            try {
                if (!audioCtx) audioCtx = new (window.AudioContext || window.webkitAudioContext)();
                const osc = audioCtx.createOscillator();
                const gain = audioCtx.createGain();
                osc.type = 'sawtooth';
                osc.frequency.setValueAtTime(880, audioCtx.currentTime);
                osc.frequency.setValueAtTime(440, audioCtx.currentTime + 0.18);
                gain.gain.setValueAtTime(0.25, audioCtx.currentTime);
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
        window.addEventListener('blur', () => {
            triggerTurbulenceViolation();
        });

        function updateFlightTick() {
            const mins = Math.floor(remainingSeconds / 60);
            const secs = remainingSeconds % 60;
            document.getElementById('countdown-timer').innerText = `${mins<10?'0'+mins:mins}:${secs<10?'0'+secs:secs}`;

            const progress = (totalFlightSeconds - remainingSeconds) / totalFlightSeconds;
            document.getElementById('flight-progress').style.width = `${progress * 100}%`;

            const distLeft = Math.max(0, Math.round(currentDistance * (1 - progress)));
            document.getElementById('fly-dist-left').innerText = distLeft;

            const lat = originAirport.coords[0] + (destAirport.coords[0] - originAirport.coords[0]) * progress;
            const lng = originAirport.coords[1] + (destAirport.coords[1] - originAirport.coords[1]) * progress;
            if (planeMarker) planeMarker.setLatLng([lat, lng]);
        }

        function centerOnPlane() {
            if (planeMarker) map.flyTo(planeMarker.getLatLng(), 14, { duration: 1.5 });
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
            document.getElementById('screen-flying').classList.add('hidden');
            document.getElementById('screen-booking').classList.remove('hidden');
            updateBookingUI();
        }

        // Âm thanh Lofi & White noise
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
                p.src = url; p.play();
                document.getElementById('eq-icon').classList.remove('hidden');
                document.getElementById('eq-icon').classList.add('flex');
                document.getElementById('lofi-btn-text').innerText = "Nhạc riêng";
            }
        }
        function handleLocalImage(input) {
            if (input.files && input.files[0]) {
                const url = URL.createObjectURL(input.files[0]);
                destAirport.img = url;
                document.getElementById('dest-banner-img').src = url;
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
        initDropdowns();
        switchMemberProfile();
    </script>
</body>
</html>
"""

components.html(app_html, height=940, scrolling=False)
