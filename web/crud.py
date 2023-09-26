from datetime import datetime, timedelta

from sqlalchemy.orm import Session
from sqlalchemy import desc

from models import SensorData


def get_sensor_data_by_id(db: Session, sensor_data_id: int):
    return db.query(SensorData).filter(SensorData.id == sensor_data_id).first()


def get_sensor_data_for_timeframe(
    db: Session, timestamp_start: datetime, timestamp_end: datetime
):
    timestamp_start = datetime.strptime(timestamp_start, "%d-%m-%y")
    timestamp_end = datetime.strptime(timestamp_end, "%d/%m/%y")
    return db.query(SensorData).filter(
        SensorData.created_at.between(timestamp_start, timestamp_end)
    )


def get_all_sensor_data(db: Session, skip: int = 0, limit: int = 100):
    return (
        db.query(SensorData)
        .order_by(desc(SensorData.created_at))
        .offset(skip)
        .limit(limit)
        .all()
    )


# if __name__ == "__main__":
#     db = SessionLocal()
#     res = get_all_sensor_data(db)

#     n = "12-09-2023"
#     y = n - timedelta(days=1)
#     res = get_sensor_data_for_timeframe(db, y, n)
#     for i in res:
#         print(i.created_at)
