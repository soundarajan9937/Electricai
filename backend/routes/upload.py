from flask import Blueprint, request, jsonify
import os
from datetime import datetime
from werkzeug.utils import secure_filename

from ai.meter_classifier import is_meter_image
from ai.meter_detection import detect_meter, unload_model
from ai.ocr import read_meter, unload_reader
from ai.bill_calculator import calculate_bill

from database import fs, bills


upload = Blueprint("upload", __name__)


# ==========================================================
# BASE DIRECTORY
# ==========================================================

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)


# ==========================================================
# TEMPORARY UPLOAD FOLDER
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

    filepath = None

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
        # 3. SAVE TEMPORARILY
        # --------------------------------------------------

        filepath = os.path.join(
            UPLOAD_FOLDER,
            filename
        )

        image.save(filepath)

        print("TEMPORARY IMAGE SAVED:")
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

            unload_model()

            return jsonify({
                "success": False,
                "message": "This is not a meter image"
            }), 400


        # --------------------------------------------------
        # 7. YOLO SUCCESS
        # --------------------------------------------------

        print("YOLO detection completed.")
        print("Meter detected successfully.")

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


        # ==================================================
        # 12. STORE IMAGE IN MONGODB ATLAS GRIDFS
        # ==================================================

        print("=" * 60)
        print("STORING IMAGE IN MONGODB ATLAS...")
        print("=" * 60)

        with open(filepath, "rb") as image_file:

            image_data = image_file.read()

        image_id = fs.put(
            image_data,
            filename=filename,
            content_type=image.content_type or "image/jpeg",
            metadata={
                "type": "electricity_meter",
                "meter_reading": reading,
                "bill_amount": bill,
                "created_at": datetime.utcnow()
            }
        )

        print("IMAGE STORED IN MONGODB!")
        print("MongoDB Image ID:", image_id)


        # ==================================================
        # 13. SAVE BILL INFORMATION
        # ==================================================

        bill_document = {

            "meter_reading": reading,

            "bill_amount": bill,

            "image_id": image_id,

            "image_filename": filename,

            "created_at": datetime.utcnow()

        }

        bill_result = bills.insert_one(
            bill_document
        )

        print(
            "Bill saved to MongoDB:",
            bill_result.inserted_id
        )


        # ==================================================
        # 14. DELETE TEMPORARY LOCAL IMAGE
        # ==================================================

        try:

            if filepath and os.path.exists(filepath):

                os.remove(filepath)

                print(
                    "Temporary image deleted:"
                )

                print(filepath)

        except Exception as delete_error:

            print(
                "Could not delete temporary image:",
                delete_error
            )


        # ==================================================
        # 15. SUCCESS RESPONSE
        # ==================================================

        print("=" * 60)
        print("UPLOAD PROCESS COMPLETED")
        print("IMAGE STORED IN MONGODB ATLAS")
        print("=" * 60)

        return jsonify({

            "success": True,

            "meter_reading": reading,

            "bill_amount": bill,

            "image_id": str(image_id),

            "image_filename": filename

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