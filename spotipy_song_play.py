import spotipy
from spotipy.oauth2 import SpotifyOAuth
import numpy as np

# --------------------------
# Spotify credentials
# --------------------------
CLIENT_ID = "202ca9b47dd94a69afdf92ebdccdcf4d"
CLIENT_SECRET = "924a75f96216442abb71bfa4e4e502f1"
REDIRECT_URI = "http://127.0.0.1:8888/callback"  # your redirect URI
SCOPE = "playlist-read-private user-modify-playback-state user-read-playback-state"

# --------------------------
# Spotipy automatic auth
# --------------------------
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    redirect_uri=REDIRECT_URI,
    scope=SCOPE,
    open_browser=True  # browser opens automatically
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
        if track:
            playlist_track_ids.append(track['id'])
            playlist_song_names.append(track['name'].lower())

    features = get_audio_features_safe(playlist_track_ids)

    if not features:
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
caption_to_mood = {
    "happy": {"danceability": 0.8, "energy": 0.8, "valence": 0.9},
    "sad": {"danceability": 0.3, "energy": 0.2, "valence": 0.2},
    "love": {"danceability": 0.6, "energy": 0.5, "valence": 0.7},
    "party": {"danceability": 0.9, "energy": 0.9, "valence": 0.8},
    "chill": {"danceability": 0.4, "energy": 0.3, "valence": 0.6},
    "mountain": {"danceability": 0.6, "energy": 0.7, "valence": 0.8},
}

# --------------------------
# Play song on active device
# --------------------------
def play_song(track_uri):
    try:
        sp.start_playback(uris=[track_uri])
        print(f"Playing: {track_uri}")
    except spotipy.SpotifyException as e:
        print("Could not start playback. Make sure a Spotify device is active and you have Premium.")
        print("Error:", e)

# --------------------------
# Recommend top 2 new Hindi songs
# --------------------------
def recommend_new_songs(caption, top_n=2):
    caption_lower = caption.lower()
    matched_moods = [mood for mood in caption_to_mood if mood in caption_lower]

    if not matched_moods:
        matched_moods = ["happy"]

    target_features = caption_to_mood[matched_moods[0]]

    results = sp.search(q=matched_moods[0], type="track", limit=50)

    song_candidates = []

    for item in results['tracks']['items']:
        if item['id'] in playlist_ids:
            continue
        name = item['name']
        artist = item['artists'][0]['name']
        uri = item['uri']

        # Filter Hindi songs only (basic keyword check)
        if not any(word in name.lower() for word in ["hindi", "bollywood"]) and \
           not any(word in artist.lower() for word in ["arijit", "shreya", "neha", "atif", "sonu"]):
            continue

        features_list = get_audio_features_safe([item['id']])
        if not features_list:
            continue

        features = features_list[0]

        score = np.sqrt(
            (features['danceability'] - target_features['danceability'])**2 +
            (features['energy'] - target_features['energy'])**2 +
            (features['valence'] - target_features['valence'])**2
        )
        song_candidates.append((score, name, artist, uri))

    song_candidates.sort(key=lambda x: x[0])
    top_songs = song_candidates[:top_n]

    recommendations = []
    for _, name, artist, uri in top_songs:
        recommendations.append({"name": name, "artist": artist, "uri": uri})

    # fallback if no Hindi songs found
    if not recommendations:
        recommendations = []
        for item in results['tracks']['items'][:top_n]:
            recommendations.append({"name": item['name'], "artist": item['artists'][0]['name'], "uri": item['uri']})

    return recommendations

# --------------------------
# Main execution
# --------------------------
caption_input = input("Enter your caption: ")
top_songs = recommend_new_songs(caption_input, top_n=2)

print("\nTop 2 NEW Hindi Songs based on your playlist and caption:")
for s in top_songs:
    print("-", s["name"], "by", s["artist"])
    play_song(s["uri"])

