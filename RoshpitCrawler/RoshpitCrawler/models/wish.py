from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from ..models import Base


class Wish(Base):
    __tablename__ = 'wish'
    id = Column(Integer, primary_key=True, autoincrement=True)
    currency = Column(Integer)
    min_level = Column(Integer)
    max_bid = Column(Integer)
    max_buyout = Column(Integer)
    user_id = Column(Integer, ForeignKey('user.id'))
    item_id = Column(String(45), ForeignKey('item.id'))
    create_date = Column(DateTime)
    modify_date = Column(DateTime)
    item = relationship('Item', backref='wish')
    wish_properties = relationship('WishProperty', backref='wish')
