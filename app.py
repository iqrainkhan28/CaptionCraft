import streamlit as st
from PIL import Image
import os
from streamlit_extras.switch_page_button import switch_page
from deep_translator import GoogleTranslator

st.set_page_config(page_title="CaptionCraft", page_icon="📸", layout="wide")

# ===== LANGUAGE OPTIONS (Supported by deep_translator) =====
language_options = {
    "en": "English",
    "mr": "Marathi",
    "as": "Assamese", "bn": "Bengali", "gu": "Gujarati", "hi": "Hindi", "kn": "Kannada",
    "ml": "Malayalam", "ne": "Nepali", "or": "Odia", "pa": "Punjabi", "sa": "Sanskrit",
    "sd": "Sindhi", "ta": "Tamil", "te": "Telugu", "ur": "Urdu",
    "de": "German", "fr": "French", "ja": "Japanese"
}

# ===== INITIALIZE SESSION STATE =====
if "selected_lang_code" not in st.session_state:
    st.session_state.selected_lang_code = "en"
if "selected_lang_name" not in st.session_state:
    st.session_state.selected_lang_name = "English"

# ===== LANGUAGE SELECTOR WITH on_change =====
def update_language():
    selected = st.session_state.lang_selector
    st.session_state.selected_lang_name = selected
    st.session_state.selected_lang_code = [code for code, name in language_options.items() if name == selected][0]

st.selectbox(
    "🌐 Choose Language",
    options=list(language_options.values()),
    index=list(language_options.values()).index(st.session_state.selected_lang_name),
    key="lang_selector",
    on_change=update_language
)

selected_lang_code = st.session_state.selected_lang_code
selected_lang_name = st.session_state.selected_lang_name

def t(text):
    try:
        return GoogleTranslator(source='en', target=selected_lang_code).translate(text)
    except Exception:
        return text

# ===== LANGUAGE DROPDOWN STYLING =====
st.markdown("""
<style>
div[data-testid="stSelectbox"] {
    position: fixed;
    top: 170px;
    right: 25px;
    width: 150px;
    z-index: 9999;
    background-color: white;
    border-radius: 8px;
    box-shadow: 0 0 10px rgba(0,0,0,0.1);
}
</style>
""", unsafe_allow_html=True)

# ===== CUSTOM STYLING =====
st.markdown("""
<style>
body {
    background: linear-gradient(135deg, #ffdee9, #b5fffc);
    background-attachment: fixed;
}
[data-testid="stAppViewContainer"] {
    background: transparent;
    padding-top: 1px !important;
}
[data-testid="stHeader"] {
    background-color: rgba(0,0,0,0);
    height: 0px;
    visibility: hidden;
} 

.navbar {
    width: 90%;
    height: 70px;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 10px;
    background: linear-gradient(to right, #ffdde1, #ee9ca7, #a1c4fd, #c2e9fb);
    border-radius: 16px;
    box-shadow: 0 4px 25px rgba(0,0,0,0.2);
    margin: 0px auto;
    position: relative;
}
.nav-right {
    display:flex;
    align-items:center;
    gap:30px;
}
.nav-item {
    font-size:18px;
    font-weight:600;
    color:white;
    cursor:pointer;
    text-shadow:0 0 10px rgba(255,255,255,0.8);
    transition:0.3s ease;
}
.nav-item:hover{
    transform:scale(1.05);
    color:#fff0f5;
}
.glowTxt {
    text-shadow: 0 0 20px rgba(255,255,255,0.8);
    color: white;
}
.card-container{
    display:flex;
    justify-content:center;
    align-items:center;
    gap:70px;
    margin-top:40px;
    flex-wrap:wrap;
}
.card-btn{
    width:320px;
    height:200px;
    background: linear-gradient(to bottom right, #ffdee9, #b5fffc);
    border-radius:30px;
    border:none;
    display:flex;
    align-items:center;
    justify-content:center; 
    font-size:24px;
    font-weight:700;
    color:#ffffff;
    cursor:pointer;
    transition: all 0.35s ease;
    box-shadow:0px 0px 15px rgba(255,255,255,0.3);
    text-shadow:0 0 8px rgba(0,0,0,0.2);    
}
.card-btn:hover{
    transform:scale(1.06);
    box-shadow:0 0 35px rgba(255,255,255,0.9);
    filter: brightness(1.1);
}

.footer{
    text-align:center;
    margin-top:60px;
    font-size:14px;
    color:black;
    text-shadow:0 0 8px rgba(255,255,255,0.6);
}
</style>
""", unsafe_allow_html=True)

# ===== NAVBAR =====
st.markdown(f"""
<div class="navbar"> 
    <div class="nav-right">
        <div class="nav-item">{t("Home")}</div>
        <a href="/CaptionGenerator" class="nav-item">{t("Caption Generator")}</a>
        <a href="/SuggestSong" class="nav-item">{t("Song Suggestion")}</a>
        <a href="/aboutus" class="nav-item">{t("About Us")}</a> 
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("<div style='height:0px'></div>", unsafe_allow_html=True)

# ===== HERO TEXT =====
image_path = "logo.png"
if os.path.exists(image_path):
    logo = Image.open(image_path)
    col1, col2, col3 = st.columns([1.5, 1, 1])
    with col2:
        st.image(logo, width=200)
else:
    st.error(f"Image not found at path: {image_path}")

st.markdown(f"<h1 class='glowTxt' style='text-align:center;margin-top:20px;font-size:48px;'>✨ {t('Welcome to CaptionCraft')} ✨</h1>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align:center;font-size:20px;color:white;font-weight:500;margin-top:-10px;'>{t('Turn your moments into magic — captions & songs that match your vibe 🎶')}</p>", unsafe_allow_html=True)

# ===== CARDS =====
st.markdown(f"""
<div class="card-container">
    <a href="/CaptionGenerator" class="card-btn">🎨 {t("Generate Caption")}</a>
    <a href="/SuggestSong" class="card-btn">🎵 {t("Suggest Song")}</a>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# ===== FOOTER =====
st.markdown(f"<div class='footer'>© 2025 CaptionCraft | {t('Made with ❤️ by ASSRI')}</div>", unsafe_allow_html=True)
