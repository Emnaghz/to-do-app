from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.database import get_db
from sqlalchemy.exc import SQLAlchemyError
from app import schemas
from .. import models

router = APIRouter(
    prefix="/tasks",
    tags=['tasks']
)

@router.get("/",  response_model = schemas.TasksOut)
def get_tasks(db: Session = Depends(get_db)):
    tasks = db.query(models.Task)
    return schemas.TasksOut(
        list = [schemas.TaskOut(**task.__dict__) for task in tasks],
        message = "all tasks",
        status = status.HTTP_200_OK
    )

@router.get("/{id}",  response_model = schemas.TaskOut)
def get_task_with_id(id: int, db: Session = Depends(get_db)):
    task= db.query(models.Task).filter(models.Task.id == id).first()
    if not task:
        return schemas.TaskOut(
            status=status.HTTP_404_NOT_FOUND,
            message = f"Task with id {id} not found"
        )
    return schemas.TaskOut(**task.__dict__,
        status=status.HTTP_200_OK)

@router.post("/", status_code = status.HTTP_201_CREATED, response_model = schemas.TaskOut)
def add_task(task:schemas.Task , db: Session = Depends(get_db)):
    try:
        new_task = models.Task(**task.dict())
        db.add(new_task)
        db.commit()
        db.refresh(new_task)
    except SQLAlchemyError as e:
        db.rollback()
        return schemas.TaskOut(
            status = status.HTTP_500_INTERNAL_SERVER_ERROR,
            message = "There is a problem, try again"
        )

    return schemas.TaskOut(**new_task.__dict__,
        status = status.HTTP_201_CREATED,
        message = "Task added"
    )

@router.put("/{id}",  status_code = status.HTTP_200_OK, response_model = schemas.TaskOut)
def update_task(id: int, task: schemas.Task, db: Session = Depends(get_db)):
    task_query = db.query(models.Task).filter(models.Task.id == id)
    task_in_db = task_query.first()
    if not task_in_db:
        return schemas.TaskOut(
            status=status.HTTP_404_NOT_FOUND,
            message = f"Task with id {id} not found"
        )

    try:
        task_query.update(task.dict())
        db.commit()
    except SQLAlchemyError as e:
        db.rollback()
        return schemas.TaskOut(
            status = status.HTTP_500_INTERNAL_SERVER_ERROR,
            message = "There is a problem, try again"
        )

    return schemas.TaskOut(**task.__dict__,
        status=status.HTTP_200_OK,
        message = f"Task with id {id} was updated succefully ")

@router.delete("/{id}",  status_code=status.HTTP_200_OK)
def delete_task(id: int, db: Session = Depends(get_db)):
    task_query = db.query(models.Task).filter(models.Task.id == id)
    task = task_query.first()
    if not task:
        return schemas.TaskOut(status=status.HTTP_404_NOT_FOUND,
            message= f"Task with id {id} not found")

    try:
        task_query.delete()
        db.commit()
    except SQLAlchemyError as e:
        db.rollback()
        return schemas.TaskOut(status=status.HTTP_400_BAD_REQUEST,
            message="Something went wrong")

    return schemas.TaskOut(**task.__dict__,
        status=status.HTTP_200_OK,
        message="Task deleted successfully")
