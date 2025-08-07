from sqlalchemy import create_engine
from models import Base

DB_URL = "sqlite:///./app.db" # dev; change to postgresql://… in prod
engine = create_engine(DB_URL, echo=True)

def init_db():
  Base.metadata.create_all(engine)
