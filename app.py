import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Focus Flight Pro - Strict Mode",
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
            background: rgba(15, 21, 35, 0.88);
            backdrop-filter: blur(24px);
            -webkit-backdrop-filter: blur(24px);
            border: 1px solid rgba(255, 255, 255, 0.14);
        }

        .focus-popover {
            background: rgba(32, 45, 72, 0.95);
            backdrop-filter: blur(28px);
            -webkit-backdrop-filter: blur(28px);
            border: 1px solid rgba(147, 197, 253, 0.25);
            box-shadow: 0 25px 60px rgba(0, 0, 0, 0.75);
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

        /* Hiệu ứng chớp đỏ báo động khi thoát ra ngoài */
        @keyframes red-alert {
            0%, 100% { background: rgba(153, 27, 27, 0.88); }
            50% { background: rgba(220, 38, 38, 0.96); }
        }
        .turbulence-alert {
            animation: red-alert 0.7s infinite;
            backdrop-filter: blur(16px);
        }

        ::-webkit-scrollbar { width: 5px; }
        ::-webkit-scrollbar-thumb { background: rgba(255,255,255,0.2); border-radius: 10px; }
        .leaflet-control-attribution { display: none !important; }
    </style>
</head>
<body class="relative w-screen h-screen" id="app-root">

    <!-- BẢN ĐỒ VỆ TINH THỰC TẾ -->
    <div id="map"></div>

    <!-- AUDIO LOFI -->
    <audio id="lofi-player" loop crossorigin="anonymous">
        <source id="lofi-source" src="https://cdn.pixabay.com/download/audio/2022/05/27/audio_1808fbf07a.mp3" type="audio/mpeg">
    </audio>

    <!-- ================= MÀN HÌNH CẢNH BÁO ĐỎ KHI NHẢY RA TAB KHÁC (STRICT MODE ALERT) ================= -->
    <div id="turbulence-modal" class="fixed inset-0 z-[999] turbulence-alert hidden flex-col items-center justify-center p-6 text-center">
        <div class="text-6xl mb-3 animate-bounce">🚨</div>
        <div class="bg-black/40 border border-white/30 px-4 py-1 rounded-full text-xs font-mono font-bold uppercase tracking-widest text-yellow-300 mb-2">
            COCKPIT MASTER WARNING • TURBULENCE DETECTED
        </div>
        <h2 class="text-2xl sm:text-3xl font-black text-white uppercase tracking-wide mb-2">
            CẢNH BÁO: BẠN ĐÃ RỜI KHỎI CHUYẾN BAY!
        </h2>
        <p class="text-sm text-red-100 max-w-md mb-5">
            Hệ thống phát hiện bạn vừa chuyển sang Tab/Ứng dụng khác hoặc thoát toàn màn hình. Đồng hồ tập trung đã bị <b>TẠM DỪNG</b>!
        </p>

        <div class="bg-black/50 border border-red-300/30 rounded-2xl p-4 w-full max-w-sm mb-6">
            <div class="text-xs text-red-200 uppercase font-bold mb-1">Số lần vi phạm trong chuyến bay này</div>
            <div id="violation-count-text" class="text-2xl font-black text-yellow-400 mono">1 / 3 LẦN</div>
            <div class="text-[11px] text-slate-300 mt-1">Vi phạm đủ 3 lần máy bay sẽ buộc phải <b>HỦY CHUYẾN (CRASH)</b>!</div>
        </div>

        <button onclick="resumeFromTurbulence()" class="bg-white hover:bg-yellow-300 text-red-900 font-black px-8 py-4 rounded-2xl shadow-2xl text-sm uppercase tracking-wider transition active:scale-95">
            🔒 Quay lại Buồng lái & Tiếp tục Học ngay
        </button>
    </div>

    <!-- ================= MÀN HÌNH HỦY CHUYẾN DO VI PHẠM QUÁ 3 LẦN ================= -->
    <div id="crash-modal" class="fixed inset-0 z-[999] bg-black/95 backdrop-blur-xl hidden flex-col items-center justify-center p-6 text-center">
        <div class="text-6xl mb-3">💥</div>
        <h2 class="text-2xl font-black text-red-500 uppercase mb-2">CHUYẾN BAY ĐÃ BỊ HỦY BỎ (FLIGHT FAILED)</h2>
        <p class="text-xs text-slate-300 max-w-sm mb-6">
            Bạn đã rời khỏi màn hình tập trung quá 3 lần cho phép. Chuyến bay không thể hoàn thành để đảm bảo kỷ luật học tập thực sự.
        </p>
        <button onclick="closeCrashModal()" class="bg-red-600 hover:bg-red-500 text-white font-extrabold px-6 py-3.5 rounded-2xl text-xs uppercase tracking-wider">
            Đặt lại chuyến bay mới
        </button>
    </div>

    <!-- THANH BAR PHÍA TRÊN -->
    <div class="fixed top-4 left-4 right-4 z-20 flex justify-between items-center pointer-events-none">
        <div class="glass-panel px-4 py-2.5 rounded-2xl flex items-center gap-3 shadow-xl pointer-events-auto">
            <div class="w-9 h-9 rounded-xl bg-gradient-to-br from-blue-500 to-cyan-400 flex items-center justify-center text-black font-black text-lg shadow">✈️</div>
            <div>
                <div class="text-xs font-extrabold tracking-wider text-white flex items-center gap-2">
                    FOCUS FLIGHT AIRLINES
                    <span id="top-aircraft-tag" class="bg-cyan-500/20 text-cyan-300 text-[10px] px-2 py-0.5 rounded-md font-mono">A321neo</span>
                </div>
                <div class="text-[11px] text-slate-400" id="top-subtitle">Chế độ Kỷ luật Hàng không • Chống xao nhãng</div>
            </div>
        </div>

        <div class="flex items-center gap-2 pointer-events-auto">
            <button onclick="toggleLofi()" class="glass-panel px-3.5 py-2.5 rounded-2xl flex items-center gap-2 text-xs font-bold text-slate-200 hover:text-white transition shadow-xl">
                <div id="eq-icon" class="hidden items-end gap-[2px] h-4">
                    <div class="eq-bar"></div><div class="eq-bar"></div><div class="eq-bar"></div>
                </div>
                <span id="lofi-btn-text">🎵 Bật Lofi</span>
            </button>
            <button onclick="openMediaModal()" class="glass-panel px-3.5 py-2.5 rounded-2xl text-xs font-bold text-cyan-400 hover:bg-slate-800 transition shadow-xl border border-cyan-500/30">
                ⚙️ Nhạc / Ảnh
            </button>
        </div>
    </div>

    <!-- MODAL THÊM NHẠC & HÌNH ẢNH NGOÀI -->
    <div id="media-modal" class="fixed inset-0 z-50 bg-black/75 backdrop-blur-md hidden items-center justify-center p-4">
        <div class="glass-panel w-full max-w-md rounded-3xl p-6 shadow-2xl">
            <div class="flex justify-between items-center mb-4">
                <h3 class="text-base font-extrabold text-white">🎧 Trạm Tùy Chỉnh Nhạc Lofi & Ảnh</h3>
                <button onclick="closeMediaModal()" class="text-slate-400 hover:text-white text-lg font-bold">✕</button>
            </div>
            <div class="space-y-3.5 text-xs">
                <div class="bg-slate-900/90 p-3.5 rounded-2xl border border-white/10">
                    <label class="font-bold text-cyan-400 block mb-1.5">1. Tải nhạc Lofi từ máy (.mp3, .wav):</label>
                    <input type="file" accept="audio/*" onchange="handleLocalAudio(this)" class="w-full text-slate-300 file:mr-3 file:py-1.5 file:px-3 file:rounded-xl file:border-0 file:font-bold file:bg-blue-600 file:text-white cursor-pointer mb-2" />
                    <input type="text" id="audio-url-input" placeholder="Hoặc dán link MP3 trực tiếp..." class="w-full bg-slate-800 text-white px-3 py-2 rounded-xl border border-white/10" />
                </div>

                <div class="bg-slate-900/90 p-3.5 rounded-2xl border border-white/10 flex items-center justify-between">
                    <div>
                        <div class="font-bold text-white">🛫 Tiếng động cơ Cabin máy bay (White Noise)</div>
                        <div class="text-[11px] text-slate-400">Tạo cảm giác ngồi trong khoang A321 thật</div>
                    </div>
                    <input type="checkbox" onchange="toggleCabinNoise(this.checked)" class="w-5 h-5 accent-cyan-400 cursor-pointer" />
                </div>

                <div class="bg-slate-900/90 p-3.5 rounded-2xl border border-white/10">
                    <label class="font-bold text-yellow-400 block mb-1.5">2. Đổi ảnh nền sân bay đang chọn:</label>
                    <input type="file" accept="image/*" onchange="handleLocalImage(this)" class="w-full text-slate-300 file:mr-3 file:py-1.5 file:px-3 file:rounded-xl file:border-0 file:font-bold file:bg-yellow-500 file:text-black cursor-pointer mb-2" />
                    <input type="text" id="img-url-input" placeholder="Hoặc dán link ảnh từ mạng..." class="w-full bg-slate-800 text-white px-3 py-2 rounded-xl border border-white/10" />
                </div>
            </div>
            <button onclick="applyCustomMedia()" class="mt-5 w-full bg-gradient-to-r from-blue-600 to-cyan-500 text-white font-extrabold py-3 rounded-xl text-xs">Lưu & Đóng</button>
        </div>
    </div>

    <!-- ================= MÀN HÌNH 1: CHỌN ĐIỂM ĐI - ĐIỂM ĐẾN & THỜI GIAN ================= -->
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

        <!-- Bộ chọn Điểm Đi & Điểm Đến -->
        <div class="grid grid-cols-11 gap-2 items-center bg-slate-900/90 p-3 rounded-2xl border border-white/10 mb-3">
            <div class="col-span-5">
                <div class="text-[10px] text-slate-400 uppercase font-bold mb-1">Điểm khởi hành</div>
                <select id="origin-select" onchange="onRouteChange()" class="w-full bg-slate-800 text-white font-extrabold text-xs px-2.5 py-2 rounded-xl border border-white/10 focus:outline-none focus:border-cyan-400 cursor-pointer"></select>
            </div>
            <div class="col-span-1 flex justify-center pt-4">
                <button onclick="swapRoute()" class="w-8 h-8 rounded-full bg-slate-800 hover:bg-blue-600 text-cyan-400 hover:text-white font-bold text-sm flex items-center justify-center transition border border-white/10" title="Đảo chiều bay">⇄</button>
            </div>
            <div class="col-span-5">
                <div class="text-[10px] text-yellow-400 uppercase font-bold mb-1">Điểm hạ cánh</div>
                <select id="dest-select" onchange="onRouteChange()" class="w-full bg-slate-800 text-white font-extrabold text-xs px-2.5 py-2 rounded-xl border border-yellow-400/40 focus:outline-none focus:border-yellow-400 cursor-pointer"></select>
            </div>
        </div>

        <!-- Thời gian bay -->
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

        <button onclick="goToSeatSelection()" class="w-full bg-gradient-to-r from-blue-600 to-cyan-500 hover:opacity-95 text-white font-extrabold py-3.5 rounded-2xl shadow-lg shadow-blue-600/30 transition active:scale-98 flex items-center justify-center gap-2 text-sm">
            <span>Book Now • Chọn Ghế & Chế Độ Tập Trung</span>
            <span>➔</span>
        </button>
    </div>

    <!-- ================= MÀN HÌNH 2: SƠ ĐỒ GHẾ & POPUP FOCUS ================= -->
    <div id="screen-seat" class="fixed inset-0 z-30 bg-[#070b14]/95 backdrop-blur-xl hidden flex-col items-center justify-between py-5 px-4">
        <div class="w-full max-w-md flex items-center justify-between">
            <button onclick="backToBooking()" class="bg-slate-800/80 hover:bg-slate-700 text-slate-200 px-3.5 py-2 rounded-xl text-xs font-bold">
                ‹ Quay lại
            </button>
            <div class="text-center">
                <div id="seat-header-aircraft" class="text-[10px] text-cyan-400 font-extrabold uppercase tracking-widest">AIRBUS A321NEO</div>
                <div id="seat-header-route" class="text-sm font-extrabold text-white mt-0.5">SGN ➔ CXR • 35m</div>
            </div>
            <div class="w-16 text-right">
                <span id="seat-selected-badge" class="bg-blue-600/30 border border-blue-400 text-blue-200 text-xs font-mono font-bold px-2.5 py-1 rounded-lg">06A</span>
            </div>
        </div>

        <div class="relative w-full max-w-[340px] h-[72vh] fuselage flex flex-col items-center pt-12 pb-8 px-6 overflow-y-auto my-2">
            <div class="w-32 h-6 border-b border-slate-700/80 mb-5 flex items-center justify-center text-[10px] font-mono text-slate-500 tracking-widest uppercase">
                Cockpit
            </div>

            <div class="grid grid-cols-5 w-full text-center text-xs font-extrabold text-slate-400 mb-3 px-1">
                <div>A</div><div>C</div><div></div><div>D</div><div>F</div>
            </div>

            <div id="seat-grid" class="w-full space-y-2.5 pb-8"></div>
        </div>

        <!-- POPUP "What do you want to focus?" + BẬT KHÓA KỶ LUẬT -->
        <div id="focus-popover-backdrop" class="fixed inset-0 z-40 bg-black/50 backdrop-blur-[2px] hidden items-center justify-center p-4">
            <div class="focus-popover w-full max-w-[360px] rounded-[28px] p-5 text-white">
                <div class="flex justify-between items-center mb-1">
                    <span class="text-xs font-bold text-blue-300/90">Seat: <span id="pop-seat-code" class="mono text-white">06A</span></span>
                    <button onclick="closeFocusPopover()" class="text-slate-400 hover:text-white text-sm font-bold">✕</button>
                </div>
                <h3 class="text-base font-extrabold text-white mb-3.5">What do you want to focus?</h3>

                <div class="flex flex-wrap gap-2 mb-3.5" id="focus-pills-container"></div>

                <div id="custom-focus-box" class="hidden mb-3">
                    <input type="text" id="custom-focus-input" placeholder="Nhập chế độ riêng (VD: Giải tích, Đồ án...)" class="w-full bg-slate-900/90 text-xs text-white px-3.5 py-2.5 rounded-xl border border-blue-400/40 focus:outline-none" />
                </div>

                <div class="bg-slate-900/60 p-3 rounded-2xl border border-white/10 mb-3">
                    <label class="block text-[10px] uppercase tracking-wider text-slate-400 font-bold mb-1">Tên hành khách in lên vé:</label>
                    <input type="text" id="passenger-name-input" value="QUANG MINH" placeholder="Nhập tên của bạn..." class="w-full bg-transparent text-xs font-extrabold text-amber-300 focus:outline-none uppercase" />
                </div>

                <!-- Tùy chọn Khóa Kỷ Luật không cho nhảy sang tab khác -->
                <div class="bg-red-500/15 border border-red-400/30 p-3 rounded-2xl flex items-center justify-between mb-4">
                    <div>
                        <div class="text-xs font-extrabold text-red-200 flex items-center gap-1">🔒 Khóa Kỷ Luật (Strict Mode)</div>
                        <div class="text-[10px] text-slate-300">Tự bung Fullscreen & Báo động nếu chuyển tab khác</div>
                    </div>
                    <input type="checkbox" id="strict-mode-toggle" checked class="w-5 h-5 accent-red-500 cursor-pointer" />
                </div>

                <button onclick="confirmSeatAndFocus()" class="w-full bg-blue-500 hover:bg-blue-400 text-white font-extrabold py-3 rounded-2xl text-xs shadow-lg shadow-blue-500/40 transition">
                    Xác nhận Ghế & Xuất Vé Boarding Pass ➔
                </button>
            </div>
        </div>

        <div class="w-full max-w-md flex items-center justify-between px-2">
            <div class="text-xs text-slate-400">Chạm vào ghế bất kỳ để chọn chế độ tập trung</div>
            <button onclick="showBoardingPass()" class="bg-blue-600 hover:bg-blue-500 text-white font-extrabold px-5 py-2.5 rounded-xl text-xs shadow-lg">
                Tiếp tục ➔
            </button>
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
                            <div id="tk-focus" class="font-extrabold text-blue-300 mt-0.5">💻 Work</div>
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
                        <div class="mono text-[10px] tracking-[0.35em] text-slate-400 mt-2">NO-DISTRACTION-FLIGHT</div>
                    </div>
                </div>
            </div>

            <div class="flex gap-2 w-full mt-5">
                <button onclick="backToSeatFromTicket()" class="w-1/3 bg-slate-800 hover:bg-slate-700 text-slate-300 font-bold py-4 rounded-2xl text-xs">‹ Đổi ghế</button>
                <button onclick="startFlight()" class="w-2/3 bg-gradient-to-r from-blue-600 to-cyan-500 hover:opacity-95 text-white font-extrabold py-4 rounded-2xl shadow-xl shadow-cyan-500/30 text-xs uppercase tracking-wider">
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
                    <button onclick="abortFlight()" class="bg-red-500/20 hover:bg-red-500/30 text-red-300 border border-red-500/30 px-3.5 py-2 rounded-xl text-xs font-bold transition">
                        Hạ cánh khẩn cấp
                    </button>
                </div>
            </div>
        </div>

        <div class="w-full bg-slate-800 h-2.5 rounded-full overflow-hidden mt-4">
            <div id="flight-progress" class="bg-gradient-to-r from-blue-500 via-cyan-400 to-yellow-400 h-full w-0 transition-all duration-500"></div>
        </div>
    </div>

    <script>
        // 1. DANH SÁCH 12 SÂN BAY
        const AIRPORTS = [
            { code: "SGN", name: "Sài Gòn (Tân Sơn Nhất)", region: "📍 TP. Hồ Chí Minh", coords: [10.8188, 106.6519], img: "https://images.unsplash.com/photo-1583417319070-4a69db38a482?w=900&q=80" },
            { code: "DAD", name: "Đà Nẵng (Quảng Nam)", region: "✨ Quê hương Quảng Nam - Đà Nẵng", coords: [16.0439, 108.1994], img: "https://images.unsplash.com/photo-1559592413-7cec4d0cae2b?w=900&q=80" },
            { code: "CXR", name: "Cam Ranh (Khánh Hòa)", region: "🏖️ Quê hương Diên Khánh - Khánh Hòa", coords: [11.9982, 109.2194], img: "https://images.unsplash.com/photo-1582297121287-75905c10640d?w=900&q=80" },
            { code: "UIH", name: "Phù Cát (Quy Nhơn)", region: "🌊 Quê hương Quy Nhơn - Bình Định", coords: [13.9550, 109.0422], img: "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=900&q=80" },
            { code: "LTH", name: "Long Thành (Đồng Nai)", region: "🛫 Quê hương Đồng Nai", coords: [10.7850, 107.0650], img: "https://images.unsplash.com/photo-1436491865332-7a61a109cc05?w=900&q=80" },
            { code: "HAN", name: "Hà Nội (Nội Bài)", region: "🏛️ Thủ đô Hà Nội", coords: [21.2212, 105.8072], img: "https://images.unsplash.com/photo-1509030450996-dd1a26dda07a?w=900&q=80" },
            { code: "HPH", name: "Hải Phòng (Cát Bi)", region: "⚓ Thành phố Cảng Hải Phòng", coords: [20.8194, 106.7250], img: "https://images.unsplash.com/photo-1540959733332-eab4deabeeaf?w=900&q=80" },
            { code: "VII", name: "TP. Vinh (Nghệ An)", region: "🌾 Miền Trung Nghệ An", coords: [18.7376, 105.6708], img: "https://images.unsplash.com/photo-1506744038136-46273834b3fb?w=900&q=80" },
            { code: "DLI", name: "Đà Lạt (Liên Khương)", region: "🌲 Cao nguyên Lâm Đồng", coords: [11.7500, 108.3667], img: "https://images.unsplash.com/photo-1509316975850-ff9c5deb0cd9?w=900&q=80" },
            { code: "PQC", name: "Phú Quốc (Kiên Giang)", region: "🏝️ Đảo Ngọc Phú Quốc", coords: [10.1698, 103.9931], img: "https://images.unsplash.com/photo-1540202404-a2f29016b523?w=900&q=80" },
            { code: "HND", name: "Tokyo Haneda (Nhật Bản)", region: "🗾 Chuyến bay Quốc tế Dài hạn", coords: [35.5494, 139.7798], img: "https://images.unsplash.com/photo-1503899036084-c55cdd92da26?w=900&q=80" },
            { code: "ICN", name: "Seoul Incheon (Hàn Quốc)", region: "❄️ Chuyến bay Quốc tế Đông Á", coords: [37.4602, 126.4407], img: "https://images.unsplash.com/photo-1517154421773-0529f29ea451?w=900&q=80" }
        ];

        const FOCUS_MODES = [
            { id: "focus", label: "Focus", icon: "⚛️", color: "bg-slate-600/90 border-slate-400 text-white" },
            { id: "work", label: "Work", icon: "💻", color: "bg-blue-600 border-blue-300 text-white" },
            { id: "meditate", label: "Meditate", icon: "🧘", color: "bg-indigo-500 border-indigo-300 text-white" },
            { id: "read", label: "Read", icon: "📖", color: "bg-teal-600 border-teal-300 text-white" },
            { id: "exercise", label: "Exercise", icon: "🏃", color: "bg-sky-500 border-sky-300 text-white" }
        ];

        let originAirport = AIRPORTS[0];
        let destAirport = AIRPORTS[2];
        let selectedDuration = 35;
        let currentDistance = 320;
        let selectedAircraft = "Airbus A321neo";
        let selectedSeat = "06A";
        let selectedFocus = FOCUS_MODES[1];
        let passengerName = "QUANG MINH";

        // Biến trạng thái Chuyến bay & Khóa kỷ luật
        let isFlying = false;
        let strictModeEnabled = true;
        let isPausedByViolation = false;
        let violationCount = 0;
        const MAX_VIOLATIONS = 3;
        let alarmInterval = null;

        let flightInterval = null;
        let remainingSeconds = 35 * 60;
        let totalFlightSeconds = 35 * 60;

        // 2. BẢN ĐỒ VỆ TINH
        const map = L.map('map', { zoomControl: false }).setView([12.5, 108.0], 6);
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
            const temp = originAirport;
            originAirport = destAirport;
            destAirport = temp;
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

        // 3. SƠ ĐỒ GHẾ & FOCUS POPOVER
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

        // 4. BOARDING PASS & CẤT CÁNH CÙNG KHÓA KỶ LUẬT
        function showBoardingPass() {
            strictModeEnabled = document.getElementById('strict-mode-toggle').checked;
            document.getElementById('screen-seat').classList.add('hidden');
            document.getElementById('screen-seat').classList.remove('flex');

            document.getElementById('tk-aircraft').innerText = selectedAircraft;
            document.getElementById('tk-passenger').innerText = passengerName;
            document.getElementById('tk-strict-badge').innerText = strictModeEnabled ? "🔒 STRICT LOCK ON" : "🔓 FREE MODE";
            document.getElementById('tk-strict-badge').className = strictModeEnabled ? "text-[11px] font-extrabold text-red-400" : "text-[11px] font-extrabold text-slate-400";
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

            // Bật Fullscreen nếu chọn Khóa Kỷ Luật
            if (strictModeEnabled) {
                requestAppFullscreen();
            }

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
                if (isPausedByViolation) return; // Đóng băng đồng hồ khi nhảy ra ngoài!
                remainingSeconds--;
                if (remainingSeconds <= 0) {
                    clearInterval(flightInterval);
                    isFlying = false;
                    alert(`🎉 Chuyến bay ${originAirport.code} ➔ ${destAirport.code} đã hạ cánh an toàn! Chúc mừng ${passengerName} đã hoàn thành phiên ${selectedFocus.label} với độ tập trung tuyệt đối.`);
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

        // 5. HỆ THỐNG BẮT LỖI CHUYỂN TAB / RỜI CỬA SỔ & CÒI BÁO ĐỘNG BUỒNG LÁI
        let audioCtx = null, cabinNoiseNode = null;

        function playCockpitAlarmBeep() {
            try {
                if (!audioCtx) audioCtx = new (window.AudioContext || window.webkitAudioContext)();
                const osc = audioCtx.createOscillator();
                const gain = audioCtx.createGain();
                osc.type = 'sawtooth';
                osc.frequency.setValueAtTime(880, audioCtx.currentTime); // Tần số cao cảnh báo
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

            // Nếu vi phạm đủ 3 lần -> Rơi máy bay (Hủy chuyến)
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

            // Hiển thị màn hình đỏ cảnh báo & phát còi liên tục
            document.getElementById('violation-count-text').innerText = `${violationCount} / ${MAX_VIOLATIONS} LẦN`;
            document.getElementById('turbulence-modal').classList.remove('hidden');
            document.getElementById('turbulence-modal').classList.add('flex');

            playCockpitAlarmBeep();
            if (alarmInterval) clearInterval(alarmInterval);
            alarmInterval = setInterval(playCockpitAlarmBeep, 900);
        }

        function stopAlarmLoop() {
            if (alarmInterval) {
                clearInterval(alarmInterval);
                alarmInterval = null;
            }
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

        // Lắng nghe sự kiện người dùng đổi sang Tab khác hoặc bấm ra ngoài cửa sổ
        document.addEventListener('visibilitychange', () => {
            if (document.hidden) triggerTurbulenceViolation();
        });

        window.addEventListener('blur', () => {
            triggerTurbulenceViolation();
        });

        // Cảnh báo nếu người dùng tự ý nhấn hộp thoại đóng/tải lại trang khi đang bay
        window.addEventListener('beforeunload', (e) => {
            if (isFlying && strictModeEnabled) {
                e.preventDefault();
                e.returnValue = 'Chuyến bay tập trung đang diễn ra! Bạn có chắc muốn hủy chuyến bay?';
            }
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

        // 6. HỆ THỐNG ÂM THANH LOFI & CUSTOM MEDIA
        function toggleLofi() {
            const p = document.getElementById('lofi-player');
            const eq = document.getElementById('eq-icon');
            const txt = document.getElementById('lofi-btn-text');
            if (p.paused) {
                p.play().then(() => {
                    eq.classList.remove('hidden'); eq.classList.add('flex');
                    txt.innerText = "Đang phát Lofi";
                }).catch(() => {});
            } else {
                p.pause();
                eq.classList.add('hidden'); eq.classList.remove('flex');
                txt.innerText = "🎵 Bật Lofi";
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
            const iUrl = document.getElementById('img-url-input').value.trim();
            if (aUrl) {
                const p = document.getElementById('lofi-player');
                p.src = aUrl; p.play();
            }
            if (iUrl) {
                destAirport.img = iUrl;
                document.getElementById('dest-banner-img').src = iUrl;
            }
            closeMediaModal();
        }

        initDropdowns();
        onRouteChange();
    </script>
</body>
</html>
"""

components.html(app_html, height=920, scrolling=False)
