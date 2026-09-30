print("NEW OCR.PY LOADED")

import os
import easyocr
import cv2
import re
import gc


reader = None


# ---------------------------------------------------------
# EASY OCR MODEL DIRECTORY
# ---------------------------------------------------------

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

MODEL_DIR = os.path.join(
    BASE_DIR,
    "ai",
    "easyocr_models"
)


# ---------------------------------------------------------
# LOAD OCR
# ---------------------------------------------------------

def load_reader():

    global reader

    if reader is None:

        print("=" * 60)
        print("Loading EasyOCR from local models...")
        print("Model directory:", MODEL_DIR)
        print("=" * 60)

        reader = easyocr.Reader(
            ['en'],
            gpu=False,
            model_storage_directory=MODEL_DIR,
            download_enabled=False,
            verbose=False
        )

        print("✅ EasyOCR loaded successfully.")

    return reader


# ---------------------------------------------------------
# UNLOAD OCR
# ---------------------------------------------------------

def unload_reader():

    global reader

    if reader is not None:

        print("=" * 60)
        print("Unloading EasyOCR...")
        print("=" * 60)

        try:
            del reader
        except Exception:
            pass

        reader = None

        gc.collect()

        print("✅ EasyOCR unloaded.")


# ---------------------------------------------------------
# READ ELECTRICITY METER
# ---------------------------------------------------------

def read_meter(image_path):

    print("=" * 60)
    print("Opening:", image_path)
    print("=" * 60)

    image = cv2.imread(image_path)

    if image is None:

        print("❌ ERROR: Image not found!")

        return ""


    print("Original Shape:", image.shape)


    gray = None
    processed = None


    try:

        # -------------------------------------------------
        # CONVERT TO GRAYSCALE
        # -------------------------------------------------

        gray = cv2.cvtColor(
            image,
            cv2.COLOR_BGR2GRAY
        )

        print("Gray Shape:", gray.shape)


        # -------------------------------------------------
        # RESIZE LARGE IMAGE
        # -------------------------------------------------

        height, width = gray.shape

        max_width = 800


        if width > max_width:

            scale = max_width / width

            new_width = int(width * scale)

            new_height = int(height * scale)

            gray = cv2.resize(
                gray,
                (new_width, new_height),
                interpolation=cv2.INTER_AREA
            )

            print(
                "Resized OCR Image:",
                gray.shape
            )


        # -------------------------------------------------
        # REDUCE NOISE
        # -------------------------------------------------

        gray = cv2.GaussianBlur(
            gray,
            (3, 3),
            0
        )


        # -------------------------------------------------
        # IMPROVE CONTRAST
        # -------------------------------------------------

        processed = cv2.threshold(
            gray,
            0,
            255,
            cv2.THRESH_BINARY + cv2.THRESH_OTSU
        )[1]


        print("Starting OCR...")


        # -------------------------------------------------
        # LOAD LOCAL OCR MODEL
        # -------------------------------------------------

        ocr_reader = load_reader()


        # -------------------------------------------------
        # RUN OCR
        # -------------------------------------------------

        results = ocr_reader.readtext(
            processed,
            detail=0,
            paragraph=False,
            batch_size=1,
            workers=0
        )


        print("OCR Finished!")

        print("OCR Results:", results)


        # -------------------------------------------------
        # COMBINE TEXT
        # -------------------------------------------------

        text = " ".join(results)

        print("Detected Text:", text)


        # -------------------------------------------------
        # FIND NUMBERS
        # -------------------------------------------------

        numbers = re.findall(
            r"\d+",
            text
        )

        print("Numbers Found:", numbers)


        # -------------------------------------------------
        # SELECT LONGEST NUMBER
        # -------------------------------------------------

        if numbers:

            meter = max(
                numbers,
                key=len
            )

            print(
                "Final Meter Reading:",
                meter
            )

            return meter


        print("❌ No numbers detected.")

        return ""


    except Exception as e:

        print("=" * 60)
        print("❌ OCR ERROR")
        print("=" * 60)

        print(e)

        return ""


    finally:

        try:
            del image
        except Exception:
            pass

        try:
            del gray
        except Exception:
            pass

        try:
            del processed
        except Exception:
            pass

        gc.collect()


# ---------------------------------------------------------
# TEST
# ---------------------------------------------------------

if __name__ == "__main__":

    print("OCR module test.")