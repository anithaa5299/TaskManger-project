from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from .db import Base, engine, get_db
from .models import *
from .schemas import *
from .auth import hash_password, verify_password, create_access_token

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
def login(user: UserLogin, db: Session = Depends(get_db)):

    db_user = db.query(User).filter(User.email == user.email).first()

    if not db_user or not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({"user_id": db_user.id})

    return {
        "access_token": token,
        "token_type": "bearer"
    }