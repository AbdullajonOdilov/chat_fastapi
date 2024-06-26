from datetime import datetime

from pydantic import BaseModel


class CreateMessage(BaseModel):
    description: str
    receiver_id: int


class UpdateMessage(BaseModel):
    id: int
    description: str

