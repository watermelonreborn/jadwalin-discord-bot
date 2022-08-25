from pydantic import BaseModel
from typing import List

class Event(BaseModel):
    summary: str

class Reminder(BaseModel):
    discord_id: str
    server_id: str
    hours: int
    events: List[Event]
