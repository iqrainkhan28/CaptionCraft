from PIL import Image
import torch
from transformers import BlipProcessor, BlipForConditionalGeneration

# -------- Load BLIP model (one-time download) --------
processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")

print("✅ BLIP model loaded")

# -------- Get image from user --------
image_path = input("Enter image filename (with extension) from current folder: ").strip()

try:
    image = Image.open(image_path).convert("RGB")
except FileNotFoundError:
    print("Image not found in current folder")
    exit()

# -------- Generate caption --------
inputs = processor(image, return_tensors="pt")
out = model.generate(**inputs, max_length=50)

caption = processor.decode(out[0], skip_special_tokens=True)

print("\n📝 Generated Caption:")
print(caption)   