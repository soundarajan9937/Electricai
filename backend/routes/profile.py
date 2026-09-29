from flask import Blueprint, request, jsonify
from database import users

profile = Blueprint("profile", __name__)

@profile.route("/profile", methods=["GET"])
def profile_page():
    return jsonify({
        "message": "Profile route working"
    })

@profile.route("/update_profile", methods=["POST"])
def update_profile():
    data = request.json
    email = data.get("email")

    if not email:
        return jsonify({"message": "Email is required to update profile"}), 400

    # Update user details based on email
    update_fields = {
        "name": data.get("name"),
        "phone": data.get("phone"),
        "meter": data.get("meter"),
        "address": data.get("address")
    }

    if data.get("password"):
        update_fields["password"] = data.get("password")

    result = users.update_one(
        {"email": email},
        {"$set": update_fields}
    )

    return jsonify({"success": True, "message": "Profile updated in database successfully"})
