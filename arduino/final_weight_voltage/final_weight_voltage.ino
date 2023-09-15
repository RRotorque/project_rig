#include <Arduino.h>
#include <ESP8266WiFi.h>
#include <WiFiClient.h>
#include "HX711.h"

// HX711 circuit wiring
const int LOADCELL_DOUT_PIN = 12;
const int LOADCELL_SCK_PIN = 13;
HX711 scale;

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
// const char* ssid = "Airtel_GS Home";
// const char* password = "Harish@9514811066";

const char* ssid = "Sam";
const char* password = "1234567890";

// Server configuration
const char* serverIP = "192.168.34.82"; // Replace with your server's IP
const int serverPort = 8081;           // Replace with your server's port

WiFiClient client;

void setup() {
  // Setup Serial Monitor
  Serial.begin(9600);
  Serial.println("DC Voltage and HX711 Load Cell Test");

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

  // Initialize HX711
  scale.begin(LOADCELL_DOUT_PIN, LOADCELL_SCK_PIN);
  scale.set_scale(101.481);
  scale.tare();
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

  // Read load cell data
  float loadCellReading = scale.get_units(1); // Read the load cell reading

  // Calculate and print the load cell average reading
  float averageReading = scale.get_units(10); // Read and calculate the average reading
  Serial.print("Load Cell Reading: ");
  Serial.print(loadCellReading, 1);
  Serial.print(" g\t| Average: ");
  Serial.println(averageReading, 5);

unsigned long currentTime = millis();
unsigned long seconds = currentTime / 1000;  // Convert milliseconds to seconds
unsigned long minutes = seconds / 60;       // Convert seconds to minutes
unsigned long hours = minutes / 60;         // Convert minutes to hours

// Calculate remaining minutes and seconds
seconds %= 60;
minutes %= 60;
hours %= 24; // If you want to keep it within a 24-hour format

// Create a formatted time string
String timeString = String(hours) + ":" + String(minutes) + ":" + String(seconds);


  // Send both the voltage data and load cell readings to the Python server
  if (client.connect(serverIP, serverPort)) {
    // Create a string containing the data to send
    String dataToSend = timeString + "," +String(millis()) + "," + String(in_voltage, 2) + "," + String(loadCellReading, 1) + "," + String(averageReading, 5);

    // Send the data to the server
    client.println(dataToSend);

    // Print the sent data to Serial Monitor
    Serial.println("Data Sent: " + dataToSend);

    // Wait for a response from the server
    while (client.connected() && !client.available()) {
      delay(1);
    }

    // Read the response from the server
    String response = client.readStringUntil('\n');
    Serial.println("Server Response: " + response);

    // Close the connection
    client.stop();
  } else {
    Serial.println("Connection to server failed");
  }

  // Short delay
  delay(500);
}

