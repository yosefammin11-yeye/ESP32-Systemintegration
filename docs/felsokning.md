# Felsökningsdokumentation

## 1. Fel 1: Tappad anslutning till MQTT-broker
* **Symptom:** ESP32-enheten slutar skicka sensordata och loggar upprepade felmeddelanden om att anslutningen till brokern misslyckades.
* **Orsak:** Tillfälliga nätverksstörningar, att Wi-Fi har tappats, eller att Mosquitto-brokern har startats om.
* **Åtgärd:** Enheten har en inbyggd automatisk återanslutningsloop (reconnect) som försöker igen efter en kort fördröjning. Kontrollera att brokern körs och att IP-adress/port (`1883`) stämmer i konfigurationen.

## 2. Fel 2: Valideringsfel vid inkommande JSON-data
* **Symptom:** Backend-tjänsten tar emot meddelandet men vägrar spara det och loggar ett felmeddelande.
* **Orsak:** Det inkommande JSON-paketet saknar obligatoriska fält (t.ex. `sensorId` eller `value`) eller innehåller felaktig datatyp.
* **Åtgärd:** Kontrollera att ESP32-koden formaterar JSON-strängen exakt enligt API-kontraktet. Läs i backend-loggen för att se exakt vilket fält som orsakade valideringsfelet.
