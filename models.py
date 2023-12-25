from sqlalchemy import (
    Boolean,
    Column,
    ForeignKey,
    Index,
    Integer,
    JSON,
    String,
    UniqueConstraint,
)
from sqlalchemy import Column, Integer, String, Text, TIMESTAMP

from sqlalchemy.orm import relationship
from session import Base

class MyLogData(Base):
    __tablename__ = 'log_data'

    id = Column(Integer, primary_key=True, index=True)
    level = Column(String(length=255))
    message = Column(Text)
    resourceid = Column(String(length=255))
    timestamp = Column(TIMESTAMP)
    traceid = Column(String(length=255))
    spanid = Column(String(length=255))
    commit = Column(String(length=255))
    metadata_parentresourceid = Column(String(length=255))