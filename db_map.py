from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class MediaIds(Base):
    __tablename__ = 'userid'
    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    userid = Column(String(255))