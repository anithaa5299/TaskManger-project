import time
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
import os

print("🔥 WORKER STARTED", flush=True)

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://postgres:postgres@db:5432/taskdb"
)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

while True:
    try:
        db = SessionLocal()

        result = db.execute(text("SELECT COUNT(*) FROM tasks"))
        count = result.scalar()

        print(f"[WORKER] Total tasks: {count}", flush=True)

        db.close()

    except Exception as e:
        print("[WORKER ERROR]", e, flush=True)

    time.sleep(5)