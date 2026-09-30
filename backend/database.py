import certifi
import gridfs

from pymongo import MongoClient
from config import Config


# ============================================================
# MongoDB Atlas Connection Settings
# ============================================================

mongo_kwargs = {
    "serverSelectionTimeoutMS": 10000,
    "connectTimeoutMS": 10000,
    "socketTimeoutMS": 10000,
    "maxPoolSize": 20,

    # TLS / SSL
    "tls": True,

    # Keep this only if your current Atlas connection
    # requires it.
    "tlsAllowInvalidCertificates": True
}


# ============================================================
# Certificate
# ============================================================

try:

    mongo_kwargs["tlsCAFile"] = certifi.where()

except Exception as e:

    print("⚠️ Could not load certifi certificate:")
    print(e)


# ============================================================
# MongoDB Client
# ============================================================

try:

    client = MongoClient(
        Config.MONGO_URI,
        **mongo_kwargs
    )

    # Test MongoDB connection
    client.admin.command("ping")

    print("✅ Connected to MongoDB Atlas Successfully!")

except Exception as e:

    print("⚠️ MongoDB Atlas Initial Ping Failed")
    print("MongoDB will retry when required.")
    print("Error:", e)


# ============================================================
# Database
# ============================================================

db = client[Config.DATABASE_NAME]


# ============================================================
# MongoDB GridFS
# ============================================================
# GridFS is used to store uploaded meter images
# inside MongoDB Atlas.
#
# Actual image data:
#     fs.chunks
#
# Image information:
#     fs.files
# ============================================================

fs = gridfs.GridFS(db)

print("✅ MongoDB GridFS initialized successfully!")


# ============================================================
# Collections
# ============================================================

users = db["users"]

bills = db["bills"]

payments = db["payments"]

history = db["history"]

profiles = db["profiles"]


# ============================================================
# Database Connection Check
# ============================================================

def check_database_connection():

    try:

        client.admin.command("ping")

        return True

    except Exception as e:

        print("❌ MongoDB connection check failed:")
        print(e)

        return False