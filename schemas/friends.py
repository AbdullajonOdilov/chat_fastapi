from pydantic import BaseModel


class CreateFriend(BaseModel):
    friend_id: int


class UpdateFriend(BaseModel):
    id: int
    friend_id: int

