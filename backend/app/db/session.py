import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from app.core.config import settings

print("SESSION.PY LOADED FROM =", os.path.abspath(__file__), flush=True)
print("DB URL =", settings.DATABASE_URL, flush=True)

engine = create_engine(settings.DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
