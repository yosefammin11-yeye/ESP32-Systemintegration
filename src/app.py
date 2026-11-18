import os
from datetime import datetime
from flask import Flask, jsonify, request
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

API_KEY = os.getenv("API_KEY", "hemlig-api-nyckel-123")

latest_sensor_data = {}
monitoring_stats = {
    "message_count": 0,
    "validation_errors": 0,
    "last_received_timestamp": None,
}

def verify_api_key():
    auth_header = request.headers.get("X-API-Key")
    return auth_header == API_KEY

@app.route("/api/data", methods=["POST"])
def receive_data():
    global latest_sensor_data, monitoring_stats

    if not verify_api_key():
        monitoring_stats["validation_errors"] += 1
        return jsonify({"error": "Unauthorized: Invalid or missing API Key"}), 401

    data = request.get_json()
    if not data:
        monitoring_stats["validation_errors"] += 1
        return jsonify({"error": "Invalid JSON format"}), 400

    required_fields = ["sensorId", "timestamp", "value", "unit"]
    for field in required_fields:
        if field not in data:
            monitoring_stats["validation_errors"] += 1
            return jsonify({"error": f"Missing required field: {field}"}), 400

    if not isinstance(data["sensorId"], str) or not isinstance(data["unit"], str):
        monitoring_stats["validation_errors"] += 1
        return jsonify({"error": "Invalid data type for sensorId or unit"}), 400

    if not isinstance(data["value"], (int, float)):
        monitoring_stats["validation_errors"] += 1
        return jsonify({"error": "Sensor value must be a number"}), 400

    if data["unit"] == "C" and not (-50 <= data["value"] <= 100):
        monitoring_stats["validation_errors"] += 1
        return jsonify({"error": "Sensor value out of reasonable range"}), 400

    latest_sensor_data = data
    monitoring_stats["message_count"] += 1
    monitoring_stats["last_received_timestamp"] = datetime.now().isoformat()

    print(f"[LOG] Mottagen giltig data från {data['sensorId']}: {data['value']} {data['unit']}")
    return jsonify({"status": "success", "message": "Data saved successfully"}), 200

@app.route("/api/sensor/latest", methods=["GET"])
def get_latest_data():
    if not latest_sensor_data:
        return jsonify({"error": "No data available yet"}), 404
    return jsonify({
        "latest_reading": latest_sensor_data,
        "monitoring": monitoring_stats
    }), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
