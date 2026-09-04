import streamlit as st
from PIL import Image
from deep_translator import GoogleTranslator
import torch
from transformers import BlipProcessor, BlipForConditionalGeneration
import random   # ✅ ADDED

# ===== PAGE CONFIG =====
st.set_page_config(page_title="CaptionGenerator", page_icon="💫", layout="wide")

# ===================== CAPTION LIBRARY =====================
CAPTION_LIBRARY = {
      # 🎉 Party / Festival
    "party": {
        "keywords": ["party", "celebration", "birthday", "wedding", "festival", "cake", "diwali", "holi"],
        "subkeywords": {
            "birthday": ["cake", "candles", "gifts"],
            "wedding": ["rings", "dance", "ceremony"],
            "diwali": ["crackers", "lights", "sweets"],
            "holi": ["colors", "gulal", "water balloons"],
            "party": ["music", "dance", "dj"],
            "festival": ["decorations", "fun", "lights"],
            "cake": ["icing", "chocolate", "candles"]
        },
        "captions": [
            "🎉 Good vibes only",
            "🕺 Dance first, think later",
            "🔊 Music loud, worries low",
            "🍾 Celebrate every small win",
            "💃 Tonight’s mood: unstoppable",
            "✨ Moments that turn into memories"
        ],
        "sub_captions": {
            "birthday": ["🎂 Cutting the birthday cake!","🎉 Gifts, smiles and cheers!","🕯️ Candles and wishes"],
            "wedding": ["💍 Rings, vows, and love!","💃 Dance like nobody’s watching!","🎊 Ceremony vibes!"],
            "diwali": ["🎆 Bursting crackers, spreading joy!","🪔 Diyas lighting the night","🍬 Sweets and happiness"],
            "holi": ["🌈 Splashing colors, spreading happiness!","💦 Water balloons fun!","🎨 Gulal everywhere!"],
            "party": ["🎶 Music on, worries gone!","🕺 Groove all night!","💃 Dance floor madness!"],
            "festival": ["✨ Decorations and fun!","🎊 Festival feels!","🪔 Lights of joy!"],
            "cake": ["🍰 Sweet and yummy!","🎂 Cake time happiness!","🕯️ Blow candles, make wishes!"]
        }
    },

    # 🎨 Hobbies
    "hobbies": {
        "keywords": ["cooking", "drawing"],
        "subkeywords": {
            "cooking": ["recipe", "kitchen", "spices"],
            "drawing": ["sketch", "colors", "canvas"]
        },
        "captions": [
            "👩‍🍳 Cooking up something delicious",
            "🎨 Drawing colors of life",
            "🍲 Experimenting in the kitchen",
            "✏️ Sketching imagination"
        ],
        "sub_captions": {
            "cooking": ["🍳 Trying a new recipe!","🌶️ Spice it up in the kitchen!","🍲 Cooking fun begins!"],
            "drawing": ["✏️ Sketching the world!","🎨 Painting dreams!","🖌️ Canvas full of colors!"]
        }
    },
    "nature": {
        "keywords": ["mountain", "beach", "forest", "river"],
        "subkeywords": {
            "mountain": ["peak", "snow", "hiking"],
            "beach": ["waves", "sun", "sand"],
            "forest": ["trees", "wildlife", "trail"],
            "river": ["flow", "boat", "reflection"]
        },
        "captions": [
            "⛰️ Where the air is thin and dreams are high",
            "🏖️ Beach day feels amazing",
            "🌲 Nature doesn’t rush, yet everything happens",
            "🚶 Every journey teaches something"
        ],
        "sub_captions": {
            "mountain": ["🏔️ Climbing the peak!","❄️ Snowy adventures!","🥾 Hiking trails ahead!"],
            "beach": ["🌊 Waves and sunshine!","🏖️ Sand between toes!","☀️ Sun-kissed day!"],
            "forest": ["🌲 Lost in the woods!","🦉 Wildlife encounters!","🍃 Peaceful forest trail!"],
            "river": ["🚣‍♂️ Rowing along the river!","💧 Water reflections!","🌊 Flowing serenity!"]
        }
    },
    # 🏟️ Sports
    "sports": {
        "keywords": ["football", "cricket", "basketball", "running", "swimming", "tennis", "gym", "yoga", "boxing", "cycling"],
        "subkeywords": {
            "football": ["goal", "kick", "match"],
            "cricket": ["bat", "ball", "innings"],
            "basketball": ["hoop", "dribble", "dunk"],
            "running": ["track", "sprint", "marathon"],
            "gym": ["weights", "workout", "strength"],
            "yoga": ["pose", "meditation", "flexibility"]
        },
        "captions": [
            "🔥 Sweat now, shine later",
            "🏆 Champions are built, not born",
            "⚡ Game on. Limits off.",
            "💪 Strong body, stronger mindset"
        ],
        "sub_captions": {
            "football": ["⚽ Kick the goal!","🥅 Match in action!","🔥 Score and win!"],
            "cricket": ["🏏 Bat and ball fun!","🥇 Winning innings!","🎯 Aim for the stumps!"],
            "basketball": ["🏀 Dunking vibes!","🔥 Dribble and shoot!","⛹️‍♂️ Hoop dreams!"],
            "running": ["🏃 Sprint to success!","⏱️ Track time running!","🥇 Marathon energy!"],
            "gym": ["💪 Lift and grow!","🏋️ Strength session!","🔥 Push limits!"],
            "yoga": ["🧘 Pose for peace!","🌿 Meditation moment!","💫 Stretch and relax!"]
        }
    },
    # 🏫 Education
    "education": {
        "keywords": ["teaching", "classroom", "students", "exam", "college", "school", "library", "hostel"],
        "subkeywords": {
            "teaching": ["lesson", "lecture", "chalk", "board"],
            "classroom": ["desk", "chair", "projector"],
            "students": ["books", "notes", "study", "group_study"],
            "exam": ["test", "revision", "papers"],
            "college": ["campus", "fest", "trip"],
            "hostel": ["roommates", "canteen", "hostel_life"]
        },
        "captions": [
            "📚 Learning is the key to success",
            "🧠 Knowledge is power",
            "✏️ Focus on growth and improvement"
        ],
        "sub_captions": {
            "teaching": ["👨‍🏫 Lecture in progress!","📝 Chalk and board vibes!","📖 Lesson time!"],
            "classroom": ["🏫 Desk and chairs ready!","💡 Projector lights on!","📚 Classroom energy!"],
            "students": ["👩‍🎓 Group study time!","📖 Notes in hand!","🧠 Students learning!"],
            "exam": ["✍️ Exam preparation mode!","📝 Papers and revision!","⏳ Test time!"],
            "college": ["🎓 Campus vibes!","🎉 College fest energy!","🚶 College trip adventure!"],
            "hostel": ["🏠 Hostel life fun!","🍽️ Canteen snacks time!","👯 Roommate moments!"]
        }
    },
    # 💼 Work / Office
    "work": {
        "keywords": ["office", "work", "job", "meeting", "startup", "company", "career", "deadline", "client", "professional"],
        "subkeywords": {
            "office": ["desk", "coffee", "cubicle"],
            "work": ["task", "project", "deadline"],
            "meeting": ["agenda", "discussion", "presentation"],
            "career": ["promotion", "growth", "success"]
        },
        "captions": [
            "💼 Building dreams one task at a time",
            "📊 Work smart. Think big.",
            "🚀 Career mode activated"
        ],
        "sub_captions": {
            "office": ["🖥️ Desk ready for work!","☕ Coffee breaks are life!","🏢 Cubicle vibes!"],
            "work": ["📌 Task list complete!","📝 Project in progress!","⏰ Meeting deadlines!"],
            "meeting": ["💬 Discussion time!","📊 Presentation mode!","🗂️ Agenda in focus!"],
            "career": ["🚀 Climbing the career ladder!","🏆 Achieving milestones!","💡 Growth mindset!"]
        }
    }
}

