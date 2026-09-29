from pymongo import MongoClient
from config import Config

# MongoDB Atlas Connection
client = MongoClient(
    Config.MONGO_URI,
    serverSelectionTimeoutMS=5000
)

# Database
db = client[Config.DATABASE_NAME]

# Collections
users = db["users"]
bills = db["bills"]
payments = db["payments"]
history = db["history"]
profiles = db["profiles"]

# Check MongoDB Connection
try:
    client.admin.command("ping")
    print("✅ Connected to MongoDB Atlas Successfully!")
except Exception as e:
    print("❌ MongoDB Atlas Connection Failed")
    print("Please check your MONGO_URI in backend/.env file and ensure your IP address is whitelisted in MongoDB Atlas.")
    print("Error:", e)