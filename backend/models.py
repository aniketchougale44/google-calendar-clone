from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import DateTime

from datetime import datetime

from database import Base


class Event(Base):

    __tablename__ = "events"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    title = Column(
        String,
        nullable=False
    )

    description = Column(
        String,
        nullable=True
    )

    start_time = Column(
        DateTime,
        nullable=False
    )

    end_time = Column(
        DateTime,
        nullable=False
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )