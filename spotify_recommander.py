import spotipy
from spotipy.oauth2 import SpotifyOAuth
import numpy as np

# --------------------------
# Spotify credentials
# --------------------------
CLIENT_ID = "202ca9b47dd94a69afdf92ebdccdcf4d"
CLIENT_SECRET = "924a75f96216442abb71bfa4e4e502f1"
REDIRECT_URI = "http://127.0.0.1:8888/callback"
SCOPE = "playlist-read-private"

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    redirect_uri=REDIRECT_URI,
    scope=SCOPE
))

# --------------------------
# Your Playlist ID
# --------------------------
PLAYLIST_ID = "57z9Iv4tGTPncvp7ghPOLt"

# --------------------------
# Safe method to fetch audio features
# --------------------------
def get_audio_features_safe(track_ids):
    features_list = []
    for track_id in track_ids:
        try:
            f = sp.audio_features([track_id])[0]
            if f:
                features_list.append(f)
        except spotipy.SpotifyException as e:
            print(f"Skipping track {track_id} due to error: {e}")
    return features_list

# --------------------------
# Analyze playlist
# --------------------------
def analyze_playlist(playlist_id):
    results = sp.playlist_items(playlist_id)
    tracks = results['items']
    playlist_track_ids = []
    playlist_song_names = []

    for item in tracks:
        track = item['track']
        if track:  # avoid None
            playlist_track_ids.append(track['id'])
            playlist_song_names.append(track['name'].lower())

    features = get_audio_features_safe(playlist_track_ids)

    if not features:
        # default values if no features available
        return playlist_track_ids, playlist_song_names, {
            "danceability": 0.5,
            "energy": 0.5,
            "valence": 0.5
        }

    danceability = np.mean([f['danceability'] for f in features])
    energy = np.mean([f['energy'] for f in features])
    valence = np.mean([f['valence'] for f in features])

    return playlist_track_ids, playlist_song_names, {
        "danceability": danceability,
        "energy": energy,
        "valence": valence
    }

playlist_ids, playlist_names, playlist_features = analyze_playlist(PLAYLIST_ID)

