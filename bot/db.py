import datetime
import sqlite3
from typing import Any, Generator, List
from contextlib import contextmanager
import json
from dataclasses import dataclass
from .logger import logger
import os
from .settings import DEFAULT_CONFIG

# Database path
DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "bot.db")


@dataclass
class Config:
    """Configuration data class"""

    admin_password: str
    api_id: int
    api_hash: str
    phone_number: str
    source_channels: List[str]
    target_channel: str
    add_fee: int
    gemini_api_key: str
    is_active: bool = True
    interval_minutes: int = 60


@contextmanager
def get_db() -> Generator[sqlite3.Connection, None, None]:
    """Database connection context manager"""
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()


def init_db() -> None:
    """Initialize database with tables"""
    logger.info(f"Initializing database at {DB_PATH}")
    with get_db() as conn:
        # Config table
        conn.execute("""
        CREATE TABLE IF NOT EXISTS config (
            key TEXT PRIMARY KEY,
            value TEXT NOT NULL,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)

        # Last message table
        conn.execute("""
        CREATE TABLE IF NOT EXISTS last_messages (
            channel_id TEXT PRIMARY KEY,
            last_message_id INTEGER NOT NULL,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)

        # Run history table with type column
        conn.execute("""
        CREATE TABLE IF NOT EXISTS run_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            status TEXT NOT NULL,
            type TEXT NOT NULL,
            message TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)

        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS phone_code_hash (
                id INTEGER PRIMARY KEY,
                hash_value TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        )

        conn.commit()
    logger.info("Database tables created successfully")


def get_db_now() -> datetime.datetime:
    """Get current time from database"""
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT CURRENT_TIMESTAMP")
        row = cursor.fetchone()
        return datetime.datetime.strptime(row["CURRENT_TIMESTAMP"], "%Y-%m-%d %H:%M:%S")


def try_parse_config(value: str) -> Any:
    try:
        return json.loads(value)
    except json.JSONDecodeError:
        return value


def get_config() -> Config:
    """Get configuration from database"""
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT key, value FROM config")
        rows = cursor.fetchall()

        config_dict = {row["key"]: try_parse_config(row["value"]) for row in rows}

        # Use default values if not found in database
        return Config(
            admin_password=config_dict.get("admin_password", ""),
            api_id=config_dict.get("api_id", 0),
            api_hash=config_dict.get("api_hash", ""),
            phone_number=str(config_dict.get("phone_number", "")),
            source_channels=config_dict.get("source_channels", []),
            target_channel=config_dict.get("target_channel", ""),
            add_fee=config_dict.get("add_fee", 0),
            gemini_api_key=config_dict.get("gemini_api_key", ""),
            is_active=config_dict.get("is_active", True),
            interval_minutes=config_dict.get("interval_minutes", 60),
        )


def update_config(key: str, value: Any) -> None:
    """Update configuration in database"""
    with get_db() as conn:
        conn.execute(
            """
            INSERT OR REPLACE INTO config (key, value, updated_at)
            VALUES (?, ?, CURRENT_TIMESTAMP)
            """,
            (key, json.dumps(value) if isinstance(value, list) else value),
        )
        conn.commit()
        logger.info(f"Updated config: {key}")


def is_config_empty() -> bool:
    """Check if config table is empty"""
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) as count FROM config")
        row = cursor.fetchone()
        return row["count"] == 0


def init_default_config() -> None:
    """Initialize default configuration in database if empty"""
    if not is_config_empty():
        logger.info("Config table already has data, skipping default initialization")
        return

    logger.info("Initializing default configuration")
    for key, value in DEFAULT_CONFIG.items():
        update_config(key, value)

    logger.info("Default configuration initialized successfully")


def get_last_message_id(channel: str) -> int:
    """Get last processed message ID for channel"""
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT last_message_id FROM last_messages WHERE channel_id = ?", (channel,)
        )
        row = cursor.fetchone()
        return row["last_message_id"] if row else -1


def update_last_message_id(channel: str, message_id: int) -> None:
    """Update last processed message ID for channel"""
    with get_db() as conn:
        conn.execute(
            """
            INSERT OR REPLACE INTO last_messages (channel_id, last_message_id, updated_at)
            VALUES (?, ?, CURRENT_TIMESTAMP)
            """,  # noqa: E501
            (channel, message_id),
        )
        conn.commit()
        logger.info(f"Updated last message ID for channel {channel}: {message_id}")


def add_run_history(status: str, message: str, type: str = "info") -> None:
    """Add new run history entry"""
    with get_db() as conn:
        conn.execute(
            """
            INSERT INTO run_history (status, type, message)
            VALUES (?, ?, ?)
            """,
            (status, type, message),
        )
        conn.commit()
        logger.info("Added new run history entry")


def get_run_history(limit: int = 10) -> list[dict]:
    """Get recent run history"""
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT status, message, created_at
            FROM run_history
            ORDER BY created_at DESC
            LIMIT ?
            """,
            (limit,),
        )
        rows = cursor.fetchall()
        return [dict(row) for row in rows]


def get_last_run_by_type(type: str) -> dict | None:
    """Get last run by type"""
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT status, type, message, created_at
            FROM run_history
            WHERE type = ?
            ORDER BY created_at DESC
            LIMIT 1
            """,
            (type,),
        )
        row = cursor.fetchone()
        return dict(row) if row else None


def reset_db_except_config() -> None:
    """Reset all tables except config"""
    with get_db() as conn:
        all_tables = conn.execute("SELECT name FROM sqlite_master WHERE type='table'")

        for table in all_tables:
            if table["name"] != "config":
                conn.execute(f"DELETE FROM {table['name']}")

        conn.commit()

        logger.info("Database reset completed (except config table)")


def save_phone_code_hash(hash_value: str) -> None:
    """Save phone code hash to database"""
    with get_db() as conn:
        conn.execute(
            """
            INSERT INTO phone_code_hash (hash_value)
            VALUES (?)
            """,
            (hash_value,),
        )
        conn.commit()
        logger.info("Phone code hash saved")


def get_phone_code_hash() -> str | None:
    """Get latest phone code hash from database"""
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT hash_value
            FROM phone_code_hash
            ORDER BY created_at DESC
            LIMIT 1
            """
        )
        row = cursor.fetchone()
        return row["hash_value"] if row else None


def clear_phone_code_hash() -> None:
    """Clear all phone code hashes from database"""
    with get_db() as conn:
        conn.execute("DELETE FROM phone_code_hash")
        conn.commit()
        logger.info("Phone code hashes cleared")
