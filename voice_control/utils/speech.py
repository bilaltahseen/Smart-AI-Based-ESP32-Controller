"""
Speech Recognition utilities for ESP32 Voice Control.

This module handles capturing audio from the microphone and
converting it to text using Google's speech recognition service.
"""

import speech_recognition as sr
import logging
from voice_control.config.settings import (
    RECOGNITION_LANGUAGE,
    RECOGNITION_TIMEOUT,
    RECOGNITION_PHRASE_TIMEOUT
)

# Set up logging
logger = logging.getLogger(__name__)

class SpeechRecognizer:
    """Handles speech recognition from microphone input."""
    
    def __init__(
        self, 
        language=RECOGNITION_LANGUAGE, 
        timeout=RECOGNITION_TIMEOUT, 
        phrase_timeout=RECOGNITION_PHRASE_TIMEOUT
    ):
        """
        Initialize the speech recognizer.
        
        Args:
            language (str): Language code for recognition
            timeout (int): How long to listen for a command in seconds
            phrase_timeout (float): Seconds of silence to mark end of phrase
        """
        self.recognizer = sr.Recognizer()
        self.language = language
        self.timeout = timeout
        self.phrase_timeout = phrase_timeout
        
        # Adjust for ambient noise when created
        try:
            with sr.Microphone() as source:
                logger.info("Adjusting for ambient noise. Please wait...")
                print("Calibrating microphone for ambient noise... Please wait.")
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
                logger.info("Ambient noise profile created")
                print("Microphone calibrated.")
        except Exception as e:
            logger.error(f"Error initializing microphone: {e}")
            print(f"Error initializing microphone: {e}")
            print("Make sure you have a working microphone connected.")
            raise
    
    def listen(self):
        """
        Listen for speech and convert to text.
        
        Returns:
            str or None: Recognized text or None if recognition failed
        """
        try:
            with sr.Microphone() as source:
                logger.info("Listening for command...")
                print("Listening... (speak now)")
                
                # Listen for audio with timeout
                audio = self.recognizer.listen(
                    source,
                    timeout=self.timeout,
                    phrase_time_limit=self.phrase_timeout
                )
                
                logger.info("Audio captured, recognizing...")
                print("Processing...")
                
                # Use Google's speech recognition
                text = self.recognizer.recognize_google(
                    audio,
                    language=self.language
                )
                
                logger.info(f"Recognized: {text}")
                print(f"You said: {text}")
                return text
                
        except sr.WaitTimeoutError:
            logger.warning("No speech detected within timeout period")
            print("No speech detected. Please try again.")
            
        except sr.UnknownValueError:
            logger.warning("Could not understand audio")
            print("Sorry, I couldn't understand that. Please try again.")
            
        except sr.RequestError as e:
            logger.error(f"Recognition service error: {e}")
            print("Speech recognition service unavailable. Check your internet connection.")
            
        except Exception as e:
            logger.error(f"Unexpected error in speech recognition: {e}")
            print(f"An error occurred: {e}")
            
        return None 