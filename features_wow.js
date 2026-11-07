// ================= 1. TỪ ĐIỂN ĐA NGÔN NGỮ TOÀN DIỆN & TÊN 34 SÂN BAY (VI / EN / 繁體中文) =================
const AIRPORT_NAMES_I18N = {
    SGN: { vi: "TP.HCM (Tân Sơn Nhất)", en: "Ho Chi Minh City (Tan Son Nhat)", zh: "胡志明市（新山一）" },
    HAN: { vi: "Hà Nội (Nội Bài)", en: "Hanoi (Noi Bai)", zh: "河內（內排）" },
    DAD: { vi: "Đà Nẵng", en: "Da Nang", zh: "峴港" },
    CXR: { vi: "Cam Ranh (Khánh Hòa)", en: "Cam Ranh (Nha Trang)", zh: "金蘭（芽莊）" },
    UIH: { vi: "Phù Cát (Quy Nhơn)", en: "Phu Cat (Quy Nhon)", zh: "符吉（歸仁）" },
    LTH: { vi: "Long Thành (Đồng Nai)", en: "Long Thanh (Dong Nai)", zh: "隆城（同奈）" },
    PQC: { vi: "Phú Quốc (Kiên Giang)", en: "Phu Quoc Island", zh: "富國島" },
    DLI: { vi: "Đà Lạt (Liên Khương)", en: "Da Lat (Lien Khuong)", zh: "大叻（聯姜）" },
    HPH: { vi: "Hải Phòng (Cát Bi)", en: "Hai Phong (Cat Bi)", zh: "海防（吉碑）" },
    VII: { vi: "Vinh (Nghệ An)", en: "Vinh (Nghe An)", zh: "榮市（乂安）" },
    HUI: { vi: "Huế (Phú Bài)", en: "Hue (Phu Bai)", zh: "順化（富牌）" },
    VCA: { vi: "Cần Thơ", en: "Can Tho", zh: "芹苴" },
    VDH: { vi: "Đồng Hới (Quảng Bình)", en: "Dong Hoi (Quang Binh)", zh: "洞海（廣平）" },
    THD: { vi: "Thanh Hóa (Thọ Xuân)", en: "Thanh Hoa (Tho Xuan)", zh: "清化（壽春）" },
    VDO: { vi: "Vân Đồn (Quảng Ninh)", en: "Van Don (Ha Long)", zh: "雲屯（廣寧）" },
    VCL: { vi: "Chu Lai (Quảng Nam)", en: "Chu Lai (Quang Nam)", zh: "朱萊（廣南）" },
    TBB: { vi: "Tuy Hòa (Phú Yên)", en: "Tuy Hoa (Phu Yen)", zh: "綏和（富安）" },
    BMV: { vi: "Buôn Ma Thuột (Đắk Lắk)", en: "Buon Ma Thuot (Dak Lak)", zh: "邦美蜀（得勒）" },
    PXU: { vi: "Pleiku (Gia Lai)", en: "Pleiku (Gia Lai)", zh: "波來古（嘉萊）" },
    VCS: { vi: "Côn Đảo (Bà Rịa - VT)", en: "Con Dao Island", zh: "崑崙島" },
    DIN: { vi: "Điện Biên Phủ", en: "Dien Bien Phu", zh: "奠邊府" },
    CAH: { vi: "Cà Mau", en: "Ca Mau", zh: "金甌" },
    TPE: { vi: "Đài Bắc - Đào Viên (Đài Loan 🇹🇼)", en: "Taipei Taoyuan (Taiwan 🇹🇼)", zh: "台北桃園（台灣 🇹🇼）" },
    BKK: { vi: "Bangkok (Thái Lan)", en: "Bangkok Suvarnabhumi (Thailand)", zh: "曼谷（泰國）" },
    SIN: { vi: "Singapore (Changi)", en: "Singapore (Changi)", zh: "新加坡（樟宜）" },
    KUL: { vi: "Kuala Lumpur (Malaysia)", en: "Kuala Lumpur (Malaysia)", zh: "吉隆坡（馬來西亞）" },
    HKG: { vi: "Hong Kong", en: "Hong Kong Intl", zh: "香港國際機場" },
    ICN: { vi: "Seoul Incheon (Hàn Quốc)", en: "Seoul Incheon (South Korea)", zh: "首爾仁川（韓國）" },
    HND: { vi: "Tokyo Haneda (Nhật Bản)", en: "Tokyo Haneda (Japan)", zh: "東京羽田（日本）" },
    MNL: { vi: "Manila (Philippines)", en: "Manila (Philippines)", zh: "馬尼拉（菲律賓）" },
    PEK: { vi: "Bắc Kinh (Trung Quốc)", en: "Beijing Capital (China)", zh: "北京首都（中國）" },
    SYD: { vi: "Sydney (Úc)", en: "Sydney Kingsford Smith (Australia)", zh: "雪梨（澳洲）" },
    CDG: { vi: "Paris (Pháp)", en: "Paris Charles de Gaulle (France)", zh: "巴黎戴高樂（法國）" },
    JFK: { vi: "New York (Mỹ)", en: "New York JFK (USA)", zh: "紐約甘迺迪（美國）" }
};

function getLocalizedAirportName(code) {
    const item = AIRPORT_NAMES_I18N[code];
    if (!item) return code;
    return item[currentLang] || item.vi;
}

