from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .config import settings


# Create engine
engine = create_engine(settings.DATABASE_URL, echo=False)

# Create session factory
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

# Dependency (for FastAPI or manual use)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
