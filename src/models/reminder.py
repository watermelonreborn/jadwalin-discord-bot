import datetime

from pydantic import BaseModel
from typing import List

class EventTime(BaseModel):
    date_time: datetime.datetime

class Event(BaseModel):
    summary: str
    start_time: EventTime
    end_time: EventTime

class Reminder(BaseModel):
    discord_id: str
    server_id: str
    hours: int
    events: List[Event]
