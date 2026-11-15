# Testprotokoll - Systemintegration

## 1. Testmiljö
* **Hårdvara:** ESP32 NodeMCU
* **Broker:** Eclipse Mosquitto (lokal installation)
* **Backend:** Python / Flask med REST-API

## 2. Utförda Tester

### Test 1: MQTT-publicering från ESP32
* **Testscenario:** Verifiera att ESP32 kan ansluta till Mosquitto-brokern och publicera JSON-data på rätt topic (`iot/building/room-a/temperature`).
* **Förväntat resultat:** Meddelandet tas emot av brokern utan avbrott.
* **Utfall:** **GODKÄNT** – Sensordata publiceras periodiskt.

### Test 2: REST-API hantering och JSON-validering
* **Testscenario:** Anropa GET-endpointen `/api/sensor/latest` när data har sparats.
* **Förväntat resultat:** HTTP 200 OK med korrekt JSON-struktur returneras.
* **Utfall:** **GODKÄNT** – Returnerar senaste mätvärdet med rätt tidsstämpel.
