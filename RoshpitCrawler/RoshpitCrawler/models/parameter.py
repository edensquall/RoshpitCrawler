from sqlalchemy import Column, String, DateTime

from ..models import Base


class Parameter(Base):
    __tablename__ = 'parameter'
    id = Column(String(45), primary_key=True)
    value = Column(String(45))
    create_date = Column(DateTime)
    modify_date = Column(DateTime)
