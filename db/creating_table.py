from db.session import engine
from db.model import Base
import logging


logging.info("Creating tables in the database...")
Base.metadata.create_all(bind=engine)
logging.info("Tables created successfully")