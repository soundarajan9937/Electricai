import certifi
from pymongo import MongoClient
from pymongo.errors import PyMongoError
from config import Config


# ============================================================
# MongoDB Atlas Connection
# ============================================================

mongo_kwargs = {
    "serverSelectionTimeoutMS": 10000,
    "connectTimeoutMS": 10000,
    "socketTimeoutMS": 10000,
    "maxPoolSize": 20,
    "tls": True,
    "tlsAllowInvalidCertificates": True
}

try:
    mongo_kwargs["tlsCAFile"] = certifi.where()
except Exception:
    pass

try:
    client = MongoClient(Config.MONGO_URI, **mongo_kwargs)

    # Test connection
    client.admin.command("ping")
    print("✅ Connected to MongoDB Atlas Successfully!")

except Exception as e:
    print("⚠️ MongoDB Atlas Initial Ping Failed (will retry on demand):")
    print("Error:", e)


# ============================================================
# Database
# ============================================================

db = client[Config.DATABASE_NAME]


# ============================================================
# Collections
# ============================================================

users = db["users"]
bills = db["bills"]
payments = db["payments"]
history = db["history"]
profiles = db["profiles"]


# ============================================================
# Connection Check
# ============================================================

def check_database_connection():
    try:
        client.admin.command("ping")
        return True

    except Exception as e:
        print("❌ MongoDB connection check failed:")
        print(e)
        return False