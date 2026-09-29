import certifi
from pymongo import MongoClient
from config import Config


# ============================================================
# MongoDB Atlas Connection
# ============================================================

client_kwargs = {
    "serverSelectionTimeoutMS": 5000,
    "connectTimeoutMS": 10000,
    "socketTimeoutMS": 10000,
    "tls": True,
    "tlsCAFile": certifi.where()
}


try:
    # Create MongoDB Atlas client
    client = MongoClient(
        Config.MONGO_URI,
        **client_kwargs
    )

    # Test connection
    client.admin.command("ping")

    print("✅ Connected to MongoDB Atlas Successfully!")

except Exception as e:
    print("❌ MongoDB Atlas Connection Failed")
    print("Please check the following:")
    print("1. MONGO_URI in backend/.env")
    print("2. MongoDB Atlas username and password")
    print("3. MongoDB Atlas Network Access / IP whitelist")
    print("4. MongoDB Atlas cluster status")
    print()
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
# Optional helper function
# ============================================================

def check_database_connection():
    """
    Check whether MongoDB Atlas is reachable.
    """
    try:
        client.admin.command("ping")
        return True

    except Exception as e:
        print("❌ Database connection check failed:")
        print(e)
        return False