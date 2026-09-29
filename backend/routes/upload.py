from flask import Blueprint, request, jsonify
import os
from werkzeug.utils import secure_filename

from ai.meter_classifier import is_meter_image
from ai.meter_detection import detect_meter, unload_model
from ai.ocr import read_meter, unload_reader
from ai.bill_calculator import calculate_bill


upload = Blueprint("upload", __name__)


# ==========================================================
# BASE DIRECTORY
# ==========================================================

# Always use the backend folder as the base directory
BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)


# ==========================================================
# UPLOAD FOLDER
# ==========================================================

UPLOAD_FOLDER = os.path.join(
    BASE_DIR,
    "uploads"
)

os.makedirs(
    UPLOAD_FOLDER,
    exist_ok=True
)


# ==========================================================
# UPLOAD ROUTE
# ==========================================================

@upload.route("/upload", methods=["POST"])
def upload_image():

    print("=" * 60)
    print("REQUEST RECEIVED")
    print("=" * 60)

    try:

        # --------------------------------------------------
        # 1. CHECK IMAGE
        # --------------------------------------------------

        if "image" not in request.files:

            print("NO IMAGE")

            return jsonify({
                "success": False,
                "message": "No image uploaded"
            }), 400

        image = request.files["image"]

        if image.filename == "":

            print("EMPTY FILENAME")

            return jsonify({
                "success": False,
                "message": "No image selected"
            }), 400

        print("IMAGE FOUND")


        # --------------------------------------------------
        # 2. SECURE FILENAME
        # --------------------------------------------------

        filename = secure_filename(
            image.filename
        )

        if not filename:

            print("INVALID FILENAME")

            return jsonify({
                "success": False,
                "message": "Invalid image filename"
            }), 400


        # --------------------------------------------------
        # 3. SAVE IMAGE
        # --------------------------------------------------

        filepath = os.path.join(
            UPLOAD_FOLDER,
            filename
        )

        image.save(filepath)

        print("IMAGE SAVED:")
        print(filepath)


        # --------------------------------------------------
        # 4. BASIC IMAGE CHECK
        # --------------------------------------------------

        print("Checking image...")

        ok = is_meter_image(
            filepath
        )

        print(
            "Image Check =",
            ok
        )


        if not ok:

            print("INVALID IMAGE")

            return jsonify({
                "success": False,
                "message": "Invalid image"
            }), 400


        # --------------------------------------------------
        # 5. YOLO METER DETECTION
        # --------------------------------------------------

        print("=" * 60)
        print("Running meter detector...")
        print("=" * 60)

        found, crop = detect_meter(
            filepath
        )

        print(
            "Detector =",
            found
        )


        # --------------------------------------------------
        # 6. NOT A METER IMAGE
        # --------------------------------------------------

        if not found:

            print("=" * 60)
            print("NO METER DETECTED")
            print("This is not a meter image")
            print("=" * 60)

            # Release YOLO memory
            unload_model()

            return jsonify({
                "success": False,
                "message": "This is not a meter image"
            }), 400


        # --------------------------------------------------
        # 7. YOLO DETECTION SUCCESS
        # --------------------------------------------------

        print("YOLO detection completed.")
        print("Meter detected successfully.")


        # Very important for memory usage
        unload_model()


        # --------------------------------------------------
        # 8. OCR
        # --------------------------------------------------

        print("=" * 60)
        print("Running OCR...")
        print("=" * 60)

        reading = read_meter(
            crop
        )

        print(
            "OCR =",
            reading
        )


        # --------------------------------------------------
        # 9. UNLOAD OCR
        # --------------------------------------------------

        unload_reader()


        # --------------------------------------------------
        # 10. CHECK OCR READING
        # --------------------------------------------------

        if not reading:

            print("=" * 60)
            print("OCR COULD NOT READ METER")
            print("=" * 60)

            return jsonify({
                "success": False,
                "message": "Unable to read meter value"
            }), 400


        # --------------------------------------------------
        # 11. CALCULATE BILL
        # --------------------------------------------------

        bill = calculate_bill(
            reading
        )

        print(
            "Bill =",
            bill
        )


        # --------------------------------------------------
        # 12. SUCCESS RESPONSE
        # --------------------------------------------------

        print("=" * 60)
        print("UPLOAD PROCESS COMPLETED")
        print("=" * 60)

        return jsonify({

            "success": True,

            "meter_reading": reading,

            "bill_amount": bill

        }), 200


    # ======================================================
    # ERROR HANDLING
    # ======================================================

    except Exception as e:

        print("=" * 60)
        print("UPLOAD ERROR")
        print("=" * 60)

        print(
            "Error:",
            e
        )


        # --------------------------------------------------
        # RELEASE YOLO MEMORY
        # --------------------------------------------------

        try:

            unload_model()

        except Exception:

            pass


        # --------------------------------------------------
        # RELEASE OCR MEMORY
        # --------------------------------------------------

        try:

            unload_reader()

        except Exception:

            pass


        # --------------------------------------------------
        # ERROR RESPONSE
        # --------------------------------------------------

        return jsonify({

            "success": False,

            "message": str(e)

        }), 500