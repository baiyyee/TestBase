from ..const import DATABASE_URL
from sqlmodel import SQLModel, Session, create_engine, select


engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})


async def get_session():
    with Session(engine) as session:
        yield session
