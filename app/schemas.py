from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel

class Task(BaseModel):
    name: str
    description: str
    completed: bool

class TaskOut(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None
    message: Optional[str] = None
    status: Optional[int] = None

    class Config:
        orm_mode=True

class TasksOut(BaseModel):
    list: Optional[List[TaskOut]] = None
    message: Optional[str] = None
    status: Optional[int] = None

    class Config:
        orm_mode=True
