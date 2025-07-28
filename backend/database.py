from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base
from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL')
if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable is required")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

# Create tables
Base.metadata.create_all(bind=engine)


