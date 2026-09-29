print("NEW OCR.PY LOADED")

import easyocr
import cv2
import re

# Load OCR once
reader = easyocr.Reader(['en'], gpu=False)


def read_meter(image_path):

    print("=" * 50)
    print("Opening:", image_path)

    image = cv2.imread(image_path)

    if image is None:
        print("ERROR: Image not found!")
        return ""

    print("Original Shape:", image.shape)

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    print("Gray Shape:", gray.shape)

    # Improve OCR quality
    gray = cv2.GaussianBlur(gray, (3, 3), 0)
    gray = cv2.threshold(
        gray,
        0,
        255,
        cv2.THRESH_BINARY + cv2.THRESH_OTSU
    )[1]

    print("Starting OCR...")

    try:

        results = reader.readtext(
            gray,
            detail=0,
            paragraph=False,
            batch_size=1,
            workers=0
        )

        print("OCR Finished!")
        print("OCR Results:", results)

    except Exception as e:

        print("OCR ERROR:", e)
        return ""

    text = " ".join(results)

    print("Detected Text:", text)

    numbers = re.findall(r"\d+", text)

    print("Numbers Found:", numbers)

    if numbers:
        meter = max(numbers, key=len)
        print("Final Meter Reading:", meter)
        return meter

    print("No numbers detected.")
    return ""