const WOW_I18N = {
    vi: {
        shortMin: "p",
        unitMin: "phút",
        unitHr: "giờ",
        vnGroup: "🇻🇳 Việt Nam (22)",
        intGroup: "🌏 Quốc tế (12)",
        originTitle: "Điểm khởi hành",
        destTitle: "Điểm hạ cánh",
        autoDurTitle: "⏱️ Thời gian học (Tính theo khoảng cách)",
        btnPickSeat: "💺 Chọn Ghế & In Vé",
        btnFlyNow: "🛫 Bay Ngay Lập Tức",
        btnCollapse: "🔽 Thu gọn bảng",
        btnExpand: "🔼 Mở bảng",
        btnGlobe3D: "🌍 Quả cầu 3D",
        btnMap2D: "🛰️ Bản đồ 2D",
        btnBackBooking: "‹ Quay lại",
        seatHint: "Chạm vào ghế bất kỳ hoặc bấm Tiếp tục",
        btnContinueTicket: "Tiếp tục ➔",
        btnConfirmSeat: "Xác nhận & Xuất Vé Boarding Pass ➔",
        strictSub: "Cảnh báo nếu rời khỏi màn hình học",
        btnChangeSeat: "‹ Đổi ghế",
        btnTakeoffTicket: "🛫 Cất Cánh Bắt Đầu Học",
        btnDoneFlight: "✓ Xong",
        btnAbortFlight: "Hủy",
        btnReadingLight: "💡 Đèn đọc sách",
        btnTrayTable: "🍱 Gấp/Mở bàn học",
        btnMoodLight: "🌈 Đèn LED trần",
        btnCallFA: "🛎️ Gọi tiếp viên",
        btnWindowShade: "🪟 Kéo Rèm Cửa Sổ Lên / Xuống",
        passportBtn: "Hộ Chiếu & VIP",
        fidsBadge: "🛫 FIDS • DEPARTURE STUDY BOARD",
        fidsTitle: "Bảng Điện Tử Lịch Bay Học Tập Trong Ngày",
        fidsSync: "● Dữ liệu thật từ Thời Gian Biểu",
        fidsCol1: "GIỜ HỌC",
        fidsCol2: "CHUYẾN BAY",
        fidsCol3: "MÔN HỌC / NHIỆM VỤ",
        fidsCol4: "TRẠNG THÁI",
        fidsCol5: "CẤT CÁNH",
        fidsEmpty: "📡 [STANDBY] Chưa có ca học nào trên bảng điện tử FIDS hôm nay. Hãy thêm lịch ở khung Thời Gian Biểu bên dưới để lên bảng điện tử!",
        fidsFlyBtn: "Bay",
        radarOn: "📡 Vị trí 6 TV: BẬT",
        radarOff: "📡 Vị trí 6 TV: TẮT",
        standbyTag: "Chờ lịch",
        standbyPopupTitle: "Đang đỗ tại",
        standbyPopupDesc: "Chưa có lịch học nào được thêm. Hãy chuyển sang hồ sơ này và thêm lịch học để cất cánh!",
        flyingPopupTitle: "Đang bay theo lịch",
        routeLabel: "Chặng",
        taskLabel: "Nhiệm vụ",
        voiceOn: "🔊 Cơ trưởng & ATC: BẬT",
        voiceOff: "🔇 Cơ trưởng & ATC: TẮT",
        wxClear: "☀️ Quang đãng",
        wxCloud: "⛅ Có mây",
        wxRain: "🌧️ Mưa",
        wxAt: "tại",
        wxWind: "Gió",
        dlTicketBtn: "📸 Tải ảnh Vé Boarding Pass (PNG - Tùy chọn)",
        vipMenuLabel: "🍽️ Menu VIP:",
        itemBoba: "🧋 Trà sữa",
        itemMatcha: "🍵 Matcha",
        itemCoffee: "☕ Cà phê",
        itemCroissant: "🥐 Bánh",
        atcAudioBtn: "🔊/🔇 Tiếng",
        atcSkipBtn: "Bỏ qua ➔ Bay luôn",
        zenBtn: "🧘 Zen HUD",
        zenLofiBtn: "🎵 Bật/Tắt Lofi",
        zenBackBtn: "🔙 Quay lại Buồng lái",
        passModalTitle: "🛂 Cuốn Hộ Chiếu 3D, Hạng Thẻ VIP & Trạng Thái 6 Thành Viên",
        passCloseBtn: "Đóng Hộ Chiếu",
        passBase: "Sân bay căn cứ",
        passMiles: "Tích lũy",
        passLanded: "Đã hạ cánh",
        passFlights: "chuyến",
        passStampsTitle: "💮 Con dấu Nhập cảnh (Chỉ đóng dấu khi hoàn thành ca học thật):",
        passEmptyStamps: "🛂 Chưa có con dấu nhập cảnh nào. Hãy hoàn thành 1 chuyến bay học tập để nhận con dấu đầu tiên!",
        passSquadronTitle: "📊 Trạng thái Thực tế của 6 Thành Viên (6 Sân bay căn cứ VN):",
        passHasSched: "🛫 Đang có lịch",
        passNoSched: "🛬 Đang đỗ tại",
        passNoSchedSub: "Chưa thêm lịch học",
        passDone: "xong",
        passWait: "chờ",
        months: ["Tháng 1", "Tháng 2", "Tháng 3", "Tháng 4", "Tháng 5", "Tháng 6", "Tháng 7", "Tháng 8", "Tháng 9", "Tháng 10", "Tháng 11", "Tháng 12"],
        phQuickTask: "Nhập tên công việc (VD: Giải đề Toán, Tạo app...)",
        phSlotSubj: "Nhập môn học, ca làm, sự kiện (VD: Toán, Đi làm, Họp CLB...)",
        phFocusInput: "Nhập mục tiêu (VD: Toán, Tạo app...)",
        phChat: "Nhập tin nhắn...",
        slotTypes: [
            "📚 Lịch học / Ôn bài (Tạo chuyến bay)",
            "🔴 Lịch học trên trường (Cố định)",
            "🟣 Việc cá nhân (Đi làm, sự kiện...)",
            "🟢 Khung giờ trống tự học"
        ],
        repeatModes: [
            "1️⃣ Không lặp lại (Chỉ ngày này)",
            "🔄 Hàng tuần (Cùng Thứ mỗi tuần)",
            "🗓️ Hàng tháng (Cùng Ngày này mỗi tháng)",
            "📆 Hàng năm (Cùng Ngày/Tháng mỗi năm)",
            "☀️ Hàng ngày (Mỗi ngày)",
            "⚙️ Tùy chỉnh chu kỳ (Tự nhập bao lâu tùy ý)..."
        ],
        customRepeatLbl: "⚙️ Lặp lại mỗi:",
        customRepeatInLbl: "Trong:",
        customUnits: ["Ngày", "Tuần", "Tháng", "Năm"],
        qChat1: "💡 Hôm nay học gì?",
        qChat2: "📋 Việc đang làm",
        qChat3: "🌪️ Dời lịch"
    },
    en: {
        shortMin: "m",
        unitMin: "mins",
        unitHr: "hrs",
        vnGroup: "🇻🇳 Vietnam Domestic (22)",
        intGroup: "🌏 International (12)",
        originTitle: "Departure",
        destTitle: "Destination",
        autoDurTitle: "⏱️ Study Duration (Calculated by Distance)",
        btnPickSeat: "💺 Select Seat & Ticket",
        btnFlyNow: "🛫 Fly Immediately",
        btnCollapse: "🔽 Collapse Panel",
        btnExpand: "🔼 Expand Panel",
        btnGlobe3D: "🌍 3D Globe",
        btnMap2D: "🛰️ 2D Map",
        btnBackBooking: "‹ Back",
        seatHint: "Tap any seat or click Continue",
        btnContinueTicket: "Continue ➔",
        btnConfirmSeat: "Confirm & Issue Boarding Pass ➔",
        strictSub: "Alert if you leave the study screen",
        btnChangeSeat: "‹ Change Seat",
        btnTakeoffTicket: "🛫 Takeoff & Start Studying",
        btnDoneFlight: "✓ Done",
        btnAbortFlight: "Abort",
        btnReadingLight: "💡 Reading Light",
        btnTrayTable: "🍱 Tray Table",
        btnMoodLight: "🌈 Cabin LED",
        btnCallFA: "🛎️ Call Crew",
        btnWindowShade: "🪟 Toggle Window Shade",
        passportBtn: "Passport & VIP",
        fidsBadge: "🛫 FIDS • DEPARTURE STUDY BOARD",
        fidsTitle: "Daily Study Flights Departure Board",
        fidsSync: "● Live Data from Personal Schedule",
        fidsCol1: "TIME",
        fidsCol2: "FLIGHT",
        fidsCol3: "SUBJECT / TASK",
        fidsCol4: "STATUS",
        fidsCol5: "ACTION",
        fidsEmpty: "📡 [STANDBY] No study flights scheduled on the FIDS board today. Add an event in the Monthly Calendar below to list your flight!",
        fidsFlyBtn: "Fly",
        radarOn: "📡 6-Member Radar: ON",
        radarOff: "📡 6-Member Radar: OFF",
        standbyTag: "Standby",
        standbyPopupTitle: "Parked at",
        standbyPopupDesc: "No study schedule added yet. Switch to this profile and add a schedule to take off!",
        flyingPopupTitle: "Flying on schedule",
        routeLabel: "Route",
        taskLabel: "Task",
        voiceOn: "🔊 Captain & ATC: ON",
        voiceOff: "🔇 Captain & ATC: OFF",
        wxClear: "☀️ Clear",
        wxCloud: "⛅ Cloudy",
        wxRain: "🌧️ Rain",
        wxAt: "at",
        wxWind: "Wind",
        dlTicketBtn: "📸 Download Boarding Pass Image (PNG - Optional)",
        vipMenuLabel: "🍽️ VIP Menu:",
        itemBoba: "🧋 Boba Tea",
        itemMatcha: "🍵 Matcha",
        itemCoffee: "☕ Espresso",
        itemCroissant: "🥐 Croissant",
        atcAudioBtn: "🔊/🔇 Audio",
        atcSkipBtn: "Skip ➔ Fly Now",
        zenBtn: "🧘 Zen HUD",
        zenLofiBtn: "🎵 Toggle Lofi",
        zenBackBtn: "🔙 Back to Cockpit",
        passModalTitle: "🛂 3D Passport, VIP Tier & 6-Member Squadron Status",
        passCloseBtn: "Close Passport",
        passBase: "Base Airport",
        passMiles: "Total Miles",
        passLanded: "Landed",
        passFlights: "flights",
        passStampsTitle: "💮 Immigration Stamps (Earned by completing real study flights):",
        passEmptyStamps: "🛂 No immigration stamps yet. Complete your first study flight to earn a stamp!",
        passSquadronTitle: "📊 Real-Time Status of 6 Members (6 Vietnam Base Airports):",
        passHasSched: "🛫 Scheduled",
        passNoSched: "🛬 Parked at",
        passNoSchedSub: "No schedule yet",
        passDone: "done",
        passWait: "pending",
        months: ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
        phQuickTask: "Enter task name (e.g., Math practice, Build app...)",
        phSlotSubj: "Enter subject, shift, or event (e.g., Math, Work, Club...)",
        phFocusInput: "Enter focus goal (e.g., Math, Coding...)",
        phChat: "Type a message...",
        slotTypes: [
            "📚 Study / Review (Create Flight)",
            "🔴 School Class (Fixed)",
            "🟣 Personal Event (Work, Club...)",
            "🟢 Free Self-Study Slot"
        ],
        repeatModes: [
            "1️⃣ Does not repeat (This date only)",
            "🔄 Weekly (Same day of week)",
            "🗓️ Monthly (Same day each month)",
            "📆 Yearly (Same date each year)",
            "☀️ Daily (Every day)",
            "⚙️ Custom recurrence (Set interval)..."
        ],
        customRepeatLbl: "⚙️ Repeat every:",
        customRepeatInLbl: "For:",
        customUnits: ["Days", "Weeks", "Months", "Years"],
        qChat1: "💡 What to study?",
        qChat2: "📋 Pending tasks",
        qChat3: "🌪️ Reschedule"
    },
    zh: {
        shortMin: "分",
        unitMin: "分鐘",
        unitHr: "小時",
        vnGroup: "🇻🇳 越南國內線 (22)",
        intGroup: "🌏 國際航線 (12)",
        originTitle: "出發機場",
        destTitle: "目的地機場",
        autoDurTitle: "⏱️ 專注學習時長（依航程距離計算）",
        btnPickSeat: "💺 選擇座位 & 登機證",
        btnFlyNow: "🛫 立即起飛",
        btnCollapse: "🔽 收合面板",
        btnExpand: "🔼 展開面板",
        btnGlobe3D: "🌍 3D 地球儀",
        btnMap2D: "🛰️ 2D 衛星圖",
        btnBackBooking: "‹ 返回",
        seatHint: "點擊任意座位或按繼續",
        btnContinueTicket: "繼續 ➔",
        btnConfirmSeat: "確認座位並印製登機證 ➔",
        strictSub: "離開學習畫面時將發出警報",
        btnChangeSeat: "‹ 更換座位",
        btnTakeoffTicket: "🛫 起飛開始專注學習",
        btnDoneFlight: "✓ 完成",
        btnAbortFlight: "取消",
        btnReadingLight: "💡 閱讀燈",
        btnTrayTable: "🍱 摺疊桌板",
        btnMoodLight: "🌈 機艙氛圍燈",
        btnCallFA: "🛎️ 呼叫空服員",
        btnWindowShade: "🪟 拉起 / 放下遮陽板",
        passportBtn: "護照與 VIP",
        fidsBadge: "🛫 FIDS • 專注航班電子看板",
        fidsTitle: "當日專注學習航班時刻表",
        fidsSync: "● 來自個人行事曆的即時數據",
        fidsCol1: "學習時間",
        fidsCol2: "航班編號",
        fidsCol3: "科目 / 任務內容",
        fidsCol4: "航班狀態",
        fidsCol5: "起飛",
        fidsEmpty: "📡 [待命] 今日 FIDS 電子看板尚無學習航班。請於下方萬年曆新增行程以登上電子看板！",
        fidsFlyBtn: "起飛",
        radarOn: "📡 6成員雷達：開啟",
        radarOff: "📡 6成員雷達：關閉",
        standbyTag: "待命中",
        standbyPopupTitle: "停靠於",
        standbyPopupDesc: "尚無安排任何學習行程。請切換至此成員檔案並新增行程即可起飛！",
        flyingPopupTitle: "依行程飛行中",
        routeLabel: "航線",
        taskLabel: "任務",
        voiceOn: "🔊 機長與塔台語音：開啟",
        voiceOff: "🔇 機長與塔台語音：關閉",
        wxClear: "☀️ 晴朗",
        wxCloud: "⛅ 多雲",
        wxRain: "🌧️ 降雨",
        wxAt: "於",
        wxWind: "風速",
        dlTicketBtn: "📸 下載登機證圖片（PNG - 選用）",
        vipMenuLabel: "🍽️ VIP 餐點：",
        itemBoba: "🧋 珍珠奶茶",
        itemMatcha: "🍵 抹茶拿鐵",
        itemCoffee: "☕ 濃縮咖啡",
        itemCroissant: "🥐 可頌麵包",
        atcAudioBtn: "🔊/🔇 語音",
        atcSkipBtn: "跳過 ➔ 立即起飛",
        zenBtn: "🧘 專注 HUD",
        zenLofiBtn: "🎵 切換 Lofi 音樂",
        zenBackBtn: "🔙 返回駕駛艙",
        passModalTitle: "🛂 3D 護照、VIP 等級與 6 成員即時狀態",
        passCloseBtn: "關閉護照",
        passBase: "基地機場",
        passMiles: "累計里程",
        passLanded: "已降落",
        passFlights: "趟航班",
        passStampsTitle: "💮 入境印章收藏（完成真實專注航班即可獲得）：",
        passEmptyStamps: "🛂 目前尚無任何入境印章。完成您的第一趟專注學習航班即可蓋章！",
        passSquadronTitle: "📊 6 位成員即時狀態（越南 6 大基地機場）：",
        passHasSched: "🛫 已排程",
        passNoSched: "🛬 停靠於",
        passNoSchedSub: "尚未新增行程",
        passDone: "完成",
        passWait: "待辦",
        months: ["1月", "2月", "3月", "4月", "5月", "6月", "7月", "8月", "9月", "10月", "11月", "12月"],
        phQuickTask: "輸入任務名稱（例如：解數學題、開發專案...）",
        phSlotSubj: "輸入科目、班表或事件（例如：數學、打工、社團...）",
        phFocusInput: "輸入專注目標（例如：微積分、寫程式...）",
        phChat: "輸入訊息...",
        slotTypes: [
            "📚 學習 / 複習（建立專注航班）",
            "🔴 學校固定課程",
            "🟣 個人事項（打工、社團...）",
            "🟢 空閒自習時段"
        ],
        repeatModes: [
            "1️⃣ 不重複（僅限此日）",
            "🔄 每週（每週同一天）",
            "🗓️ 每月（每月同一日）",
            "📆 每年（每年同月同日）",
            "☀️ 每天（每日重複）",
            "⚙️ 自訂重複週期..."
        ],
        customRepeatLbl: "⚙️ 重複頻率：",
        customRepeatInLbl: "持續：",
        customUnits: ["天", "週", "個月", "年"],
        qChat1: "💡 今天學什麼？",
        qChat2: "📋 待辦任務",
        qChat3: "🌪️ 順延行程"
    }
};

