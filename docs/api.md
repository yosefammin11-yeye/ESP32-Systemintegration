# API-dokumentation

## 1. Översikt
Lösningen tillgängliggör sensordata via ett REST-API som tar emot och exponerar validerad data från MQTT-bearbetningstjänsten.

## 2. Datakontrakt (JSON)
All sensordata som skickas över MQTT och exponeras via API:et följer detta strukturformat:
```json
{
  "sensorId": "room-a-temp-01",
  "timestamp": "2026-11-15T12:30:00+01:00",
  "value": 21.7,
  "unit": "C"
}
