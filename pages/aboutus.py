import streamlit as st
from PIL import Image
import os
import base64
from deep_translator import GoogleTranslator

st.set_page_config(page_title="About Us", page_icon="📘", layout="wide")

# ===== LANGUAGE OPTIONS =====
language_options = {
    "en": "English", "mr": "Marathi", "as": "Assamese", "bn": "Bengali", "gu": "Gujarati", "hi": "Hindi",
    "kn": "Kannada", "ml": "Malayalam", "ne": "Nepali", "or": "Odia", "pa": "Punjabi", "sa": "Sanskrit",
    "sd": "Sindhi", "ta": "Tamil", "te": "Telugu", "ur": "Urdu", "de": "German", "fr": "French", "ja": "Japanese"
}

# ===== SESSION STATE =====
if "selected_lang_code" not in st.session_state:
    st.session_state.selected_lang_code = "en"
if "selected_lang_name" not in st.session_state:
    st.session_state.selected_lang_name = "English"

def update_language():
    selected = st.session_state.lang_selector
    st.session_state.selected_lang_name = selected
    st.session_state.selected_lang_code = [
        code for code, name in language_options.items() if name == selected
    ][0]

st.selectbox(
    "",
    options=list(language_options.values()),
    index=list(language_options.values()).index(st.session_state.selected_lang_name),
    key="lang_selector",
    on_change=update_language
)

def t(text):
    try:
        return GoogleTranslator(
            source="en",
            target=st.session_state.selected_lang_code
        ).translate(text)
    except:
        return text

# ===== LANGUAGE DROPDOWN POSITION =====
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

# ===== MAIN CSS =====
st.markdown("""
<style>
#MainMenu, footer {visibility:hidden;}

.navbar {
    width:90%;
    height:70px;
    display:flex;
    align-items:center;
    justify-content:center;
    gap:50px;
    background: linear-gradient(to right, #ffdde1, #ee9ca7, #a1c4fd, #c2e9fb);
    border-radius:16px;
    box-shadow:0 4px 25px rgba(0,0,0,0.2);
    margin: 20px auto;
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
    text-decoration:none;
    text-shadow:0 0 10px rgba(255,255,255,0.8);
}

.nav-item:hover {
    transform:scale(1.05);
    color:#fff0f5;
}

.about-section {
    text-align:center;
    margin-top:30px;
    padding:20px 50px;
}

.about-title {
    font-size:42px;
    font-weight:bold;
    color:#00a86b;
}

.about-text {
    font-size:18px;
    color:#333;
    margin-top:20px;
    max-width:900px;
    margin:auto;
    background:#fff7e1;
    padding:20px 30px;
    border-radius:16px;
}

/* ===== TEAM SECTION ===== */
.team-section {
    text-align:center;
    margin-top:80px;
}

.team-title {
    font-size:36px;
    font-weight:700;
    color:#008b8b;
    margin-bottom:40px;
}

.team-card {
    background:#fff7ec;
    border-radius:22px;
    padding:25px 20px;
    text-align:center;
    box-shadow:0 10px 30px rgba(0,0,0,0.15);
    height:340px;
}

/* ===== FIXED IMAGE STYLING ===== */
.image-wrapper {
    width:140px;
    height:140px;
    border-radius:50%;
    overflow:hidden;
    margin:0 auto 15px auto;
    box-shadow:0 6px 15px rgba(0,0,0,0.15);
}

.image-wrapper img {
    width:100%;
    height:100%;
    object-fit:cover;
}

.team-img {
    width:140px;
    height:140px;
    object-fit:cover;
    border-radius:12px;
    margin-bottom:15px;
}

.member-name {
    font-size:18px;
    font-weight:700;
}

.member-role {
    font-size:14px;
    color:#00a86b;
}
</style>
""", unsafe_allow_html=True)

# ===== NAVBAR =====
st.markdown(f"""
<div class="navbar"> 
    <div class="nav-right">
        <a href="/" class="nav-item">{t("Home")}</a>
        <a href="/CaptionGenerator" class="nav-item">{t("Caption Generator")}</a>
        <a href="/SuggestSong" class="nav-item">{t("Song Suggestion")}</a>
        <a href="/about" class="nav-item">{t("About Us")}</a> 
    </div>
</div>
""", unsafe_allow_html=True)

# ===== LOGO =====
if os.path.exists("logo.png"):
    col1, col2, col3 = st.columns([1.5, 1, 1])
    with col2:
        st.image("logo.png", width=200)

# ===== ABOUT SECTION =====
st.markdown(f"""
<div class="about-section">
    <div class="about-title">📸 {t("About CaptionCraft")}</div>
    <div class="about-text">
        <p><b>CaptionCraft</b> {t("is an AI-powered caption generation platform designed to transform images into engaging, meaningful, and social-media-ready captions. With a clean, modern interface and a strong focus on accessibility, CaptionCraft helps users create captions effortlessly in multiple Indian languages.")}</p>
    </div>
</div>
""", unsafe_allow_html=True)

# ===== TEAM SECTION =====
st.markdown(f"""
<div class="team-section">
    <div class="team-title">👩‍💻 {t("Meet Our Team")}</div>
</div>
""", unsafe_allow_html=True)

team_members = [
    {"name": "Anjali Rane", "role": "Frontend Developer", "photo": r"C:\Users\ANJALI\Desktop\captioncraft\team\anjali.jpeg"},
    {"name": "Ruchita Mane", "role": "Backend Developer", "photo": r"C:\Users\ANJALI\Desktop\captioncraft\team\ruchita.jpeg"},
    {"name": "Snehal Bomble", "role": "ML Engineer", "photo": r"C:\Users\ANJALI\Desktop\captioncraft\team\snehal.jpeg"},
    {"name": "Shraddha kale", "role": "Backend Developer", "photo": r"C:\Users\ANJALI\Desktop\captioncraft\team\shraddha.jpeg"},
    {"name": "Iqra Khan", "role": "Backend Developer", "photo": r"C:\Users\ANJALI\Desktop\captioncraft\team\iqra.jpeg"},
]

def img_to_base64(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

cols = st.columns(5)

for i, member in enumerate(team_members):
    with cols[i]:
        if not os.path.exists(member["photo"]):
            continue

        img64 = img_to_base64(member["photo"])

        st.markdown(f"""
        <div class="team-card">
            <div class="image-wrapper">
                <img src="data:image/jpeg;base64,{img64}">
            </div>
            <div class="member-name">{member['name']}</div>
            <div class="member-role">{t(member['role'])}</div>
        </div>
        """, unsafe_allow_html=True)

# ===== FOOTER =====
st.markdown(
    f"<div style='text-align:center;margin-top:60px;'>© 2025 CaptionCraft | {t('Made with ❤️ by ASSRI')}</div>",
    unsafe_allow_html=True
)
