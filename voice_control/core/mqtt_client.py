"""
MQTT Client for ESP32 Voice Control.

This module handles MQTT communication with the ESP32 device,
including connecting to the broker and publishing control messages.
"""

import json
import logging
import random
import time
import ssl
import paho.mqtt.client as mqtt
from voice_control.config.settings import (
    MQTT_BROKER, MQTT_PORT, MQTT_USERNAME, MQTT_PASSWORD, 
    MQTT_CLIENT_ID, MQTT_USE_TLS, MQTT_TOPIC_CONTROL,
    DEVICE_MAPPINGS, VALUE_MAPPINGS
)

# Set up logging
logger = logging.getLogger(__name__)

class MQTTClient:
    """Handles MQTT communication with the ESP32."""
    
    def __init__(
        self, 
        broker=MQTT_BROKER, 
        port=MQTT_PORT, 
        username=MQTT_USERNAME, 
        password=MQTT_PASSWORD,
        client_id=None,
        use_tls=MQTT_USE_TLS
    ):
        """
        Initialize the MQTT client.
        
        Args:
            broker (str): MQTT broker address
            port (int): MQTT broker port
            username (str): MQTT username
            password (str): MQTT password
            client_id (str): Client ID (generated if None)
            use_tls (bool): Whether to use TLS encryption
        """
        # Generate a unique client ID if none provided
        if client_id is None:
            client_id = f"{MQTT_CLIENT_ID}-{random.randint(1000, 9999)}"
        
        self.broker = broker
        self.port = port
        self.username = username
        self.password = password
        self.client_id = client_id
        self.use_tls = use_tls
        
        # Create MQTT client instance
        self.client = mqtt.Client(client_id=self.client_id)
        
        # Set username and password if provided
        if username and password:
            self.client.username_pw_set(username, password)
        
        # Configure TLS if enabled
        if use_tls:
            self.client.tls_set(cert_reqs=ssl.CERT_REQUIRED, tls_version=ssl.PROTOCOL_TLS)
            self.client.tls_insecure_set(True)  # For development only
        
        # Set callback handlers
        self.client.on_connect = self._on_connect
        self.client.on_disconnect = self._on_disconnect
        self.client.on_publish = self._on_publish
        
        self.connected = False
    
    def connect(self):
        """
        Connect to the MQTT broker.
        
        Returns:
            bool: True if connected successfully, False otherwise
        """
        try:
            logger.info(f"Connecting to MQTT broker at {self.broker}:{self.port}")
            print(f"Connecting to MQTT broker at {self.broker}...")
            
            self.client.connect(self.broker, self.port, keepalive=60)
            self.client.loop_start()
            
            # Wait for connection to establish
            timeout = 10  # seconds
            start_time = time.time()
            while not self.connected and time.time() - start_time < timeout:
                time.sleep(0.1)
            
            if not self.connected:
                logger.error("Failed to connect to MQTT broker (timeout)")
                print("Failed to connect to MQTT broker (timeout)")
                return False
                
            print("Connected to MQTT broker successfully.")
            return True
            
        except Exception as e:
            logger.error(f"Error connecting to MQTT broker: {e}")
            print(f"Error connecting to MQTT broker: {e}")
            return False
    
    def disconnect(self):
        """Disconnect from the MQTT broker."""
        self.client.loop_stop()
        self.client.disconnect()
        logger.info("Disconnected from MQTT broker")
    
    def publish_command(self, command_data):
        """
        Publish a command to the ESP32.
        
        Args:
            command_data (dict): Command data from the LLM
            
        Returns:
            bool: True if published successfully, False otherwise
        """
        try:
            # The command data already has the correct format: {"pin": X, "state": boolean}
            # Just convert to JSON
            payload = json.dumps(command_data)
            
            # Publish to the control topic
            logger.info(f"Publishing to {MQTT_TOPIC_CONTROL}: {payload}")
            print(f"Sending command: {command_data}")
            
            result = self.client.publish(MQTT_TOPIC_CONTROL, payload, qos=1)
            
            # Check if publish was successful
            if result.rc != mqtt.MQTT_ERR_SUCCESS:
                logger.error(f"Failed to publish message: {mqtt.error_string(result.rc)}")
                print("Failed to send command.")
                return False
                
            print("Command sent successfully.")
            return True
            
        except Exception as e:
            logger.error(f"Error publishing command: {e}")
            print(f"Error sending command: {e}")
            return False
    
    def _on_connect(self, client, userdata, flags, rc):
        """Callback for when the client connects to the broker."""
        if rc == 0:
            logger.info("Connected to MQTT broker")
            self.connected = True
        else:
            logger.error(f"Failed to connect to MQTT broker: {mqtt.connack_string(rc)}")
            self.connected = False
    
    def _on_disconnect(self, client, userdata, rc):
        """Callback for when the client disconnects from the broker."""
        if rc != 0:
            logger.warning(f"Unexpected disconnection from MQTT broker: {rc}")
        else:
            logger.info("Disconnected from MQTT broker")
        self.connected = False
    
    def _on_publish(self, client, userdata, mid):
        """Callback for when a message is published."""
        logger.debug(f"Message {mid} published") 