/*
 * Smart AI-Based ESP32 Controller
 * ESP32 MQTT GPIO Controller Firmware
 * 
 * This firmware allows remote control of ESP32 GPIO pins via MQTT protocol.
 * It connects to WiFi, subscribes to control topics, and publishes status.
 */

#include <WiFi.h>
#include <WiFiClientSecure.h>  // Added for secure MQTT connection
#include <PubSubClient.h>  // MQTT Client
#include <ArduinoJson.h>   // For parsing JSON commands
#include <DHT.h>          // For temperature/humidity sensor (optional)
#include "config.h"       // Configuration file

// Initialize WiFi client (secure)
WiFiClientSecure espClient;  // Changed from WiFiClient to WiFiClientSecure

// Initialize MQTT client
PubSubClient mqttClient(espClient);

// Initialize DHT sensor (if enabled)
#ifdef DHT_SENSOR_PIN
DHT dht(DHT_SENSOR_PIN, DHT_SENSOR_TYPE);
#endif

// Variables to track connection state
bool wifiConnected = false;
bool mqttConnected = false;
unsigned long lastReconnectAttempt = 0;
unsigned long lastTelemetryUpdate = 0;

// GPIO pin states
bool pinState[NUM_CONTROL_PINS] = {false};

// Setup function - runs once at startup
void setup() {
  // Initialize serial communication
  Serial.begin(SERIAL_BAUD_RATE);
  Serial.println("\n\nESP32 MQTT GPIO Controller");
  Serial.println("===========================");
  
  // Initialize GPIO pins as outputs
  for (int i = 0; i < NUM_CONTROL_PINS; i++) {
    pinMode(CONTROL_PINS[i], OUTPUT);
    digitalWrite(CONTROL_PINS[i], LOW);  // Default to OFF
    pinState[i] = false;
  }
  
  // Connect to WiFi
  setupWiFi();
  
  // Configure secure client to bypass certificate validation (only for development)
  espClient.setInsecure();  // Added to allow connection without certificate validation
  
  // Initialize MQTT client
  mqttClient.setServer(MQTT_BROKER, MQTT_PORT);
  mqttClient.setCallback(mqttCallback);
  
  // Initialize DHT sensor if enabled
  #ifdef DHT_SENSOR_PIN
  dht.begin();
  #endif
  
  // Attempt initial MQTT connection
  connectMQTT();
}

// Main loop - runs repeatedly after setup
void loop() {
  // Check WiFi connection
  if (!wifiConnected) {
    setupWiFi();
  }
  
  // Check MQTT connection
  if (wifiConnected && !mqttClient.connected()) {
    unsigned long currentMillis = millis();
    if (currentMillis - lastReconnectAttempt > MQTT_RECONNECT_DELAY) {
      lastReconnectAttempt = currentMillis;
      // Attempt to reconnect
      connectMQTT();
    }
  }
  
  // Process MQTT messages if connected
  if (mqttClient.connected()) {
    mqttClient.loop();
  }
  
  // Send telemetry data periodically (every 30 seconds)
  unsigned long currentMillis = millis();
  if (currentMillis - lastTelemetryUpdate > 30000) {
    lastTelemetryUpdate = currentMillis;
    publishTelemetry();
  }
}

// Connect to WiFi network
void setupWiFi() {
  if (wifiConnected) return;
  
  Serial.print("Connecting to WiFi network: ");
  Serial.println(WIFI_SSID);
  
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
  
  // Wait for connection with timeout
  unsigned long startTime = millis();
  while (WiFi.status() != WL_CONNECTED && millis() - startTime < WIFI_TIMEOUT) {
    delay(500);
    Serial.print(".");
  }
  
  if (WiFi.status() == WL_CONNECTED) {
    wifiConnected = true;
    Serial.println("");
    Serial.println("WiFi connected");
    Serial.print("IP address: ");
    Serial.println(WiFi.localIP());
  } else {
    wifiConnected = false;
    Serial.println("");
    Serial.println("WiFi connection FAILED");
  }
}

// Connect to MQTT broker
bool connectMQTT() {
  if (!wifiConnected) return false;
  
  Serial.print("Connecting to MQTT broker at ");
  Serial.print(MQTT_BROKER);
  Serial.print(":");
  Serial.println(MQTT_PORT);
  
  // Create a random client ID
  String clientId = MQTT_CLIENT_ID;
  clientId += "-";
  clientId += String(random(0xffff), HEX);
  
  // Attempt to connect with improved error reporting
  bool connected = false;
  if (strlen(MQTT_USERNAME) > 0) {
    connected = mqttClient.connect(clientId.c_str(), MQTT_USERNAME, MQTT_PASSWORD);
  } else {
    connected = mqttClient.connect(clientId.c_str());
  }
  
  if (connected) {
    Serial.println("Connected to MQTT broker");
    
    // Subscribe to control topic
    mqttClient.subscribe(MQTT_TOPIC_CONTROL);
    Serial.print("Subscribed to: ");
    Serial.println(MQTT_TOPIC_CONTROL);
    
    // Publish initial status
    publishStatus();
    
    mqttConnected = true;
    return true;
  } else {
    Serial.print("MQTT connection failed, rc=");
    int state = mqttClient.state();
    Serial.print(state);
    // Add more detailed error messages based on error code
    switch(state) {
      case -4:
        Serial.println(" (MQTT_CONNECTION_TIMEOUT)");
        break;
      case -3:
        Serial.println(" (MQTT_CONNECTION_LOST)");
        break;
      case -2:
        Serial.println(" (MQTT_CONNECT_FAILED)");
        break;
      case -1:
        Serial.println(" (MQTT_DISCONNECTED)");
        break;
      case 1:
        Serial.println(" (MQTT_CONNECT_BAD_PROTOCOL)");
        break;
      case 2:
        Serial.println(" (MQTT_CONNECT_BAD_CLIENT_ID)");
        break;
      case 3:
        Serial.println(" (MQTT_CONNECT_UNAVAILABLE)");
        break;
      case 4:
        Serial.println(" (MQTT_CONNECT_BAD_CREDENTIALS)");
        break;
      case 5:
        Serial.println(" (MQTT_CONNECT_UNAUTHORIZED)");
        break;
      default:
        Serial.println(" (Unknown error)");
    }
    mqttConnected = false;
    return false;
  }
}

