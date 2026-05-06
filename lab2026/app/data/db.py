from sqlmodel import SQLModel, create_engine, Session
from typing import Annotated
from fastapi import Depends

sqlite_file_name = "C:/Users/Gabriele/Documents/GitHub/g.milia/lab2026/app/data/database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"
engine = create_engine(
    sqlite_url,
    connect_args={"check_same_thread": False},
    echo=True
)

def init_database():
    SQLModel.metadata.create_all(engine)



def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]