from flask import Flask, jsonify, abort, Response
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
@app.route("/all/<int:limit>")
@cross_origin()
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


@app.route("/id/<int:id>")
@cross_origin()
def get_single_data_point_by_id(id):
    db = get_db_conn()
    data = get_sensor_data_by_id(db, id)
    data_dict = []
    if data is not None:
        data_dict.append(
            {
                "created_at": data.created_at,
                "co2": data.co2,
                "humidity": data.humidity,
                "temperature": data.temperature,
                "dust": data.dust,
            }
        )
    else:
        data_dict = 404
    return jsonify(data_dict)


@app.route("/data-for-time/<start>/<end>")
@cross_origin()
def get_data_for_time(start, end):
    db = get_db_conn()
    data = get_sensor_data_for_timeframe(db, start, end)
    data_dict = []
    if data is not None:
        data_dict.append(
            {
                "created_at": data.created_at,
                "co2": data.co2,
                "humidity": data.humidity,
                "temperature": data.temperature,
                "dust": data.dust,
            }
        )
    else:
        data_dict = 404
    return jsonify(data_dict)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5555, debug=True)
