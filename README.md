# 📸 CaptionCraft

**AI-powered social media caption generator** — upload a photo and get ready-to-post captions, matching emojis, a suggested Bollywood song, and optional voice/multilingual output.

Built as a Streamlit web app, CaptionCraft combines image captioning (BLIP), rule-based mood/keyword matching, translation, text-to-speech, and Spotify song recommendations into a single, multi-page experience for creating social-media-ready posts.

---

## ✨ Features

- **Image → Caption**: Upload any photo and generate a natural-language caption using Salesforce's BLIP image-captioning model.
- **Caption Library**: A rule-based keyword/mood engine (parties, travel, nature, food, sports, etc.) that maps captions to curated, ready-to-use caption suggestions.
- **Emoji Suggestions**: Automatically suggests relevant emojis based on the caption's detected mood/keywords.
- **Multilingual Support**: Translate generated captions into 18 languages (Hindi, Marathi, Bengali, Tamil, Telugu, French, German, Japanese, and more) via Google Translate.
- **Song Suggestions**: Recommends a Bollywood song matching the photo's mood using the Spotify Web API.
- **Voice Features**: Speech-to-text (Vosk) for voice input and text-to-speech (pyttsx3 / gTTS) to read captions aloud.
- **Multi-page Streamlit App**: Organized into Home, Caption Generator, Suggest Song, and About Us pages.

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Frontend / App framework | Streamlit |
| Image captioning | BLIP (`Salesforce/blip-image-captioning-base`) via Hugging Face `transformers`, PyTorch |
| Translation | `deep-translator` (Google Translate) |
| Music recommendation | Spotify Web API via `spotipy` |
| Speech-to-text | Vosk (offline model: `vosk-model-small-en-us-0.15`) |
| Text-to-speech | `pyttsx3`, `gTTS` |
| Audio I/O | `sounddevice`, `audiofile`, `scipy` |
| Data handling | `pandas`, `numpy` |

## 📁 Project Structure

```
captioncraft/
├── app.py                     # Main Streamlit entry point (Home page)
├── app1.py                    # Variant of app.py with background image + voice import
├── blip_caption.py            # Standalone CLI script for BLIP image captioning
├── test_model.py              # Script to test Vosk model loading
├── test_voice.py              # Script to test voice module
├── text_speech_utils.py       # Audio recording/playback + TTS helper functions
├── songplay.py / songplay2.py / songplaywithgui.py
│                               # Spotify playback experiments
├── spotify_recommander.py     # Analyzes a Spotify playlist's audio features
├── spotipy_song_play.py       # Spotify playback helper
├── requirements.txt
├── pages/
│   ├── CaptionGenerator.py    # Caption generation + emoji suggestion page
│   ├── caption.py             # Caption library (mood/keyword → caption mapping)
│   ├── SuggestSong.py         # Song suggestion page (Spotify search)
│   └── aboutus.py             # About Us / team page
├── voice/
│   └── voice_module.py        # Speech recognition (Vosk) + TTS (pyttsx3)
├── vosk-model-small-en-us-0.15/  # Offline speech recognition model
└── team/                      # Team member photos
```

## ⚙️ Setup & Installation

1. **Clone the repository** and navigate into the project folder.

2. **Create a virtual environment** (recommended):
   ```bash
   python -m venv venv
   venv\Scripts\activate      # Windows
   source venv/bin/activate   # macOS/Linux
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   pip install torch transformers spotipy deep-translator vosk streamlit-extras
   ```
   > `requirements.txt` doesn't currently list `torch`, `transformers`, `spotipy`, `deep-translator`, `vosk`, and `streamlit-extras` even though the app imports them — install these separately or add them to `requirements.txt`.

4. **Set up Spotify API credentials**. The app currently has a Client ID/Secret hardcoded in `spotify_recommander.py` and `pages/SuggestSong.py` — move these into environment variables before sharing or publishing the code:
   ```bash
   export SPOTIFY_CLIENT_ID="your_client_id"
   export SPOTIFY_CLIENT_SECRET="your_client_secret"
   ```

5. **Run the app**:
   ```bash
   streamlit run app.py

- Usage
Launch the app and select a language from the top-right dropdown (optional).
Go to the Caption Generator page and upload an image.
View the AI-generated caption, suggested captions from the mood library, and matching emojis.
Visit the Suggest Song page to get a Bollywood song recommendation based on the caption's mood.
Use the voice module to speak captions aloud or provide voice input where enabled.

👥 Team

Anjali · Iqra · Ruchita · Shraddha · Snehal
