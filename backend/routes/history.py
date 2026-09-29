from flask import Blueprint, jsonify

history = Blueprint("history", __name__)

@history.route("/history", methods=["GET"])
def history_page():
    return jsonify({
        "message": "History route working"
    })