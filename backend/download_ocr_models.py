import os
import easyocr

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

MODEL_DIR = os.path.join(
    BASE_DIR,
    "ai",
    "easyocr_models"
)

os.makedirs(MODEL_DIR, exist_ok=True)

print("=" * 70)
print("DOWNLOADING EASY OCR MODELS")
print("=" * 70)

print("Model directory:")
print(MODEL_DIR)

reader = easyocr.Reader(
    ['en'],
    gpu=False,
    model_storage_directory=MODEL_DIR,
    download_enabled=True,
    verbose=True
)

print("=" * 70)
print("✅ EASY OCR MODELS DOWNLOADED SUCCESSFULLY")
print("=" * 70)