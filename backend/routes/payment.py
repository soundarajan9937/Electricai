from flask import Blueprint, jsonify

payment = Blueprint("payment", __name__)

@payment.route("/payment", methods=["GET"])
def payment_page():
    return jsonify({
        "message": "Payment route working"
    })