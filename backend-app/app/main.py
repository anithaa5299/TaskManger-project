from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from .db import Base, engine, get_db
from .models import Task, User
from .schemas import TaskCreate,UserCreate,UserLogin
from .auth import hash_password, verify_password, create_access_token, get_current_user, oauth2_scheme

app = FastAPI()

# create tables
Base.metadata.create_all(bind=engine)

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

    return {"message": "deleted"}

@app.get("/debug")
def debug(token: str = Depends(oauth2_scheme)):
    return {"token": token}