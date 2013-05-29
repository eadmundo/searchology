from sqlalchemy import (Column, Integer, String)
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class SiteSearch(Base):
    __tablename__ = 'site_search'
    id = Column(Integer, primary_key=True)
    domain = Column(String, nullable=False)
