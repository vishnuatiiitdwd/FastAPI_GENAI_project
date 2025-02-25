from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DB_URL = "postgresql://postgres:Dhilip04@localhost:5432/GenAI"
engine = create_engine(DB_URL)

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base = declarative_base()
def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()