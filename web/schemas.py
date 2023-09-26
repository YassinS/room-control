from datetime import datetime
from pydantic import BaseModel


class SensorDataBase(BaseModel):
    created_at: datetime
    co2: int
    temperature: int
    humidity: int
    pressure: int
    dust: int


class SensorData(SensorDataBase):
    id: int

    class Config:
        from_attributes = True
