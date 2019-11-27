from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, Boolean

from ..models import Base


class Property(Base):
    __tablename__ = "property"
    id = Column(String(90), primary_key=True)
    name = Column(String(45))
    type = Column(Integer)
    is_ability = Column(Boolean)
    min = Column(Integer)
    max = Column(Integer)
    item_id = Column(String(45), ForeignKey("item.id"))
    create_date = Column(DateTime)
    modify_date = Column(DateTime)
