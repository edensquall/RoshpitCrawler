from sqlalchemy import Column, String, DateTime

from ..models import Base


class ItemType(Base):
    __tablename__ = "item_type"
    id = Column(String(30), primary_key=True)
    name = Column(String(30))
    create_date = Column(DateTime)
    modify_date = Column(DateTime)