function getW() {
    return WOW_I18N[currentLang] || WOW_I18N.vi;
}

// ================= 2. GHI ĐÈ TRỰC TIẾP CÁC HÀM XỬ LÝ NGÔN NGỮ, ĐƠN VỊ PHÚT & SÂN BAY =================
window.getLunarDateInfo = function(year, month, day) {
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
            fullEn: `Lunar Date: ${String(lDay).padStart(2,'0')}/${String(lMonth).padStart(2,'0')} (Lunar Calendar)`,
            fullZh: `農曆 ${lMonth}月${lDay}日 • ${canChiZh}`
        };
    } catch (e) {
        return { lDay: day, lMonth: month, shortStr: `${day}`, fullVi: "Âm lịch", fullEn: "Lunar", fullZh: "農曆" };
    }
};

window.updateSlotDurationPreview = function() {
    const s = document.getElementById('new-slot-start').value;
    const e = document.getElementById('new-slot-end').value;
    const mins = calcMinutesBetweenTimes(s, e);
    const matchedAirport = findBestAirportForDuration(mins);
    const w = getW();
    setTextIfExist('calc-slot-mins-preview', `${mins}${w.shortMin} (✈️${matchedAirport.code})`);
};

window.formatDurationLabel = function(mins) {
    const w = getW();
    if (mins < 60) return `${mins} ${w.unitMin}`;
    const h = Math.floor(mins / 60), m = mins % 60;
    return m > 0 ? `${h}h ${m}${w.shortMin} (${mins} ${w.unitMin})` : `${h} ${w.unitHr} (${mins} ${w.unitMin})`;
};

