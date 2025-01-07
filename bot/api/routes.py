from fastapi import APIRouter, HTTPException, Depends
from typing import List
import json
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import secrets
from pydantic import BaseModel

from ..db import get_run_history, get_db
from .models import ConfigResponse, MessageResponse, BotConfig
from ..logger import logger
from ..config import get_config
from ..utils import get_status_message
from ..client import is_bot_logged, send_login_code, login_bot_with_code

router = APIRouter()


security = HTTPBasic()


def verify_password(credentials: HTTPBasicCredentials = Depends(security)) -> bool:
    """Verify password for authentication"""
    config = get_config(force=True)
    is_correct = secrets.compare_digest(
        credentials.password.encode("utf8"), config.admin_password.encode("utf8")
    )

    if not is_correct:
        raise HTTPException(
            status_code=401,
            detail="Incorrect password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return True


@router.get("/config", response_model=ConfigResponse)
async def get_configuration() -> ConfigResponse:
    """Get current configuration"""
    try:
        config = get_config(force=True)
        return ConfigResponse(**config.__dict__)
    except Exception as e:
        logger.error(f"Error getting configuration: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/config/bulk", response_model=MessageResponse)
async def bulk_update_configuration(config_updates: BotConfig) -> MessageResponse:
    """Update multiple configuration values at once"""
    try:
        config_dict = config_updates.model_dump(mode="json")

        with get_db() as conn:
            for key, value in config_dict.items():
                conn.execute(
                    """
                    INSERT OR REPLACE INTO config (key, value, updated_at)
                    VALUES (?, ?, CURRENT_TIMESTAMP)
                    """,
                    (key, json.dumps(value)),
                )
            conn.commit()

        get_config(force=True)

        return MessageResponse(
            status="success", message="Tüm ayarlar başarıyla güncellendi"
        )
    except Exception as e:
        logger.error(f"Error updating configurations: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/status", response_model=MessageResponse)
async def get_status() -> MessageResponse:
    """Get bot status"""
    try:
        config = get_config(force=True)
        status_message = get_status_message(config)

        return MessageResponse(
            status="active" if config.is_active else "inactive",
            message=status_message,
        )
    except Exception as e:
        logger.error(f"Error getting status: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/history", response_model=List[dict])
async def get_history() -> List[dict]:
    """Get run history"""
    try:
        history = get_run_history()
        return history
    except Exception as e:
        logger.error(f"Error getting history: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/reset", response_model=MessageResponse)
async def reset_database() -> MessageResponse:
    """Reset database (except config)"""
    try:
        from ..db import reset_db_except_config

        reset_db_except_config()
        return MessageResponse(
            status="success", message="Veritabanı başarıyla sıfırlandı (ayarlar hariç)"
        )
    except Exception as e:
        logger.error(f"Error resetting database: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/auth", response_model=MessageResponse)
async def authenticate(
    credentials: HTTPBasicCredentials = Depends(security),
) -> MessageResponse:
    """Authenticate user"""
    if verify_password(credentials):
        return MessageResponse(status="success", message="Authentication successful")
    else:
        raise HTTPException(status_code=401, detail="Unauthorized")


@router.get("/bot-status", response_model=MessageResponse)
async def get_bot_login_status() -> MessageResponse:
    """Get bot login status"""
    try:
        is_logged = await is_bot_logged()
        return MessageResponse(
            status="logged_in" if is_logged else "not_logged",
            message="Bot giriş yapmış" if is_logged else "Bot giriş yapmamış",
        )
    except Exception as e:
        logger.error(f"Error getting bot status: {e}")
        raise HTTPException(status_code=500, detail=str(e))


class PhoneCodeRequest(BaseModel):
    code: str


@router.get("/login", response_model=MessageResponse)
async def request_login_code() -> MessageResponse:
    """Request login code to be sent to phone"""
    try:
        await send_login_code()
        return MessageResponse(status="pending", message="Telefonunuza kod gönderildi")
    except Exception as e:
        logger.error(f"Error requesting login code: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/login", response_model=MessageResponse)
async def login_bot(request: PhoneCodeRequest) -> MessageResponse:
    """Login bot with phone code"""
    try:
        await login_bot_with_code(request.code)
        return MessageResponse(status="success", message="Bot başarıyla giriş yaptı")
    except Exception as e:
        logger.error(f"Error logging in bot: {e}")
        raise HTTPException(status_code=500, detail=str(e))
