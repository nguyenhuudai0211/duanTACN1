from pathlib import Path
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="StudyHub & 3D Flight Sim (VI / EN / 繁體中文)",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="collapsed"
)

BASE_DIR = Path(__file__).parent

def read_source_file(filename: str) -> str:
    target = BASE_DIR / filename
    if target.exists():
        return target.read_text(encoding="utf-8")
    for p in BASE_DIR.iterdir():
        if p.is_file() and p.name.strip().lower() == filename.lower():
            return p.read_text(encoding="utf-8")
    return ""

css_content = read_source_file("styles.css")
layout_content = read_source_file("layout.html")
data_i18n_js = read_source_file("data_i18n.js")
logic_dashboard_js = read_source_file("logic_dashboard.js")
logic_flight_js = read_source_file("logic_flight.js")
features_wow_js = read_source_file("features_wow.js")

# Dự phòng nếu bạn vẫn còn giữ script_logic.js cũ
fallback_logic_js = ""
if not (logic_dashboard_js and logic_flight_js):
    fallback_logic_js = read_source_file("script_logic.js")

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

app_html = f"""<!DOCTYPE html>
<html lang="vi" translate="no" class="notranslate">
<head>
    <meta charset="UTF-8">
    <meta name="google" content="notranslate">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
    <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/html2canvas/1.4.1/html2canvas.min.js"></script>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@500;700;800&family=Noto+Sans+TC:wght@400;500;700;900&display=swap" rel="stylesheet">
    <style>
{css_content}
    </style>
</head>
<body class="relative w-screen h-screen overflow-hidden bg-[#03060f] notranslate" translate="no">
{layout_content}
    <script>
{data_i18n_js}
    </script>
    <script>
{logic_dashboard_js}
{logic_flight_js}
{features_wow_js}
{fallback_logic_js}
    </script>
</body>
</html>
"""

components.html(app_html, height=800, scrolling=False)
