from pydantic import BaseModel, Field
from typing import Annotated
from sqlmodel import SQLModel, Field



class BookBase(SQLModel):
    title: str
    author: str
    review: Annotated[int, Field(ge=1, le=5)] = None


class BookCreate(BookBase):
    pass


class BookPublic(BookBase):
    id: int


class BookDB(BookBase, table=True):
    id: int = Field(default=None, primary_key=True)



books = {
    0: Book(id=0, title="Il nome della Rosa", author="Umberto Eco", review=5),
    1: Book(id=1, title="Il gioco dei sei", author="Umberto Eco", review=3),
    2: Book(id=2, title="Il gioco dei sette", author="Maccio Capatonda", review=4)
}








