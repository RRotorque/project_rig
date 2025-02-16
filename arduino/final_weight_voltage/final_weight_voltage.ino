#include <Arduino.h>
#include <ESP8266WiFi.h>
#include <WiFiClient.h>
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

const char* serverIP = "192.168.151.110";
const int serverPort = 1883;

WiFiClient client;

void setup() {
  Serial.begin(115200);
  Serial.println("DC Voltage and HX711 Load Cell Test");

  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting to WiFi...");
  }
  Serial.println("Connected to WiFi");

  if (client.connect(serverIP, serverPort)) {
    Serial.println("Connected to server");
  } else {
    Serial.println("Connection to server failed");
  }

  scale.begin(LOADCELL_DOUT_PIN, LOADCELL_SCK_PIN);
  scale.set_scale(101.481);
  scale.tare();
}

void loop() {
  adc_value = analogRead(ANALOG_IN_PIN);
  Serial.println(adc_value);

  adc_voltage = (adc_value * ref_voltage) / 1024.0;
  in_voltage = adc_voltage / (R2 / (R1 + R2));
  Serial.print("Input Voltage = ");
  Serial.println(in_voltage, 2);

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
    String dataToSend = timeString + "," + String(millis()) + "," + String(in_voltage, 2) + "," + String(loadCellReading, 1) + "," + String(averageReading, 5);
    client.println(dataToSend);
    Serial.println("Data Sent: " + dataToSend);
  } else {
    Serial.println("Connection to server lost. Reconnecting...");
    if (client.connect(serverIP, serverPort)) {
      Serial.println("Reconnected to server");
    } else {
      Serial.println("Reconnection to server failed");
    }
  }

  delay(500);
}
