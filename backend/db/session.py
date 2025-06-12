from sqlmodel import SQLModel, create_engine, Session

DATABASE_URL = "sqlite:///./pets.db"  # or use PostgreSQL URL

engine = create_engine(DATABASE_URL, echo=True)


def init_db():
    print("Initializing database...")
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session
