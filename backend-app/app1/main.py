from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
import pika
from fastapi.middleware.cors import CORSMiddleware
import json
from sqlalchemy.orm import Session
from .db import Base, engine, get_db
from .models import Task, User
from .schemas import TaskCreate,UserCreate,UserLogin
from .auth import hash_password, verify_password, create_access_token, get_current_user, oauth2_scheme

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    # allow_origins=["http://localhost:5173"],  # frontend URL
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# create tables
Base.metadata.create_all(bind=engine)



def publish_task_event(task_id, title):
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host="rabbitmq")
    )
    channel = connection.channel()

    channel.queue_declare(queue="tasks")

    message = json.dumps({
        "task_id": task_id,
        "title": title
    })

    channel.basic_publish(exchange="", routing_key="tasks", body=message)

    connection.close()

@app.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):
    db_user = User(
        email=user.email,
        hashed_password=hash_password(user.password)
    )
    print("PASSWORD:", user.password)
    print("TYPE:", type(user.password))
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return {"message": "user created"}

@app.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == form_data.username).first()

    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({"user_id": user.id})

    return {
        "access_token": token,
        "token_type": "bearer"
    }

@app.post("/tasks")
def create_task(
    task: TaskCreate,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user)
):
    db_task = Task(
        title=task.title,
        description=task.description,
        owner_id=user_id
    )

    db.add(db_task)
    db.commit()
    db.refresh(db_task)

    publish_task_event(db_task.id, db_task.title)

    return db_task

@app.get("/tasks")
def get_tasks(
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user)
):
    tasks = db.query(Task).filter(Task.owner_id == user_id).all()
    return tasks

@app.put("/tasks/{task_id}")
def update_task(
    task_id: int,
    updated_task: TaskCreate,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user)
):
    task = db.query(Task).filter(
        Task.id == task_id,
        Task.owner_id == user_id
    ).first()

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    task.title = updated_task.title
    task.description = updated_task.description

    db.commit()
    db.refresh(task)
    publish_task_event(task.id, task.title)

    return task

@app.delete("/tasks/{task_id}")
def delete_task(
    task_id: int,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user)
):
    task = db.query(Task).filter(
        Task.id == task_id,
        Task.owner_id == user_id
    ).first()

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    db.delete(task)
    db.commit()
    publish_task_event(task.id, "deleted")
    return {"message": "deleted"}

@app.get("/debug")
def debug(token: str = Depends(oauth2_scheme)):
    return {"token": token}

from fastapi import Request

@app.get("/debug-auth")
def debug_auth(request: Request):
    return dict(request.headers)