# --------------------------
# Caption → Mood mapping
# --------------------------
caption_to_query = {
    # General Moods
    "happy": {"danceability": 0.8, "energy": 0.8, "valence": 0.9},
    "sad": {"danceability": 0.3, "energy": 0.2, "valence": 0.2},
    "love": {"danceability": 0.6, "energy": 0.5, "valence": 0.7},
    "party": {"danceability": 0.9, "energy": 0.9, "valence": 0.8},
    "chill": {"danceability": 0.4, "energy": 0.3, "valence": 0.6},
    "mountain": {"danceability": 0.6, "energy": 0.7, "valence": 0.8},
    "romantic": {"danceability": 0.5, "energy": 0.4, "valence": 0.8},
    "adventurous": {"danceability": 0.7, "energy": 0.8, "valence": 0.85},
    "motivated": {"danceability": 0.75, "energy": 0.85, "valence": 0.9},
    "reflective": {"danceability": 0.3, "energy": 0.4, "valence": 0.5},
    "nostalgic": {"danceability": 0.4, "energy": 0.3, "valence": 0.6},
    "relaxed": {"danceability": 0.5, "energy": 0.4, "valence": 0.7},
    "energetic": {"danceability": 0.9, "energy": 0.95, "valence": 0.85},
    "mysterious": {"danceability": 0.4, "energy": 0.5, "valence": 0.4},
    "summer": {"danceability": 0.85, "energy": 0.8, "valence": 0.9},
    "rainy": {"danceability": 0.3, "energy": 0.2, "valence": 0.3},
    "friendship": {"danceability": 0.7, "energy": 0.75, "valence": 0.85},
    "travel": {"danceability": 0.8, "energy": 0.8, "valence": 0.8},
    "calm": {"danceability": 0.3, "energy": 0.3, "valence": 0.6},
    "sunset": {"danceability": 0.4, "energy": 0.3, "valence": 0.7},
    "sunrise": {"danceability": 0.5, "energy": 0.4, "valence": 0.75},
    "forest": {"danceability": 0.5, "energy": 0.5, "valence": 0.65},
    "beach": {"danceability": 0.8, "energy": 0.7, "valence": 0.85},
    "winter": {"danceability": 0.3, "energy": 0.3, "valence": 0.5},
    "spring": {"danceability": 0.6, "energy": 0.6, "valence": 0.8},
    "autumn": {"danceability": 0.5, "energy": 0.4, "valence": 0.7},
    "cozy": {"danceability": 0.3, "energy": 0.2, "valence": 0.7},
    "uplifting": {"danceability": 0.8, "energy": 0.85, "valence": 0.9},
    "dramatic": {"danceability": 0.5, "energy": 0.7, "valence": 0.5},
    "chill_vibes": {"danceability": 0.4, "energy": 0.3, "valence": 0.6},

    # Sports
    "football": {"danceability": 0.8, "energy": 0.9, "valence": 0.85},
    "cricket": {"danceability": 0.8, "energy": 0.85, "valence": 0.85},
    "basketball": {"danceability": 0.85, "energy": 0.9, "valence": 0.85},
    "running": {"danceability": 0.9, "energy": 0.95, "valence": 0.9},
    "tennis": {"danceability": 0.8, "energy": 0.85, "valence": 0.85},
    "swimming": {"danceability": 0.7, "energy": 0.8, "valence": 0.8},
    "cycling": {"danceability": 0.8, "energy": 0.85, "valence": 0.85},
    "skiing": {"danceability": 0.7, "energy": 0.9, "valence": 0.85},
    "boxing": {"danceability": 0.85, "energy": 0.95, "valence": 0.8},
    "yoga": {"danceability": 0.3, "energy": 0.4, "valence": 0.7},
    "gym": {"danceability": 0.8, "energy": 0.9, "valence": 0.85},

    # Festivals
    "diwali": {"danceability": 0.9, "energy": 0.9, "valence": 0.95},
    "christmas": {"danceability": 0.85, "energy": 0.85, "valence": 0.95},
    "holi": {"danceability": 0.95, "energy": 0.95, "valence": 0.95},
    "eid": {"danceability": 0.8, "energy": 0.85, "valence": 0.9},
    "halloween": {"danceability": 0.7, "energy": 0.8, "valence": 0.75},
    "navratri": {"danceability": 0.9, "energy": 0.9, "valence": 0.9},
    "pongal": {"danceability": 0.8, "energy": 0.8, "valence": 0.85},
    "thanksgiving": {"danceability": 0.7, "energy": 0.7, "valence": 0.85},
    "new_year": {"danceability": 0.9, "energy": 0.95, "valence": 0.95},
    "raksha_bandhan": {"danceability": 0.7, "energy": 0.75, "valence": 0.9},

    # Life events & Celebrations
    "weddings": {"danceability": 0.8, "energy": 0.8, "valence": 0.95},
    "celebration": {"danceability": 0.9, "energy": 0.85, "valence": 0.95},
    "graduation": {"danceability": 0.8, "energy": 0.85, "valence": 0.9},
    "birthday": {"danceability": 0.9, "energy": 0.9, "valence": 0.95},
    "anniversary": {"danceability": 0.7, "energy": 0.7, "valence": 0.9},
    "promotion": {"danceability": 0.8, "energy": 0.85, "valence": 0.9},
    "retirement": {"danceability": 0.5, "energy": 0.4, "valence": 0.8},

    # Places / Travel
    "city": {"danceability": 0.7, "energy": 0.8, "valence": 0.75},
    "countryside": {"danceability": 0.4, "energy": 0.5, "valence": 0.7},
    "desert": {"danceability": 0.5, "energy": 0.6, "valence": 0.65},
    "waterfall": {"danceability": 0.6, "energy": 0.7, "valence": 0.8},

    # Emotions / Vibes
    "anxious": {"danceability": 0.3, "energy": 0.5, "valence": 0.3},
    "excited": {"danceability": 0.9, "energy": 0.95, "valence": 0.9},
    "surprised": {"danceability": 0.7, "energy": 0.8, "valence": 0.75},
    "thankful": {"danceability": 0.6, "energy": 0.6, "valence": 0.85},
    "playful": {"danceability": 0.85, "energy": 0.9, "valence": 0.9},
    "sleepy": {"danceability": 0.2, "energy": 0.1, "valence": 0.3},

    # Activities / Hobbies
    "reading": {"danceability": 0.2, "energy": 0.2, "valence": 0.6},
    "gaming": {"danceability": 0.5, "energy": 0.7, "valence": 0.75},
    "cooking": {"danceability": 0.5, "energy": 0.6, "valence": 0.8},
    "painting": {"danceability": 0.4, "energy": 0.5, "valence": 0.8},
    "dancing": {"danceability": 0.95, "energy": 0.95, "valence": 0.9},
    "photography": {"danceability": 0.5, "energy": 0.6, "valence": 0.8},

    # College-related
    "class": {"danceability": 0.3, "energy": 0.4, "valence": 0.6},
    "lecture": {"danceability": 0.2, "energy": 0.3, "valence": 0.5},
    "exam": {"danceability": 0.2, "energy": 0.6, "valence": 0.4},
    "library": {"danceability": 0.2, "energy": 0.3, "valence": 0.6},
    "hostel_life": {"danceability": 0.5, "energy": 0.6, "valence": 0.75},
    "college_fest": {"danceability": 0.9, "energy": 0.9, "valence": 0.95},
    "sports_day": {"danceability": 0.85, "energy": 0.9, "valence": 0.9},
    "group_study": {"danceability": 0.4, "energy": 0.5, "valence": 0.7},
    "canteen_time": {"danceability": 0.5, "energy": 0.6, "valence": 0.8},
    "college_trip": {"danceability": 0.8, "energy": 0.85, "valence": 0.9},
    "project_work": {"danceability": 0.3, "energy": 0.5, "valence": 0.7},
    "presentation_day": {"danceability": 0.4, "energy": 0.6, "valence": 0.75},
    "exam_result": {"danceability": 0.3, "energy": 0.5, "valence": 0.6},
    "friendship_moments": {"danceability": 0.7, "energy": 0.75, "valence": 0.9},

    # Other
    "politics": {"danceability": 0.4, "energy": 0.5, "valence": 0.5},
    "teaching": {"danceability": 0.5, "energy": 0.5, "valence": 0.7},

        # Car / Road Travel
    "car": {"danceability": 0.6, "energy": 0.7, "valence": 0.75},
    "road_trip": {"danceability": 0.8, "energy": 0.85, "valence": 0.9},
    "long_drive": {"danceability": 0.6, "energy": 0.6, "valence": 0.8},
    "night_drive": {"danceability": 0.5, "energy": 0.6, "valence": 0.7},
    "highway": {"danceability": 0.7, "energy": 0.8, "valence": 0.8},
    "driving": {"danceability": 0.6, "energy": 0.7, "valence": 0.75},
    "solo_drive": {"danceability": 0.4, "energy": 0.5, "valence": 0.6},
    "friends_trip": {"danceability": 0.85, "energy": 0.9, "valence": 0.95},
    "family_trip": {"danceability": 0.6, "energy": 0.65, "valence": 0.85},
    "roadside_views": {"danceability": 0.5, "energy": 0.6, "valence": 0.75},
    "mountain_drive": {"danceability": 0.6, "energy": 0.75, "valence": 0.85},
    "coastal_drive": {"danceability": 0.7, "energy": 0.7, "valence": 0.9},
    "rainy_drive": {"danceability": 0.4, "energy": 0.4, "valence": 0.6},
    "sunset_drive": {"danceability": 0.5, "energy": 0.4, "valence": 0.8},


    "dance": {"danceability": 0.95, "energy": 0.95, "valence": 0.9},
    "dance_floor": {"danceability": 0.95, "energy": 0.95, "valence": 0.9},
    "groove": {"danceability": 0.9, "energy": 0.85, "valence": 0.9},
    "freestyle": {"danceability": 0.9, "energy": 0.9, "valence": 0.85},
    "hip_hop": {"danceability": 0.85, "energy": 0.9, "valence": 0.8},
    "bollywood_dance": {"danceability": 0.9, "energy": 0.9, "valence": 0.95},
    "dance_practice": {"danceability": 0.85, "energy": 0.9, "valence": 0.85},

    "food": {"danceability": 0.6, "energy": 0.6, "valence": 0.85},
    "foodie": {"danceability": 0.65, "energy": 0.7, "valence": 0.9},
    "street_food": {"danceability": 0.7, "energy": 0.75, "valence": 0.9},
    "home_food": {"danceability": 0.5, "energy": 0.5, "valence": 0.85},
    "coffee": {"danceability": 0.4, "energy": 0.5, "valence": 0.75},
    "dessert": {"danceability": 0.6, "energy": 0.6, "valence": 0.9},
    "pizza_time": {"danceability": 0.7, "energy": 0.7, "valence": 0.9},
    "late_night_snacks": {"danceability": 0.6, "energy": 0.6, "valence": 0.8},

    "outfit_check": {"danceability": 0.7, "energy": 0.7, "valence": 0.85},
    "traditional_wear": {"danceability": 0.6, "energy": 0.6, "valence": 0.85},
    "fashion": {"danceability": 0.75, "energy": 0.8, "valence": 0.85},
    "ethnic_look": {"danceability": 0.6, "energy": 0.6, "valence": 0.8},
    "style_vibes": {"danceability": 0.8, "energy": 0.8, "valence": 0.9},

    "shopping": {"danceability": 0.8, "energy": 0.85, "valence": 0.9},
    "mall_time": {"danceability": 0.75, "energy": 0.8, "valence": 0.85},
    "online_shopping": {"danceability": 0.7, "energy": 0.7, "valence": 0.85},
    "sale_day": {"danceability": 0.85, "energy": 0.9, "valence": 0.9},
    "window_shopping": {"danceability": 0.6, "energy": 0.6, "valence": 0.75},

    "new_gadget": {"danceability": 0.7, "energy": 0.8, "valence": 0.85},
    "tech_life": {"danceability": 0.6, "energy": 0.7, "valence": 0.8},
    "smartphone": {"danceability": 0.65, "energy": 0.7, "valence": 0.8},
    "laptop_work": {"danceability": 0.4, "energy": 0.6, "valence": 0.7},
    "gaming_setup": {"danceability": 0.8, "energy": 0.9, "valence": 0.85},

    # Confidence-based moods
    "confident": {"danceability": 0.8, "energy": 0.85, "valence": 0.9},
    "self_confident": {"danceability": 0.75, "energy": 0.8, "valence": 0.9},
    "bold": {"danceability": 0.85, "energy": 0.9, "valence": 0.88},
    "fearless": {"danceability": 0.8, "energy": 0.9, "valence": 0.9},
    "strong": {"danceability": 0.7, "energy": 0.85, "valence": 0.85},
    "powerful": {"danceability": 0.8, "energy": 0.9, "valence": 0.88},
    "determined": {"danceability": 0.65, "energy": 0.85, "valence": 0.8},
    "focused": {"danceability": 0.6, "energy": 0.8, "valence": 0.75},
    "winning": {"danceability": 0.85, "energy": 0.9, "valence": 0.92},
    "leader_vibes": {"danceability": 0.75, "energy": 0.85, "valence": 0.9},
    "unstoppable": {"danceability": 0.85, "energy": 0.95, "valence": 0.9},
    "boss_vibes": {"danceability": 0.8, "energy": 0.9, "valence": 0.88},
    "success": {"danceability": 0.75, "energy": 0.85, "valence": 0.9},
    "achievement": {"danceability": 0.7, "energy": 0.8, "valence": 0.88},
    "proud": {"danceability": 0.65, "energy": 0.75, "valence": 0.85},
}

