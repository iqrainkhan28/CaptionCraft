import streamlit as st
from PIL import Image
from deep_translator import GoogleTranslator
import torch
from transformers import BlipProcessor, BlipForConditionalGeneration

# ===== PAGE CONFIG =====
st.set_page_config(page_title="CaptionGenerator", page_icon="💫", layout="wide")
 


# ===== LANGUAGE OPTIONS =====
language_options = {
    "en": "English", "mr": "Marathi", "as": "Assamese", "bn": "Bengali", "gu": "Gujarati",
    "hi": "Hindi", "kn": "Kannada", "ml": "Malayalam", "ne": "Nepali", "or": "Odia",
    "pa": "Punjabi", "sa": "Sanskrit", "sd": "Sindhi", "ta": "Tamil", "te": "Telugu",
    "ur": "Urdu", "de": "German", "fr": "French", "ja": "Japanese"
}

# ===== INITIALIZE SESSION STATE =====
if "selected_lang_code" not in st.session_state:
    st.session_state.selected_lang_code = "en"
if "selected_lang_name" not in st.session_state:
    st.session_state.selected_lang_name = "English"


# ===== LANGUAGE SELECTOR =====
def update_language():
    selected = st.session_state.lang_selector
    st.session_state.selected_lang_name = selected
    st.session_state.selected_lang_code = [code for code, name in language_options.items() if name == selected][0]



selected_lang_code = st.session_state.selected_lang_code

def t(text):
    try:
        return GoogleTranslator(source='en', target=selected_lang_code).translate(text)
    except Exception:
        return text


# =====EMOJI SUGGESTION=====
def suggest_emojis(caption):
    caption = caption.lower()
    emojis = []

    # Map keywords to emojis based on caption_to_mood
    mood_emoji_map = {
        # Travel / Places
        "travel": ["✈️", "🌍", "🧳", "🚗", "📍"],
        "trip": ["✈️", "🚗", "🗺️", "🌍"],
        "journey": ["🧳", "🌄", "🚗"],
        "beach": ["🏖️", "🌊", "☀️", "🐚"],
        "mountain": ["⛰️", "🏔️", "🌄"],
        "forest": ["🌳", "🌲", "🍃"],
        "city": ["🏙️", "🚕", "🌆"],
        "countryside": ["🌾", "🚜", "🌻"],
        "sunset": ["🌅", "🧡"],
        "sunrise": ["🌄", "🌞"],
        "desert": ["🏜️", "🌵", "☀️"],
        "waterfall": ["🌊", "💦", "🏞️"],
        "road_trip": ["🚗", "🛣️", "🧳"],
        "mountain_drive": ["🚙", "⛰️", "🛣️"],
        "coastal_drive": ["🚗", "🌊", "🏖️"],
        "rainy_drive": ["🌧️", "🚗", "☔"],

        # Love / Romance
        "love": ["❤️", "💕", "💖", "😍", "💞"],
        "heart": ["❤️", "💓", "💖"],
        "romantic": ["💞", "💕", "😍"],

        # Happiness / Mood
        "happy": ["😊", "😄", "😁", "🤍", "✨"],
        "smile": ["😊", "😃", "😁"],
        "joy": ["😁", "😆", "✨"],
        "uplifting": ["💫", "✨", "🌟"],

        # Food
        "food": ["🍕", "🍔", "🍟", "🍰", "🍩", "🍜"],
        "eat": ["🍴", "🥗", "🍽️"],
        "meal": ["🥘", "🍱"],

        # Confidence / Motivation
        "confident": ["😎", "🔥", "💪", "👑"],
        "strong": ["💪", "🔥", "⚡"],
        "motivated": ["💪", "🚀", "🔥"],
        "bold": ["🦁", "💪", "🔥"],
        "winner": ["🏆", "🥇", "🎯"],

        # Dance / Music
        "dance": ["💃", "🕺", "🎶", "🎧"],
        "music": ["🎵", "🎶", "🎧"],
        "song": ["🎵", "🎤", "🎶"],

        # Night / Relax
        "night": ["🌙", "✨", "⭐", "🌌"],
        "late": ["🌙", "🛌", "⭐"],
        "chill": ["🛋️", "☕", "🌙"],

        # Sports / Fitness
        "football": ["⚽", "🏟️", "🥅"],
        "cricket": ["🏏", "🥅", "🏆"],
        "basketball": ["🏀", "🏟️", "⛹️"],
        "running": ["🏃‍♂️", "🏃‍♀️", "👟"],
        "gym": ["💪", "🏋️", "🔥"],
        "yoga": ["🧘‍♀️", "🕉️", "🌿"],

        # Celebration / Party
        "party": ["🥳", "🎉", "🎊"],
        "celebrate": ["🎊", "🎉", "🥳"],
        "birthday": ["🎂", "🎉", "🎁"],
        "weddings": ["💍", "🎉", "🥂"],
        "festival": ["🎊", "🪔", "🎆"],

        # Tech / Gadgets
        "phone": ["📱", "💬", "📲"],
        "laptop": ["💻", "🖱️", "⌨️"],
        "gaming": ["🎮", "🕹️", "👾"],

        
    # Classroom / College
    "class": ["📚", "📝", "🎓", "🏫", "📖"],
    "lecture": ["📚", "📝", "🎓", "🏫", "📖"],
    "library": ["📚", "📖", "📝", "🎓", "🤓"],
    "college": ["🎓", "🏫", "🎉", "🚌", "👩‍🎓", "👨‍🎓"],
    "college_fest": ["🎓", "🎉", "🎊", "🚌", "🎶"],
    "hostel_life": ["🏘️", "🛏️", "🍲", "👫", "📝"],
    "canteen_time": ["🍔", "🍕", "🥪", "🥤", "🍟"],

    # Food
    "food": ["🍕", "🍔", "🍟", "🍣", "🍰", "🍜", "🥗", "🍩"],
    "meal": ["🍽️", "🥘", "🍲", "🍛", "🍝"],
    "eat": ["🍴", "🥗", "🍽️", "🍔", "🍕"],
    "coffee": ["☕", "🥐", "🍪"],
    "dessert": ["🍰", "🍩", "🍮", "🍫"],
    "pizza_time": ["🍕", "🧀", "🍅"],
    "late_night_snacks": ["🍿", "🥨", "🍫", "🍪"],


        

        # Default fallback emojis
        "default": ["🔥", "😎", "💫", "✨"]
    }

    # Add emojis based on keywords in caption
    for keyword, emoji_list in mood_emoji_map.items():
        if keyword in caption:
            emojis += emoji_list

    # If no emojis matched, add default
    if len(emojis) == 0:
        emojis += mood_emoji_map["default"]

    # Remove duplicates
    emojis = list(dict.fromkeys(emojis))

    return emojis




