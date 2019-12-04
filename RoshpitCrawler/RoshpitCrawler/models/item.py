from sqlalchemy import Column, String, DateTime
from sqlalchemy.orm import relationship

from ..models import Base


class Item(Base):
    __tablename__ = "item"
    id = Column(String(45), primary_key=True)
    name = Column(String(45))
    img = Column(String(45))
    type = Column(String(30))
    rarity = Column(String(30))
    create_date = Column(DateTime)
    modify_date = Column(DateTime)
    properties = relationship("Property", backref="item")
