"""
Configuration settings for the Voice Control Module.

This file contains all configurable parameters for the voice control system,
including API keys, MQTT broker details, and device mappings.
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Google Gemini API settings
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
GEMINI_MODEL = "gemini-1.5-flash"  # Using the text-only model for our use case

# MQTT Broker settings (defaults to HiveMQ broker from the ESP32 project)
MQTT_BROKER = os.getenv("MQTT_BROKER", "<your_mqtt_broker>")
MQTT_PORT = int(os.getenv("MQTT_PORT", 8883))
MQTT_USERNAME = os.getenv("MQTT_USERNAME", "<your_mqtt_username>")
MQTT_PASSWORD = os.getenv("MQTT_PASSWORD", "<your_mqtt_password>")
MQTT_CLIENT_ID = "voice_control_client"
MQTT_USE_TLS = True

# MQTT Topics
MQTT_TOPIC_CONTROL = "esp32/gpio/control"
MQTT_TOPIC_STATUS = "esp32/gpio/status"
MQTT_TOPIC_TELEMETRY = "esp32/gpio/telemetry"

# Voice Recognition settings
RECOGNITION_LANGUAGE = "en-US"  # Language for speech recognition
RECOGNITION_TIMEOUT = 10  # Maximum time to listen for a command (seconds)
RECOGNITION_PHRASE_TIMEOUT = 3.0  # Timeout for end of phrase detection

# Device to GPIO pin mappings
DEVICE_MAPPINGS = {
    "light": 5,
    "fan": 15, 
    "heater": 17,
    "door": 18
}

# Value mappings for devices with variable settings
VALUE_MAPPINGS = {
    "low": 64,
    "medium": 128,
    "high": 255
}

# Feedback settings
VOICE_FEEDBACK = True  # Whether to provide voice feedback
TEXT_FEEDBACK = True  # Whether to provide text feedback 