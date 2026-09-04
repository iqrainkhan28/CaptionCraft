import tkinter as tk
import threading
import yt_dlp
import vlc
import os

# VLC path (adjust if installed elsewhere)
vlc_path = r"C:\Program Files\VideoLAN\VLC"
os.add_dll_directory(vlc_path)

player = None  # Global VLC player

def play_song():
    global player
    song_name = song_entry.get()
    if not song_name:
        label_var.set("Please enter a song name")
        return

    # Search YouTube and get first result URL
    ydl_opts = {'format': 'bestaudio/best', 'quiet': True, 'noplaylist': True, 'default_search': 'ytsearch1'}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(song_name, download=False)
        audio_url = info['entries'][0]['url']
        title = info['entries'][0]['title']

    # Create VLC player and play
    if player:
        player.stop()
    player = vlc.MediaPlayer(audio_url)
    player.play()
    label_var.set(f"Now Playing: {title}")

def stop_song():
    global player
    if player:
        player.stop()
        label_var.set("Playback Stopped")

# ---- GUI ----
root = tk.Tk()
root.title("YouTube Music Player")
root.geometry("500x200")

label_var = tk.StringVar()
label_var.set("Enter song name and click Play")
label = tk.Label(root, textvariable=label_var, font=("Arial", 12))
label.pack(pady=20)

song_entry = tk.Entry(root, width=40, font=("Arial", 12))
song_entry.pack(pady=10)

play_button = tk.Button(root, text="Play", width=10, bg="green", fg="white",
                        command=lambda: threading.Thread(target=play_song, daemon=True).start())
play_button.pack(side="left", padx=50, pady=20)

stop_button = tk.Button(root, text="Stop", width=10, bg="red", fg="white", command=stop_song)
stop_button.pack(side="right", padx=50, pady=20)

root.mainloop()
