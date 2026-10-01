import os
import gc
import cv2
from datetime import datetime

from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename

from ai.meter_classifier import is_meter_image
from ai.meter_detection import detect_meter, unload_model
from ai.ocr import read_meter, unload_reader
from ai.bill_calculator import calculate_bill

from database import bills, fs


# ============================================================
# BLUEPRINT & CONSTANTS
# ============================================================

upload = Blueprint("upload", __name__)

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

UPLOAD_FOLDER = os.path.join(
    BASE_DIR,
    "uploads"
)

os.makedirs(
    UPLOAD_FOLDER,
    exist_ok=True
)

MAX_IMAGE_DIMENSION = 1600


# ============================================================
# HELPER: RESIZE LARGE IMAGES
# ============================================================

def resize_if_large(image_path, max_dim=MAX_IMAGE_DIMENSION):
    """
    Resizes extremely large high-res camera photos to keep memory
    usage lightweight during detection and OCR.
    """
    try:
        img = cv2.imread(image_path)
        if img is None:
            return
        h, w = img.shape[:2]
        if max(h, w) > max_dim:
            scale = max_dim / float(max(h, w))
            new_w = int(w * scale)
            new_h = int(h * scale)
            resized = cv2.resize(img, (new_w, new_h), interpolation=cv2.INTER_AREA)
            cv2.imwrite(image_path, resized)
            print(f"IMAGE SIZE: Resized from {w}x{h} to {new_w}x{new_h}")
        else:
            print(f"IMAGE SIZE: {w}x{h}")
    except Exception as e:
        print("Image resize warning:", e)


# ============================================================
# UPLOAD ROUTE
# ============================================================

@upload.route("/upload", methods=["POST"])
def upload_meter():

    image_path = None

    try:
        print("")
        print("========================================")
        print("       UPLOAD START")
        print("========================================")

        # 1. CHECK FILE IN REQUEST
        if "image" not in request.files:
            print("❌ Image field missing")
            return jsonify({
                "success": False,
                "message": "No image uploaded"
            }), 400

        file = request.files["image"]

        if file.filename == "":
            print("❌ Empty filename")
            return jsonify({
                "success": False,
                "message": "No image selected"
            }), 400

        # Check content length if available
        if request.content_length and request.content_length > 8 * 1024 * 1024:
            print("❌ Image exceeds 8 MB size limit")
            return jsonify({
                "success": False,
                "message": "Image is too large. Please upload an image smaller than 8 MB."
            }), 400

        # 2. SAVE TEMPORARY FILE
        filename = secure_filename(file.filename) or "meter.jpg"
        image_path = os.path.join(UPLOAD_FOLDER, filename)
        file.save(image_path)
        print("IMAGE VALIDATION: Saved to", image_path)

        # 3. RESIZE LARGE IMAGE BEFORE PROCESSING
        resize_if_large(image_path)

        # 4. BASIC METER IMAGE CHECK
        if not is_meter_image(image_path):
            print("❌ Image check failed")
            return jsonify({
                "success": False,
                "message": "This image does not appear to be a supported electricity meter. Please upload a clear meter image."
            }), 400

        # 5. METER DETECTION START
        print("METER DETECTION START")
        crop_path = None
        found = False

        try:
            found, crop_path = detect_meter(image_path)
        finally:
            unload_model()

        if not found or not crop_path or not os.path.exists(crop_path):
            print("❌ NON-METER IMAGE: Detection failed")
            return jsonify({
                "success": False,
                "message": "This image does not appear to be a supported electricity meter. Please upload a clear meter image."
            }), 400

        print("METER DETECTED SUCCESSFULLY: Crop at", crop_path)

        # 6. OCR START
        print("OCR START")
        reading = None

        try:
            reading = read_meter(crop_path)
        except Exception as e:
            print("❌ OCR Exception:", str(e))
            reading = None
        finally:
            unload_reader()

        print("FINAL OCR READING:", reading)

        if reading is None:
            print("❌ OCR FAILED: Unable to read meter display")
            return jsonify({
                "success": False,
                "message": "Unable to read the meter display. Please upload a clearer meter image."
            }), 400

        reading_string = str(reading).strip()

        try:
            numeric_reading = float(reading_string)
        except ValueError:
            print("❌ Invalid numeric reading:", reading_string)
            return jsonify({
                "success": False,
                "message": "Unable to read the meter display. Please upload a clearer meter image."
            }), 400

        if numeric_reading <= 0:
            print("❌ Zero or negative numeric reading:", numeric_reading)
            return jsonify({
                "success": False,
                "message": "Unable to read the meter display. Please upload a clearer meter image."
            }), 400

        # 7. BILL CALCULATION
        print("BILL CALCULATION START")
        bill_amount = calculate_bill(numeric_reading)

        # 8. DATABASE & GRIDFS SAVE
        image_id = None
        try:
            with open(image_path, "rb") as img_f:
                image_id = fs.put(
                    img_f,
                    filename=filename,
                    contentType="image/jpeg"
                )
            print("DATABASE SAVE: GridFS image_id =", image_id)
        except Exception as e:
            print("GridFS save warning:", e)

        bill_doc = {
            "meter_reading": reading_string,
            "units": numeric_reading,
            "bill_amount": bill_amount,
            "image_id": str(image_id) if image_id else None,
            "image_filename": filename,
            "created_at": datetime.utcnow()
        }

        try:
            result = bills.insert_one(bill_doc)
            print("DATABASE SAVE: Bill document inserted ID =", result.inserted_id)
        except Exception as e:
            print("Database save warning:", e)

        print("========================================")
        print("       UPLOAD SUCCESS")
        print(f"Reading: {reading_string} | Units: {numeric_reading} | Bill: {bill_amount}")
        print("========================================")

        return jsonify({
            "success": True,
            "meter_reading": reading_string,
            "units": numeric_reading,
            "bill_amount": bill_amount,
            "image_id": str(image_id) if image_id else None,
            "image_filename": filename
        }), 200

    except Exception as e:
        print("========================================")
        print("          UPLOAD ERROR")
        print(str(e))
        print("========================================")
        return jsonify({
            "success": False,
            "message": "An error occurred while processing the image. Please try again."
        }), 500

    finally:
        # CLEANUP TEMPORARY FILES
        print("CLEANUP: Removing temporary files")
        if image_path and os.path.exists(image_path):
            try:
                os.remove(image_path)
            except Exception:
                pass
        gc.collect()
