#include <WiFi.h>
#include <PubSubClient.h>
#include <ArduinoJson.h>

const char* ssid = "Wokwi-GUEST";
const char* password = "";
const char* mqtt_server = "broker.hivemq.com";

WiFiClient espClient;
PubSubClient client(espClient);

void setup_wifi() {
  delay(10);
  Serial.println("Ansluter till WiFi...");
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\nWiFi anslutet!");
}

void reconnect() {
  while (!client.connected()) {
    Serial.print("Försöker ansluta till MQTT...");
    if (client.connect("ESP32Client_Yosef")) {
      Serial.println("Ansluten!");
    } else {
      Serial.print("Misslyckades, rc=");
      Serial.print(client.state());
      Serial.println(" Försöker igen om 5 sekunder");
      delay(5000);
    }
  }
}

void setup() {
  Serial.begin(115200);
  setup_wifi();
  client.setServer(mqtt_server, 1883);
}

void loop() {
  if (!client.connected()) {
    reconnect();
  }
  client.loop();

  float temperature = 21.7;

  StaticJsonDocument<200> doc;
  doc["sensorId"] = "room-a-temp-01";
  doc["timestamp"] = "2026-11-18T12:00:00+01:00";
  doc["value"] = temperature;
  doc["unit"] = "C";

  char buffer[256];
  serializeJson(doc, buffer);

  client.publish("sodertalje/fastighet/sensor/temp", buffer);
  Serial.println("Skickat meddelande till broker!");

  delay(10000);
}
