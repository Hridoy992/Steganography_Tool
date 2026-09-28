import streamlit as st
from PIL import Image
import numpy as np
import io


# ----------------------------------------------------------------------
# Streamlit UI
# ----------------------------------------------------------------------

st.set_page_config(page_title="Image Steganography Tool", page_icon="🔐", layout="centered")

# ----------------------------------------------------------------------
# Custom Theme (colorful "cyber" look instead of the default plain background)
# ----------------------------------------------------------------------
CUSTOM_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;600;700&family=JetBrains+Mono:wght@400;600&display=swap');

/* Page background: deep navy-to-violet gradient with soft glow accents */
.stApp {
    background:
        radial-gradient(circle at 15% 20%, rgba(0, 217, 255, 0.12) 0%, transparent 40%),
        radial-gradient(circle at 85% 80%, rgba(255, 46, 151, 0.12) 0%, transparent 40%),
        linear-gradient(160deg, #0b0d2a 0%, #17123f 45%, #1a0e33 100%);
    color: #e8e8f4;
    font-family: 'Space Grotesk', sans-serif;
}

/* Title */
h1 {
    font-family: 'Space Grotesk', sans-serif;
    font-weight: 700;
    background: linear-gradient(90deg, #00d9ff 0%, #7b5cff 50%, #ff2e97 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}

h2, h3 { color: #f1f0ff; font-family: 'Space Grotesk', sans-serif; }

/* Caption under the title */
[data-testid="stCaptionContainer"], .stCaption {
    color: #9d9dc7 !important;
}

/* Tabs */
.stTabs [data-baseweb="tab-list"] {
    gap: 8px;
    border-bottom: 1px solid rgba(255,255,255,0.08);
}
.stTabs [data-baseweb="tab"] {
    background-color: rgba(255,255,255,0.03);
    border-radius: 10px 10px 0 0;
    color: #9d9dc7;
    padding: 8px 18px;
}
.stTabs [aria-selected="true"] {
    background: linear-gradient(90deg, rgba(0,217,255,0.15), rgba(255,46,151,0.15));
    color: #ffffff !important;
    border-bottom: 2px solid #00d9ff;
}

/* Buttons */
.stButton > button {
    background: linear-gradient(90deg, #00d9ff 0%, #7b5cff 60%, #ff2e97 100%);
    color: #0b0d2a;
    font-weight: 700;
    border: none;
    border-radius: 8px;
    padding: 0.55em 1.4em;
    transition: transform 0.15s ease, box-shadow 0.15s ease;
    box-shadow: 0 4px 18px rgba(123, 92, 255, 0.35);
}
.stButton > button:hover {
    transform: translateY(-1px);
    box-shadow: 0 6px 22px rgba(0, 217, 255, 0.45);
    color: #0b0d2a;
}

/* Text areas / text inputs */
.stTextArea textarea, .stTextInput input {
    background-color: rgba(255,255,255,0.04) !important;
    color: #f1f0ff !important;
    border: 1px solid rgba(123, 92, 255, 0.35) !important;
    border-radius: 8px !important;
}
.stTextArea textarea:focus, .stTextInput input:focus {
    border: 1px solid #00d9ff !important;
    box-shadow: 0 0 0 1px #00d9ff !important;
}

/* File uploader */
[data-testid="stFileUploaderDropzone"] {
    background-color: rgba(255,255,255,0.03);
    border: 1px dashed rgba(0, 217, 255, 0.4);
    border-radius: 12px;
}

/* Checkbox label */
.stCheckbox label p { color: #d8d8f0 !important; }

/* Alerts (info / success / warning / error) get a colorful left border */
div[data-testid="stAlert"] {
    border-radius: 10px;
    background-color: rgba(255,255,255,0.04);
}

/* Code / monospace accents used for the delimiter or capacity text */
code {
    color: #00d9ff;
    background: rgba(0, 217, 255, 0.08);
}

/* Horizontal divider */
hr { border-color: rgba(255,255,255,0.08); }

/* Footer caption */
.footer-note { color: #75759e; font-size: 0.85em; }
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

st.title("🔐 Image Steganography Tool")
st.caption("Hide and reveal secret messages inside images using LSB steganography")

tab1, tab2, tab3 = st.tabs(["🙈 Hide Message", "🔍 Reveal Message", "ℹ️ How it works"])
