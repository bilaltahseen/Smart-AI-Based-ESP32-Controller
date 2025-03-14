/*
 * Smart AI-Based ESP32 Controller
 * Configuration File
 */

#ifndef CONFIG_H
#define CONFIG_H

// WiFi Configuration
#define WIFI_SSID "<your_wifi_ssid>"
#define WIFI_PASSWORD "<your_wifi_password>"
#define WIFI_TIMEOUT 20000  // 20 seconds timeout for WiFi connection

// MQTT Configuration
#define MQTT_BROKER "<your_mqtt_broker>" // e.g., "192.168.1.100" or "broker.hivemq.com"
#define MQTT_PORT 8883  // 8883 is the standard port for MQTT over TLS
#define MQTT_CLIENT_ID "ESP32_GPIO_Controller"
#define MQTT_USERNAME "<your_mqtt_username>"  // Leave empty if not required
#define MQTT_PASSWORD "<your_mqtt_password>"  // Leave empty if not required
#define MQTT_RECONNECT_DELAY 5000 // 5 seconds delay between reconnection attempts

/*
 * IMPORTANT NOTE: For HiveMQ Cloud connections
 * ---------------------------------------
 * 1. This configuration requires WiFiClientSecure (now included in the main code)
 * 2. We've set espClient.setInsecure() to bypass certificate verification for development
 * 3. For production use, you should use proper certificate verification:
 *    - Download the root CA cert for HiveMQ Cloud
 *    - Use espClient.setCACert(rootCA) in your code
 * 4. If connection still fails, check:
 *    - Username/password correctness
 *    - MQTT broker URL is exact
 *    - Your network allows outbound connections on port 8883
 */

// MQTT Topics
#define MQTT_TOPIC_PREFIX "esp32/gpio"
#define MQTT_TOPIC_CONTROL MQTT_TOPIC_PREFIX "/control"   // Topic to receive commands
#define MQTT_TOPIC_STATUS MQTT_TOPIC_PREFIX "/status"     // Topic to publish status
#define MQTT_TOPIC_TELEMETRY MQTT_TOPIC_PREFIX "/telemetry" // Topic to publish sensor data

// GPIO Pin Configuration
#define NUM_CONTROL_PINS 4  // Number of pins that can be controlled via MQTT

// Define the GPIO pins that can be controlled
const int CONTROL_PINS[NUM_CONTROL_PINS] = {
  5,  // GPIO5
  15, // GPIO15
  17, // GPIO17
  18  // GPIO18
};

// Sensor pins (if applicable)
#define DHT_SENSOR_PIN 4
#define DHT_SENSOR_TYPE DHT22  // DHT11 or DHT22

// Debug settings
#define DEBUG_ENABLED true
#define SERIAL_BAUD_RATE 115200

#endif // CONFIG_H 