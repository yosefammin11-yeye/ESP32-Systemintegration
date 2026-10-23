# Systemintegration & Embedded IoT System

## 1. Systemarkitektur
Detta projekt demonstrerar en komplett systemintegrationskedja för IoT-tillämpningar. Systemet består av två huvudkomponenter:
* **Embedded Edge-enhet (ESP32):** Ansvarar för att läsa in sensordata, strukturera datan i JSON-format och överföra den över lokalt nätverk via HTTP POST-anrop.
* **Backend REST API (Python/Flask):** Fungerar som central mottagare för mätdata. Servern tar emot HTTP-förfrågningar, validerar datans struktur och svarar med lämpliga statuskoder.
