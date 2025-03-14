# Smart AI-Based ESP32 Controller

A cutting-edge IoT project that combines the power of ESP32 microcontrollers with artificial intelligence to create an intelligent control system.

## Overview

This Smart AI-Based ESP32 Controller project integrates IoT capabilities with AI algorithms to create a versatile and intelligent control system. The ESP32 microcontroller serves as the hardware foundation, offering built-in Wi-Fi and Bluetooth connectivity, while the AI components enable advanced features like pattern recognition, predictive analytics, and autonomous decision-making.

## Features

- **Real-time Data Processing**: Collect and analyze sensor data in real-time
- **AI-Powered Decision Making**: Utilize machine learning algorithms for intelligent control
- **Remote Monitoring & Control**: Access your system from anywhere via web or mobile interfaces
- **Voice Command Support**: Control your devices using natural language
- **Customizable Automation Rules**: Create personalized automation workflows
- **Energy Efficiency Optimization**: AI-driven power management for extended battery life
- **OTA Updates**: Over-the-air firmware updates for seamless maintenance
- **Local and Cloud Processing**: Edge computing with cloud backup for complex tasks
- **Expandable System**: Support for adding multiple sensors and actuators

## Hardware Requirements

- ESP32 Development Board
- Power supply (USB or battery)
- Sensors (based on your specific use case):
  - Temperature/humidity sensors
  - Motion sensors
  - Light sensors
  - Sound sensors
  - etc.
- Actuators (based on your specific use case):
  - Relays
  - Motors
  - LEDs
  - Servos
  - etc.
- Breadboard and jumper wires for prototyping
- Microphone (for voice control)

## Software Requirements

- Arduino IDE or PlatformIO
- ESP32 Board Support Package
- Required Libraries:
  - WiFi, Bluetooth libraries
  - MQTT client
  - TensorFlow Lite for microcontrollers
  - Sensor-specific libraries
  - Web server libraries
- Python 3.7+ (for voice control)
- Google Gemini API key (for voice control)
- Backend server (optional, for advanced features)
- Mobile app or web interface (for remote control)

## Getting Started

### Installation

1. Clone this repository:
   ```
   git clone https://github.com/bilaltahseen/smart-ai-esp32-controller.git
   cd smart-ai-esp32-controller
   ```

2. Install the required software dependencies (see Software Requirements)

3. Configure your hardware setup according to the provided schematics

4. Upload the firmware to your ESP32 board:
   - See the `firmware/` directory for ESP32 code
   - Configure WiFi and MQTT settings in `firmware/ESP32_MQTT_GPIO_Controller/config.h`

5. Set up voice control (optional):
   - Go to the voice control directory: `cd voice_control`
   - Install Python dependencies: `pip install -r requirements.txt`
   - Copy `.env.example` to `.env` and fill in your API keys
   - Run the voice control application: `python voice_control.py`

### Configuration

Modify the `firmware/ESP32_MQTT_GPIO_Controller/config.h` file to customize your ESP32 setup:

```cpp
// Network settings
#define WIFI_SSID "your_wifi_ssid"
#define WIFI_PASSWORD "your_wifi_password"

// MQTT broker settings
#define MQTT_BROKER "mqtt_broker_address"
#define MQTT_PORT 8883

// Sensor pins
#define TEMP_SENSOR_PIN 4
// Add more pins as needed
```

For voice control configuration, edit `voice_control/config.py` to customize device mappings and commands.

## Project Structure

```
├── firmware/               # ESP32 firmware code
│   ├── ESP32_MQTT_GPIO_Controller/  # Main MQTT controller firmware
│   └── other_firmware/     # Additional firmware options
├── hardware/               # Hardware design files and schematics
├── tools/                  # Utility scripts and tools
├── voice_control/          # Voice control component
│   ├── voice_control.py    # Main voice control application
│   ├── speech_recognition_module.py  # Speech recognition
│   ├── gemini_module.py    # Gemini AI integration
│   ├── mqtt_module.py      # MQTT client
│   └── config.py           # Configuration settings
└── docs/                   # Documentation
```

## Voice Control

The voice control module lets you command your ESP32 using natural language. It works by:

1. Capturing voice input through your computer's microphone
2. Converting speech to text using Google's speech recognition
3. Processing the text with Google's Gemini AI to understand your intent
4. Sending the appropriate command to the ESP32 via MQTT

Example voice commands include:
- "Turn on the light"
- "Turn off the fan"
- "Set the heater to high"
- "What's the current temperature?"

For detailed instructions, see the [Voice Control README](voice_control/README.md).

## Usage Examples

### Basic Sensor Reading

```cpp
void readSensors() {
  float temperature = readTemperature();
  float humidity = readHumidity();
  
  Serial.printf("Temperature: %.2f°C, Humidity: %.2f%%\n", temperature, humidity);
  
  // Process with AI model
  float prediction = aiModel.predict(temperature, humidity);
  
  // Take action based on prediction
  if (prediction > THRESHOLD) {
    activateActuator();
  }
}
```

### Setting Up Automation Rules

Through the web interface, you can create rules like:
- "If temperature exceeds 30°C AND humidity is below 40%, turn on the humidifier"
- "If motion is detected AND time is between 10 PM and 6 AM, turn on lights at 30% brightness"

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgements

- [ESP32 Community](https://esp32.com/)
- [TensorFlow Lite for Microcontrollers](https://www.tensorflow.org/lite/microcontrollers)
- [Google Gemini API](https://ai.google.dev/)
- [HiveMQ MQTT Broker](https://www.hivemq.com/)
- [Contributors and supporters of this project](#) 