from datetime import date

from fastapi import FastAPI
from fastapi import Depends
from fastapi import HTTPException

from fastapi.middleware.cors import CORSMiddleware

from sqlalchemy.orm import Session

from database import SessionLocal
from database import engine

from models import Base
from models import Event

from schemas import EventCreate
from schemas import EventResponse


Base.metadata.create_all(
    bind=engine
)

app = FastAPI(
    title="Google Calendar Clone API"
)

# CORS

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Database Session

def get_db():

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()


# Home

@app.get("/")
def home():

    return {
        "message": "Calendar API Running"
    }


# Create Event

@app.post(
    "/events",
    response_model=EventResponse
)
def create_event(
    event: EventCreate,
    db: Session = Depends(get_db)
):

    new_event = Event(
        title=event.title,
        description=event.description,
        start_time=event.start_time,
        end_time=event.end_time
    )

    db.add(new_event)

    db.commit()

    db.refresh(new_event)

    return new_event


# Get All Events

@app.get(
    "/events",
    response_model=list[EventResponse]
)
def get_events(
    db: Session = Depends(get_db)
):

    return db.query(Event).all()


# Get Single Event

@app.get(
    "/events/{event_id}",
    response_model=EventResponse
)
def get_event(
    event_id: int,
    db: Session = Depends(get_db)
):

    event = (
        db.query(Event)
        .filter(
            Event.id == event_id
        )
        .first()
    )

    if not event:

        raise HTTPException(
            status_code=404,
            detail="Event not found"
        )

    return event


# Update Event

@app.put(
    "/events/{event_id}",
    response_model=EventResponse
)
def update_event(
    event_id: int,
    event_data: EventCreate,
    db: Session = Depends(get_db)
):

    event = (
        db.query(Event)
        .filter(
            Event.id == event_id
        )
        .first()
    )

    if not event:

        raise HTTPException(
            status_code=404,
            detail="Event not found"
        )

    event.title = event_data.title
    event.description = event_data.description
    event.start_time = event_data.start_time
    event.end_time = event_data.end_time

    db.commit()

    db.refresh(event)

    return event


# Delete Event

@app.delete(
    "/events/{event_id}"
)
def delete_event(
    event_id: int,
    db: Session = Depends(get_db)
):

    event = (
        db.query(Event)
        .filter(
            Event.id == event_id
        )
        .first()
    )

    if not event:

        raise HTTPException(
            status_code=404,
            detail="Event not found"
        )

    db.delete(event)

    db.commit()

    return {
        "message": "Event deleted successfully"
    }


# Events By Date

@app.get(
    "/events/date/{event_date}"
)
def get_events_by_date(
    event_date: date,
    db: Session = Depends(get_db)
):

    events = db.query(
        Event
    ).all()

    result = []

    for event in events:

        if (
            event.start_time.date()
            == event_date
        ):
            result.append(event)

    return result


# Monthly Calendar

@app.get(
    "/calendar/{year}/{month}"
)
def monthly_events(
    year: int,
    month: int,
    db: Session = Depends(get_db)
):

    events = db.query(
        Event
    ).all()

    result = []

    for event in events:

        if (
            event.start_time.year == year
            and
            event.start_time.month == month
        ):
            result.append(event)

    return result