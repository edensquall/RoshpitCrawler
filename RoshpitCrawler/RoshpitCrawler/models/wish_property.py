from sqlalchemy import Column, Integer, DateTime, ForeignKey, String
from sqlalchemy.orm import relationship

from ..models import Base


class WishProperty(Base):
    __tablename__ = 'wish_property'
    id = Column(Integer, primary_key=True, autoincrement=True)
    roll = Column(Integer)
    property_id = Column(String(90), ForeignKey('property.id'))
    wish_id = Column(Integer, ForeignKey('wish.id'))
    create_date = Column(DateTime)
    modify_date = Column(DateTime)
    property = relationship('Property', backref='wish_property')
