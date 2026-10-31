import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="SGN Focus Airlines", page_icon="✈️", layout="wide", initial_sidebar_state="collapsed")
st.markdown("""
    <style>
        #MainMenu {visibility: hidden;} header {visibility: hidden;} footer {visibility: hidden;}
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
        .glass-panel { background: rgba(13, 18, 30, 0.86); backdrop-filter: blur(24px); border: 1px solid rgba(255, 255, 255, 0.12); }
        .fuselage { border-top-left-radius: 150px 240px; border-top-right-radius: 150px 240px; border-left: 3px solid rgba(56, 189, 248, 0.25); border-right: 3px solid rgba(56, 189, 248, 0.25); border-top: 3px solid rgba(56, 189, 248, 0.4); background: linear-gradient(180deg, rgba(15, 23, 42, 0.9) 0%, rgba(9, 13, 22, 0.95) 100%); box-shadow: 0 0 50px rgba(14, 165, 233, 0.15); }
        .ticket-cutout-left { position: absolute; left: -14px; top: 64%; width: 28px; height: 28px; background: #060911; border-radius: 50%; border-right: 1px solid rgba(255,255,255,0.15); }
        .ticket-cutout-right { position: absolute; right: -14px; top: 64%; width: 28px; height: 28px; background: #060911; border-radius: 50%; border-left: 1px solid rgba(255,255,255,0.15); }
        ::-webkit-scrollbar { width: 5px; } ::-webkit-scrollbar-thumb { background: rgba(255,255,255,0.2); border-radius: 10px; }
        .leaflet-control-attribution { display: none !important; }
    </style>
</head>
<body class="relative w-screen h-screen">
    <div id="map"></div>

    <!-- AUDIO ELEMENT -->
    <audio id="lofi-player" loop crossorigin="anonymous">
        <source id="lofi-source" src="https://cdn.pixabay.com/download/audio/2022/05/27/audio_1808fbf07a.mp3" type="audio/mpeg">
    </audio>

    <!-- THANH CÔNG CỤ -->
    <div class="fixed top-4 left-4 right-4 z-20 flex justify-between items-center pointer-events-none">
        <div class="glass-panel px-4 py-2.5 rounded-2xl flex items-center gap-3 shadow-xl pointer-events-auto">
            <div class="w-8 h-8 rounded-xl bg-gradient-to-br from-blue-500 to-cyan-400 flex items-center justify-center text-black font-black">✈️</div>
            <div>
                <div class="text-xs font-extrabold tracking-wider text-white">SGN FOCUS AIRLINES</div>
                <div class="text-[10px] text-slate-400">Tân Sơn Nhất (SGN) ➔ Home</div>
            </div>
        </div>
        <button onclick="toggleLofi()" class="glass-panel pointer-events-auto px-4 py-2.5 rounded-2xl text-xs font-bold text-cyan-400 hover:text-white transition shadow-xl border border-cyan-500/30" id="lofi-btn">🎵 Bật nhạc Lofi</button>
    </div>

    <!-- MÀN HÌNH 1: ĐẶT VÉ -->
    <div id="screen-booking" class="fixed bottom-5 left-1/2 -translate-x-1/2 z-20 w-[94%] max-w-lg glass-panel rounded-3xl p-5 shadow-2xl transition-all">
        <div class="relative w-full h-28 rounded-2xl overflow-hidden mb-4 border border-white/10">
            <img id="dest-banner-img" src="" class="w-full h-full object-cover opacity-80" />
            <div class="absolute inset-0 bg-gradient-to-t from-[#090d16] via-[#090d16]/40 to-transparent"></div>
            <div class="absolute top-2.5 left-3"><span class="bg-yellow-400 text-black font-black text-[10px] px-2 py-0.5 rounded-md">SGN ➔ <span id="banner-dest-code"></span></span></div>
            <div class="absolute bottom-2.5 left-3"><div id="banner-region-tag" class="text-[10px] text-cyan-300 font-bold uppercase"></div><div id="banner-dest-title" class="text-lg font-extrabold text-white"></div></div>
        </div>

        <div class="text-xs font-bold text-slate-300 mb-2">Chọn chặng bay về quê của nhóm:</div>
        <div id="dest-list" class="grid grid-cols-2 gap-2.5 mb-4 max-h-44 overflow-y-auto pr-1"></div>
        <button onclick="goToSeatSelection()" class="w-full bg-gradient-to-r from-blue-600 to-cyan-500 text-white font-extrabold py-3.5 rounded-2xl shadow-lg hover:opacity-90">Làm thủ tục Check-in ➔</button>
    </div>

    <!-- MÀN HÌNH 2: CHỌN GHẾ -->
    <div id="screen-seat" class="fixed inset-0 z-30 bg-[#060911]/95 backdrop-blur-xl hidden flex-col items-center justify-between py-5 px-4">
        <div class="w-full max-w-md flex justify-between"><button onclick="backToBooking()" class="text-slate-400 text-xs font-bold">‹ Đổi chuyến</button><div class="text-sm font-extrabold text-white" id="seat-route-title"></div><div class="w-16"></div></div>
        
        <div class="relative w-full max-w-[330px] h-[64vh] fuselage flex flex-col items-center pt-12 pb-6 px-6 overflow-y-auto">
            <div class="w-36 h-7 border-b border-cyan-500/30 mb-4 text-center text-[10px] text-cyan-300/70">▲ Cockpit ▲</div>
            <div class="grid grid-cols-5 w-full text-center text-xs font-extrabold text-slate-400 mb-2"><div>A</div><div>C</div><div></div><div>D</div><div>F</div></div>
            <div id="seat-grid" class="w-full space-y-2 pb-6"></div>
        </div>

        <!-- Popup Nhập thông tin -->
        <div id="focus-modal" class="fixed inset-0 z-40 bg-black/80 hidden items-center justify-center p-4">
            <div class="glass-panel w-full max-w-sm rounded-3xl p-6">
                <div class="text-xs text-cyan-400 font-extrabold mb-3">Ghế <span id="modal-seat-label">06A</span></div>
                <input type="text" id="passenger-name" placeholder="Tên hành khách (VD: Minh, Đại...)" class="w-full bg-slate-900 text-sm text-white px-4 py-3 rounded-xl border border-white/20 mb-3" />
                <input type="text" id="custom-task" placeholder="Mục tiêu (VD: Code đồ án Streamlit)" class="w-full bg-slate-900 text-sm text-white px-4 py-3 rounded-xl border border-white/20 mb-4" />
                <div class="flex gap-2">
                    <button onclick="document.getElementById('focus-modal').classList.remove('flex'); document.getElementById('focus-modal').classList.add('hidden');" class="w-1/3 bg-slate-800 text-white font-bold py-3 rounded-xl text-xs">Hủy</button>
                    <button onclick="showBoardingPass()" class="w-2/3 bg-blue-600 text-white font-extrabold py-3 rounded-xl text-xs">In vé Boarding Pass ➔</button>
                </div>
            </div>
        </div>
    </div>

    <!-- MÀN HÌNH 3: VÉ MÁY BAY -->
    <div id="screen-ticket" class="fixed inset-0 z-40 bg-black/85 hidden items-center justify-center p-4">
        <div class="w-full max-w-sm">
            <div class="w-full bg-[#111622] border border-white/15 rounded-3xl overflow-hidden relative">
                <div class="bg-gradient-to-r from-blue-600 to-cyan-500 px-6 py-3 text-xs font-black text-white">SGN FOCUS AIRLINES</div>
                <div class="p-6">
                    <div class="text-[10px] text-slate-400 uppercase">Passenger</div>
                    <div id="tk-name" class="text-xl font-black text-amber-300 mb-4 uppercase">MINH QUANG</div>
                    <div class="flex justify-between items-center mb-5">
                        <div><div class="text-4xl font-black text-white">SGN</div></div>
                        <div class="text-cyan-400 text-xl">✈️</div>
                        <div class="text-right"><div id="tk-dest-code" class="text-4xl font-black text-yellow-400">CXR</div></div>
                    </div>
                    <div class="grid grid-cols-2 gap-2 pt-4 border-t border-white/10 text-xs mb-4">
                        <div><div class="text-slate-500 text-[10px]">SEAT</div><div id="tk-seat" class="font-extrabold text-white">06A</div></div>
                        <div class="text-right"><div class="text-slate-500 text-[10px]">TIME</div><div id="tk-duration" class="font-bold text-white">35m</div></div>
                    </div>
                    <div class="bg-slate-900 rounded-xl p-3 border border-white/5">
                        <div class="text-[10px] text-slate-400">FOCUS TASK:</div>
                        <div id="tk-activity" class="text-xs font-extrabold text-cyan-400">Code đồ án</div>
                    </div>
                </div>
            </div>
            <button onclick="startFlight()" class="mt-5 w-full bg-gradient-to-r from-blue-600 to-cyan-500 text-white font-extrabold py-4 rounded-2xl">🛫 BẮT ĐẦU CHUYẾN BAY</button>
        </div>
    </div>

    <!-- MÀN HÌNH 4: ĐANG BAY -->
    <div id="screen-flying" class="fixed bottom-5 left-1/2 -translate-x-1/2 z-20 w-[94%] max-w-lg glass-panel rounded-3xl p-5 hidden">
        <div class="flex items-end justify-between border-b border-white/10 pb-3 mb-3">
            <div>
                <div class="text-xs font-extrabold text-white" id="fly-route-text">Tân Sơn Nhất ➔ Cam Ranh</div>
                <div class="text-[10px] text-cyan-400 mt-1 uppercase" id="fly-pass-name">HÀNH KHÁCH: MINH</div>
            </div>
            <div id="countdown-timer" class="mono text-4xl font-extrabold text-yellow-400">35:00</div>
        </div>
        <button onclick="abortFlight()" class="w-full bg-red-500/20 text-red-300 py-2 rounded-xl text-xs font-bold">Hạ cánh khẩn cấp (Hủy)</button>
    </div>

    <script>
        const ORIGIN_SGN = { code: "SGN", coords: [10.8188, 106.6519] };
        
        // DANH SÁCH SÂN BAY BỔ SUNG CAM RANH (CXR)
        const DESTINATIONS = [
            { code: "DAD", name: "Đà Nẵng", regionTag: "✨ Quê hương Quảng Nam - Đà Nẵng", coords: [16.0439, 108.1994], duration: 45, img: "https://images.unsplash.com/photo-1559592413-7cec4d0cae2b?w=800&q=80" },
            { code: "UIH", name: "Quy Nhơn", regionTag: "🌊 Quê hương Phù Cát - Bình Định", coords: [13.9550, 109.0422], duration: 35, img: "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=800&q=80" },
            { code: "CXR", name: "Cam Ranh", regionTag: "🏖️ Quê hương Diên Khánh - Khánh Hòa", coords: [11.9982, 109.2194], duration: 35, img: "https://images.unsplash.com/photo-1582297121287-75905c10640d?w=800&q=80" },
            { code: "LTH", name: "Long Thành", regionTag: "🛫 Quê hương Đồng Nai", coords: [10.7850, 107.0650], duration: 15, img: "https://images.unsplash.com/photo-1436491865332-7a61a109cc05?w=800&q=80" }
        ];

        let selectedDest = DESTINATIONS[2]; // Mặc định Cam Ranh (CXR)
        let selectedSeat = "06A";
        let flightInterval = null, remainingSeconds = 35 * 60;
        
        const map = L.map('map', { zoomControl: false }).setView([13.5, 107.5], 6);
        L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}', { maxZoom: 18 }).addTo(map);
        let routeLine = null, planeMarker = null;

        function updateMap() {
            document.getElementById('dest-banner-img').src = selectedDest.img;
            document.getElementById('banner-dest-code').innerText = selectedDest.code;
            document.getElementById('banner-region-tag').innerText = selectedDest.regionTag;
            document.getElementById('banner-dest-title').innerText = selectedDest.name;

            if(routeLine) map.removeLayer(routeLine);
            routeLine = L.polyline([ORIGIN_SGN.coords, selectedDest.coords], { color: '#38bdf8', weight: 3, dashArray: '8, 8' }).addTo(map);
            map.fitBounds(routeLine.getBounds(), { padding: [50, 50] });
        }

        function renderDestinations() {
            const list = document.getElementById('dest-list');
            list.innerHTML = '';
            DESTINATIONS.forEach(d => {
                const btn = document.createElement('button');
                btn.className = `p-3 rounded-2xl text-left border ${d.code === selectedDest.code ? 'bg-blue-600/30 border-cyan-400' : 'bg-slate-900 border-white/10'}`;
                btn.innerHTML = `<div class="font-black text-sm text-white">${d.name} (${d.code})</div><div class="text-xs text-cyan-400">${d.duration} phút</div>`;
                btn.onclick = () => { selectedDest = d; renderDestinations(); updateMap(); };
                list.appendChild(btn);
            });
        }

        function renderSeats() {
            const grid = document.getElementById('seat-grid');
            grid.innerHTML = '';
            for(let r=1; r<=10; r++) {
                const row = document.createElement('div'); row.className = 'grid grid-cols-5 gap-2 w-full';
                ['A','C','','D','F'].forEach(c => {
                    if(!c) { row.innerHTML += `<div class="text-center text-xs text-slate-500">${r}</div>`; return; }
                    const seat = (r<10?'0'+r:r)+c;
                    const btn = document.createElement('button');
                    btn.className = `h-10 rounded-xl font-bold text-xs border ${seat===selectedSeat ? 'bg-cyan-500 text-black' : 'bg-slate-800 text-slate-300 border-white/10'}`;
                    btn.innerText = seat;
                    btn.onclick = () => {
                        selectedSeat = seat; renderSeats();
                        document.getElementById('modal-seat-label').innerText = seat;
                        document.getElementById('focus-modal').classList.remove('hidden');
                        document.getElementById('focus-modal').classList.add('flex');
                    };
                    row.appendChild(btn);
                });
                grid.appendChild(row);
            }
        }

        function goToSeatSelection() {
            document.getElementById('seat-route-title').innerText = `SGN ➔ ${selectedDest.code}`;
            document.getElementById('screen-booking').classList.add('hidden');
            document.getElementById('screen-seat').classList.remove('hidden');
            document.getElementById('screen-seat').classList.add('flex');
            renderSeats();
        }

        function backToBooking() {
            document.getElementById('screen-seat').classList.add('hidden'); document.getElementById('screen-seat').classList.remove('flex');
            document.getElementById('screen-booking').classList.remove('hidden');
        }

        function showBoardingPass() {
            document.getElementById('focus-modal').classList.add('hidden'); document.getElementById('screen-seat').classList.add('hidden');
            
            const name = document.getElementById('passenger-name').value || "MEMBER KHẨN DANH";
            const task = document.getElementById('custom-task').value || "Tập trung tối đa";
            
            document.getElementById('tk-name').innerText = name;
            document.getElementById('tk-dest-code').innerText = selectedDest.code;
            document.getElementById('tk-seat').innerText = selectedSeat;
            document.getElementById('tk-duration').innerText = selectedDest.duration + 'm';
            document.getElementById('tk-activity').innerText = task;
            
            document.getElementById('fly-pass-name').innerText = "HÀNH KHÁCH: " + name;
            document.getElementById('screen-ticket').classList.remove('hidden');
            document.getElementById('screen-ticket').classList.add('flex');
        }

        function startFlight() {
            document.getElementById('screen-ticket').classList.add('hidden'); document.getElementById('screen-ticket').classList.remove('flex');
            document.getElementById('screen-flying').classList.remove('hidden');
            
            document.getElementById('fly-route-text').innerText = `Tân Sơn Nhất ➔ ${selectedDest.name}`;
            remainingSeconds = selectedDest.duration * 60;
            
            const icon = L.divIcon({ html: `<div class="w-8 h-8 bg-yellow-400 rounded-full flex items-center justify-center text-lg">✈️</div>` });
            if(planeMarker) map.removeLayer(planeMarker);
            planeMarker = L.marker(ORIGIN_SGN.coords, {icon: icon}).addTo(map);
            
            if(flightInterval) clearInterval(flightInterval);
            flightInterval = setInterval(() => {
                remainingSeconds--;
                if(remainingSeconds <= 0) { clearInterval(flightInterval); alert("🎉 Hạ cánh an toàn!"); abortFlight(); }
                
                const mins = Math.floor(remainingSeconds / 60); const secs = remainingSeconds % 60;
                document.getElementById('countdown-timer').innerText = `${mins<10?'0'+mins:mins}:${secs<10?'0'+secs:secs}`;
                
                const prog = 1 - (remainingSeconds / (selectedDest.duration * 60));
                const lat = ORIGIN_SGN.coords[0] + (selectedDest.coords[0] - ORIGIN_SGN.coords[0]) * prog;
                const lng = ORIGIN_SGN.coords[1] + (selectedDest.coords[1] - ORIGIN_SGN.coords[1]) * prog;
                planeMarker.setLatLng([lat, lng]);
            }, 1000);
            
            document.getElementById('lofi-player').play();
        }

        function abortFlight() {
            clearInterval(flightInterval); document.getElementById('screen-flying').classList.add('hidden');
            document.getElementById('screen-booking').classList.remove('hidden'); document.getElementById('lofi-player').pause();
        }
        
        function toggleLofi() {
            const p = document.getElementById('lofi-player');
            if(p.paused) { p.play(); document.getElementById('lofi-btn').innerText = "⏸️ Đang phát Lofi"; }
            else { p.pause(); document.getElementById('lofi-btn').innerText = "🎵 Bật nhạc Lofi"; }
        }

        renderDestinations(); updateMap();
    </script>
</body>
</html>
"""
components.html(app_html, height=920, scrolling=False)
