from flask import Blueprint, jsonify

bill = Blueprint("bill", __name__)

@bill.route("/bill", methods=["GET"])
def get_bill():
    return jsonify({
        "message": "Bill route working"
    })