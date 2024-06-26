from datetime import datetime

from sqlalchemy.orm import relationship, backref

from db import Base
from sqlalchemy import Column, Integer, and_

from models.users import Users


class Friends(Base):
    __tablename__ = 'friends'
    id = Column(Integer, primary_key=True, autoincrement=True)
    friend_id = Column(Integer, nullable=False)
    user_id = Column(Integer, nullable=False)

    current_user = relationship('Users', foreign_keys=[user_id],
                                primaryjoin=lambda: and_(Users.id == Friends.user_id))

    user = relationship('Users', foreign_keys=[friend_id],
                             primaryjoin=lambda: and_(Users.id == Friends.friend_id), backref=backref("friends"))



