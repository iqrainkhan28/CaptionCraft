from vosk import Model

model_path = r"C:\Users\ANJALI\Desktop\captioncraft\vosk-model-small-en-us-0.15"

# Try loading the model
try:
    model = Model(model_path)
    print("Model loaded successfully!")
except Exception as e:
    print("Error loading model:", e)
