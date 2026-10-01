import cv2
import os
import json
import numpy as np
import onnxruntime as ort


# ============================================================
# PATHS
# ============================================================

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

MODEL_PATH = os.path.join(
    BASE_DIR,
    "ai",
    "models",
    "best.onnx"
)

DEBUG_DIR = os.path.join(
    BASE_DIR,
    "ai",
    "ocr_debug"
)

os.makedirs(DEBUG_DIR, exist_ok=True)


# ============================================================
# MODEL SETTINGS
# ============================================================

INPUT_SIZE = 640
CONFIDENCE_THRESHOLD = 0.20
IOU_THRESHOLD = 0.45


_session = None


# ============================================================
# LOAD MODEL
# ============================================================

def load_model():

    global _session

    if _session is not None:
        return _session

    print()
    print("=" * 60)
    print("LOADING ONNX METER MODEL")
    print("=" * 60)

    print("Model:", MODEL_PATH)

    _session = ort.InferenceSession(
        MODEL_PATH,
        providers=["CPUExecutionProvider"]
    )

    print(
        "Input:",
        _session.get_inputs()[0].shape
    )

    print(
        "Output:",
        _session.get_outputs()[0].shape
    )

    print(
        "Provider:",
        _session.get_providers()
    )

    print("=" * 60)

    return _session


# ============================================================
# IOU
# ============================================================

def calculate_iou(box1, box2):

    x1 = max(box1[0], box2[0])
    y1 = max(box1[1], box2[1])

    x2 = min(box1[2], box2[2])
    y2 = min(box1[3], box2[3])

    intersection_width = max(
        0,
        x2 - x1
    )

    intersection_height = max(
        0,
        y2 - y1
    )

    intersection = (
        intersection_width *
        intersection_height
    )

    area1 = (
        max(0, box1[2] - box1[0]) *
        max(0, box1[3] - box1[1])
    )

    area2 = (
        max(0, box2[2] - box2[0]) *
        max(0, box2[3] - box2[1])
    )

    union = area1 + area2 - intersection

    if union <= 0:
        return 0

    return intersection / union


# ============================================================
# NMS
# ============================================================

def non_max_suppression(
    boxes,
    scores,
    threshold
):

    if len(boxes) == 0:
        return []

    boxes = np.array(
        boxes,
        dtype=np.float32
    )

    scores = np.array(
        scores,
        dtype=np.float32
    )

    order = scores.argsort()[::-1]

    keep = []

    while len(order) > 0:

        index = order[0]

        keep.append(index)

        remaining = []

        for current in order[1:]:

            iou = calculate_iou(
                boxes[index],
                boxes[current]
            )

            if iou < threshold:
                remaining.append(current)

        order = np.array(
            remaining,
            dtype=np.int64
        )

    return keep


# ============================================================
# PREPROCESS
# ============================================================

def preprocess(image):

    resized = cv2.resize(
        image,
        (INPUT_SIZE, INPUT_SIZE)
    )

    rgb = cv2.cvtColor(
        resized,
        cv2.COLOR_BGR2RGB
    )

    normalized = (
        rgb.astype(np.float32) /
        255.0
    )

    tensor = np.transpose(
        normalized,
        (2, 0, 1)
    )

    tensor = np.expand_dims(
        tensor,
        axis=0
    )

    return tensor


# ============================================================
# DETECT
# ============================================================

def detect_objects(image):

    session = load_model()

    original_height, original_width = image.shape[:2]

    input_tensor = preprocess(image)

    input_name = session.get_inputs()[0].name

    outputs = session.run(
        None,
        {
            input_name: input_tensor
        }
    )

    output = outputs[0]

    print(
        "Raw output shape:",
        output.shape
    )

    # --------------------------------------------------------
    # YOLO output:
    #
    # [1, 5, 8400]
    #
    # x
    # y
    # width
    # height
    # confidence
    # --------------------------------------------------------

    predictions = output[0].T

    boxes = []
    scores = []

    scale_x = original_width / INPUT_SIZE
    scale_y = original_height / INPUT_SIZE

    for prediction in predictions:

        x_center = float(prediction[0])
        y_center = float(prediction[1])

        width = float(prediction[2])
        height = float(prediction[3])

        confidence = float(prediction[4])

        if confidence < CONFIDENCE_THRESHOLD:
            continue

        x1 = (
            x_center -
            width / 2
        )

        y1 = (
            y_center -
            height / 2
        )

        x2 = (
            x_center +
            width / 2
        )

        y2 = (
            y_center +
            height / 2
        )

        x1 *= scale_x
        y1 *= scale_y
        x2 *= scale_x
        y2 *= scale_y

        x1 = max(
            0,
            min(original_width, x1)
        )

        y1 = max(
            0,
            min(original_height, y1)
        )

        x2 = max(
            0,
            min(original_width, x2)
        )

        y2 = max(
            0,
            min(original_height, y2)
        )

        boxes.append(
            [
                int(x1),
                int(y1),
                int(x2),
                int(y2)
            ]
        )

        scores.append(
            confidence
        )

    if not boxes:
        return []

    keep = non_max_suppression(
        boxes,
        scores,
        IOU_THRESHOLD
    )

    detections = []

    for index in keep:

        detections.append(
            {
                "box": boxes[index],
                "confidence": scores[index]
            }
        )

    detections.sort(
        key=lambda item: item["confidence"],
        reverse=True
    )

    return detections


# ============================================================
# CREATE OCR CROP
# ============================================================

