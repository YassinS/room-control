import datetime

from peewee import (
    MySQLDatabase,
    Model,
    IntegerField,
    DateTimeField,
    AutoField,
    FloatField,
)


db = MySQLDatabase(
    "sensor_data", user="admin", password="admin", host="localhost", port=3306
)


class SensorData(Model):
    id = AutoField()
    created_at = DateTimeField(default=datetime.datetime.now)
    co2 = IntegerField()
    temperature = IntegerField()
    humidity = IntegerField()
    pressure = IntegerField()
    dust = FloatField()

    class Meta:
        database = db


db.connect()
db.create_tables([SensorData])
