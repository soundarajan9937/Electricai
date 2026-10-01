import os
import re
import cv2
import pytesseract
from collections import defaultdict


# ============================================================
# TESSERACT
# ============================================================

TESSERACT_PATH = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

if os.path.exists(TESSERACT_PATH):
    pytesseract.pytesseract.tesseract_cmd = TESSERACT_PATH


_reader_ready = False


# ============================================================
# LOAD OCR
# ============================================================

def load_reader():
    global _reader_ready

    if _reader_ready:
        return

    try:
        version = pytesseract.get_tesseract_version()
        print("Tesseract version:", version)

        _reader_ready = True

        print("OCR reader ready.")

    except Exception as e:
        print("Tesseract initialization error:", e)
        _reader_ready = False


# ============================================================
# UNLOAD OCR
# ============================================================

def unload_reader():
    global _reader_ready

    _reader_ready = False

    print("OCR reader unloaded.")


# ============================================================
# CLEAN TEXT
# ============================================================

def clean_text(text):

    if not text:
        return ""

    text = text.strip()

    # Only numbers and decimal point
    text = re.sub(r"[^0-9.]", "", text)

    # Multiple dots -> one
    text = re.sub(r"\.{2,}", ".", text)

    # Remove dots at beginning/end
    text = text.strip(".")

    return text


# ============================================================
# NORMALIZE READING
# ============================================================

def normalize_reading(text):

    if not text:
        return None

    text = clean_text(text)

    if not text:
        return None

    # --------------------------------------------------------
    # EXPLICIT DECIMAL
    # Example:
    # 3560.8
    # 3769.9
    # --------------------------------------------------------

    if "." in text:

        parts = text.split(".")

        if len(parts) != 2:
            return None

        integer_part = re.sub(
            r"\D",
            "",
            parts[0]
        )

        decimal_part = re.sub(
            r"\D",
            "",
            parts[1]
        )

        if not integer_part or not decimal_part:
            return None

        # Meter reading uses one decimal digit
        decimal_part = decimal_part[0]

        integer_part = integer_part.lstrip("0")

        if integer_part == "":
            integer_part = "0"

        try:

            value = float(
                integer_part + "." + decimal_part
            )

            if value <= 0:
                return None

            return round(value, 1)

        except ValueError:

            return None

    # --------------------------------------------------------
    # DIGITS ONLY
    # --------------------------------------------------------

    digits = re.sub(
        r"\D",
        "",
        text
    )

    if not digits:
        return None

    # --------------------------------------------------------
    # IMPORTANT
    #
    # 6 digits are accepted ONLY when the first digit is 0.
    #
    # 035608 -> 3560.8
    #
    # 137655 -> REJECT
    # 856017 -> REJECT
    #
    # This prevents OCR from turning printed numbers into
    # fake meter readings.
    # --------------------------------------------------------

    if len(digits) == 6:

        if digits[0] != "0":
            return None

        integer_part = digits[1:5]
        decimal_part = digits[5]

        integer_part = integer_part.lstrip("0")

        if integer_part == "":
            integer_part = "0"

        try:

            value = float(
                integer_part + "." + decimal_part
            )

            if value <= 0:
                return None

            return round(value, 1)

        except ValueError:

            return None

    # --------------------------------------------------------
    # 5 digits
    #
    # 37699 -> 3769.9
    # 35608 -> 3560.8
    # --------------------------------------------------------

    if len(digits) == 5:

        integer_part = digits[:4]
        decimal_part = digits[4]

        integer_part = integer_part.lstrip("0")

        if integer_part == "":
            integer_part = "0"

        try:

            value = float(
                integer_part + "." + decimal_part
            )

            if value <= 0:
                return None

            return round(value, 1)

        except ValueError:

            return None

    # --------------------------------------------------------
    # Everything else rejected
    # --------------------------------------------------------

    return None


# ============================================================
# EXTRACT CANDIDATES
# ============================================================

def extract_candidates(text):

    candidates = []

    if not text:
        return candidates

    cleaned = clean_text(text)

    if not cleaned:
        return candidates

    # --------------------------------------------------------
    # EXPLICIT DECIMAL
    # --------------------------------------------------------

    decimal_matches = re.findall(
        r"\d{3,5}\.\d",
        cleaned
    )

    for item in decimal_matches:

        value = normalize_reading(item)

        if value is not None:

            candidates.append({
                "value": value,
                "source": item,
                "type": "explicit_decimal"
            })

    # --------------------------------------------------------
    # DIGIT GROUPS
    #
    # IMPORTANT:
    # NO SUBSTRING EXTRACTION
    #
    # This prevents:
    # 137655 -> 37655
    # 137655 -> 13765
    # etc.
    # --------------------------------------------------------

    digit_matches = re.findall(
        r"\d{5,6}",
        cleaned
    )

    for item in digit_matches:

        value = normalize_reading(item)

        if value is not None:

            candidates.append({
                "value": value,
                "source": item,
                "type": "implicit_decimal"
            })

    return candidates


