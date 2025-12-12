from flask import Flask, jsonify, request, Response
from flask_pymongo import PyMongo
from bson import json_util
from config import Config

app = Flask(__name__)

app.config['MONGO_URI'] = "mongodb://{}:{}@{}/IOT?authSource=admin".format(Config.DB_USERNAME,Config.DB_PASSWORD,Config.DB_SERVER_NAME)

mongo = PyMongo(app)

@app.route("/api/submit/device", methods=["POST"])

def create_device():
    device = request.get_json()
    _id = mongo.db.devices.insert_one(device)
    return jsonify({
        "message": "Received",
        "_id": str(_id.inserted_id)
    })

@app.route("/api/devices", methods=["GET"])

def get_devices():
    devices =  mongo.db.devices.find()
    resp = json_util.dumps(devices)
    return Response(resp, mimetype="application/json")

@app.route("/api/device/<ip>", methods=["GET"])

def get_one_device(ip):
    device = mongo.db.devices.find_one({"ip":ip})
    resp = json_util.dumps(device)
    return Response(resp, mimetype="application/json")


@app.route("/api/delete/device/<ip>", methods=["DELETE"])

def delete_device(ip):
    mongo.db.devices.delete_one({"ip":ip})
    return jsonify({"message": "Deleted Successfully"})


@app.route("/api/submit/report", methods=["POST"])

def create_report():
    report = request.get_json()
    _id = mongo.db.reports.insert_one(report)
    return jsonify({
        "message": "Received",
        "_id": str(_id.inserted_id)
    })

@app.route("/api/reports", methods=["GET"])

def get_all_reports():
    reports = mongo.db.reports.find()
    resp = json_util.dumps(reports)
    return Response(resp, mimetype="application/json")

@app.errorhandler(404)
def not_found(error=None):
    message = {
        'message': 'Resource Not Found ' + request.url,
        'status': 404
    }
    response = jsonify(message)
    response.status_code = 404
    return response


if __name__ == "__main__":
    app.run(debug=True, port=5000)