# ===== CSS STYLING =====
st.markdown("""
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
.center {display:flex; justify-content:center; align-items:center; flex-direction:column;}
.navbar {width: 90%; height: 70px; display: flex; align-items: center; justify-content: center; gap: 10px; background: linear-gradient(to right, #ffdde1, #ee9ca7, #a1c4fd, #c2e9fb); border-radius: 16px; box-shadow: 0 4px 25px rgba(0,0,0,0.2); margin: 0px auto; position: relative;}
.nav-right {display:flex; align-items:center; gap:30px;}
.nav-item {font-size:18px; font-weight:600; color:white; cursor:pointer; text-shadow:0 0 10px rgba(255,255,255,0.8); transition:0.3s ease;}
.nav-item:hover{transform:scale(1.05); color:#fff0f5;}
.generate-btn, .copy-btn{font-weight:bold; font-size:18px; border-radius:12px; padding:10px 20px; cursor:pointer; margin:5px; color:white; border:none;}
.generate-btn{background: linear-gradient(to right, #feda75, #fa7e1e, #d62976, #962fbf, #4f5bd5);}
.copy-btn{background: #00a86b;}
.caption-box{padding:15px; border-radius:12px; background-color:#fff7e1; font-size:16px; margin-top:10px; width:80%;}
.emoji-container{display:flex; flex-wrap:wrap; justify-content:center; margin-top:15px;}
.emoji-card{width:60px; height:60px; display:flex; justify-content:center; align-items:center; font-size:28px; background-color:#ffffff; border-radius:12px; box-shadow:0px 0px 10px rgba(0,0,0,0.2); cursor:pointer; margin:5px; transition:0.3s ease;}
.emoji-card:hover{transform:scale(1.2); box-shadow:0 0 20px rgba(0,0,0,0.3);}
</style>
""", unsafe_allow_html=True)