# ============================================================
# IMAGE PREPROCESSING
# ============================================================

def prepare_images(image):

    result = {}

    # --------------------------------------------------------
    # Original grayscale
    # --------------------------------------------------------

    gray = cv2.cvtColor(
        image,
        cv2.COLOR_BGR2GRAY
    )

    result["gray"] = gray

    # --------------------------------------------------------
    # 4X UPSCALE
    # --------------------------------------------------------

    enlarged = cv2.resize(
        gray,
        None,
        fx=4.0,
        fy=4.0,
        interpolation=cv2.INTER_CUBIC
    )

    result["upscaled"] = enlarged

    # --------------------------------------------------------
    # Gaussian blur
    # --------------------------------------------------------

    blurred = cv2.GaussianBlur(
        enlarged,
        (3, 3),
        0
    )

    result["blurred"] = blurred

    # --------------------------------------------------------
    # CLAHE
    # --------------------------------------------------------

    clahe = cv2.createCLAHE(
        clipLimit=2.0,
        tileGridSize=(8, 8)
    )

    clahe_image = clahe.apply(
        enlarged
    )

    result["clahe"] = clahe_image

    # --------------------------------------------------------
    # OTSU
    # --------------------------------------------------------

    _, otsu = cv2.threshold(
        clahe_image,
        0,
        255,
        cv2.THRESH_BINARY + cv2.THRESH_OTSU
    )

    result["otsu"] = otsu

    # --------------------------------------------------------
    # ADAPTIVE THRESHOLD
    # --------------------------------------------------------

    adaptive = cv2.adaptiveThreshold(
        clahe_image,
        255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        31,
        7
    )

    result["adaptive"] = adaptive

    # --------------------------------------------------------
    # INVERSE OTSU
    # --------------------------------------------------------

    _, inverse = cv2.threshold(
        clahe_image,
        0,
        255,
        cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU
    )

    result["inverse"] = inverse

    return result


# ============================================================
# RUN OCR
# ============================================================

def run_ocr(
    image,
    psm
):

    config = (
        f"--psm {psm} "
        "-c tessedit_char_whitelist=0123456789."
    )

    try:

        data = pytesseract.image_to_data(
            image,
            config=config,
            output_type=pytesseract.Output.DICT
        )

    except Exception as e:

        print(
            "Tesseract error:",
            e
        )

        return []

    results = []

    total = len(
        data["text"]
    )

    for i in range(total):

        raw_text = data["text"][i].strip()

        if not raw_text:
            continue

        try:

            confidence = float(
                data["conf"][i]
            )

        except Exception:

            confidence = 0.0

        # ----------------------------------------------------
        # Reject zero/negative confidence
        # ----------------------------------------------------

        if confidence <= 0:
            continue

        cleaned = clean_text(
            raw_text
        )

        if not cleaned:
            continue

        candidates = extract_candidates(
            cleaned
        )

        for candidate in candidates:

            candidate["confidence"] = confidence

            candidate["bbox"] = (
                int(data["left"][i]),
                int(data["top"][i]),
                int(data["width"][i]),
                int(data["height"][i])
            )

            results.append(candidate)

    return results


# ============================================================
# SELECT BEST READING
# ============================================================

