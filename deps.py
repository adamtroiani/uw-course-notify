from typing import Generator
from sqlalchemy.orm import Session
from database import engine

def get_db() -> Generator[Session, None, None]:
    with Session(engine) as db:
      yield db