# ===== NAVBAR =====
st.markdown(f"""
<div class="navbar"> 
    <div class="nav-right">
        <a href="/" class="nav-item">{t("Home")}</a>
        <div class="nav-item">{t("Caption Generator")}</div>
        <a href="/SuggestSong" class="nav-item">{t("Song Suggestion")}</a>
        <a href="/aboutus" class="nav-item">{t("About Us")}</a> 
    </div>
</div>
""", unsafe_allow_html=True)
st.markdown("<div style='height:0px'></div>", unsafe_allow_html=True)
# ===== LANGUAGE SELECTOR (RIGHT SIDE BELOW NAVBAR) =====
col_left, col_right = st.columns([4, 1])

with col_right:
    st.selectbox(
        "🌐 Language",
        options=list(language_options.values()),
        index=list(language_options.values()).index(st.session_state.selected_lang_name),
        key="lang_selector",
        on_change=update_language
    )


# ===== TITLE =====
st.markdown(f"<h2 style='text-align:center;color:#00a86b;'>🖌️ {t('CaptionCraft AI')}</h2>", unsafe_allow_html=True)


# ===== IMAGE INPUT =====
input_option = st.radio(t("Select Image Input:"), options=[t("Upload Image"), t("Use Camera")], horizontal=True)
img = None

if input_option == t("Upload Image"):
    uploaded_image = st.file_uploader("", type=["png", "jpg", "jpeg"])
    if uploaded_image:
        img = Image.open(uploaded_image).convert("RGB")
elif input_option == t("Use Camera"):
    camera_image = st.camera_input(t("Take a photo"))
    if camera_image:
        img = Image.open(camera_image).convert("RGB")

if img:
    col1, col2, col3 = st.columns([3, 1, 3])
    with col2:
        st.image(img, width=500, caption=t("Selected Image"))


# ===== LOAD BLIP MODEL =====
@st.cache_resource(show_spinner=True)
def load_blip_model():
    processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
    model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")
    return processor, model

processor, blip_model = load_blip_model()

# ===== GENERATE BLIP CAPTION =====
def generate_blip_caption(image):
    inputs = processor(image, return_tensors="pt")
    out = blip_model.generate(**inputs, max_length=50)
    caption = processor.decode(out[0], skip_special_tokens=True)
    return caption

# ===== CAPTION INPUT =====
# If image exists, generate BLIP caption automatically
default_caption = generate_blip_caption(img) if img else ""
caption_input = st.text_area(t("Write Caption keywords / line"), value=default_caption, placeholder=t("Type something..."))

# ===== BUTTONS =====
col1, col2 = st.columns([1, 1])
with col1:
    generate_clicked = st.button(f"✨ {t('Generate Caption')}")
with col2:
    copy_clicked = st.button(f"📋 {t('Copy Caption')}")

# ===== GENERATE CAPTION ON BUTTON CLICK =====
# ===== GENERATE CAPTION ON BUTTON CLICK =====
if generate_clicked and (caption_input.strip() != "" or img is not None):

    # Step 1: Always define English caption first
    final_caption_en = caption_input.strip() if caption_input.strip() != "" else "Model generated caption"

    # Step 2: Translate if needed
    final_caption = final_caption_en  # ✅ default assignment (IMPORTANT)

    if selected_lang_code != "en":
        try:
            final_caption = GoogleTranslator(
                source="en",
                target=selected_lang_code
            ).translate(final_caption_en)
        except Exception:
            final_caption = final_caption_en

    # Step 3: Emoji suggestion based on English caption
    emojis = suggest_emojis(final_caption_en)

    # Step 4: Combine caption + emojis
    full_caption = final_caption + " " + " ".join(emojis)

    st.markdown(
        f"<div class='caption-box' id='caption-box'>{full_caption}</div>",
        unsafe_allow_html=True
    )


 

     

# ===== COPY BUTTON FUNCTIONALITY =====
if copy_clicked:
    st.markdown(f"""
    <script>
    const captionInput = document.querySelector('textarea');
    captionInput.select();
    navigator.clipboard.writeText(captionInput.value);
    alert('{t("Caption copied!")}');
    </script>
    """, unsafe_allow_html=True)

