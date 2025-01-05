import os
from telethon import TelegramClient
from telethon.sessions import StringSession
from telethon.errors import SessionPasswordNeededError, PhoneCodeExpiredError
from .config import get_config
from .logger import logger
from fastapi import HTTPException
from .db import save_phone_code_hash, get_phone_code_hash, clear_phone_code_hash

_client_instance: TelegramClient | None = None
SESSION_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), "bot.session")


def _read_session() -> str | None:
    """Read session string from file"""
    if not os.path.exists(SESSION_FILE) or os.path.getsize(SESSION_FILE) == 0:
        return None

    with open(SESSION_FILE, "r") as f:
        return f.read() or None


def _save_session(session_str: str) -> None:
    """Save session string to file"""
    with open(SESSION_FILE, "w") as f:
        f.write(session_str)


def _create_client(session: str | None = None) -> TelegramClient:
    """Create new Telegram client instance"""
    config = get_config()
    return TelegramClient(
        StringSession(session) if session else StringSession(),
        config.api_id,
        config.api_hash,
    )


async def _handle_sign_in(client: TelegramClient, phone_code: str) -> None:
    """Handle sign in process"""
    phone_code_hash = get_phone_code_hash()
    if not phone_code_hash:
        raise HTTPException(status_code=400, detail="Please request code first")

    try:
        config = get_config()
        await client.sign_in(
            phone=config.phone_number,
            code=phone_code,
            phone_code_hash=phone_code_hash,
        )
    except PhoneCodeExpiredError:
        clear_phone_code_hash()
        raise HTTPException(
            status_code=400, detail="Code expired, please request new code"
        )
    except SessionPasswordNeededError:
        raise HTTPException(
            status_code=400, detail="Two-factor authentication is enabled"
        )
    except Exception as e:
        logger.error(f"Error during sign in: {e}")
        raise HTTPException(status_code=500, detail=str(e))


async def _request_code(client: TelegramClient) -> None:
    """Request verification code"""
    config = get_config()
    result = await client.send_code_request(config.phone_number, force_sms=True)
    save_phone_code_hash(result.phone_code_hash)
    logger.info(f"Please check your Telegram app on {config.phone_number}")


def is_bot_logged() -> bool:
    """Check if bot is logged in by looking for session file"""
    try:
        session_str = _read_session()
        if not session_str:
            return False

        client = _create_client(session_str)
        try:
            client.connect()
            return client.is_user_authorized()
        except Exception as e:
            logger.error(f"Error checking session: {e}")
            return False

    except Exception as e:
        logger.error(f"Error checking bot login status: {e}")
        return False


async def send_login_code() -> None:
    """Send login code to bot"""
    global _client_instance

    if not _client_instance:
        _client_instance = _create_client()
        await _client_instance.connect()

    if not is_bot_logged():
        await _request_code(_client_instance)


async def login_bot_with_code(phone_code: str) -> None:
    """Login bot with phone code"""
    global _client_instance

    if not _client_instance:
        raise Exception("Please send code first")

    await _handle_sign_in(_client_instance, phone_code)
    session_str = StringSession.save(_client_instance.session)
    _save_session(session_str or "")
    clear_phone_code_hash()
    await _client_instance.disconnect()
    _client_instance = None


async def get_client() -> TelegramClient:
    """Get Telegram client instance"""

    if not is_bot_logged():
        raise Exception("Please login first")

    client = _create_client()
    await client.connect()
    return client
