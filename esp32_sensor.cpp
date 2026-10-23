#include <stdio.h>
#include <string.h>
#include <stdlib.h>

// Struktur för sensordata i C/C++
typedef struct {
    char device_id[32];
    float temperature;
    float humidity;
} sensor_data_t;

// Funktion för att strukturera sensordata till JSON-sträng
int serialize_sensor_data(const sensor_data_t* sensor, char* buffer, size_t buffer_len) {
    if (!sensor || !buffer) return -1;
    return snprintf(buffer, buffer_len, 
                    "{\"device_id\": \"%s\", \"temperature\": %.2f, \"humidity\": %.2f}",
                    sensor->device_id, sensor->temperature, sensor->humidity);
}

// Huvudfunktion för IoT-enhetens mätcykel
int main(void) {
    sensor_data_t current_reading = {
        .device_id = "ESP32_SENSOR_NODE_01",
        .temperature = 23.4f,
        .humidity = 48.2f
    };

    char json_payload[256];
    if (serialize_sensor_data(&current_reading, json_payload, sizeof(json_payload)) > 0) {
        printf("Genererad JSON-payload för REST API:\n%s\n", json_payload);
    }

    return 0;
}
