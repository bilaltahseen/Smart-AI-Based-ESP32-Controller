"""
LangChain prompts for the voice control system.

This file contains structured prompt templates for LangChain to process
voice commands and extract structured information.
"""

from langchain.prompts import PromptTemplate
from langchain.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field
from typing import Optional, Union

# Define the simplified command schema
class Command(BaseModel):
    """Simplified schema for ESP32 MQTT commands."""
    pin: int = Field(
        description="The GPIO pin number to control (e.g., 5 for light, 16 for fan, 17 for heater, 18 for door)"
    )
    state: bool = Field(
        description="Whether to turn the pin ON (true) or OFF (false)"
    )

# Create the output parser
command_parser = PydanticOutputParser(pydantic_object=Command)

# Create the prompt template
COMMAND_EXTRACTION_TEMPLATE = PromptTemplate(
    template="""
You are an intelligent voice assistant that controls IoT devices via an ESP32 microcontroller.
Your task is to analyze voice commands and translate them into the exact pin control format for an MQTT message.

Device to GPIO pin mapping:
- light: pin 5
- fan: pin 15
- heater: pin 17
- door: pin 18

Parse the following voice command and extract the pin number and desired state:

Voice command: "{command}"

{format_instructions}

Examples:
Voice command: "Turn on the light"
Output: {{"pin": 5, "state": true}}

Voice command: "Turn off the fan"
Output: {{"pin": 15, "state": false}}

Voice command: "Switch on the heater"
Output: {{"pin": 17, "state": true}}

Voice command: "Close the door" (closing means turning off)
Output: {{"pin": 18, "state": false}}

Voice command: "Open the door" (opening means turning on)
Output: {{"pin": 18, "state": true}}

Voice command: "Turn off pin 5"
Output: {{"pin": 5, "state": false}}
""",
    input_variables=["command"],
    partial_variables={"format_instructions": command_parser.get_format_instructions()}
)

def get_command_extraction_prompt(voice_command):
    """Create a prompt with the given voice command."""
    return COMMAND_EXTRACTION_TEMPLATE.format(command=voice_command) 