
from spotipy.exceptions import SpotifyException
import os
from pathlib import Path
import streamlit as st
from deep_translator import GoogleTranslator
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from dotenv import load_dotenv

# Load .env from the main captioncraft folder
env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

# Get Spotify credentials
CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")

# Spotify Setup
sp = spotipy.Spotify(
    auth_manager=SpotifyClientCredentials(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET
    )
)
# ===========================
# Caption → search keyword mapping
# ===========================
caption_to_query = {
    # General moods
    "happy": "happy bollywood",
    "sad": "sad bollywood",
    "love": "romantic bollywood",
    "romantic": "romantic bollywood",
    "motivated": "motivated bollywood",
    "reflective": "reflective bollywood",
    "nostalgic": "nostalgic bollywood",
    "relaxed": "relaxed bollywood",
    "energetic": "energetic bollywood",
    "mysterious": "mysterious bollywood",
    "uplifting": "uplifting bollywood",
    "dramatic": "dramatic bollywood",
    "chill_vibes": "chill_vibes bollywood",

    # Seasonal / Time
    "summer": "summer bollywood",
    "rainy": "rainy bollywood",
    "sunset": "sunset bollywood",
    "sunrise": "sunrise bollywood",
    "winter": "winter bollywood",
    "spring": "spring bollywood",
    "autumn": "autumn bollywood",
    "cozy": "cozy bollywood",

    # Travel / Nature
    "mountain": "travel bollywood",
    "climb": "travel bollywood",
    "forest": "forest bollywood",
    "beach": "beach bollywood",
    "travel": "travel bollywood",

    # Sports / Fitness
    "gym": "gym bollywood",
    "yoga": "yoga bollywood",
    "football": "football bollywood",
    "cricket": "cricket bollywood",
    "basketball": "basketball bollywood",
    "running": "running bollywood",
    "tennis": "tennis bollywood",
    "swimming": "swimming bollywood",
    "cycling": "cycling bollywood",
    "skiing": "skiing bollywood",
    "boxing": "boxing bollywood",

    # Celebrations / Festivals
    "party": "party bollywood",
    "diwali": "diwali bollywood",
    "christmas": "christmas bollywood",
    "holi": "holi bollywood",
    "eid": "eid bollywood",
    "halloween": "halloween bollywood",
    "navratri": "navratri bollywood",
    "pongal": "pongal bollywood",
    "thanksgiving": "thanksgiving bollywood",
    "new_year": "new_year bollywood",
    "raksha_bandhan": "raksha_bandhan bollywood",
    "ball": "ball bollywood",

    # Life events
    "weddings": "weddings bollywood",
    "celebration": "celebration bollywood",
    "graduation": "graduation bollywood",
    "birthday": "birthday bollywood",
    "anniversary": "anniversary bollywood",
    "promotion": "promotion bollywood",
    "retirement": "retirement bollywood",

    # College / Study
    "class": "class bollywood",
    "banch": "class bollywood",
    "lecture": "lecture bollywood",
    "exam": "exam bollywood",
    "library": "library bollywood",
    "notebook": "library bollywood",
    "hostel_life": "hostel_life bollywood",
    "college_fest": "college_fest bollywood",
    "sports_day": "sports_day bollywood",
    "group_study": "group_study bollywood",
    "canteen_time": "canteen_time bollywood",
    "college_trip": "college_trip bollywood",
    "project_work": "project_work bollywood",
    "presentation_day": "presentation_day bollywood",
    "exam_result": "exam_result bollywood",
    "friendship_moments": "friendship_moments bollywood",

    # Food / Lifestyle
    "food": "food bollywood",
    "foodie": "foodie bollywood",
    "street_food": "street_food bollywood",
    "home_food": "home_food bollywood",
    "coffee": "coffee bollywood",
    "dessert": "dessert bollywood",
    "pizza_time": "pizza_time bollywood",
    "late_night_snacks": "late_night_snacks bollywood",

    # Dance / Music
    "dance": "dance bollywood",
    "dance_floor": "dance_floor bollywood",
    "groove": "groove bollywood",
    "freestyle": "freestyle bollywood",
    "hip_hop": "hip_hop bollywood",
    "bollywood_dance": "bollywood_dance",
    "dance_practice": "dance_practice bollywood",

    # Fashion / Shopping
    "outfit_check": "outfit_check bollywood",
    "traditional_wear": "traditional_wear bollywood",
    "fashion": "fashion bollywood",
    "ethnic_look": "ethnic_look bollywood",
    "style_vibes": "style_vibes bollywood",
    "shopping": "shopping bollywood",
    "mall_time": "mall_time bollywood",
    "online_shopping": "online_shopping bollywood",
    "sale_day": "sale_day bollywood",
    "window_shopping": "window_shopping bollywood",

    # Tech / Gadgets
    "new_gadget": "new_gadget bollywood",
    "tech_life": "tech_life bollywood",
    "smartphone": "smartphone bollywood",
    "laptop_work": "laptop_work bollywood",
    "gaming_setup": "gaming_setup bollywood",

    # Confidence / Motivation
    "confident": "confident bollywood",
    "self_confident": "self_confident bollywood",
    "bold": "bold bollywood",
    "fearless": "fearless bollywood",
    "strong": "strong bollywood",
    "powerful": "powerful bollywood",
    "determined": "determined bollywood",
    "focused": "focused bollywood",
    "winning": "winning bollywood",
    "leader_vibes": "leader_vibes bollywood",
    "unstoppable": "unstoppable bollywood",
    "boss_vibes": "boss_vibes bollywood",
    "success": "success bollywood",
    "achievement": "achievement bollywood",
    "proud": "proud bollywood"
    
}

