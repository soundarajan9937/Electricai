from ultralytics import YOLO
import os
import cv2
import gc


# Current folder: backend/ai
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Trained YOLO model
MODEL_PATH = os.path.join(BASE_DIR, "models", "best.pt")

# Keep model as None until it is actually needed.
# This prevents YOLO from loading when Flask starts.
model = None


def load_model():
    """
    Load YOLO only when detection is actually required.
    """

    global model

    if model is None:
        print("=" * 60)
        print("Loading YOLO model...")
        print("Model:", MODEL_PATH)
        print("=" * 60)

        model = YOLO(MODEL_PATH)

        print("YOLO model loaded successfully.")

    return model


def detect_meter(image_path):
    """
    Detect the meter and create a cropped meter image.

    Returns:
        True, crop_path
    or
        False, None
    """

    global model

    # Convert to absolute path
    if not os.path.isabs(image_path):
        image_path = os.path.join(os.getcwd(), image_path)

    if not os.path.exists(image_path):
        print("Image not found:", image_path)
        return False, None

    # Read image
    image = cv2.imread(image_path)

    if image is None:
        print("Cannot read image.")
        return False, None

    print("Image loaded successfully.")
    print("Image shape:", image.shape)

    try:

        # Load YOLO only now
        detector = load_model()

        print("Running YOLO detection...")

        results = detector.predict(
            source=image,
            conf=0.10,
            imgsz=640,
            save=False,
            verbose=False,
            device="cpu"
        )

        if len(results) == 0:
            print("No YOLO results.")
            return False, None

        result = results[0]

        if result.boxes is None or len(result.boxes) == 0:
            print("No meter detected.")
            return False, None

        print("Meter detected.")

        # Take the first detected object
        box = result.boxes.xyxy[0].cpu().numpy()

        x1, y1, x2, y2 = map(int, box)

        height, width = image.shape[:2]

        # Keep coordinates inside image
        x1 = max(0, x1)
        y1 = max(0, y1)
        x2 = min(width, x2)
        y2 = min(height, y2)

        crop = image[y1:y2, x1:x2]

        if crop.size == 0:
            print("Crop is empty.")
            return False, None

        print("Crop shape:", crop.shape)

        # Save cropped meter image
        crop_path = os.path.join(BASE_DIR, "cropped_meter.jpg")

        success = cv2.imwrite(crop_path, crop)

        if not success:
            print("Failed to save cropped image.")
            return False, None

        print("Meter crop saved:")
        print(crop_path)

        return True, crop_path

    except Exception as e:

        print("YOLO DETECTION ERROR:")
        print(e)

        return False, None


def unload_model():
    """
    Release YOLO from memory before EasyOCR starts.
    This is important for Render's limited RAM.
    """

    global model

    if model is not None:

        print("=" * 60)
        print("Unloading YOLO model to free RAM...")
        print("=" * 60)

        del model
        model = None

        gc.collect()

        print("YOLO model unloaded.")


if __name__ == "__main__":

    test_image = os.path.join(
        BASE_DIR,
        "meter.jpg"
    )

    found, crop_path = detect_meter(test_image)

    print("Found:", found)

    if found:
        print("Crop:", crop_path)

    # Free memory after testing
    unload_model()