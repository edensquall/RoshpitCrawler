from sqlalchemy import Column, String, Integer, DateTime, Boolean
from sqlalchemy.orm import relationship

from ..models import Base


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, autoincrement=True)
    account = Column(String(45))
    password = Column(String(45))
    name = Column(String(45))
    email = Column(String(45))
    type = Column(String(2))
    is_notification = Column(Boolean, default=True)
    notification_method = Column(Integer)
    create_date = Column(DateTime)
    modify_date = Column(DateTime)
    wishes = relationship('Wish', backref='user')
    notify = relationship('Notify', backref='user')
