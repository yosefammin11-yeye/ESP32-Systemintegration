import json
import os
from datetime import datetime
from dotenv import load_dotenv
from flask import Flask, jsonify, request
import paho.mqtt.client as mqtt

load_dotenv()

app = Flask(__name__)

API_KEY = os.getenv("API_KEY", "hemlig-api-nyckel-123")

MQTT_BROKER = os.getenv("MQTT_BROKER", "broker.hivemq.com")
MQTT_PORT = int(os.getenv("MQTT_PORT", "1883"))
MQTT_TOPIC = os.getenv("MQTT_TOPIC", "sodertalje/fastighet/sensor/temp")
MQTT_USERNAME = os.getenv("MQTT_USERNAME")
MQTT_PASSWORD = os.getenv("MQTT_PASSWORD")

latest_sensor_data = {}
monitoring_stats = {
    "message_count": 0,
    "validation_errors": 0,
    "last_received_timestamp": None,
}


def verify_api_key():
    auth_header = request.headers.get("X-API-Key")
    return auth_header == API_KEY


def process_sensor_payload(data):
    global latest_sensor_data, monitoring_stats

    if not isinstance(data, dict):
        monitoring_stats["validation_errors"] += 1
        return False, "Invalid JSON format", 400

    required_fields = ["sensorId", "timestamp", "value", "unit"]
    for field in required_fields:
        if field not in data:
            monitoring_stats["validation_errors"] += 1
            return False, f"Missing required field: {field}", 400

    if not isinstance(data["sensorId"], str) or not isinstance(data["unit"], str):
        monitoring_stats["validation_errors"] += 1
        return False, "Invalid data type for sensorId or unit", 400

    if not isinstance(data["value"], (int, float)) or isinstance(data["value"], bool):
        monitoring_stats["validation_errors"] += 1
        return False, "Sensor value must be a number", 400

    if data["unit"] == "C" and not (-50 <= data["value"] <= 100):
        monitoring_stats["validation_errors"] += 1
        return False, "Sensor value out of reasonable range", 400

    latest_sensor_data = data
    monitoring_stats["message_count"] += 1
    monitoring_stats["last_received_timestamp"] = datetime.now().isoformat()

    print(f"[LOG] Mottagen giltig data från {data['sensorId']}: {data['value']} {data['unit']}")
    return True, "Data saved successfully", 200


def on_mqtt_connect(client, userdata, flags, reason_code, properties=None):
    print(f"[MQTT] Ansluten till broker ({MQTT_BROKER}:{MQTT_PORT}) med kod: {reason_code}")
    client.subscribe(MQTT_TOPIC)
    print(f"[MQTT] Prenumererar på topic: {MQTT_TOPIC}")


def on_mqtt_message(client, userdata, msg):
    global monitoring_stats
    try:
        raw_payload = msg.payload.decode("utf-8")
        data = json.loads(raw_payload)
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        monitoring_stats["validation_errors"] += 1
        print(f"[MQTT-ERROR] Ogiltigt payload-format på {msg.topic}: {exc}")
        return

    ok, message, _ = process_sensor_payload(data)
    if not ok:
        print(f"[MQTT-ERROR] Validering misslyckades för meddelande på {msg.topic}: {message}")


def start_mqtt_client():
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    if MQTT_USERNAME and MQTT_PASSWORD:
        client.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)
    client.on_connect = on_mqtt_connect
    client.on_message = on_mqtt_message
    client.connect(MQTT_BROKER, MQTT_PORT, keepalive=60)
    client.loop_start()
    return client


@app.route("/api/data", methods=["POST"])
def receive_data():
    global monitoring_stats

    if not verify_api_key():
        monitoring_stats["validation_errors"] += 1
        return jsonify({"error": "Unauthorized: Invalid or missing API Key"}), 401

    data = request.get_json(silent=True)
    if not data:
        monitoring_stats["validation_errors"] += 1
        return jsonify({"error": "Invalid JSON format"}), 400

    ok, message, status_code = process_sensor_payload(data)
    if not ok:
        return jsonify({"error": message}), status_code

    return jsonify({"status": "success", "message": message}), 200


@app.route("/api/sensor/latest", methods=["GET"])
def get_latest_data():
    if not latest_sensor_data:
        return jsonify({"error": "No data available yet"}), 404
    return jsonify({
        "latest_reading": latest_sensor_data,
        "monitoring": monitoring_stats
    }), 200


if __name__ == "__main__":
    start_mqtt_client()
    app.run(host="0.0.0.0", port=5000, debug=True, use_reloader=False)
