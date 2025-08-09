from sqlalchemy import create_engine
from models import Base

DB_URL = "sqlite:///./app.db"
engine = create_engine(DB_URL, echo=True)

def init_db():
  Base.metadata.create_all(engine)