# ===========================
# Caption → Audio Feature Mapping
# ===========================
caption_to_features = {
    # General moods
    "happy": {"valence": 0.9, "energy": 0.6, "danceability": 0.6},
    "sad": {"valence": 0.2, "energy": 0.3, "danceability": 0.3},
    "love": {"valence": 0.8, "energy": 0.5, "danceability": 0.6},
    "romantic": {"valence": 0.8, "energy": 0.5, "danceability": 0.6},
    "motivated": {"valence": 0.9, "energy": 0.9, "danceability": 0.8},
    "reflective": {"valence": 0.4, "energy": 0.3, "danceability": 0.3},
    "nostalgic": {"valence": 0.5, "energy": 0.4, "danceability": 0.4},
    "relaxed": {"valence": 0.7, "energy": 0.3, "danceability": 0.5},
    "energetic": {"valence": 0.8, "energy": 0.9, "danceability": 0.6},
    "mysterious": {"valence": 0.3, "energy": 0.4, "danceability": 0.4},
    "uplifting": {"valence": 0.9, "energy": 0.85, "danceability": 0.8},
    "dramatic": {"valence": 0.4, "energy": 0.7, "danceability": 0.5},
    "chill_vibes": {"valence": 0.7, "energy": 0.3, "danceability": 0.5},
    "dancing":{"valence": 0.85, "energy": 0.9, "danceability": 0.9},

    # Seasonal / Time
    "summer": {"valence": 0.9, "energy": 0.8, "danceability": 0.85},
    "rainy": {"valence": 0.5, "energy": 0.4, "danceability": 0.4},
    "sunset": {"valence": 0.75, "energy": 0.4, "danceability": 0.5},
    "sunrise": {"valence": 0.8, "energy": 0.5, "danceability": 0.6},
    "winter": {"valence": 0.5, "energy": 0.3, "danceability": 0.4},
    "spring": {"valence": 0.8, "energy": 0.6, "danceability": 0.7},
    "autumn": {"valence": 0.6, "energy": 0.5, "danceability": 0.5},
    "cozy": {"valence": 0.7, "energy": 0.3, "danceability": 0.4},

    # Travel / Nature
    "mountain": {"valence": 0.8, "energy": 0.7, "danceability": 0.7},
    "climb": {"valence": 0.8, "energy": 0.75, "danceability": 0.7},
    "forest": {"valence": 0.6, "energy": 0.3, "danceability": 0.4},
    "beach": {"valence": 0.9, "energy": 0.7, "danceability": 0.8},
    "travel": {"valence": 0.85, "energy": 0.75, "danceability": 0.8},

    # Sports / Fitness
    "gym": {"valence": 0.7, "energy": 0.95, "danceability": 0.8},
    "yoga": {"valence": 0.7, "energy": 0.3, "danceability": 0.4},
    "football": {"valence": 0.85, "energy": 0.9, "danceability": 0.8},
    "cricket": {"valence": 0.85, "energy": 0.9, "danceability": 0.8},
    "basketball": {"valence": 0.85, "energy": 0.9, "danceability": 0.8},
    "running": {"valence": 0.8, "energy": 0.85, "danceability": 0.7},
    "tennis": {"valence": 0.8, "energy": 0.85, "danceability": 0.7},
    "swimming": {"valence": 0.8, "energy": 0.8, "danceability": 0.7},
    "cycling": {"valence": 0.8, "energy": 0.85, "danceability": 0.7},
    "skiing": {"valence": 0.85, "energy": 0.9, "danceability": 0.7},
    "boxing": {"valence": 0.85, "energy": 0.95, "danceability": 0.7},
    "ball": {"valence": 0.8, "energy": 0.9, "danceability": 0.7},

    # Celebrations / Festivals
    "party": {"valence": 0.95, "energy": 0.95, "danceability": 0.95},
    "diwali": {"valence": 0.9, "energy": 0.85, "danceability": 0.8},
    "christmas": {"valence": 0.9, "energy": 0.8, "danceability": 0.8},
    "holi": {"valence": 0.95, "energy": 0.9, "danceability": 0.9},
    "eid": {"valence": 0.85, "energy": 0.8, "danceability": 0.8},
    "halloween": {"valence": 0.7, "energy": 0.6, "danceability": 0.6},
    "navratri": {"valence": 0.9, "energy": 0.85, "danceability": 0.9},
    "pongal": {"valence": 0.85, "energy": 0.8, "danceability": 0.8},
    "thanksgiving": {"valence": 0.8, "energy": 0.7, "danceability": 0.7},
    "new_year": {"valence": 0.95, "energy": 0.95, "danceability": 0.95},
    "raksha_bandhan": {"valence": 0.85, "energy": 0.7, "danceability": 0.7},

    # Life events
    "weddings": {"valence": 0.9, "energy": 0.8, "danceability": 0.85},
    "celebration": {"valence": 0.95, "energy": 0.9, "danceability": 0.9},
    "graduation": {"valence": 0.9, "energy": 0.85, "danceability": 0.8},
    "birthday": {"valence": 0.95, "energy": 0.9, "danceability": 0.9},
    "anniversary": {"valence": 0.85, "energy": 0.7, "danceability": 0.7},
    "promotion": {"valence": 0.9, "energy": 0.85, "danceability": 0.8},
    "retirement": {"valence": 0.8, "energy": 0.6, "danceability": 0.6},

    # College / Study
    "class": {"valence": 0.5, "energy": 0.4, "danceability": 0.3},
    "banch": {"valence": 0.5, "energy": 0.4, "danceability": 0.3},
    "lecture": {"valence": 0.5, "energy": 0.4, "danceability": 0.3},
    "exam": {"valence": 0.4, "energy": 0.4, "danceability": 0.2},
    "library": {"valence": 0.5, "energy": 0.3, "danceability": 0.2},
    "notebook": {"valence": 0.5, "energy": 0.3, "danceability": 0.2},
    "hostel_life": {"valence": 0.7, "energy": 0.6, "danceability": 0.6},
    "college_fest": {"valence": 0.9, "energy": 0.85, "danceability": 0.9},
    "sports_day": {"valence": 0.85, "energy": 0.9, "danceability": 0.85},
    "group_study": {"valence": 0.6, "energy": 0.5, "danceability": 0.5},
    "canteen_time": {"valence": 0.7, "energy": 0.6, "danceability": 0.6},
    "college_trip": {"valence": 0.85, "energy": 0.8, "danceability": 0.8},
    "project_work": {"valence": 0.5, "energy": 0.5, "danceability": 0.4},
    "presentation_day": {"valence": 0.6, "energy": 0.6, "danceability": 0.5},
    "exam_result": {"valence": 0.5, "energy": 0.4, "danceability": 0.3},
    "friendship_moments": {"valence": 0.85, "energy": 0.75, "danceability": 0.8},

    # Food / Lifestyle
    "food": {"valence": 0.8, "energy": 0.6, "danceability": 0.7},
    "foodie": {"valence": 0.85, "energy": 0.65, "danceability": 0.7},
    "street_food": {"valence": 0.85, "energy": 0.7, "danceability": 0.7},
    "home_food": {"valence": 0.8, "energy": 0.5, "danceability": 0.6},
    "coffee": {"valence": 0.7, "energy": 0.4, "danceability": 0.5},
    "dessert": {"valence": 0.8, "energy": 0.5, "danceability": 0.6},
    "pizza_time": {"valence": 0.85, "energy": 0.6, "danceability": 0.7},
    "late_night_snacks": {"valence": 0.7, "energy": 0.5, "danceability": 0.6},

    # Dance / Music
    "dance": {"valence": 0.9, "energy": 0.85, "danceability": 0.9},
    "dance_floor": {"valence": 0.9, "energy": 0.9, "danceability": 0.95},
    "groove": {"valence": 0.85, "energy": 0.8, "danceability": 0.9},
    "freestyle": {"valence": 0.85, "energy": 0.85, "danceability": 0.9},
    "hip_hop": {"valence": 0.85, "energy": 0.9, "danceability": 0.9},
    "bollywood_dance": {"valence": 0.9, "energy": 0.85, "danceability": 0.95},
    "dance_practice": {"valence": 0.85, "energy": 0.8, "danceability": 0.9},

    # Fashion / Shopping
    "outfit_check": {"valence": 0.8, "energy": 0.6, "danceability": 0.7},
    "traditional_wear": {"valence": 0.8, "energy": 0.5, "danceability": 0.6},
    "fashion": {"valence": 0.85, "energy": 0.65, "danceability": 0.7},
    "ethnic_look": {"valence": 0.85, "energy": 0.6, "danceability": 0.65},
    "style_vibes": {"valence": 0.85, "energy": 0.65, "danceability": 0.7},
    "shopping": {"valence": 0.8, "energy": 0.7, "danceability": 0.7},
    "mall_time": {"valence": 0.85, "energy": 0.7, "danceability": 0.75},
    "online_shopping": {"valence": 0.8, "energy": 0.65, "danceability": 0.7},
    "sale_day": {"valence": 0.85, "energy": 0.75, "danceability": 0.75},
    "window_shopping": {"valence": 0.8, "energy": 0.6, "danceability": 0.65},

    # Tech / Gadgets
    "new_gadget": {"valence": 0.85, "energy": 0.7, "danceability": 0.7},
    "tech_life": {"valence": 0.8, "energy": 0.7, "danceability": 0.7},
    "smartphone": {"valence": 0.8, "energy": 0.65, "danceability": 0.7},
    "laptop_work": {"valence": 0.7, "energy": 0.6, "danceability": 0.6},
    "gaming_setup": {"valence": 0.85, "energy": 0.8, "danceability": 0.75},

    # Confidence / Motivation
    "confident": {"valence": 0.85, "energy": 0.85, "danceability": 0.7},
    "self_confident": {"valence": 0.85, "energy": 0.85, "danceability": 0.7},
    "bold": {"valence": 0.9, "energy": 0.85, "danceability": 0.7},
    "fearless": {"valence": 0.9, "energy": 0.9, "danceability": 0.7},
    "strong": {"valence": 0.85, "energy": 0.9, "danceability": 0.7},
    "powerful": {"valence": 0.9, "energy": 0.95, "danceability": 0.75},
    "determined": {"valence": 0.85, "energy": 0.9, "danceability": 0.7},
    "focused": {"valence": 0.8, "energy": 0.85, "danceability": 0.7},
    "winning": {"valence": 0.9, "energy": 0.95, "danceability": 0.75},
    "leader_vibes": {"valence": 0.9, "energy": 0.9, "danceability": 0.7},
    "unstoppable": {"valence": 0.95, "energy": 0.95, "danceability": 0.8},
    "boss_vibes": {"valence": 0.95, "energy": 0.95, "danceability": 0.8},
    "success": {"valence": 0.95, "energy": 0.95, "danceability": 0.8},
    "achievement": {"valence": 0.95, "energy": 0.95, "danceability": 0.8},
    "proud": {"valence": 0.9, "energy": 0.9, "danceability": 0.7}
}


