# Dokumentation: Systemintegration & ESP32

## 1. Systemarkitektur
Systemet består av en ESP32-mikrokontroller utrustad med sensorer. ESP32-enheten ansluter till det lokala nätverket via Wi-Fi och skickar mätdata i JSON-format till ett centralt REST-API skapat i Python (Flask).

## 2. API-struktur
API:et har en endpoint för inkommande sensordata:
* **Endpoint:** `POST /api/data`
* **Format:** JSON
* **Exempel på JSON-payload:**
```json
{
  "device_id": "ESP32_01",
  "temperature": 22.5,
  "humidity": 45.0
}
