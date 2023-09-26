from sqlalchemy import Column, Integer, DateTime, Float

from db import Base


class SensorData(Base):
    __tablename__ = "sensordata"

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime)
    co2 = Column(Integer)
    temperature = Column(Integer)
    humidity = Column(Integer)
    pressure = Column(Integer)
    dust = Column(Float)
