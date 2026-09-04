import os
import yt_dlp
import vlc
import time

# ⚡ VLC path (adjust if VLC is installed elsewhere)
vlc_path = r"C:\Program Files\VideoLAN\VLC"
os.add_dll_directory(vlc_path)

# 1️⃣ Get song name input
song_name = input("Enter the song name: ")

# 2️⃣ Fetch audio URL from YouTube
ydl_opts = {
    'format': 'bestaudio/best',
    'quiet': True,
    'noplaylist': True,
    'default_search': 'ytsearch1',  # first search result
}

with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    info = ydl.extract_info(song_name, download=False)
    audio_url = info['entries'][0]['url']
    song_title = info['entries'][0]['title']
    duration = info['entries'][0].get('duration', 0)  # duration in seconds

if duration == 0:
    duration = 300  # fallback to 5 minutes

# 3️⃣ Play the audio stream
player = vlc.MediaPlayer(audio_url)
player.play()
print(f"Now playing: {song_title}")
print("Press Ctrl+C to stop playback.")

# 4️⃣ Keep program alive while song plays
try:
    for _ in range(duration):
        time.sleep(1)
except KeyboardInterrupt:
    print("\nStopping playback...")
player.stop()