# ===================== SMART CAPTION FUNCTION =====================
def generate_crazy_caption(text):
    text = text.lower()
    best_caption = None
    max_score = 0

    for category in CAPTION_LIBRARY.values():
        score = 0
        chosen_caption = None
        keyword_matched = False

        for keyword in category["keywords"]:
            if keyword in text:
                score += 2
                keyword_matched = True

        if not keyword_matched:
            continue

        for sub, sublist in category.get("subkeywords", {}).items():
            if sub in text or any(w in text for w in sublist):
                score += 3
                if sub in category.get("sub_captions", {}):
                    chosen_caption = random.choice(category["sub_captions"][sub])

        if not chosen_caption:
            chosen_caption = random.choice(category["captions"])

        if score > max_score:
            max_score = score
            best_caption = chosen_caption

    return best_caption if best_caption else "✨ Moments worth remembering"

# ===================== SESSION STATE =====================
if "final_caption_ready" not in st.session_state:
    st.session_state.final_caption_ready = ""

# ===================== LANGUAGE =====================
language_options = {
    "en": "English", "mr": "Marathi", "hi": "Hindi", "fr": "French"
}

if "selected_lang_code" not in st.session_state:
    st.session_state.selected_lang_code = "en"

def t(text):
    try:
        return GoogleTranslator(source="en", target=st.session_state.selected_lang_code).translate(text)
    except:
        return text

# ===================== EMOJI FUNCTION (UNCHANGED) =====================
def suggest_emojis(caption):
    caption = caption.lower()
    emojis = []
    if "party" in caption or "celebration" in caption:
        emojis = ["🎉", "🥳", "✨"]
    return emojis if emojis else ["✨"]

# ===================== IMAGE =====================
img = None
uploaded_image = st.file_uploader("Upload Image", type=["png", "jpg", "jpeg"])
if uploaded_image:
    img = Image.open(uploaded_image).convert("RGB")
    st.image(img, caption="Selected Image")

# ===================== BLIP =====================
@st.cache_resource
def load_blip_model():
    processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
    model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")
    return processor, model

processor, blip_model = load_blip_model()

def generate_blip_caption(image):
    inputs = processor(image, return_tensors="pt")
    out = blip_model.generate(**inputs, max_length=50)
    return processor.decode(out[0], skip_special_tokens=True)

default_caption = generate_blip_caption(img) if img else ""
caption_input = st.text_area("Write Caption keywords / line", value=default_caption)

# ===================== BUTTONS =====================
generate_clicked = st.button("✨ Generate Caption")

# ===================== GENERATE CAPTION (UPDATED) =====================
if generate_clicked and (caption_input.strip() != "" or img is not None):

    input_text = caption_input.strip() if caption_input.strip() != "" else "photo moment"

    final_caption_en = generate_crazy_caption(input_text)

    final_caption = final_caption_en
    if st.session_state.selected_lang_code != "en":
        final_caption = t(final_caption_en)

    emojis = suggest_emojis(final_caption_en)
    full_caption = final_caption + " " + " ".join(emojis)

    st.session_state.final_caption_ready = full_caption

    st.markdown(f"<div class='caption-box'>{full_caption}</div>", unsafe_allow_html=True)

# ===================== READY TO USE =====================
st.markdown("<br><hr><br>", unsafe_allow_html=True)

additional_input = st.text_input(
    "Ready to use caption:",
    value=st.session_state.final_caption_ready,
    placeholder="Type something extra..."
)

if additional_input.strip():
    st.info(f"You entered: {additional_input}")
