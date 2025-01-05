from pydantic import BaseModel
from typing import List


class BotConfig(BaseModel):
    """Bot configuration model"""
    api_id: int
    api_hash: str
    phone_number: str
    source_channels: List[str]
    target_channel: str
    add_fee: int
    gemini_api_key: str
    is_active: bool
    interval_minutes: int


class ConfigResponse(BotConfig):
    """Configuration response model inherits from BotConfig"""
    pass


class MessageResponse(BaseModel):
    """Message processing response"""
    status: str
    message: str
