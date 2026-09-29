print("NEW OCR.PY LOADED")

import easyocr
import cv2
import re
import gc


# Do NOT load EasyOCR when Flask starts.
# It will be loaded only when OCR is actually required.
reader = None


def load_reader():
    """
    Load EasyOCR only when needed.
    """

    global reader

    if reader is None:

        print("=" * 60)
        print("Loading EasyOCR...")
        print("=" * 60)

        reader = easyocr.Reader(
            ['en'],
            gpu=False,
            verbose=True
        )

        print("EasyOCR loaded successfully.")

    return reader


def unload_reader():
    """
    Release EasyOCR from memory.
    """

    global reader

    if reader is not None:

        print("=" * 60)
        print("Unloading EasyOCR to free RAM...")
        print("=" * 60)

        del reader
        reader = None

        gc.collect()

        print("EasyOCR unloaded.")


def read_meter(image_path):

    print("=" * 50)
    print("Opening:", image_path)

    image = cv2.imread(image_path)

    if image is None:
        print("ERROR: Image not found!")
        return ""

    print("Original Shape:", image.shape)

    try:

        # Convert to grayscale
        gray = cv2.cvtColor(
            image,
            cv2.COLOR_BGR2GRAY
        )

        print("Gray Shape:", gray.shape)

        # Reduce noise
        gray = cv2.GaussianBlur(
            gray,
            (3, 3),
            0
        )

        # Improve contrast
        gray = cv2.threshold(
            gray,
            0,
            255,
            cv2.THRESH_BINARY + cv2.THRESH_OTSU
        )[1]

        print("Starting OCR...")

        # Load OCR only now
        ocr_reader = load_reader()

        results = ocr_reader.readtext(
            gray,
            detail=0,
            paragraph=False,
            batch_size=1,
            workers=0
        )

        print("OCR Finished!")
        print("OCR Results:", results)

        text = " ".join(results)

        print("Detected Text:", text)

        # Find numbers
        numbers = re.findall(
            r"\d+",
            text
        )

        print("Numbers Found:", numbers)

        if numbers:

            # Select the longest number
            meter = max(
                numbers,
                key=len
            )

            print(
                "Final Meter Reading:",
                meter
            )

            return meter

        print("No numbers detected.")

        return ""

    except Exception as e:

        print("OCR ERROR:")
        print(e)

        return ""


if __name__ == "__main__":

    print("OCR module test.")