# --------------------------
# Recommend top 2 new Hindi songs
# --------------------------
def recommend_new_songs(caption, top_n=2):
    caption_lower = caption.lower()
    matched_moods = [mood for mood in caption_to_mood if mood in caption_lower]

    if not matched_moods:
        matched_moods = ["happy"]  # default mood

    target_features = caption_to_mood[matched_moods[0]]

    # Search Spotify for tracks using the keyword
    results = sp.search(q=matched_moods[0], type="track", limit=50)

    song_candidates = []

    for item in results['tracks']['items']:
        if item['id'] in playlist_ids:
            continue  # skip songs already in your playlist
        name = item['name']
        artist = item['artists'][0]['name']

        # Filter Hindi songs only (basic keyword check)
        if not any(word in name.lower() for word in ["hindi", "bollywood"]) and \
           not any(word in artist.lower() for word in ["arijit", "shreya", "neha", "atif", "sonu"]):
            continue

        features_list = get_audio_features_safe([item['id']])
        if not features_list:
            continue  # skip if features not available

        features = features_list[0]

        # similarity score: lower = closer to playlist mood
        score = np.sqrt(
            (features['danceability'] - target_features['danceability'])**2 +
            (features['energy'] - target_features['energy'])**2 +
            (features['valence'] - target_features['valence'])**2
        )
        song_candidates.append((score, f"{name} by {artist}"))

    # Sort by similarity
    song_candidates.sort(key=lambda x: x[0])

    # Return top N
    recommendations = [s[1] for s in song_candidates[:top_n]]

    # fallback if no Hindi songs found
    if not recommendations:
        recommendations = [f"{item['name']} by {item['artists'][0]['name']}" 
                           for item in results['tracks']['items'][:top_n]]

    return recommendations

# --------------------------
# Example usage
# --------------------------
caption_input = input("Enter your caption: ")
top_songs = recommend_new_songs(caption_input, top_n=2)

print("\nTop 2 NEW Hindi Songs based on your playlist and caption:")
for s in top_songs:
    print("-", s)
