import sounddevice as sd
import audiofile as af
from scipy.io.wavfile import write
from gtts import gTTS
import pyttsx3  

 

# ✅ Record audio for a fixed duration
def record_audio(filename, sec=5, sr=44100):
    audio = sd.rec(int(sec * sr), samplerate=sr, channels=2)
    sd.wait()
    write(filename, sr, audio)

# ✅ Record audio manually (start/stop with input prompts — terminal only)
def record_audio_manual(filename, sr=44100):
    input("  ** Press enter to start recording **")
    audio = sd.rec(int(10 * sr), samplerate=sr, channels=2)
    input("  ** Press enter to stop recording **")
    sd.stop()
    write(filename, sr, audio)

# ✅ Play an audio file
def play_audio(filename):
    signal, sr = af.read(filename)
    sd.play(signal, sr)

 

# ✅ Save text as MP3 using gTTS
def save_text_as_audio(text, audio_filename):
    tts = gTTS(text=text, lang='en', slow=False)
    tts.save(audio_filename)