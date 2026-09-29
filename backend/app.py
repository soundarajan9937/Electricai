import os
import traceback
from flask import Flask, send_from_directory, jsonify
from flask_cors import CORS

# Path setup for frontend static files
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
FRONTEND_DIR = os.path.abspath(os.path.join(BASE_DIR, "..", "frontend"))

# Import Routes
from routes.auth import auth
from routes.upload import upload
from routes.bill import bill
from routes.payment import payment
from routes.history import history
from routes.profile import profile

app = Flask(__name__, static_folder=FRONTEND_DIR, static_url_path="")

# Enable CORS
CORS(app)

# Register Blueprints
app.register_blueprint(auth)
app.register_blueprint(upload)
app.register_blueprint(bill)
app.register_blueprint(payment)
app.register_blueprint(history)
app.register_blueprint(profile)


@app.route("/")
def home():
    if os.path.exists(os.path.join(FRONTEND_DIR, "index.html")):
        return send_from_directory(FRONTEND_DIR, "index.html")
    return jsonify({
        "success": True,
        "message": "AI Electricity Bill Analyzer Backend Running"
    })


@app.route("/<path:path>")
def serve_static(path):
    if os.path.exists(os.path.join(FRONTEND_DIR, path)):
        return send_from_directory(FRONTEND_DIR, path)
    return jsonify({
        "success": False,
        "message": "Page or resource not found"
    }), 404


# Global Error Handler
@app.errorhandler(Exception)
def handle_error(e):
    print("\n" + "=" * 60)
    print("FLASK ERROR")
    print("=" * 60)
    traceback.print_exc()
    print("=" * 60 + "\n")

    return jsonify({
        "success": False,
        "message": str(e)
    }), 500


# Run Flask
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(
        host="0.0.0.0",
        port=port,
        debug=False
    )