def select_best_reading(candidates):

    if not candidates:
        return None

    # --------------------------------------------------------
    # Only reliable candidates
    # --------------------------------------------------------

    candidates = [
        item
        for item in candidates
        if item.get("confidence", 0) >= 10
    ]

    if not candidates:
        return None

    # --------------------------------------------------------
    # Group readings by exact integer part
    #
    # 3765.5
    # 3765.3
    #
    # => group 3765
    # --------------------------------------------------------

    groups = defaultdict(list)

    for item in candidates:

        value = item["value"]

        integer_part = int(value)

        groups[integer_part].append(
            item
        )

    # --------------------------------------------------------
    # Score groups
    # --------------------------------------------------------

    group_results = []

    for integer_part, items in groups.items():

        count = len(items)

        confidence_sum = sum(
            item["confidence"]
            for item in items
        )

        max_confidence = max(
            item["confidence"]
            for item in items
        )

        # Repetition + confidence
        score = (
            count * 100
            + confidence_sum
            + max_confidence * 2
        )

        group_results.append(
            (
                score,
                integer_part,
                items
            )
        )

    group_results.sort(
        key=lambda x: x[0],
        reverse=True
    )

    best_score, best_integer, best_items = (
        group_results[0]
    )

    # --------------------------------------------------------
    # Decimal digit consensus
    # --------------------------------------------------------

    decimal_groups = defaultdict(list)

    for item in best_items:

        value = item["value"]

        decimal_digit = int(
            round(
                (value - int(value)) * 10
            )
        )

        decimal_groups[
            decimal_digit
        ].append(item)

    decimal_results = []

    for decimal_digit, items in decimal_groups.items():

        count = len(items)

        confidence_sum = sum(
            item["confidence"]
            for item in items
        )

        max_confidence = max(
            item["confidence"]
            for item in items
        )

        score = (
            count * 100
            + confidence_sum
            + max_confidence * 2
        )

        decimal_results.append(
            (
                score,
                decimal_digit,
                items
            )
        )

    decimal_results.sort(
        key=lambda x: x[0],
        reverse=True
    )

    final_score, best_decimal, decimal_items = (
        decimal_results[0]
    )

    final_value = round(
        best_integer + best_decimal / 10,
        1
    )

    best_candidate = max(
        decimal_items,
        key=lambda x: x["confidence"]
    )

    return {
        "value": final_value,
        "score": round(
            final_score,
            2
        ),
        "confidence": round(
            best_candidate["confidence"],
            2
        ),
        "source": best_candidate["source"],
        "type": best_candidate["type"],
        "supporting_candidates": len(
            best_items
        )
    }


# ============================================================
# MAIN FUNCTION
# ============================================================

def read_meter(image_path):

    print("")
    print("========================================")
    print("        SMART METER OCR")
    print("========================================")

    if not os.path.exists(image_path):

        print(
            "OCR image does not exist:",
            image_path
        )

        return None

    load_reader()

    image = cv2.imread(
        image_path
    )

    if image is None:

        print(
            "Unable to read OCR image."
        )

        return None

    print(
        "OCR image:",
        image_path
    )

    print(
        "Image shape:",
        image.shape
    )

    # --------------------------------------------------------
    # PREPROCESS
    # --------------------------------------------------------

    images = prepare_images(
        image
    )

    print("")
    print(
        "OCR preprocessing completed."
    )

    # --------------------------------------------------------
    # OCR MODES
    # --------------------------------------------------------

    psm_modes = [
        6,
        7,
        8,
        10,
        11,
        13
    ]

    all_candidates = []

    # --------------------------------------------------------
    # RUN ALL OCR
    # --------------------------------------------------------

    for image_name, processed in images.items():

        print("")
        print(
            "OCR region:",
            image_name
        )

        for psm in psm_modes:

            results = run_ocr(
                processed,
                psm
            )

            for result in results:

                result["region"] = image_name
                result["psm"] = psm

                all_candidates.append(
                    result
                )

    print("")
    print(
        "Total valid OCR candidates:",
        len(all_candidates)
    )

    # --------------------------------------------------------
    # PRINT CANDIDATES
    # --------------------------------------------------------

    print("")
    print("OCR CANDIDATES:")

    printed = set()

    for item in all_candidates:

        key = (
            item["value"],
            item["source"],
            item["region"],
            item["psm"]
        )

        if key in printed:
            continue

        printed.add(key)

        print(
            f'{item["value"]:.1f}',
            "| source=",
            item["source"],
            "| conf=",
            round(
                item["confidence"],
                1
            ),
            "| region=",
            item["region"],
            "| PSM=",
            item["psm"]
        )

    # --------------------------------------------------------
    # SELECT
    # --------------------------------------------------------

    selected = select_best_reading(
        all_candidates
    )

    if selected is None:

        print("")
        print(
            "Unable to determine meter reading."
        )

        return None

    # --------------------------------------------------------
    # FINAL
    # --------------------------------------------------------

    final_reading = (
        f'{selected["value"]:.1f}'
    )

    print("")
    print("========================================")
    print("FINAL METER READING")
    print("========================================")

    print(
        "Reading:",
        final_reading
    )

    print(
        "Consensus score:",
        selected["score"]
    )

    print(
        "Best OCR confidence:",
        selected["confidence"]
    )

    print(
        "OCR source:",
        selected["source"]
    )

    print(
        "OCR type:",
        selected["type"]
    )

    print(
        "Supporting candidates:",
        selected["supporting_candidates"]
    )

    print("========================================")
    print("")

    return final_reading


# ============================================================
# DIRECT TEST
# ============================================================

if __name__ == "__main__":

    test_image = os.path.join(
        os.path.dirname(__file__),
        "display_for_ocr.jpg"
    )

    result = read_meter(
        test_image
    )

    print("")
    print("TEST RESULT")
    print(
        "READING:",
        result
    )