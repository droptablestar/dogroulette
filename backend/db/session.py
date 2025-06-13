import os

from dotenv import load_dotenv
from sqlalchemy.ext.declarative import declarative_base
from sqlmodel import SQLModel, Session, create_engine

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL, echo=True)

Base = declarative_base()

def init_db():
    print("Initializing database...")
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session
