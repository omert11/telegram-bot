from typing import List
from pydantic import BaseModel, Field
from .db import get_config as get_db_config


class BotConfig(BaseModel):
    """Bot configuration model"""

    admin_password: str = Field(description="Admin password")
    api_id: int = Field(description="Telegram API ID")
    api_hash: str = Field(description="Telegram API Hash")
    phone_number: str = Field(description="Phone number for Telegram client")
    source_channels: List[str] = Field(description="List of source channels to monitor")
    target_channel: str = Field(description="Target channel for forwarding messages")
    add_fee: int = Field(description="Fee to add to prices")
    gemini_api_key: str = Field(description="Gemini API key for price parsing")
    is_active: bool = Field(description="Bot active status", default=True)
    interval_minutes: int = Field(description="Run interval in minutes", default=60)

    class Config:
        """Pydantic model configuration"""

        validate_assignment = True
        frozen = True


_config_instance: BotConfig | None = None


def get_config(force: bool = False) -> BotConfig:
    """
    Get bot configuration

    Args:
        force: Force reload configuration from database
    """
    global _config_instance

    if _config_instance is None or force:
        db_config = get_db_config()
        _config_instance = BotConfig(
            admin_password=db_config.admin_password,
            api_id=db_config.api_id,
            api_hash=db_config.api_hash,
            phone_number=db_config.phone_number,
            source_channels=db_config.source_channels,
            target_channel=db_config.target_channel,
            add_fee=db_config.add_fee,
            gemini_api_key=db_config.gemini_api_key,
            is_active=db_config.is_active,
            interval_minutes=db_config.interval_minutes,
        )

    return _config_instance