# ===========================
# Song Recommendation Function
# ===========================
def get_song_recommendations(caption, limit=5):
    caption = caption.lower()
    
    # Keyword query
    query = next((caption_to_query[k] for k in caption_to_query if k in caption), "bollywood hits")
    
    # Audio features
    features = next(
        (caption_to_features[k] for k in caption_to_features if k in caption),
        {"valence": 0.6, "energy": 0.6, "danceability": 0.6}
    )

    # Search seed tracks
    search_results = sp.search(q=query, type="track", limit=5, market="IN")
    seed_tracks = [t["id"] for t in search_results["tracks"]["items"] if t["id"]]

    if not seed_tracks:
        return []

    # Recommendations with safe error handling
    try:
        recommendations = sp.recommendations(
            seed_tracks=seed_tracks[:5],
            limit=limit,
            target_valence=features["valence"],
            target_energy=features["energy"],
            target_danceability=features["danceability"],
            market="IN"
        )
        tracks = recommendations["tracks"]
    except:
        # fallback to seed tracks if recommendations fail
        tracks = search_results["tracks"]["items"]

    songs = []
    for track in tracks:
        songs.append({
            "name": track["name"],
            "artist": track["artists"][0]["name"],
            "spotify_id": track["id"]
        })

    return songs

# ===========================
# Streamlit App
# ===========================
st.set_page_config(page_title="Song Suggestion", page_icon="🎵", layout="wide")

