"""
LLM Processor for Voice Control.

This module handles the LangChain integration with Google Gemini to extract
intent and parameters from voice commands.
"""

import logging
from langchain_google_genai import ChatGoogleGenerativeAI
from voice_control.config.settings import GEMINI_API_KEY, GEMINI_MODEL
from voice_control.config.prompts import get_command_extraction_prompt, command_parser

# Set up logging
logger = logging.getLogger(__name__)

class LLMProcessor:
    """Processes text commands using LangChain and Google's Gemini model."""
    
    def __init__(self, api_key=GEMINI_API_KEY, model_name=GEMINI_MODEL):
        """
        Initialize the LLM processor with LangChain.
        
        Args:
            api_key (str): Google Gemini API key
            model_name (str): Gemini model to use
        """
        if not api_key:
            raise ValueError("Gemini API key is required. Set it in .env file or as an environment variable.")
            
        try:
            # Initialize the LangChain LLM
            self.llm = ChatGoogleGenerativeAI(
                model=model_name,
                google_api_key=api_key,
                temperature=0.1,  # Low temperature for more deterministic outputs
                convert_system_message_to_human=True
            )
            logger.info(f"Initialized LangChain with {model_name}")
            
        except Exception as e:
            logger.error(f"Error initializing LangChain: {e}")
            raise
    
    def process_command(self, text_command):
        """
        Process a text command through LangChain to extract intent.
        
        Args:
            text_command (str): The text command to process
            
        Returns:
            dict or None: Structured command data or None if processing failed
        """
        if not text_command:
            logger.warning("Empty command received")
            return None
        
        try:
            # Get the formatted prompt
            prompt = get_command_extraction_prompt(text_command)
            
            # Generate a response using LangChain
            logger.info(f"Sending command to LangChain: {text_command}")
            response = self.llm.invoke(prompt)
            response_text = response.content
            
            logger.info(f"LLM response: {response_text}")
            
            # Parse the response into a structured format
            try:
                # Extract JSON from response if needed
                if "```json" in response_text:
                    json_text = response_text.split("```json")[1].split("```")[0].strip()
                elif "```" in response_text:
                    json_text = response_text.split("```")[1].strip()
                else:
                    json_text = response_text.strip()
                
                # Parse using the Pydantic parser
                command_data = command_parser.parse(json_text)
                logger.info(f"Parsed command: {command_data.dict()}")
                
                # Validate that we have the required fields
                if command_data.pin is None:
                    logger.error("Missing required pin number in command")
                    print("Error: I need a specific pin number to control.")
                    return None
                
                # Convert Pydantic model to dict
                return command_data.dict()
                
            except Exception as e:
                logger.error(f"Failed to parse LLM response: {e}")
                print(f"Error processing command: Invalid response format")
                return None
                
        except Exception as e:
            logger.error(f"Error processing command with LLM: {e}")
            print(f"Error processing command: {e}")
            return None 