from flask import Blueprint, request, jsonify
import os
from werkzeug.utils import secure_filename

from ai.meter_classifier import is_meter_image
from ai.meter_detection import detect_meter
from ai.ocr import read_meter
from ai.bill_calculator import calculate_bill

upload = Blueprint("upload", __name__)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@upload.route("/upload", methods=["POST"])
def upload_image():

    print("========== REQUEST RECEIVED ==========")

    if "image" not in request.files:
        print("NO IMAGE")
        return jsonify({
            "success": False,
            "message": "No image uploaded"
        })

    print("IMAGE FOUND")

    image = request.files["image"]

    filename = secure_filename(image.filename)

    filepath = os.path.join(UPLOAD_FOLDER, filename)

    image.save(filepath)

    print("IMAGE SAVED")

    print("Checking meter...")

    ok = is_meter_image(filepath)

    print("Meter Check =", ok)

    if not ok:
        return jsonify({
            "success": False,
            "message": "Not a meter"
        })

    print("Running detector...")

    found, crop = detect_meter(filepath)

    print("Detector =", found)

    if not found:
        return jsonify({
            "success": False,
            "message": "Meter not detected"
        })

    print("Running OCR...")

    reading = read_meter(crop)

    print("OCR =", reading)

    bill = calculate_bill(reading)

    print("Bill =", bill)

    return jsonify({
        "success": True,
        "meter_reading": reading,
        "bill_amount": bill
    })