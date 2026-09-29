from pymongo import MongoClient
from pymongo.errors import PyMongoError
from config import Config


# ============================================================
# MongoDB Atlas Connection
# ============================================================

try:
    client = MongoClient(
        Config.MONGO_URI,
        serverSelectionTimeoutMS=10000,
        connectTimeoutMS=10000,
        socketTimeoutMS=10000,
        maxPoolSize=20,
        tls=True
    )

    # Test connection
    client.admin.command("ping")

    print("✅ Connected to MongoDB Atlas Successfully!")

except PyMongoError as e:
    print("❌ MongoDB Atlas Connection Failed")
    print("Error:", e)
    raise


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