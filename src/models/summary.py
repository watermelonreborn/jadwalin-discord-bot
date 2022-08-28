import datetime

from pydantic import BaseModel
from typing import List

class Availability(BaseModel):
    start_hour: int
    end_hour: int

class Summary(BaseModel):
    date: datetime.date
    availability: List[Availability]