// MQTT message callback
void mqttCallback(char* topic, byte* payload, unsigned int length) {
  Serial.print("Message received on topic: ");
  Serial.println(topic);
  
  // Create a null-terminated string from the payload
  char message[length + 1];
  for (unsigned int i = 0; i < length; i++) {
    message[i] = (char)payload[i];
  }
  message[length] = '\0';
  
  Serial.print("Message: ");
  Serial.println(message);
  
  // Process control messages
  if (strcmp(topic, MQTT_TOPIC_CONTROL) == 0) {
    processControlMessage(message);
  }
}

// Process control messages (JSON format expected)
void processControlMessage(const char* message) {
  // Reserve memory for the JSON document
  StaticJsonDocument<256> doc;
  
  // Parse JSON
  DeserializationError error = deserializeJson(doc, message);
  
  // Check for parsing errors
  if (error) {
    Serial.print("JSON parsing failed: ");
    Serial.println(error.c_str());
    return;
  }
  
  // Check if it's a pin control command
  if (doc.containsKey("pin") && doc.containsKey("state")) {
    int pin = doc["pin"];
    bool state = doc["state"];
    
    // Find the index of the pin in our control array
    int pinIndex = -1;
    for (int i = 0; i < NUM_CONTROL_PINS; i++) {
      if (CONTROL_PINS[i] == pin) {
        pinIndex = i;
        break;
      }
    }
    
    // If pin is valid, control it
    if (pinIndex >= 0) {
      digitalWrite(pin, state ? HIGH : LOW);
      pinState[pinIndex] = state;
      
      Serial.print("Set GPIO ");
      Serial.print(pin);
      Serial.print(" to ");
      Serial.println(state ? "HIGH" : "LOW");
      
      // Publish updated status
      publishStatus();
    } else {
      Serial.print("Invalid pin: ");
      Serial.println(pin);
    }
  }
  
  // Check for a status request command
  if (doc.containsKey("command") && strcmp(doc["command"], "getStatus") == 0) {
    publishStatus();
  }
}

// Publish GPIO status to MQTT
void publishStatus() {
  if (!mqttClient.connected()) return;
  
  // Create JSON document
  StaticJsonDocument<512> doc;
  
  // Add information about each controlled pin
  JsonArray pins = doc.createNestedArray("pins");
  
  for (int i = 0; i < NUM_CONTROL_PINS; i++) {
    JsonObject pin = pins.createNestedObject();
    pin["gpio"] = CONTROL_PINS[i];
    pin["state"] = pinState[i];
  }
  
  // Add device information
  doc["deviceId"] = MQTT_CLIENT_ID;
  doc["ipAddress"] = WiFi.localIP().toString();
  doc["rssi"] = WiFi.RSSI();
  
  // Serialize to JSON string
  char jsonBuffer[512];
  serializeJson(doc, jsonBuffer);
  
  // Publish to status topic
  Serial.print("Publishing status: ");
  Serial.println(jsonBuffer);
  mqttClient.publish(MQTT_TOPIC_STATUS, jsonBuffer);
}

// Publish telemetry data (sensor readings)
void publishTelemetry() {
  if (!mqttClient.connected()) return;
  
  // Create JSON document
  StaticJsonDocument<256> doc;
  
  // Add device information
  doc["deviceId"] = MQTT_CLIENT_ID;
  
  // Read and add DHT sensor data if available
  #ifdef DHT_SENSOR_PIN
  float humidity = dht.readHumidity();
  float temperature = dht.readTemperature();
  
  if (!isnan(humidity) && !isnan(temperature)) {
    doc["temperature"] = temperature;
    doc["humidity"] = humidity;
  }
  #endif
  
  // Add free heap memory (useful for diagnostics)
  doc["freeHeap"] = ESP.getFreeHeap();
  
  // Add uptime in seconds
  doc["uptime"] = millis() / 1000;
  
  // Serialize to JSON string
  char jsonBuffer[256];
  serializeJson(doc, jsonBuffer);
  
  // Publish to telemetry topic
  mqttClient.publish(MQTT_TOPIC_TELEMETRY, jsonBuffer);
} 