language_options = {
    "en": "English", "mr": "Marathi", "as": "Assamese", "bn": "Bengali", "gu": "Gujarati", "hi": "Hindi",
    "kn": "Kannada", "ml": "Malayalam", "ne": "Nepali", "or": "Odia", "pa": "Punjabi", "sa": "Sanskrit",
    "sd": "Sindhi", "ta": "Tamil", "te": "Telugu", "ur": "Urdu", "de": "German", "fr": "French", "ja": "Japanese"
}

if "selected_lang_code" not in st.session_state:
    st.session_state.selected_lang_code = "en"
if "selected_lang_name" not in st.session_state:
    st.session_state.selected_lang_name = "English"

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

def t(text):
    try:
        return GoogleTranslator(source='en', target=selected_lang_code).translate(text)
    except:
        return text

# ===== CSS styling =====
st.markdown("""
<style>
div[data-testid="stSelectbox"] {position: fixed; top: 170px; right: 25px; width: 150px; z-index: 9999; background-color: white; border-radius: 8px; box-shadow: 0 0 10px rgba(0,0,0,0.1);}
#MainMenu {visibility: hidden;} footer {visibility: hidden;}
.navbar {width: 90%; height: 70px; display: flex; align-items: center; justify-content: center; gap: 10px; background: linear-gradient(to right, #ffdde1, #ee9ca7, #a1c4fd, #c2e9fb); border-radius: 16px; box-shadow: 0 4px 25px rgba(0,0,0,0.2); margin: 0px auto; position: relative;}
.nav-right {display:flex;align-items:center;gap:30px;}
.nav-item {font-size:18px;font-weight:600;color:white;cursor:pointer;text-shadow:0 0 10px rgba(255,255,255,0.8);transition:0.3s ease;}
.nav-item:hover {transform:scale(1.05);color:#fff0f5;}
.center {display:flex;flex-direction:column;align-items:center;justify-content:center;margin-top:150px;}
.heading {font-size:48px;font-weight:bold;text-align:center;color:#00a86b;margin-bottom:5px;}
.subheading {font-size:20px;text-align:center;color:#008b8b;margin-bottom:30px;}
.caption-input {width:400px;height:80px;border-radius:16px;padding:10px;font-size:16px;resize:none;background-color:#fff7e1;border:none;box-shadow:0 0 10px rgba(0,0,0,0.2);}
.generate-btn{font-weight:bold;font-size:18px;align:center;border-radius:12px;padding:12px 24px;cursor:pointer;margin-top:15px;color:white;border:none;background: linear-gradient(to right, #feda75, #fa7e1e, #d62976, #962fbf, #4f5bd5);}
.generate-btn:hover{transform:scale(1.05); transition:0.3s ease;}
.song-card{width:400px;min-height:250px;border-radius:16px;background-color:#fff7e1;text-align:center;font-size:18px;margin:20px auto;padding:15px;box-shadow:0 0 20px rgba(0,0,0,0.2);display:flex;flex-direction:column;justify-content:center;align-items:center;word-wrap:break-word;}.audio-btn{font-weight:bold;font-size:16px;border-radius:12px;padding:8px 16px;cursor:pointer;margin:5px;color:white;border:none;background:#00a86b;}
.audio-btn:hover{transform:scale(1.05);}
.footer{text-align:center;margin-top:60px;font-size:14px;color:black;text-shadow:0 0 8px rgba(0,0,0,0.2);}
</style>
""", unsafe_allow_html=True)

