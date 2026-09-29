from flask import Flask
from flask_cors import CORS
import traceback

# Import Routes
from routes.auth import auth
from routes.upload import upload
from routes.bill import bill
from routes.payment import payment
from routes.history import history
from routes.profile import profile

app = Flask(__name__)

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
    return {
        "success": True,
        "message": "AI Electricity Bill Analyzer Backend Running"
    }


# Global Error Handler
@app.errorhandler(Exception)
def handle_error(e):
    print("\n" + "=" * 60)
    print("FLASK ERROR")
    print("=" * 60)
    traceback.print_exc()
    print("=" * 60 + "\n")

    return {
        "success": False,
        "message": str(e)
    }, 500


# Run Flask
if __name__ == "__main__":
    app.run(
        host="127.0.0.1",
        port=5000,
        debug=False
    )