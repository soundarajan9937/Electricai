import os
import urllib.parse
from dotenv import load_dotenv

# Base Project Folder
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# Load environment variables from .env file
load_dotenv(os.path.join(BASE_DIR, ".env"))


def sanitize_mongo_uri(uri: str) -> str:
    """
    Sanitizes MongoDB URI by escaping special characters in username/password
    such as '@' according to RFC 3986 (e.g., '@' -> '%40').
    """
    if not uri or "://" not in uri:
        return uri

    scheme, rest = uri.split("://", 1)
    if "@" not in rest:
        return uri

    path_sep_idx = len(rest)
    for char in ("/", "?", "#"):
        idx = rest.find(char)
        if idx != -1 and idx < path_sep_idx:
            path_sep_idx = idx

    userinfo_and_host = rest[:path_sep_idx]
    path_and_query = rest[path_sep_idx:]

    if "@" not in userinfo_and_host:
        return uri

    last_at_idx = userinfo_and_host.rfind("@")
    userinfo = userinfo_and_host[:last_at_idx]
    host = userinfo_and_host[last_at_idx + 1:]

    if ":" in userinfo:
        username, password = userinfo.split(":", 1)
        safe_username = urllib.parse.quote_plus(urllib.parse.unquote(username))
        safe_password = urllib.parse.quote_plus(urllib.parse.unquote(password))
        safe_userinfo = f"{safe_username}:{safe_password}"
    else:
        safe_userinfo = urllib.parse.quote_plus(urllib.parse.unquote(userinfo))

    return f"{scheme}://{safe_userinfo}@{host}{path_and_query}"


class Config:

    # Flask
    SECRET_KEY = os.getenv("SECRET_KEY", "electric_ai_project")

    DEBUG = os.getenv("DEBUG", "False").lower() in ("true", "1", "t")

    # MongoDB Atlas
    MONGO_URI = sanitize_mongo_uri(
        os.getenv(
            "MONGO_URI",
            "mongodb+srv://<username>:<password>@cluster0.mongodb.net/electric_ai?retryWrites=true&w=majority"
        )
    )
    DATABASE_NAME = os.getenv("DATABASE_NAME", "electric_ai")

    # Upload Folder
    UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")

    # Maximum Upload Size (8 MB)
    MAX_CONTENT_LENGTH = 8 * 1024 * 1024

    # Allowed Image Extensions
    ALLOWED_EXTENSIONS = {
        "png",
        "jpg",
        "jpeg"
    }

    # OCR Language
    OCR_LANGUAGE = ["en"]

    # Electricity Bill Rate
    UNIT_RATE = 2

    # Crop Image Name
    CROPPED_IMAGE = os.path.join(
        BASE_DIR,
        "ai",
        "cropped_meter.jpg"
    )