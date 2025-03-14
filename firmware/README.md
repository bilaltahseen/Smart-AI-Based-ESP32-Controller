# ESP32 MQTT GPIO Controller Firmware

This firmware allows you to control your ESP32's GPIO pins remotely using the MQTT protocol. It provides a simple yet powerful way to integrate your ESP32 into IoT systems, home automation setups, or AI-powered control systems.

## Features

- Control ESP32 GPIO pins remotely via MQTT
- Connect to any MQTT broker (local or cloud-based)
- Automatic reconnection to WiFi and MQTT broker
- JSON-based command interface
- Status reporting and telemetry publication
- Optional temperature and humidity sensor support (DHT11/DHT22)

## Prerequisites

To use this firmware, you'll need:

1. Arduino IDE with ESP32 board support installed
2. The following libraries:
   - WiFi (included with ESP32 board package)
   - PubSubClient (MQTT client)
   - ArduinoJson
   - DHT sensor library (if using temperature/humidity sensor)
3. Access to an MQTT broker (local or cloud-based)

## Installation

1. Open the Arduino IDE
2. Install the required libraries via the Library Manager:
   - Go to Sketch > Include Library > Manage Libraries...
   - Search for and install:
     - "PubSubClient" by Nick O'Leary
     - "ArduinoJson" by Benoit Blanchon
     - "DHT sensor library" by Adafruit (if using a DHT sensor)
3. Open the `ESP32_MQTT_GPIO_Controller.ino` file
4. Edit the `config.h` file to set your WiFi and MQTT broker details
5. Upload the sketch to your ESP32 board

## Configuration

Edit the `config.h` file to customize the firmware for your setup:

- Set your WiFi credentials
- Set your MQTT broker address and credentials
- Configure which GPIO pins should be controllable
- Set up sensor pins if applicable

## Usage

### Controlling GPIO Pins

To control a GPIO pin, publish a JSON message to the control topic (default: `esp32/gpio/control`):

```json
{
  "pin": 5,
  "state": true
}
```

Where:
- `pin` is the GPIO pin number (must be one of the pins defined in configuration)
- `state` is `true` for HIGH (ON) or `false` for LOW (OFF)

### Requesting Status

To request the current status of all pins, publish:

```json
{
  "command": "getStatus"
}
```

### Monitoring Status

Subscribe to the status topic (default: `esp32/gpio/status`) to receive status updates in JSON format:

```json
{
  "pins": [
    {
      "gpio": 5,
      "state": true
    },
    {
      "gpio": 16,
      "state": false
    },
    {
      "gpio": 17,
      "state": false
    },
    {
      "gpio": 18,
      "state": false
    }
  ],
  "deviceId": "ESP32_GPIO_Controller",
  "ipAddress": "192.168.1.100",
  "rssi": -65
}
```

### Monitoring Telemetry

Subscribe to the telemetry topic (default: `esp32/gpio/telemetry`) to receive sensor data and system information:

```json
{
  "deviceId": "ESP32_GPIO_Controller",
  "temperature": 25.4,
  "humidity": 48.2,
  "freeHeap": 240368,
  "uptime": 3600
}
```

## Wiring Example

### Basic GPIO Control

![Basic GPIO Control Wiring](../hardware/basic_gpio_wiring.png)

(Note: Create and add schematics to the hardware directory)

### With DHT22 Sensor

![DHT22 Sensor Wiring](../hardware/dht22_wiring.png)

(Note: Create and add schematics to the hardware directory)

## Troubleshooting

- Check serial monitor output for debugging information (115200 baud)
- Verify WiFi and MQTT credentials in config.h
- Ensure your MQTT broker is accessible from the ESP32's network
- Confirm you're publishing to the correct topics with valid JSON format

## Extending the Firmware

This firmware can be extended with additional features:

- Add support for more sensors
- Implement secure MQTT connections (TLS)
- Add OTA update functionality
- Integrate with specific IoT platforms
- Add support for different actuators

## License

This firmware is released under the MIT License. 