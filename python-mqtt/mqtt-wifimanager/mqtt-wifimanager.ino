#include <Arduino.h>
#include <ESP8266WiFi.h>
#include <WiFiManager.h>
#include <WiFiClient.h>
#include <PubSubClient.h>
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
const char* mqttServer = "d55e4c6c198a48739d2f5f4c17588e22.s1.eu.hivemq.cloud";
 // Max IP address length is 15 characters (xxx.xxx.xxx.xxx)
char mqttUser[32];
char mqttPassword[32];
const char* clientId = "ESP8266_Client";

WiFiClient espClient;
PubSubClient client(espClient);

// Function prototype
void callback(char* topic, byte* payload, unsigned int length);

void setup() {
  client.subscribe("voltage", 0);
  // Setup Serial Monitor
  Serial.begin(9600);
  Serial.println("DC Voltage and HX711 Load Cell Test");

  // Initialize WiFiManager
  WiFiManager wifiManager;
  
  // Uncomment the next line to reset the settings (for testing purposes)
  wifiManager.resetSettings();

  // Set custom parameters for configuration
  //WiFiManagerParameter custom_mqtt_server("mqttServer", "MQTT Server", mqttServer, 16);

  WiFiManagerParameter custom_mqtt_user("mqttUser", "MQTT User", mqttUser, 32);
  WiFiManagerParameter custom_mqtt_password("mqttPassword", "MQTT Password", mqttPassword, 32);


  // Add parameters to WiFiManager
  //wifiManager.addParameter(&custom_mqtt_server);

  wifiManager.addParameter(&custom_mqtt_user);
  wifiManager.addParameter(&custom_mqtt_password);


  // Connect to Wi-Fi or configure it if not yet configured
  if (!wifiManager.autoConnect("Rotorque ThrustRig")) {
    Serial.println("Failed to connect and hit timeout");
    delay(3000);
    // Reset and try again, or put it to deep sleep
    ESP.reset();
    delay(5000);
  }

  Serial.println("Connected to WiFi");

  // Copy the custom MQTT server value after the WiFiManager configuration
  //strcpy(mqttServer, custom_mqtt_server.getValue());
  strcpy(mqttUser, custom_mqtt_user.getValue());
  strcpy(mqttPassword, custom_mqtt_password.getValue());
  Serial.print("MQTT Server: ");
  Serial.println(mqttServer);
 

  // Setup MQTT
  client.setServer(mqttServer, 1883);
  client.setCallback(callback);

  // Connect to the server
  if (client.connect(clientId, mqttUser, mqttPassword)) {
    Serial.println("Connected to MQTT server");
} else {
    Serial.println("MQTT Connection failed. Error code: " + String(client.state()));
}

  // Initialize HX711
  scale.begin(LOADCELL_DOUT_PIN, LOADCELL_SCK_PIN);
  scale.set_scale(101.481);
  scale.tare();
}

void loop() {
  client.loop();
  Serial.println("Entering loop...");

  // Read the Analog Input
  adc_value = analogRead(ANALOG_IN_PIN);
  Serial.println("ADC Value: " + String(adc_value));

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

  // Create a formatted time string
  String timeString = String(millis());

  // Send data to MQTT topics
  Serial.println("Publishing to voltage topic");
  client.publish("voltage", String(in_voltage, 2).c_str());
  Serial.println("Publishing to loadCellReading topic");
  client.publish("loadCellReading", String(loadCellReading, 1).c_str());
  Serial.println("Publishing to averageReading topic");
  client.publish("averageReading", String(averageReading, 5).c_str());

  Serial.println("Exiting loop...");

  // Short delay
  delay(500);
}

// MQTT callback function
void callback(char* topic, byte* payload, unsigned int length) {
  // Handle incoming MQTT messages here
  Serial.print("Message arrived [");
  Serial.print(topic);
  Serial.print("] ");
  for (int i = 0; i < length; i++) {
    Serial.print((char)payload[i]);
  }
  Serial.println();
}
