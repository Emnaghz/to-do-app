import datetime
from sqlalchemy import Integer, String, Column, DateTime, Boolean
from ...database import Base

class Task(Base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key = True, nullable = False) 
    name = Column(String, nullable = False)
    description = Column(String, nullable = True)
    completed = Column(Boolean, nullable = False, default=False)
