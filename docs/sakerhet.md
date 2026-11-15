# Säkerhetsbeskrivning

## 1. Identifikation och Autentisering
* **MQTT Broker (Mosquitto):** Konfigurerad med användarnamn och lösenord för att förhindra obehöriga enheter från att publicera eller prenumerera på topics.
* **API-åtkomst:** Endpoints skyddas vid behov med API-nycklar eller tokens för att säkerställa att endast behöriga konsumenter kan hämta sensordata.

## 2. Kryptering i transit
* **MQTT:** Kan konfigureras med TLS/SSL på port `8883` för krypterad kommunikation mellan ESP32 och broker. Vid lokal utveckling används port `1883`.
* **REST-API:** Använder HTTPS (TLS) i produktionsmiljö för att kryptera HTTP-trafiken.

## 3. Hantering av hemligheter (Credentials)
* Inga lösenord, API-nycklar eller Wi-Fi-uppgifter (SSID/lösenord) hårdkodas i källkoden. 
* Dessa hanteras via externa konfigurationsfiler (t.ex. miljötavlor/environment variables eller `secrets.h`) som undantas från versionshantering via `.gitignore`.
