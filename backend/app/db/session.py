from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings
from app.db.base import Base

# PostgreSQL engine (no check_same_thread needed!)
engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,  # Check connection health
    echo=True  # Log SQL queries (useful for debugging)
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    from app.db import models
    Base.metadata.create_all(bind=engine)
    print(' PostgreSQL database initialized successfully!')
