from datetime import datetime

from sqlalchemy.orm import relationship, backref

from db import Base
from sqlalchemy import Column, String, Integer, DateTime, Text, Boolean, and_

from models.users import Users


class Messages(Base):
    __tablename__ = 'messages'
    id = Column(Integer, primary_key=True, autoincrement=True)
    description = Column(Text, nullable=True)
    sender_id = Column(String(255))
    receiver_id = Column(String(255))
    time = Column(DateTime, default=datetime.utcnow, autoincrement=True)
    seen = Column(Boolean, default=False)

    sender_user = relationship('Users', foreign_keys=[sender_id],
                        primaryjoin=lambda: and_(Users.id == Messages.sender_id), backref=backref("sender_messages"))
    receiver_user = relationship('Users',  foreign_keys=[receiver_id],
                        primaryjoin=lambda: and_(Users.id == Messages.receiver_id), backref=backref("receiver_messages"))




