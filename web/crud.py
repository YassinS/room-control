from datetime import datetime, timedelta

from sqlalchemy.orm import Session
from sqlalchemy import desc

from models import SensorData


def get_sensor_data_by_id(db: Session, sensor_data_id: int):
    result = db.query(SensorData).filter(SensorData.id == sensor_data_id).first()
    db.close()
    return result


def get_sensor_data_for_timeframe(db: Session, start: int, end: int, limit: int):
    start = int(start)
    end = int(end)
    limit = int(limit)
    timestamp_start = datetime.fromtimestamp(start)
    timestamp_end = datetime.fromtimestamp(end)
    result = (
        db.query(SensorData)
        .filter(SensorData.created_at.between(timestamp_start, timestamp_end))
        .order_by(desc(SensorData.created_at))
        .limit(limit)
        .all()
    )
    db.close()
    return result


def get_all_sensor_data(db: Session, skip: int = 0, limit: int = 100):
    result = (
        db.query(SensorData)
        .order_by(desc(SensorData.created_at))
        .offset(skip)
        .limit(limit)
        .all()
    )
    db.close()
    return result


# if __name__ == "__main__":
#     db = SessionLocal()
#     res = get_all_sensor_data(db)

#     n = "12-09-2023"
#     y = n - timedelta(days=1)
#     res = get_sensor_data_for_timeframe(db, y, n)
#     for i in res:
#         print(i.created_at)
