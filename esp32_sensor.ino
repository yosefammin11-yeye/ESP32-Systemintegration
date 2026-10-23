#include <WiFi.h>
#include <HTTPClient.h>

const char* ssid = "DittWiFiNamn";
const char* password = "DittWiFiLösenord";
const char* serverUrl = "http://192.168.1.50:5000/api/data";

void setup() {
  Serial.begin(115200);
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\nAnsluten till WiFi!");
}

void loop() {
  if (WiFi.status() == WL_CONNECTED) {
    HTTPClient http;
    http.begin(serverUrl);
    http.addHeader("Content-Type", "application/json");

    // JSON-meddelande med sensordata
    String jsonPayload = "{\"device_id\":\"ESP32_01\", \"temperature\":22.5, \"humidity\":45.0}";

    int httpResponseCode = http.POST(jsonPayload);
    Serial.print("HTTP Svar: ");
    Serial.println(httpResponseCode);

    http.end();
  }
  delay(10000); // Skickar data var 10:e sekund
}
