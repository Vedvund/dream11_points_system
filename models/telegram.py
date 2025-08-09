from typing import Optional, List, BinaryIO, Union

from pydantic import BaseModel
from sqlmodel import Field

from core.config import settings


class PhotoSize(BaseModel):
    file_id: str
    file_unique_id: str
    file_size: int
    width: int
    height: int


class Message(BaseModel):
    message_id: int
    text: Optional[str] = None
    photo: Optional[List[PhotoSize]] = None


class UpdateResult(BaseModel):
    update_id: int
    message: Optional[Message] = None

class FileResult(BaseModel):
    file_id: str
    file_unique_id: str
    file_size: int
    file_path: str


class GetUpdatesResponse(BaseModel):
    ok: bool
    result: Union[List[UpdateResult], FileResult]


class SendMessage(BaseModel):
    chat_id: int = Field(default=settings.TELEGRAM_DEFAULT_OWNER_ID)
    text: str


class SendFile(BaseModel):
    chat_id: int = Field(default=settings.TELEGRAM_DEFAULT_OWNER_ID)
    file: BinaryIO

    model_config = {
        "arbitrary_types_allowed": True
    }
