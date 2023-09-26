from flask import Flask, jsonify, abort, Response

from crud import get_all_sensor_data
from db import SessionLocal

app = Flask(__name__)


def get_db_conn():
    try:
        db = SessionLocal()
    except Exception:
        abort(500)
    return db


@app.route("/all")
@app.route("/all/<int:limit>")
def all_data(limit=50):
    db = get_db_conn()
    data = get_all_sensor_data(db, limit=limit)
    data_dict = []
    for i in data:
        data_dict.append(
            {
                "created_at": i.created_at,
                "co2": i.co2,
                "humidity": i.humidity,
                "temperature": i.temperature,
                "dust": i.dust,
            }
        )
    return jsonify(data_dict)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80, debug=True)
