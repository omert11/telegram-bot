import os
import json
from typing import List
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


def get_list_from_env(key: str, default: List | None = None) -> List:
    """Get list from environment variable"""
    value = os.getenv(key)
    if not value:
        return default or []
    try:
        return json.loads(value)
    except json.JSONDecodeError:
        return value.split(",")


def get_bool_from_env(key: str, default: bool = False) -> bool:
    """Get boolean from environment variable"""
    value = os.getenv(key, str(default)).lower()
    return value in ("true", "1", "yes", "on")


def get_int_from_env(key: str, default: int = 0) -> int:
    """Get integer from environment variable"""
    try:
        return int(os.getenv(key, default))
    except (TypeError, ValueError):
        return default


# Default configuration from environment variables
DEFAULT_CONFIG = {
    "admin_password": os.getenv("ADMIN_PASSWORD", ""),
    "api_id": get_int_from_env("API_ID", 0),
    "api_hash": os.getenv("API_HASH", ""),
    "phone_number": os.getenv("PHONE_NUMBER", ""),
    "source_channels": get_list_from_env("SOURCE_CHANNELS", []),
    "target_channel": os.getenv("TARGET_CHANNEL", ""),
    "add_fee": get_int_from_env("ADD_FEE", 0),
    "gemini_api_key": os.getenv("GEMINI_API_KEY", ""),
    "is_active": get_bool_from_env("IS_ACTIVE", False),
    "interval_minutes": get_int_from_env("INTERVAL_MINUTES", 60),
}
