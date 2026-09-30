print("NEW OCR.PY LOADED")

import easyocr
import cv2
import re
import gc


# ============================================================
# EASY OCR READER
# ============================================================

reader = None


def load_reader():
    """
    Load EasyOCR only when OCR is required.
    """

    global reader

    if reader is None:

        print("=" * 60)
        print("Loading EasyOCR...")
        print("=" * 60)

        reader = easyocr.Reader(
            ['en'],
            gpu=False,
            verbose=False
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

        try:
            del reader
        except Exception:
            pass

        reader = None

        gc.collect()

        print("EasyOCR unloaded.")


# ============================================================
# OCR FUNCTION
# ============================================================

def read_meter(image_path):

    print("=" * 50)
    print("Opening:", image_path)
    print("=" * 50)

    image = cv2.imread(image_path)

    if image is None:

        print("ERROR: Image not found!")

        return ""


    print("Original Shape:", image.shape)


    try:

        # ----------------------------------------------------
        # Convert to grayscale
        # ----------------------------------------------------

        gray = cv2.cvtColor(
            image,
            cv2.COLOR_BGR2GRAY
        )

        print("Gray Shape:", gray.shape)


        # ----------------------------------------------------
        # Resize extremely large images
        # ----------------------------------------------------

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


        # ----------------------------------------------------
        # Reduce noise
        # ----------------------------------------------------

        gray = cv2.GaussianBlur(
            gray,
            (3, 3),
            0
        )


        # ----------------------------------------------------
        # Improve contrast
        # ----------------------------------------------------

        processed = cv2.threshold(
            gray,
            0,
            255,
            cv2.THRESH_BINARY + cv2.THRESH_OTSU
        )[1]


        print("Starting OCR...")


        # ----------------------------------------------------
        # Load EasyOCR
        # ----------------------------------------------------

        ocr_reader = load_reader()


        # ----------------------------------------------------
        # Run OCR
        # ----------------------------------------------------

        results = ocr_reader.readtext(
            processed,
            detail=0,
            paragraph=False,
            batch_size=1,
            workers=0
        )


        print("OCR Finished!")
        print("OCR Results:", results)


        # ----------------------------------------------------
        # Combine detected text
        # ----------------------------------------------------

        text = " ".join(results)

        print("Detected Text:", text)


        # ----------------------------------------------------
        # Find numbers
        # ----------------------------------------------------

        numbers = re.findall(
            r"\d+",
            text
        )

        print("Numbers Found:", numbers)


        # ----------------------------------------------------
        # Select longest number
        # ----------------------------------------------------

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


        print("No numbers detected.")

        return ""


    except Exception as e:

        print("=" * 60)
        print("OCR ERROR")
        print("=" * 60)
        print(e)

        return ""


    finally:

        # ----------------------------------------------------
        # Release temporary image data
        # ----------------------------------------------------

        try:
            del image
            del gray
            del processed
        except Exception:
            pass

        gc.collect()


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":

    print("OCR module test.")