def create_display_crop(
    image,
    detection_box
):

    height, width = image.shape[:2]

    x1, y1, x2, y2 = detection_box

    box_width = x2 - x1
    box_height = y2 - y1

    # --------------------------------------------------------
    # Small padding around detector box.
    #
    # Important:
    # Do NOT use huge horizontal padding because that brings
    # printed serial/specification numbers into OCR.
    # --------------------------------------------------------

    horizontal_padding = int(
        box_width * 0.12
    )

    vertical_padding = int(
        box_height * 0.35
    )

    crop_x1 = max(
        0,
        x1 - horizontal_padding
    )

    crop_y1 = max(
        0,
        y1 - vertical_padding
    )

    crop_x2 = min(
        width,
        x2 + horizontal_padding
    )

    crop_y2 = min(
        height,
        y2 + vertical_padding
    )

    crop = image[
        crop_y1:crop_y2,
        crop_x1:crop_x2
    ]

    return crop, (
        crop_x1,
        crop_y1,
        crop_x2,
        crop_y2
    )


# ============================================================
# SAVE DETECTION INFORMATION
# ============================================================

def save_detection_box(
    detection_box,
    confidence,
    original_image_shape,
    display_crop_coordinates
):

    data = {
        "detection_box_original": [
            int(detection_box[0]),
            int(detection_box[1]),
            int(detection_box[2]),
            int(detection_box[3])
        ],

        "confidence": float(confidence),

        "original_image_width": int(
            original_image_shape[1]
        ),

        "original_image_height": int(
            original_image_shape[0]
        ),

        "display_crop_coordinates": [
            int(display_crop_coordinates[0]),
            int(display_crop_coordinates[1]),
            int(display_crop_coordinates[2]),
            int(display_crop_coordinates[3])
        ]
    }

    json_path = os.path.join(
        DEBUG_DIR,
        "detection_box.json"
    )

    with open(
        json_path,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            data,
            file,
            indent=4
        )

    print(
        "Detection information saved:",
        json_path
    )


# ============================================================
# MAIN DETECTION FUNCTION
# ============================================================

def detect_meter(image_path):

    print()
    print("=" * 60)
    print("ONNX METER DETECTION")
    print("=" * 60)

    image = cv2.imread(image_path)

    if image is None:

        print(
            "Unable to read image:",
            image_path
        )

        return False, None

    print(
        "Image shape:",
        image.shape
    )

    print("=" * 60)

    detections = detect_objects(image)

    if not detections:

        print()
        print(
            "NO METER / DISPLAY DETECTED"
        )

        print("=" * 60)

        return False, None

    best = detections[0]

    detection_box = best["box"]
    confidence = best["confidence"]

    x1, y1, x2, y2 = detection_box

    print()
    print("=" * 60)
    print("METER / DISPLAY DETECTED")
    print("=" * 60)

    print(
        "Confidence:",
        f"{confidence:.4f}"
    )

    print(
        "Detection box:"
    )

    print(
        "x1:",
        x1,
        "y1:",
        y1,
        "x2:",
        x2,
        "y2:",
        y2
    )

    print(
        "Detection width:",
        x2 - x1
    )

    print(
        "Detection height:",
        y2 - y1
    )

    # --------------------------------------------------------
    # Save exact detection visualization
    # --------------------------------------------------------

    debug_image = image.copy()

    cv2.rectangle(
        debug_image,
        (x1, y1),
        (x2, y2),
        (0, 255, 0),
        3
    )

    detection_debug_path = os.path.join(
        DEBUG_DIR,
        "detected_box.jpg"
    )

    cv2.imwrite(
        detection_debug_path,
        debug_image
    )

    print(
        "Detection debug image:",
        detection_debug_path
    )

    # --------------------------------------------------------
    # Create OCR crop
    # --------------------------------------------------------

    crop, crop_coordinates = create_display_crop(
        image,
        detection_box
    )

    crop_path = os.path.join(
        BASE_DIR,
        "ai",
        "cropped_meter.jpg"
    )

    cv2.imwrite(
        crop_path,
        crop
    )

    print()
    print("=" * 60)
    print("OCR DISPLAY CROP")
    print("=" * 60)

    print(
        "Crop coordinates:",
        crop_coordinates
    )

    print(
        "Crop shape:",
        crop.shape
    )

    print(
        "Crop saved:",
        crop_path
    )

    # --------------------------------------------------------
    # Save exact detector information
    # --------------------------------------------------------

    save_detection_box(
        detection_box,
        confidence,
        image.shape,
        crop_coordinates
    )

    # --------------------------------------------------------
    # Save display_for_ocr.jpg
    #
    # This is the image that ocr.py receives.
    # --------------------------------------------------------

    ocr_path = os.path.join(
        BASE_DIR,
        "ai",
        "display_for_ocr.jpg"
    )

    cv2.imwrite(
        ocr_path,
        crop
    )

    print(
        "OCR image:",
        ocr_path
    )

    print("=" * 60)

    return True, ocr_path


# ============================================================
# UNLOAD MODEL
# ============================================================

def unload_model():

    global _session

    print()
    print(
        "Unloading ONNX model..."
    )

    _session = None

    print(
        "ONNX model unloaded."
    )


# ============================================================
# DIRECT TEST
# ============================================================

if __name__ == "__main__":

    test_image = os.path.join(
        BASE_DIR,
        "uploads",
        "meter.jpg"
    )

    found, crop = detect_meter(
        test_image
    )

    print()
    print("=" * 60)
    print("TEST RESULT")
    print("=" * 60)

    print(
        "FOUND:",
        found
    )

    print(
        "OCR CROP:",
        crop
    )

    unload_model()