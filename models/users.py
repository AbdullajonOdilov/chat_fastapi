from datetime import datetime

from db import Base
from sqlalchemy import Column, String, Integer, DateTime


class Users(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    fullname = Column(String(255), nullable=False)
    username = Column(String(15), nullable=False, unique=True)
    password_hash = Column(String(255), nullable=False)
    role = Column(String(255), default='user', nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    token = Column(String(255), default='token')