# ESP32 Systemintegration

## 1. Lösningens syfte
Projektet syftar till att bygga en komplett end-to-end IoT-lösning där mätdata samlas in från en ESP32-enhet (simulerad i Wokwi), skickas via MQTT till en broker, och vidarebefordras till en Python/Flask-backend för validering och lagring.

## 2. Installationsanvisningar
1. Klona repot till din dator:
   `git clone https://github.com/yosefammin11-yeye/ESP32-Systemintegration.git`
2. Navigera till mappen och installera beroenden:
   `pip install -r requirements.txt`

## 3. Nödvändiga beroenden
* Python 3.8+
* Flask
* python-dotenv
* Paho-MQTT
* ArduinoJson (för ESP32)

## 4. Konfiguration
Skapa en `.env`-fil i roten av projektet med följande innehåll för att hantera API-nyckeln säkert:
`API_KEY=hemlig-api-nyckel-123`

## 5. Instruktioner för att starta lösningen
1. Starta Flask-backenden: `python src/app.py`
2. Starta ESP32-simuleringen som ansluter till MQTT-brokern `broker.hivemq.com` och publicerar data.

## 6. Instruktioner för att verifiera dataflödet
Du kan verifiera att data sparas genom att göra ett GET-anrop mot API:et:
`curl http://localhost:5000/api/sensor/latest`

För att testa POST-anropet med validering och API-nyckel:
`curl -X POST http://localhost:5000/api/data -H "Content-Type: application/json" -H "X-API-Key: hemlig-api-nyckel-123" -d '{"sensorId":"room-a-temp-01","timestamp":"2026-11-18T12:00:00+01:00","value":21.7,"unit":"C"}'`

## 7. Kända begränsningar
* Systemet lagrar endast den senaste mätningen i minnet (ingen persistent databas som SQLite/PostgreSQL används i denna version).
