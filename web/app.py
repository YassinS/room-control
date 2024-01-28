import time
from flask import Flask, jsonify, abort, request
from flask_cors import CORS, cross_origin

from crud import (
    get_all_sensor_data,
    get_sensor_data_by_id,
    get_sensor_data_for_timeframe,
)
from db import SessionLocal

app = Flask(__name__)
cors = CORS(app)
app.config["CORS_HEADERS"] = "Content-Type"


def get_db_conn():
    try:
        db = SessionLocal()
    except Exception:
        abort(500)
    return db


@app.route("/all")
@cross_origin()
def all_data():
    limit = request.args.get("limit")
    start = request.args.get("start")
    end = request.args.get("end")
    print(start, end, limit)
    db = get_db_conn()
    if limit and start and end:
        data = get_sensor_data_for_timeframe(db, start, end, limit)
    elif limit is None and start and end:
        data = get_sensor_data_for_timeframe(db, start, end, 50)
    elif limit and start is None and end is None:
        data = get_all_sensor_data(db, limit=limit)
    else:
        data = get_all_sensor_data(db, limit=50)
    data_dict = []
    for i in data:
        data_dict.append(
            {
                "id": i.id,
                "created_at": i.created_at,
                "co2": i.co2,
                "humidity": i.humidity,
                "pressure": i.pressure,
                "temperature": i.temperature,
                "dust": i.dust,
            }
        )
    return jsonify(data_dict)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5555, debug=True)
