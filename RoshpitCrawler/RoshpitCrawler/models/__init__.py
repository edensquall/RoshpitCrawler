from scrapy.utils.project import get_project_settings
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

Base = declarative_base()

engine = create_engine(get_project_settings().get("SQLALCHEMY_DATABASE_URI"))

session = scoped_session(sessionmaker(autocommit=False,
                                      autoflush=False,
                                      bind=engine))