from ultralytics import YOLO
import os
import cv2

# Current folder (backend/ai)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Path to trained model
MODEL_PATH = os.path.join(BASE_DIR, "models", "best.pt")

# Load YOLO model
model = YOLO(MODEL_PATH)


def detect_meter(image_path):

    if not os.path.isabs(image_path):
        image_path = os.path.join(os.getcwd(), image_path)

    if not os.path.exists(image_path):
        print("Image not found:", image_path)
        return False, None

    image = cv2.imread(image_path)

    if image is None:
        print("Cannot read image.")
        return False, None

    results = model.predict(
        source=image_path,
        conf=0.10,
        imgsz=640,
        save=False,
        verbose=False
    )

    if len(results) == 0 or len(results[0].boxes) == 0:
        print("No meter detected.")
        return False, None

    box = results[0].boxes.xyxy[0].cpu().numpy()

    x1, y1, x2, y2 = map(int, box)

    h, w = image.shape[:2]

    x1 = max(0, x1)
    y1 = max(0, y1)
    x2 = min(w, x2)
    y2 = min(h, y2)

    crop = image[y1:y2, x1:x2]

    if crop.size == 0:
        print("Crop is empty!")
        return False, None

    print("Crop shape:", crop.shape)

    crop_path = os.path.join(BASE_DIR, "cropped_meter.jpg")
    cv2.imwrite(crop_path, crop)

    print("Meter detected!")
    print("Saved:", crop_path)

    return True, crop_path


if __name__ == "__main__":

    found, crop_path = detect_meter("backend/ai/meter.jpg")

    print("Found:", found)

    if found:
        print("Crop:", crop_path)