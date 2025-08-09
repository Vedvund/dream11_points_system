from typing import Optional, List, BinaryIO

from pydantic import BaseModel
from sqlmodel import Field

from core.config import settings


class Message(BaseModel):
    message_id: int
    text: Optional[str] = None


class UpdateResult(BaseModel):
    update_id: int
    message: Optional[Message] = None


class GetUpdatesResponse(BaseModel):
    ok: bool
    result: List[UpdateResult]


class SendMessage(BaseModel):
    chat_id: int = Field(default=settings.TELEGRAM_DEFAULT_OWNER_ID)
    text: str


class SendFile(BaseModel):
    chat_id: int = Field(default=settings.TELEGRAM_DEFAULT_OWNER_ID)
    file: BinaryIO

    model_config = {
        "arbitrary_types_allowed": True
    }
