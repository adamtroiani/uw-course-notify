import datetime as dt
from sqlalchemy.orm import Mapped, mapped_column
from .base import Base


class Subscriber(Base):
  __tablename__ = "subscriber"
  
  course: Mapped[str] = mapped_column(primary_key=True, nullable=False)
  term: Mapped[int] = mapped_column(primary_key=True, nullable=False)
  token: Mapped[str] = mapped_column(primary_key=True, nullable=False)
  
  created_at: Mapped[dt.datetime] = mapped_column(
    nullable=False, default=dt.datetime.utcnow
  )
  last_notified: Mapped[dt.datetime] = mapped_column(
    nullable=True, default=None
  )
