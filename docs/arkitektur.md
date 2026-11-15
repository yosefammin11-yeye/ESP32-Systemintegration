# Arkitekturbeskrivning - IoT- och Systemintegrationslösning

## 1. Systemöversikt och Dataflöde
Lösningen samlar in miljödata från en sensor ansluten till en ESP32-enhet, överför datan via MQTT till en broker, bearbetar och validerar den i en backend-tjänst och tillgängliggör den via ett REST-API.

### Dataflödesdiagram
```text
[ESP32 / Sensor] 
       │ 
       ▼ (MQTT / Port 1883)
[MQTT Broker (Mosquitto)] 
       │ 
       ▼ (Prenumeration / Bearbetningstjänst)
[Backend / Bearbetningstjänst (Python)] 
       │ 
       ▼ (HTTP/REST / Port 5000)
[API-klient / Konsument]