window.initAirportDropdowns = function() {
    const oSel = document.getElementById('origin-select');
    const dSel = document.getElementById('dest-select');
    const qSel = document.getElementById('quick-task-dest');
    const w = getW();

    const prevOrigin = (oSel && oSel.value) ? oSel.value : originAirport.code;
    const prevDest = (dSel && dSel.value) ? dSel.value : destAirport.code;
    const prevQuick = (qSel && qSel.value) ? qSel.value : "DAD";

    const vnAirports = AIRPORTS.filter(a => a.group === 'VN');
    const intAirports = AIRPORTS.filter(a => a.group === 'INT');

    const buildOptions = (withTimeHint = false) => {
        let html = `<optgroup label="${w.vnGroup}" class="bg-slate-900">`;
        vnAirports.forEach(a => {
            const dist = calcDistanceKm(originAirport.coords, a.coords);
            const mins = calcStudyDurationFromDistance(dist, "Airbus A321neo");
            const localName = getLocalizedAirportName(a.code);
            html += `<option value="${a.code}">${a.code} - ${localName} ${withTimeHint ? `(~${mins}${w.shortMin})` : ''}</option>`;
        });
        html += `</optgroup><optgroup label="${w.intGroup}" class="bg-slate-900">`;
        intAirports.forEach(a => {
            const dist = calcDistanceKm(originAirport.coords, a.coords);
            const mins = calcStudyDurationFromDistance(dist, "Airbus A321neo");
            const localName = getLocalizedAirportName(a.code);
            html += `<option value="${a.code}">${a.code} - ${localName} ${withTimeHint ? `(~${mins}${w.shortMin})` : ''}</option>`;
        });
        html += `</optgroup>`;
        return html;
    };

    if (oSel) { oSel.innerHTML = buildOptions(false); oSel.value = prevOrigin; }
    if (dSel) { dSel.innerHTML = buildOptions(false); dSel.value = prevDest; }
    if (qSel) { qSel.innerHTML = buildOptions(true); qSel.value = prevQuick; }
};

window.updateBookingUI = function() {
    const specs = getAircraftSpecs(selectedAircraft);
    const box = document.getElementById('booking-plane-svg-box');
    if (box) box.innerHTML = getAircraftSVG(selectedAircraft, 45);
    setTextIfExist('badge-origin', originAirport.code);
    setTextIfExist('badge-dest', destAirport.code);
    setTextIfExist('badge-dist', `${currentDistance} km`);
    const oShort = getLocalizedAirportName(originAirport.code).split(' (')[0].split('（')[0];
    const dShort = getLocalizedAirportName(destAirport.code);
    setTextIfExist('banner-dest-title', `${oShort} ➔ ${dShort}`);
    setTextIfExist('auto-calc-duration-text', formatDurationLabel(selectedDuration));
    setTextIfExist('auto-calc-speed-text', `(${currentDistance} km • ${specs.speedKmh} km/h)`);

    const now = new Date();
    setTextIfExist('booking-realtime-eta', `${String(now.getHours()).padStart(2,'0')}:${String(now.getMinutes()).padStart(2,'0')} ➔ ${calcRealTimeETA(selectedDuration)}`);

    if (map && typeof L !== 'undefined') {
        if (routeLine) map.removeLayer(routeLine);
        if (originMarker) map.removeLayer(originMarker);
        if (destMarker) map.removeLayer(destMarker);

        originMarker = L.marker(originAirport.coords, { icon: createAirportBadge(originAirport.code, false) }).addTo(map);
        destMarker = L.marker(destAirport.coords, { icon: createAirportBadge(destAirport.code, true) }).addTo(map);
        routeLine = L.polyline([originAirport.coords, destAirport.coords], { color: '#38bdf8', weight: 3.5, dashArray: '8, 8', opacity: 0.95 }).addTo(map);

        if (is2DMapActive) { map.invalidateSize(true); map.fitBounds(routeLine.getBounds(), { padding: [90, 90], maxZoom: 7 }); }
    }
    update3DGlobeRouteArc();
    updateCameraViewsData();
};

