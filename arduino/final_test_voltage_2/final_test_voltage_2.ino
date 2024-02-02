#include <Arduino.h>
#include <ESP8266WiFi.h>
#include <WiFiClient.h>
#include <PubSubClient.h>
#include "HX711.h"

const int LOADCELL_DOUT_PIN = 12;
const int LOADCELL_SCK_PIN = 13;
HX711 scale;

#define ANALOG_IN_PIN A0

float adc_voltage = 0.0;
float in_voltage = 0.0;
float R1 = 98000.0;
float R2 = 9600.0;
float ref_voltage = 3.118;
int adc_value = 0;

const char* ssid = "Sam";
const char* password = "1234567890";

const char* mqttServer = "192.168.151.110";
const int mqttPort = 1883;

WiFiClient espClient;
PubSubClient client(espClient);

#define MIN_RECONNECT_DELAY 5000  // 5 seconds
#define MAX_RECONNECT_DELAY 60000 // 1 minute

int reconnectDelay = MIN_RECONNECT_DELAY;

void setup() {
  Serial.begin(9600);

  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting to WiFi...");
  }
  Serial.println("Connected to WiFi");

  client.setServer(mqttServer, mqttPort);

  scale.begin(LOADCELL_DOUT_PIN, LOADCELL_SCK_PIN);
  scale.set_scale(101.481);
  scale.tare();
}

void loop() {
  client.loop();

  // Read the Analog Input
  adc_value = analogRead(ANALOG_IN_PIN);
  Serial.println(adc_value);

  // Determine voltage at ADC input
  adc_voltage = (adc_value * ref_voltage) / 1024.0;

  // Calculate voltage at divider input
  in_voltage = adc_voltage / (R2 / (R1 + R2));

  Serial.print("Input Voltage = ");
  Serial.println(in_voltage, 2);

  // Read load cell data
  float loadCellReading = scale.get_units(1);
  float averageReading = scale.get_units(10);

  Serial.print("Load Cell Reading: ");
  Serial.print(loadCellReading, 1);
  Serial.print(" g\t| Average: ");
  Serial.println(averageReading, 5);

  unsigned long currentTime = millis();
  unsigned long seconds = currentTime / 1000;
  unsigned long minutes = seconds / 60;
  unsigned long hours = minutes / 60;

  seconds %= 60;
  minutes %= 60;
  hours %= 24;

  String timeString = String(hours) + ":" + String(minutes) + ":" + String(seconds);

  if (client.connected()) {
    // Construct the JSON string
    String dataToSend = String("{\"time\":\"") + timeString + "\",\"reading\":" + String(loadCellReading, 1) + ",\"voltage\":" + String(in_voltage, 2) + "}";
    client.publish("sensorData", dataToSend.c_str());
    Serial.println("Data Sent: " + dataToSend);
  } else {
    Serial.println("Connection to server lost. Reconnecting...");
    if (client.connect("ESP8266Client")) {
      Serial.println("Reconnected to server");
      reconnectDelay = MIN_RECONNECT_DELAY;
    } else {
      Serial.println("Reconnection to server failed");
      delay(reconnectDelay);
      reconnectDelay = min(reconnectDelay * 2, MAX_RECONNECT_DELAY);
    }
  }

  delay(500);
}
