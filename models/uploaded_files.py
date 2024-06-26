from sqlalchemy import *
from sqlalchemy.orm import relationship, backref

from db import Base
from models.users import Users


class Uploaded_files(Base):
    __tablename__ = "uploaded_files"
    id = Column(Integer, autoincrement=True, primary_key=True)
    file = Column(String(255))
    source = Column(String(255))
    source_id = Column(Integer)
    comment = Column(String(255))

    user = relationship('Users', foreign_keys=[source_id],
                             primaryjoin=lambda: and_(Users.id == Uploaded_files.source_id,
                                                      Uploaded_files.source == "user"), backref=backref("user_files"))