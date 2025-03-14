"""
Main Application for ESP32 Voice Control.

This module orchestrates the voice recognition, LLM processing, and MQTT
communication components to enable voice control of an ESP32.
"""

import logging
import time
from voice_control.utils.speech import SpeechRecognizer
from voice_control.core.llm_processor import LLMProcessor
from voice_control.core.mqtt_client import MQTTClient

# Set up logging
logger = logging.getLogger(__name__)

class VoiceControlApp:
    """Main application for voice controlling ESP32 via MQTT."""
    
    def __init__(self):
        """Initialize the voice control application."""
        logger.info("Initializing Voice Control Application")
        print("\n===== Initializing ESP32 Voice Control =====")
        
        # Initialize components
        try:
            print("Setting up speech recognition...")
            self.speech_recognizer = SpeechRecognizer()
            logger.info("Speech recognition initialized")
            
            print("Setting up LLM processor...")
            self.llm_processor = LLMProcessor()
            logger.info("LLM processor initialized")
            
            print("Setting up MQTT client...")
            self.mqtt_client = MQTTClient()
            logger.info("MQTT client initialized")
            
        except Exception as e:
            logger.error(f"Error initializing components: {e}")
            raise
        
        # Connect to MQTT broker
        if not self.mqtt_client.connect():
            logger.error("Failed to connect to MQTT broker")
            raise ConnectionError("Could not connect to MQTT broker")
            
        logger.info("Voice Control Application initialized successfully")
        print("===== ESP32 Voice Control Ready =====\n")
        
    def run_once(self):
        """
        Process a single voice command.
        
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # 1. Listen for voice command
            voice_command = self.speech_recognizer.listen()
            if not voice_command:
                logger.info("No voice command detected")
                return False
                
            # 2. Process command with LLM
            command_data = self.llm_processor.process_command(voice_command)
            if not command_data:
                logger.warning("Failed to process command with LLM")
                print("Sorry, I couldn't understand the command. Please try again.")
                return False
                
            # Print the extracted command
            pin = command_data.get('pin')
            state = command_data.get('state')
            
            device_name = self._get_device_name(pin)
            state_text = "ON" if state else "OFF"
            
            print(f"Command understood: Turn {state_text} {device_name} (Pin {pin})")
            
            # 3. Publish to MQTT
            if self.mqtt_client.publish_command(command_data):
                logger.info("Command published successfully")
                return True
            else:
                logger.warning("Failed to publish command to MQTT broker")
                return False
                
        except Exception as e:
            logger.error(f"Error processing voice command: {e}")
            print(f"An error occurred: {e}")
            return False
    
    def _get_device_name(self, pin):
        """Helper method to get device name from pin number."""
        from voice_control.config.settings import DEVICE_MAPPINGS
        
        # Create reverse mapping
        pin_to_device = {v: k for k, v in DEVICE_MAPPINGS.items()}
        
        return pin_to_device.get(pin, f"Pin {pin}")
    
    def run_continuous(self):
        """Run the voice control application continuously."""
        print("\n===== ESP32 Voice Control Started =====")
        print("Say a command to control your ESP32...")
        print("Press Ctrl+C to exit\n")
        
        try:
            while True:
                self.run_once()
                time.sleep(2)  # Increased pause between command attempts from 1 to 2 seconds
                
        except KeyboardInterrupt:
            logger.info("User interrupted execution")
            print("\nExiting Voice Control Application...")
            
        finally:
            # Clean up
            self.cleanup()
    
    def cleanup(self):
        """Clean up resources."""
        try:
            self.mqtt_client.disconnect()
            logger.info("Resources cleaned up")
            print("Resources cleaned up successfully.")
        except Exception as e:
            logger.error(f"Error during cleanup: {e}")
            print(f"Error during cleanup: {e}") 