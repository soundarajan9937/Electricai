from ultralytics import YOLO
import os

# Current folder (backend/ai)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Path to trained model
MODEL_PATH = os.path.join(BASE_DIR, "models", "best.pt")

# Load YOLO model
model = YOLO(MODEL_PATH)


def is_meter_image(image_path):

    results = model.predict(
        source=image_path,
        conf=0.10,      # Lower confidence threshold
        imgsz=640,
        verbose=False
    )

    for result in results:
        if len(result.boxes) > 0:
            return True

    return False