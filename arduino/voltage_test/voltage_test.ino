#include <ESP8266WiFi.h>
#include <WiFiClient.h>

// Define analog input
#define ANALOG_IN_PIN A0

// Global variables
float adc_voltage = 0.0;
float in_voltage = 0.0;
float R1 = 98000.0;
float R2 = 9600.0;
float ref_voltage = 3.118;
int adc_value = 0;

// Your Wi-Fi network credentials
const char* ssid = "Airtel_GS Home";
const char* password = "Harish@9514811066";

// Server configuration
const char* serverIP = "192.168.1.100"; // Replace with your server's IP
const int serverPort = 8080;           // Replace with your server's port

WiFiClient client;

void setup() {
  // Setup Serial Monitor
  Serial.begin(9600);
  Serial.println("DC Voltage Test");

  // Connect to Wi-Fi
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting to WiFi...");
  }
  Serial.println("Connected to WiFi");

  // Connect to the server
  if (client.connect(serverIP, serverPort)) {
    Serial.println("Connected to server");
  } else {
    Serial.println("Connection failed");
  }
}

void loop() {
  // Read the Analog Input
  adc_value = analogRead(ANALOG_IN_PIN);
  Serial.println(adc_value);

  // Determine voltage at ADC input
  adc_voltage = (adc_value * ref_voltage) / 1024.0;

  // Calculate voltage at divider input
  in_voltage = adc_voltage / (R2 / (R1 + R2));

  // Print results to Serial Monitor to 2 decimal places
  Serial.print("Input Voltage = ");
  Serial.println(in_voltage, 2);

  // Send the voltage data to the Python server
  client.println(in_voltage, 2);

  // Short delay
  delay(500);
}
