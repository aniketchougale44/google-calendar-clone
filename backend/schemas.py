from datetime import datetime

from pydantic import BaseModel
from pydantic import field_validator


class EventCreate(BaseModel):

    title: str
    description: str | None = None
    start_time: datetime
    end_time: datetime

    @field_validator("end_time")
    @classmethod
    def validate_end_time(
        cls,
        end_time,
        info
    ):

        start_time = info.data.get(
            "start_time"
        )

        if (
            start_time
            and end_time <= start_time
        ):
            raise ValueError(
                "end_time must be greater than start_time"
            )

        return end_time


class EventResponse(BaseModel):

    id: int
    title: str
    description: str | None
    start_time: datetime
    end_time: datetime
    created_at: datetime

    model_config = {
        "from_attributes": True
    }