# ===== Navbar =====
st.markdown(f"""
<div class="navbar"> 
    <div class="nav-right">
        <a href="/" class="nav-item">{t("Home")}</a>
        <a href="/CaptionGenerator" class="nav-item">{t("Caption Generator")}</a>
        <div class="nav-item">{t("Song Suggestion")}</div>
        <a href="/aboutus" class="nav-item">{t("About Us")}</a> 
    </div>
</div>
""", unsafe_allow_html=True)
st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)

# ===== Center container =====
st.markdown('<div class="center">', unsafe_allow_html=True)
st.markdown(f"<div class='heading'>🎵 {t('Song Suggestion')}</div>", unsafe_allow_html=True)
st.markdown(f"<div class='subheading'>{t('Enter your vibe and get a perfect song match!')}</div>", unsafe_allow_html=True)

# ===== Caption Input =====
caption = st.text_area("", placeholder=t("Type your caption here..."), key="song_input", height=80)
suggest_btn = st.button(f"🎵 {t('Suggest Song')}", key="suggest_song")
song_placeholder = st.empty()

# ===== Display multiple songs =====
if suggest_btn and caption.strip() != "":
    songs = get_song_recommendations(caption)
    if songs:
        for s in songs:
            song_html = f"""
            <div class="song-card">
                <b>{s['name']} - {s['artist']}</b><br><br>
                <iframe src="https://open.spotify.com/embed/track/{s['spotify_id']}" 
                width="300" height="80" frameborder="0" allowtransparency="true" allow="encrypted-media"></iframe>
            </div>
            """
            song_placeholder.markdown(song_html, unsafe_allow_html=True)
    else:
        song_placeholder.warning("No suitable songs found. Try a different caption.")

st.markdown('</div>', unsafe_allow_html=True)
st.markdown(f"<div class='footer'>© 2025 CaptionCraft | {t('Made with ❤️ by ASSRI')}</div>", unsafe_allow_html=True)