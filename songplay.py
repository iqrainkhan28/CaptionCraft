import os
from playsound import playsound

# 1️⃣ Song name input
song_name = input("Subha Hone Na De by Pritam")

# 2️⃣ Download song from YouTube as MP3 using yt-dlp
# Output file format: SongTitle.mp3
os.system(f'yt-dlp -x --audio-format mp3 "ytsearch1:{song_name}" -o "%(title)s.%(ext)s"')

# 3️⃣ Find the downloaded MP3 file (latest one)
files = [f for f in os.listdir() if f.endswith('.mp3')]
latest_file = max(files, key=os.path.getctime)  # Latest downloaded MP3

# 4️⃣ Play the song in terminal
print(f"Playing: {latest_file}")
playsound(latest_file)