// Ghi đè hàm setAppLanguage để chắc chắn 100% mọi nhãn đều đổi khi bấm VI / EN / 繁體
window.setAppLanguage = function(lang) {
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
    const w = getW();

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

    setTextIfExist('lbl-origin-title', w.originTitle);
    setTextIfExist('lbl-dest-title', w.destTitle);
    setTextIfExist('lbl-auto-dur-title', w.autoDurTitle);
    setTextIfExist('lbl-btn-pick-seat', w.btnPickSeat);
    setTextIfExist('lbl-btn-fly-now', w.btnFlyNow);
    setTextIfExist('toggle-booking-btn', isBookingCollapsed ? w.btnExpand : w.btnCollapse);
    setTextIfExist('quick-switch-proj-btn', is2DMapActive ? w.btnGlobe3D : w.btnMap2D);

    setSelectorText('button[onclick="backToBooking()"]', w.btnBackBooking);
    setSelectorText('button[onclick="showBoardingPass()"]', w.btnContinueTicket);
    setSelectorText('button[onclick="confirmSeatAndFocus()"]', w.btnConfirmSeat);
    setSelectorText('button[onclick="backToSeatFromTicket()"]', w.btnChangeSeat);
    setSelectorText('#screen-ticket button[onclick="startFlight()"]', w.btnTakeoffTicket);
    setSelectorText('button[onclick="completeFlightEarly()"]', w.btnDoneFlight);
    setSelectorText('button[onclick="abortFlight()"]', w.btnAbortFlight);
    setTextIfExist('btn-reading-light', w.btnReadingLight);
    setTextIfExist('btn-tray-table', w.btnTrayTable);
    setSelectorText('button[onclick="cycleCabinMoodLight()"]', w.btnMoodLight);
    setSelectorText('button[onclick="callFlightAttendant()"]', w.btnCallFA);
    setSelectorText('button[onclick="toggleWindowShade()"]', w.btnWindowShade);

    const wkRow = document.getElementById('calendar-weekdays-row');
    if (wkRow) wkRow.innerHTML = t.weekdays.map((wk, idx) => `<div class="${idx === 6 ? 'text-red-400' : ''}">${wk}</div>`).join('');

    updateWowLabelsByLang();
    initAirportDropdowns();
    updateSlotDurationPreview();
    updateBookingUI();
    updateRealTimeClock();
    renderCalendarGrid();
    renderDashboard();
    resetChat();
};

// ================= 3. CẤU HÌNH SÂN BAY CĂN CỨ CỦA 6 THÀNH VIÊN =================
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

function updateWowLabelsByLang() {
    const w = getW();
    setTextIfExist('lbl-passport-top', w.passportBtn);
    setTextIfExist('fids-badge-lbl', w.fidsBadge);
    setTextIfExist('fids-title-lbl', w.fidsTitle);
    setTextIfExist('fids-sync-lbl', w.fidsSync);
    setTextIfExist('fids-col-1', w.fidsCol1);
    setTextIfExist('fids-col-2', w.fidsCol2);
    setTextIfExist('fids-col-3', w.fidsCol3);
    setTextIfExist('fids-col-4', w.fidsCol4);
    setTextIfExist('fids-col-5', w.fidsCol5);

    setTextIfExist('btn-squadron-radar', squadronRadarEnabled ? w.radarOn : w.radarOff);
    setTextIfExist('btn-captain-voice-toggle', captainVoiceEnabled ? w.voiceOn : w.voiceOff);
    setTextIfExist('btn-download-ticket-png', w.dlTicketBtn);
    setTextIfExist('btn-zen-focus', w.zenBtn);
    setTextIfExist('zen-lofi-btn', w.zenLofiBtn);
    setTextIfExist('zen-back-btn', w.zenBackBtn);
    setTextIfExist('atc-mute-btn', w.atcAudioBtn);
    setTextIfExist('atc-skip-btn', w.atcSkipBtn);
    setTextIfExist('passport-modal-title', w.passModalTitle);
    setTextIfExist('passport-close-btn', w.passCloseBtn);
    setTextIfExist('vip-menu-title', w.vipMenuLabel);
    setTextIfExist('vip-btn-boba', w.itemBoba);
    setTextIfExist('vip-btn-matcha', w.itemMatcha);
    setTextIfExist('vip-btn-coffee', w.itemCoffee);
    setTextIfExist('vip-btn-croissant', w.itemCroissant);

    const mSel = document.getElementById('cal-month-select');
    if (mSel && mSel.options.length === 12) {
        for (let i = 0; i < 12; i++) mSel.options[i].text = w.months[i];
    }

    const qInput = document.getElementById('quick-task-title');
    if (qInput) qInput.placeholder = w.phQuickTask;
    const sInput = document.getElementById('new-slot-subject');
    if (sInput) sInput.placeholder = w.phSlotSubj;
    const fInput = document.getElementById('custom-focus-input');
    if (fInput) fInput.placeholder = w.phFocusInput;
    const cInput = document.getElementById('chat-input');
    if (cInput) cInput.placeholder = w.phChat;

    const typeSel = document.getElementById('new-slot-type');
    if (typeSel && typeSel.options.length === 4) {
        for (let i = 0; i < 4; i++) typeSel.options[i].text = w.slotTypes[i];
    }
    const repSel = document.getElementById('slot-repeat-mode');
    if (repSel && repSel.options.length === 6) {
        for (let i = 0; i < 6; i++) repSel.options[i].text = w.repeatModes[i];
    }

    const unitSel = document.getElementById('custom-repeat-unit');
    if (unitSel && unitSel.options.length === 4) {
        for (let i = 0; i < 4; i++) unitSel.options[i].text = w.customUnits[i];
    }

    const qBtns = document.querySelectorAll('#chatbot-window button[onclick^="sendQuickChat"]');
    if (qBtns.length >= 3) {
        qBtns[0].innerText = w.qChat1;
        qBtns[1].innerText = w.qChat2;
        qBtns[2].innerText = w.qChat3;
    }

    renderWeatherBadgeText();
    renderFidsDepartureBoard();
    renderSquadronRadarOn2DMap();
}

