from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base

DATABASE_URL = "postgresql://lox_main:loxlox@localhost:5432/lox_database"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

# Create tables
Base.metadata.create_all(bind=engine)


