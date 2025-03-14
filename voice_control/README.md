# Voice Control Module for ESP32 MQTT Controller

This module enables voice command processing for the Smart AI-Based ESP32 Controller project. It captures voice input, processes it using Google's speech recognition and LangChain with Gemini AI, and sends commands to the ESP32 via MQTT.

## Overview

The voice control module follows a pipeline architecture:
1. Capture voice input from microphone
2. Convert speech to text using Google Speech Recognition
3. Process text with LangChain and Google's Gemini model to extract intent and parameters
4. Format and send MQTT commands to control the ESP32
5. Provide feedback to the user

## Features

- **Speech Recognition**: Captures and transcribes voice commands
- **LangChain Integration**: Uses structured output parsing for reliable command extraction
- **MQTT Communication**: Securely communicates with ESP32 using TLS
- **Modular Design**: Well-organized code structure for easy maintenance
- **Simple Command Interface**: Control devices with natural language

## Prerequisites

- Python 3.7+
- Microphone connected to your computer
- Internet connection for speech recognition and Gemini API
- MQTT broker (HiveMQ Cloud account or local broker)
- Google Gemini API key

## Project Structure

```
voice_control/
├── core/                  # Core functionality
│   ├── app.py             # Main application logic
│   ├── llm_processor.py   # LangChain-based LLM processing
│   └── mqtt_client.py     # MQTT client functionality
├── utils/                 # Utility modules
│   └── speech.py          # Speech recognition utilities
├── config/                # Configuration files
│   ├── settings.py        # Configuration settings
│   └── prompts.py         # LangChain prompts
├── main.py                # Entry point
├── requirements.txt       # Python dependencies
└── README.md              # This file
```

## Installation

1. Install required Python packages:
   ```bash
   pip install -r requirements.txt
   ```

2. Create a `.env` file with your API keys and credentials:
   ```
   # Copy from .env.example
   cp .env.example .env
   
   # Edit the file with your actual values
   nano .env
   ```

## Usage

Run the voice control module from the project root directory:

```bash
python -m voice_control.main
```

Or from within the voice_control directory:

```bash
python main.py
```

### Command Line Options

- `--once`: Process a single voice command and exit
- `--verbose`: Enable detailed logging

Example:
```bash
python -m voice_control.main --verbose
```

## Example Commands

Speak commands after the "Listening..." prompt, such as:

| Voice Command | Extracted Intent | MQTT Message |
|---------------|------------------|--------------|
| "Turn on the living room light" | {action: "turn_on", device: "light"} | `{"pin": 5, "state": true}` |
| "Get temperature" | {action: "get_status", sensor: "temperature"} | `{"command": "getStatus"}` |
| "Set fan speed to high" | {action: "set_value", device: "fan", value: "high"} | `{"pin": 16, "value": 255}` |

## How It Works

### 1. Voice Capture (utils/speech.py)
The system uses the `speech_recognition` library to listen for commands through your microphone, with automatic ambient noise adjustment.

### 2. Intent Extraction (core/llm_processor.py)
Using LangChain with Google's Gemini model, the text command is processed through a structured output parser to reliably extract the command intent and parameters.

### 3. MQTT Communication (core/mqtt_client.py)
The extracted command is formatted into an MQTT message and published to the broker, where the ESP32 is subscribed and waiting to execute commands.

### 4. Application Orchestration (core/app.py)
The main application ties everything together, managing the flow from voice input to command execution.

## Customization

- Edit device mappings in `config/settings.py` to match your ESP32 GPIO configuration
- Modify LangChain prompts in `config/prompts.py` to improve command recognition
- Adjust MQTT settings in `config/settings.py` to match your broker

## Troubleshooting

- **Speech not recognized**: Check microphone settings and network connection
- **LLM not responding**: Verify your Gemini API key is correct
- **MQTT connection issues**: Check broker address, port, and credentials
- **ESP32 not responding**: Ensure it's connected to Wi-Fi and subscribed to the correct MQTT topics

## Future Enhancements

- Add offline speech recognition option
- Implement conversation history for context-aware commands
- Add support for custom wake words
- Create a GUI interface for configuration and monitoring

## Related Components

This module works with the ESP32 MQTT GPIO Controller firmware found in the `firmware/` directory of the main project. 