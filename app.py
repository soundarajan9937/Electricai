from flask import Flask, send_from_directory
from flask_cors import CORS
import traceback
import os

from routes.auth import auth
from routes.upload import upload
from routes.bill import bill
from routes.payment import payment
from routes.history import history
from routes.profile import profile


# ==========================================================
# CREATE FLASK APP
# ==========================================================

app = Flask(__name__)


# ==========================================================
# CORS CONFIGURATION
# ==========================================================

CORS(
    app,
    resources={
        r"/*": {
            "origins": "*"
        }
    },
    methods=[
        "GET",
        "POST",
        "PUT",
        "DELETE",
        "OPTIONS"
    ],
    allow_headers=[
        "Content-Type",
        "Authorization"
    ]
)


# ==========================================================
# BASE DIRECTORY
# ==========================================================

BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
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
# REGISTER BLUEPRINTS
# ==========================================================

app.register_blueprint(auth)

app.register_blueprint(upload)

app.register_blueprint(bill)

app.register_blueprint(payment)

app.register_blueprint(history)

app.register_blueprint(profile)


# ==========================================================
# HOME
# ==========================================================

@app.route("/", methods=["GET"])
def home():

    return {
        "success": True,
        "message": "AI Electricity Bill Analyzer Backend Running"
    }


# ==========================================================
# UPLOADED FILE
# ==========================================================

@app.route(
    "/uploads/<filename>",
    methods=["GET"]
)
def uploaded_file(filename):

    return send_from_directory(
        UPLOAD_FOLDER,
        filename
    )


# ==========================================================
# HEALTH CHECK
# ==========================================================

@app.route(
    "/health",
    methods=["GET"]
)
def health():

    return {
        "success": True,
        "message": "Backend is healthy"
    }


# ==========================================================
# CORS OPTIONS TEST
# ==========================================================

@app.route(
    "/cors-test",
    methods=["GET", "OPTIONS"]
)
def cors_test():

    return {
        "success": True,
        "message": "CORS is working"
    }


# ==========================================================
# ERROR HANDLER
# ==========================================================

@app.errorhandler(Exception)
def handle_error(e):

    print("\n" + "=" * 70)
    print("❌ FLASK ERROR")
    print("=" * 70)

    traceback.print_exc()

    print("=" * 70 + "\n")

    return {
        "success": False,
        "message": str(e)
    }, 500


# ==========================================================
# START SERVER
# ==========================================================

if __name__ == "__main__":

    print("\n" + "=" * 70)
    print("        ⚡ ELECTRIC AI BACKEND")
    print("=" * 70)

    print(
        "Upload folder:",
        UPLOAD_FOLDER
    )

    print(
        "Server:",
        "http://127.0.0.1:5000"
    )

    print("=" * 70 + "\n")

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=False
    )