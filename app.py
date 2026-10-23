from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/api/data', methods=['POST'])
def receive_sensor_data():
    data = request.get_json()
    print("Mottagen sensordata från ESP32:", data)
    return jsonify({"status": "Success", "message": "Data mottagen!"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
