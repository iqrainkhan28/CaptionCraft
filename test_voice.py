from voice.voice_module import listen, speak

text = listen()
print("You said:", text)
speak("You said " + text)