// ================= 4. RADAR 6 THÀNH VIÊN & BẢNG ĐIỆN TỬ FIDS =================
function renderSquadronRadarOn2DMap() {
    if (!map || typeof L === 'undefined') return;
    squadronMarkers2D.forEach(m => { try { map.removeLayer(m); } catch (e) {} });
    squadronMarkers2D = [];
    if (!squadronRadarEnabled) return;

    const w = getW();
    Object.keys(MEMBER_BASE_AIRPORTS).forEach((key, idx) => {
        if (key === currentMemberKey) return;
        const cfg = MEMBER_BASE_AIRPORTS[key];
        const homeAir = AIRPORTS.find(a => a.code === cfg.home) || AIRPORTS[0];
        const realTask = getMemberRealActiveTask(key);

        if (realTask) {
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
                <div class="font-black text-sm">✈️ ${cfg.name} (${w.flyingPopupTitle})</div>
                <div class="text-[11px] font-bold text-blue-700">${w.routeLabel}: ${cfg.home} ➔ ${destAir.code} • ⏰ ${realTask.slot}</div>
                <div class="text-[11px] mt-1">📚 ${w.taskLabel}: <b>${realTask.title}</b></div>
            </div>`);
            squadronMarkers2D.push(marker);
        } else {
            const icon = L.divIcon({
                className: 'squadron-standby-icon',
                html: `<div class="flex items-center gap-1 bg-slate-950/90 border border-white/25 text-slate-300 px-2 py-0.5 rounded-full text-[9px] font-bold shadow-lg whitespace-nowrap">
                    <span class="w-2 h-2 rounded-full" style="background:${cfg.color}"></span>
                    <span>${cfg.name} (${cfg.home} • ${w.standbyTag})</span>
                </div>`,
                iconSize: [110, 22], iconAnchor: [55, -10]
            });

            const marker = L.marker(homeAir.coords, { icon }).addTo(map);
            marker.bindPopup(`<div class="text-slate-900 text-xs font-sans p-1">
                <div class="font-black text-sm">🛬 ${cfg.name} (${w.standbyPopupTitle} ${cfg.home})</div>
                <div class="text-[11px] text-slate-600 mt-0.5">${w.standbyPopupDesc}</div>
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
    const w = getW();
    const btn = document.getElementById('btn-squadron-radar');
    if (btn) {
        btn.innerText = squadronRadarEnabled ? w.radarOn : w.radarOff;
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

function renderFidsDepartureBoard() {
    const container = document.getElementById('fids-board-rows');
    if (!container) return;

    const w = getW();
    const profile = appState.members[currentMemberKey];
    const homeCode = getMemberHomeAirportCode(currentMemberKey);
    const tasks = profile.tasks || [];

    const now = new Date();
    const curMins = now.getHours() * 60 + now.getMinutes();

    if (tasks.length === 0) {
        container.innerHTML = `<div class="col-span-12 py-4 text-center text-xs text-slate-400 font-mono">${w.fidsEmpty}</div>`;
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
                    ${!tk.done ? `<button onclick="startFlightFromTask(${tk.id})" class="bg-cyan-500 hover:bg-cyan-400 text-black font-sans font-black px-2 py-0.5 rounded text-[10px]">${w.fidsFlyBtn}</button>` : `<span class="text-emerald-400">✓</span>`}
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
        zenOverlay.classList.remove('hidden'); zenOverlay.classList.add('flex');
        syncZenHudTick();
    } else {
        zenOverlay.classList.add('hidden'); zenOverlay.classList.remove('flex');
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
    if (zenRoute) zenRoute.innerText = `✈️ ${originAirport.code} ➔ ${destAirport.code} • SEAT ${selectedSeat} • ${appState.members[currentMemberKey].name}`;
    if (zenBar) zenBar.style.width = `${(currentFlightProgress || 0) * 100}%`;
}
setInterval(syncZenHudTick, 500);

// ================= 5. ĐÀI ATC, GIỌNG CƠ TRƯỞNG, THỜI TIẾT & HỘ CHIẾU 3D =================
function toggleCaptainVoice() {
    captainVoiceEnabled = !captainVoiceEnabled;
    if (!captainVoiceEnabled && ('speechSynthesis' in window)) window.speechSynthesis.cancel();
    const w = getW();
    const btn = document.getElementById('btn-captain-voice-toggle');
    if (btn) {
        btn.innerText = captainVoiceEnabled ? w.voiceOn : w.voiceOff;
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

    if (currentLang === 'en') {
        stageText.innerHTML = `🗼 [ATC TOWER ${originAirport.code} - 118.1 MHz]: Taxi Clearance`;
        subText.innerHTML = `"${selectedAircraft}, Runway 25R clear, wind ${liveWeatherCache.wind} km/h. Cleared to taxi for departure to ${destAirport.code}!"`;
    } else if (currentLang === 'zh') {
        stageText.innerHTML = `🗼 [塔台管制 ${originAirport.code} - 118.1 MHz]：滑行許可`;
        subText.innerHTML = `「${selectedAircraft}，25R 跑道淨空，風速 ${liveWeatherCache.wind} km/h。允許滑行至跑道準備起飛前往 ${destAirport.code}！」`;
    } else {
        stageText.innerHTML = `🗼 [ATC TOWER ${originAirport.code} - 118.1 MHz]: Cấp huấn lệnh lăn bánh`;
        subText.innerHTML = `"${selectedAircraft}, đường băng 25R thông thoáng, gió ${liveWeatherCache.wind} km/h. Cho phép lăn ra đường băng chuẩn bị cất cánh đi ${destAirport.code}!"`;
    }
    prog.style.width = "33%";

    if (atcStepTimer1) clearTimeout(atcStepTimer1);
    if (atcStepTimer2) clearTimeout(atcStepTimer2);
    if (atcStepTimer3) clearTimeout(atcStepTimer3);

    atcStepTimer1 = setTimeout(() => {
        if (currentLang === 'en') {
            stageText.innerHTML = `🛞 [RUNWAY TAXIING]: Taxiing to Runway 25R...`;
            subText.innerHTML = `Focus Goal: "${selectedFocus.label}" • Passenger ${profile.name} (${tier.name}) seated at ${selectedSeat}.`;
        } else if (currentLang === 'zh') {
            stageText.innerHTML = `🛞 [跑道滑行]：飛機正滑行進入 25R 跑道...`;
            subText.innerHTML = `專注目標：「${selectedFocus.label}」• 旅客 ${profile.name} (${tier.name}) 就座於 ${selectedSeat}。`;
        } else {
            stageText.innerHTML = `🛞 [RUNWAY TAXIING]: Máy bay đang lăn ra đường băng 25R...`;
            subText.innerHTML = `Mục tiêu ca học: "${selectedFocus.label}" • Hành khách ${profile.name} (${tier.name}) ổn định tại ghế ${selectedSeat}.`;
        }
        prog.style.width = "68%";
    }, 2800);

    atcStepTimer2 = setTimeout(() => {
        stageText.innerHTML = `🎙️ [CAPTAIN PA]: V1... Rotate!`;
        let speechMsg = `Cơ trưởng xin chào hành khách ${profile.name}. Chuyến bay tập trung từ ${getLocalizedAirportName(originAirport.code).split(' (')[0]} đi ${getLocalizedAirportName(destAirport.code)} thời lượng ${selectedDuration} phút xin phép cất cánh!`;
        if (currentLang === 'en') speechMsg = `Captain speaking. Welcome passenger ${profile.name} aboard our focus flight from ${originAirport.code} to ${destAirport.code}. Flight time is ${selectedDuration} minutes. Cleared for takeoff!`;
        if (currentLang === 'zh') speechMsg = `機長廣播：歡迎旅客 ${profile.name} 搭乘從 ${originAirport.code} 前往 ${destAirport.code} 的專注航班，飛行時間 ${selectedDuration} 分鐘，現在起飛！`;
        subText.innerHTML = `"${speechMsg}"`;
        prog.style.width = "100%";
        speakCaptainAnnouncement(speechMsg);
    }, 5600);

    atcStepTimer3 = setTimeout(() => { closeAtcTaxiOverlay(); }, 10500);
}

function closeAtcTaxiOverlay() {
    if (atcStepTimer1) clearTimeout(atcStepTimer1);
    if (atcStepTimer2) clearTimeout(atcStepTimer2);
    if (atcStepTimer3) clearTimeout(atcStepTimer3);
    const overlay = document.getElementById('atc-taxi-overlay');
    if (overlay) { overlay.classList.add('hidden'); overlay.classList.remove('flex'); }
}

function renderWeatherBadgeText() {
    const badge = document.getElementById('live-weather-badge');
    if (!badge) return;
    const w = getW();
    const code = destAirport ? destAirport.code : "DAD";
    const icon = liveWeatherCache.code >= 51 ? w.wxRain : (liveWeatherCache.code >= 1 ? w.wxCloud : w.wxClear);
    badge.innerHTML = `${icon} ${w.wxAt} <b>${code}</b>: <b>${liveWeatherCache.temp}°C</b> • ${w.wxWind} ${liveWeatherCache.wind} km/h`;
}

async function updateDestinationLiveWeather(airportCode) {
    const air = AIRPORTS.find(a => a.code === airportCode) || destAirport;
    try {
        const res = await fetch(`https://api.open-meteo.com/v1/forecast?latitude=${air.coords[0]}&longitude=${air.coords[1]}&current_weather=true`);
        const data = await res.json();
        if (data && data.current_weather) {
            liveWeatherCache.temp = Math.round(data.current_weather.temperature);
            liveWeatherCache.wind = Math.round(data.current_weather.windspeed);
            liveWeatherCache.code = data.current_weather.weathercode;
        }
    } catch (e) {}
    renderWeatherBadgeText();
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
        origin: originCode, dest: destCode, dist: distKm, date: dateStr, subject: subject || "Focus Study"
    });
    savePersistentState();
}

function openPassportAndBlackboxModal() {
    const w = getW();
    const profile = appState.members[currentMemberKey];
    const homeCode = getMemberHomeAirportCode(currentMemberKey);
    const tier = getFrequentFlyerTier(profile.miles || 0);
    const stamps = profile.passportStamps || [];

    setTextIfExist('passport-modal-title', w.passModalTitle);
    setTextIfExist('passport-close-btn', w.passCloseBtn);

    let stampsHtml = stamps.length === 0
        ? `<div class="col-span-3 text-center py-6 bg-slate-900/50 rounded-2xl border border-dashed border-white/10 text-xs text-slate-400">${w.passEmptyStamps}</div>`
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
                        <span class="text-[9px] bg-blue-500/20 text-cyan-300 px-1.5 py-0.2 rounded">${w.passBase}: ${cfg.home}</span>
                        <span class="text-[9px] px-1.5 py-0.2 rounded border ${mTier.bg}">${mTier.name}</span>
                    </div>
                    <div class="text-[10px] text-slate-400 mt-0.5">
                        ${realTask ? `${w.passHasSched}: <b class="text-amber-300">${realTask.title}</b> (${realTask.slot})` : `${w.passNoSched} ${cfg.home} (${w.passNoSchedSub})`}
                    </div>
                </div>
                <div class="text-right font-mono">
                    <div class="text-xs font-black text-amber-300">${m.miles || 0} km</div>
                    <div class="text-[10px] text-emerald-400">${doneCount} ${w.passDone} • ${pendingCount} ${w.passWait}</div>
                </div>
            </div>
        `;
    }).join('');

    document.getElementById('passport-modal-body').innerHTML = `
        <div class="bg-gradient-to-r from-blue-950 via-slate-900 to-indigo-950 border border-amber-400/40 rounded-2xl p-3.5 mb-3 flex flex-wrap items-center justify-between gap-2">
            <div>
                <div class="text-[9px] text-amber-300 font-bold uppercase tracking-widest">PASSPORT & FREQUENT FLYER CARD</div>
                <div class="text-base font-black text-white mt-0.5">🛂 ${profile.name} • ${w.passBase}: ${homeCode}</div>
                <div class="text-xs text-cyan-300">${w.passMiles}: <b>${profile.miles || 0} km</b> • ${w.passLanded}: <b>${profile.flights || 0} ${w.passFlights}</b></div>
            </div>
            <div class="px-3 py-1.5 rounded-xl border font-black text-xs ${tier.bg}">${tier.name}</div>
        </div>
        <div class="text-xs font-extrabold text-amber-300 mb-2">${w.passStampsTitle}</div>
        <div class="grid grid-cols-2 sm:grid-cols-3 gap-2.5 mb-4 max-h-40 overflow-y-auto p-1">${stampsHtml}</div>
        <div class="text-xs font-extrabold text-cyan-300 mb-2">${w.passSquadronTitle}</div>
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
    if (!cardEl || typeof html2canvas === 'undefined') return;
    html2canvas(cardEl, { backgroundColor: '#03060f', scale: 2, useCORS: true }).then(canvas => {
        const a = document.createElement('a');
        a.download = `BoardingPass_${appState.members[currentMemberKey].name}_${originAirport.code}_${destAirport.code}.png`;
        a.href = canvas.toDataURL('image/png');
        a.click();
    });
}

// ================= 6. TỰ ĐỘNG NÂNG CẤP GIAO DIỆN ĐA NGÔN NGỮ =================
function injectWowUIElements() {
    const w = getW();
    try {
        const statName = document.getElementById('stat-member-name');
        if (statName && !document.getElementById('vip-tier-badge')) {
            const badge = document.createElement('span');
            badge.id = 'vip-tier-badge';
            badge.className = "ml-1.5 text-[10px] font-black px-2 py-0.5 rounded-full border";
            statName.parentElement.appendChild(badge);
        }
    } catch (e) {}

    try {
        const dashContainer = document.querySelector('#page-dashboard > div');
        if (dashContainer && !document.getElementById('fids-departure-board')) {
            const fidsBoard = document.createElement('div');
            fidsBoard.id = 'fids-departure-board';
            fidsBoard.className = "bg-gradient-to-b from-[#0b1326] to-[#060a14] border-2 border-amber-400/35 rounded-3xl p-4 shadow-2xl";
            fidsBoard.innerHTML = `
                <div class="flex flex-wrap items-center justify-between gap-2 pb-2.5 mb-2.5 border-b border-white/10">
                    <div class="flex items-center gap-2">
                        <span id="fids-badge-lbl" class="bg-amber-400 text-black font-mono font-black text-xs px-2.5 py-0.5 rounded uppercase tracking-wider">${w.fidsBadge}</span>
                        <span id="fids-title-lbl" class="text-xs font-extrabold text-white">${w.fidsTitle}</span>
                    </div>
                    <span id="fids-sync-lbl" class="text-[11px] font-mono text-emerald-400">${w.fidsSync}</span>
                </div>
                <div class="grid grid-cols-12 px-3 pb-1 text-[10px] font-mono font-bold text-slate-400 uppercase">
                    <div id="fids-col-1" class="col-span-2">${w.fidsCol1}</div>
                    <div id="fids-col-2" class="col-span-2">${w.fidsCol2}</div>
                    <div id="fids-col-3" class="col-span-5">${w.fidsCol3}</div>
                    <div id="fids-col-4" class="col-span-2 text-right">${w.fidsCol4}</div>
                    <div id="fids-col-5" class="col-span-1 text-right">${w.fidsCol5}</div>
                </div>
                <div id="fids-board-rows" class="space-y-1.5"></div>
            `;
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
            passBtn.innerHTML = `🛂 <span id="lbl-passport-top" class="hidden sm:inline">${w.passportBtn}</span>`;
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
            radBtn.innerText = w.radarOn;
            zoomCtrl.appendChild(radBtn);
        }
    } catch (e) {}

    try {
        const flyDockRight = document.querySelector('#screen-flying .flex.items-center.gap-1\\.5:last-child');
        if (flyDockRight && !document.getElementById('btn-zen-focus')) {
            const zenBtn = document.createElement('button');
            zenBtn.id = 'btn-zen-focus';
            zenBtn.onclick = toggleZenFocusHud;
            zenBtn.className = "bg-amber-400 hover:bg-amber-300 text-black px-2.5 py-1.5 rounded-xl text-[11px] font-black shadow";
            zenBtn.innerHTML = w.zenBtn;
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
                <span id="live-weather-badge" class="text-cyan-300 font-semibold">☀️ DAD: 28°C</span>
                <div class="flex items-center gap-1">
                    <button id="btn-captain-voice-toggle" onclick="toggleCaptainVoice()" class="bg-amber-500/20 text-amber-300 border border-amber-400/40 px-2 py-0.5 rounded-lg text-[10px] font-extrabold transition">${w.voiceOn}</button>
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
            dlBtn.innerHTML = w.dlTicketBtn;
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
                    <span id="vip-menu-title">${w.vipMenuLabel}</span>
                    <button id="vip-btn-boba" onclick="serveCabinItem('🧋','Boba Tea')" class="bg-white hover:bg-amber-100 px-2 py-0.5 rounded-lg shadow-sm">${w.itemBoba}</button>
                    <button id="vip-btn-matcha" onclick="serveCabinItem('🍵','Matcha Latte')" class="bg-white hover:bg-emerald-100 px-2 py-0.5 rounded-lg shadow-sm">${w.itemMatcha}</button>
                    <button id="vip-btn-coffee" onclick="serveCabinItem('☕','Espresso')" class="bg-white hover:bg-amber-100 px-2 py-0.5 rounded-lg shadow-sm">${w.itemCoffee}</button>
                    <button id="vip-btn-croissant" onclick="serveCabinItem('🥐','Croissant')" class="bg-white hover:bg-yellow-100 px-2 py-0.5 rounded-lg shadow-sm">${w.itemCroissant}</button>
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
                <div id="atc-taxi-overlay" style="z-index: 8200;" class="fixed top-16 left-1/2 -translate-x-1/2 w-[94%] max-w-lg glass-panel rounded-3xl p-4 border-2 border-amber-400/50 shadow-2xl hidden flex-col gap-2">
                    <div class="flex items-center justify-between">
                        <span id="atc-stage-text" class="text-xs font-black text-amber-300 uppercase tracking-wider">🗼 [ATC TOWER]</span>
                        <div class="flex items-center gap-1.5">
                            <button id="atc-mute-btn" onclick="toggleCaptainVoice()" class="text-[10px] bg-white/10 hover:bg-white/20 text-white px-2 py-0.5 rounded-lg font-bold">${w.atcAudioBtn}</button>
                            <button id="atc-skip-btn" onclick="closeAtcTaxiOverlay()" class="text-[10px] bg-emerald-500 hover:bg-emerald-400 text-black font-black px-2.5 py-0.5 rounded-lg">${w.atcSkipBtn}</button>
                        </div>
                    </div>
                    <div id="atc-sub-text" class="text-xs text-slate-200 leading-relaxed font-mono bg-black/40 p-2.5 rounded-xl border border-white/10"></div>
                    <div class="w-full bg-slate-800 h-1.5 rounded-full overflow-hidden">
                        <div id="atc-taxi-bar" class="bg-gradient-to-r from-amber-400 to-emerald-400 h-full w-1/3 transition-all duration-700"></div>
                    </div>
                </div>

                <div id="zen-focus-hud-overlay" style="z-index: 8800;" class="fixed inset-0 bg-[#03060f]/90 backdrop-blur-2xl hidden flex-col items-center justify-center p-6 text-center">
                    <div id="zen-route-label" class="text-xs font-mono font-bold text-cyan-400 tracking-widest uppercase mb-2">✈️ SGN ➔ DAD • SEAT 06A</div>
                    <div id="zen-task-label" class="text-xl sm:text-3xl font-extrabold text-white mb-4 max-w-2xl">💻 Focus Study</div>
                    <div id="zen-big-timer" class="mono text-6xl sm:text-8xl font-black text-amber-400 tracking-tight my-4 drop-shadow-[0_0_35px_rgba(250,204,21,0.35)]">55:00</div>
                    <div class="w-full max-w-md bg-slate-800 h-2.5 rounded-full overflow-hidden my-6 border border-white/10">
                        <div id="zen-progress-bar" class="bg-gradient-to-r from-cyan-400 to-amber-400 h-full w-0 transition-all duration-500"></div>
                    </div>
                    <div class="flex items-center gap-3">
                        <button id="zen-lofi-btn" onclick="toggleLofi()" class="bg-slate-800 hover:bg-slate-700 text-slate-200 font-bold px-4 py-2.5 rounded-2xl text-xs border border-white/15">${w.zenLofiBtn}</button>
                        <button id="zen-back-btn" onclick="toggleZenFocusHud()" class="bg-gradient-to-r from-cyan-500 to-blue-600 text-white font-black px-6 py-2.5 rounded-2xl text-xs shadow-xl">${w.zenBackBtn}</button>
                    </div>
                </div>

                <div id="passport-blackbox-modal" style="z-index: 9200;" class="fixed inset-0 bg-black/80 backdrop-blur-md hidden items-center justify-center p-4">
                    <div class="glass-panel w-full max-w-2xl rounded-3xl p-5 shadow-2xl border border-amber-400/40">
                        <div class="flex justify-between items-center mb-3 pb-2 border-b border-white/10">
                            <h3 id="passport-modal-title" class="text-sm sm:text-base font-black text-amber-300">${w.passModalTitle}</h3>
                            <button onclick="closePassportAndBlackboxModal()" class="text-slate-400 hover:text-white text-lg font-bold">✕</button>
                        </div>
                        <div id="passport-modal-body"></div>
                        <button id="passport-close-btn" onclick="closePassportAndBlackboxModal()" class="mt-4 w-full bg-gradient-to-r from-amber-500 to-yellow-500 text-black font-black py-2.5 rounded-xl text-xs uppercase">${w.passCloseBtn}</button>
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
try { setAppLanguage(currentLang); } catch (e) {}
