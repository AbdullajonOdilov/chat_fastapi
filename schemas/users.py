
from pydantic import BaseModel


class CreateUser(BaseModel):
    fullname: str
    username: str
    role: str
    password_hash: str


class UpdateUser(BaseModel):
    id: int
    fullname: str
    username: str
    role: str
    password_hash: str


class UserCurrent(BaseModel):
    id: int
    fullname: str
    username: str
    role: str
    password_hash: str


