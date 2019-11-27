from sqlalchemy import Column, String, Integer, DateTime, ForeignKey

from ..models import Base


class Notify(Base):
    __tablename__ = 'notify'
    id = Column(String(45), primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    create_date = Column(DateTime)
    modify_date = Column(DateTime)
