from flask import Blueprint, request, jsonify
from database import users

auth = Blueprint("auth", __name__)


# Register
@auth.route("/register", methods=["POST"])
def register():
    data = request.json or {}

    email = data.get("email")
    if not email:
        return jsonify({"message": "Email is required"}), 400

    if users.find_one({"email": email}):
        return jsonify({"message": "Email already registered, you can login"}), 400

    new_user = {
        "name": data.get("name", ""),
        "email": email,
        "phone": data.get("phone", ""),
        "meter": data.get("meter", ""),
        "address": data.get("address", ""),
        "password": data.get("password", "")
    }

    result = users.insert_one(new_user)
    print(f"✅ User registered successfully in MongoDB Atlas: {email} (Document ID: {result.inserted_id})")

    return jsonify({"message": "Registration Successful", "user_id": str(result.inserted_id)})


# Login
@auth.route("/login", methods=["POST"])
def login():
    data = request.json or {}

    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"message": "Email and Password are required"}), 400

    user_by_email = users.find_one({"email": email})
    if not user_by_email:
        return jsonify({"message": "Email not found, register first"}), 404

    if user_by_email.get("password") != password:
        return jsonify({"message": "Invalid Email or Password"}), 401

    print(f"✅ User logged in successfully: {email}")

    return jsonify({
        "message": "Login Successful",
        "name": user_by_email.get("name", ""),
        "email": user_by_email.get("email", ""),
        "phone": user_by_email.get("phone", ""),
        "meter": user_by_email.get("meter", ""),
        "address": user_by_email.get("address", ""),
        "password": user_by_email.get("password", "")
    })