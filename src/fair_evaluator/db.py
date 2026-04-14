import os
from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()

TEST_MODE = os.environ.get("TESTING", "false").lower() == "true"

if TEST_MODE:
    SQLITE_DB_PATH = "sqlite:///./data/fairs_test.db"
else:
    SQLITE_DB_PATH = "sqlite:///./data/fairs.db"

Path("./data").mkdir(parents=True, exist_ok=True)

engine = create_engine(SQLITE_DB_PATH, echo=False, future=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
