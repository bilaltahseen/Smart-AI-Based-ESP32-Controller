#!/usr/bin/env python3
"""
ESP32 Voice Control with LangChain and MQTT.

This is the main entry point for the voice control application.
It sets up logging and provides command-line options for running
the application in different modes.
"""

import os
import sys
import logging
import argparse
from dotenv import load_dotenv

# Add the parent directory to sys.path for package imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('voice_control.log')
    ]
)
logger = logging.getLogger(__name__)

def main():
    """Main entry point for the application."""
    # Load environment variables
    load_dotenv()
    
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description='ESP32 Voice Control via MQTT with LangChain')
    parser.add_argument('--once', action='store_true', help='Process a single command and exit')
    parser.add_argument('--verbose', action='store_true', help='Enable verbose logging')
    args = parser.parse_args()
    
    # Adjust logging level if requested
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
        logger.debug("Verbose logging enabled")
    
    # Import here to avoid circular imports
    from voice_control.core.app import VoiceControlApp
    
    try:
        # Create and run the application
        app = VoiceControlApp()
        
        if args.once:
            # Process a single command
            app.run_once()
        else:
            # Run continuously until interrupted
            app.run_continuous()
            
    except KeyboardInterrupt:
        logger.info("Application interrupted by user")
        print("\nExiting...")
        
    except Exception as e:
        logger.error(f"Application error: {e}")
        print(f"Error: {e}")
        return 1
        
    return 0

if __name__ == "__main__":
    sys.exit(main()) 