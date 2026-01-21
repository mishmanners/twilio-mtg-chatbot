"""
WebSocket server for handling Twilio ConversationRelay messages
"""
import asyncio
import json
import logging
import os
import hmac
import hashlib
import base64
from urllib.parse import urlparse, parse_qs
import websockets
from websockets.server import serve
from dotenv import load_dotenv
from mtg_knowledge import MTGKnowledge

# Load environment variables
load_dotenv()

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ConversationRelayHandler:
    def __init__(self):
        self.mtg_knowledge = MTGKnowledge()
        self.auth_token = os.getenv("TWILIO_AUTH_TOKEN")
    
    def validate_signature(self, signature, url, body=""):
        """Validate Twilio signature for security"""
        if not self.auth_token or not signature:
            return False
            
        expected_signature = base64.b64encode(
            hmac.new(
                self.auth_token.encode('utf-8'),
                (url + body).encode('utf-8'),
                hashlib.sha1
            ).digest()
        ).decode()
        
        return hmac.compare_digest(signature, expected_signature)
    
    async def handle_websocket(self, websocket, path):
        """Handle WebSocket connections from Twilio ConversationRelay"""
        logger.info(f"New WebSocket connection from {websocket.remote_address}")
        
        # Validate signature from headers
        signature = websocket.request_headers.get('X-Twilio-Signature')
        if signature and not self.validate_signature(signature, f"wss://{websocket.host}{path}"):
            logger.warning("Invalid Twilio signature")
            await websocket.close(code=1008, reason="Invalid signature")
            return
        
        try:
            async for message in websocket:
                await self.handle_message(websocket, message)
        except websockets.exceptions.ConnectionClosed:
            logger.info("WebSocket connection closed")
        except Exception as e:
            logger.error(f"Error handling WebSocket: {e}")
    
    async def handle_message(self, websocket, message):
        """Process incoming messages from Twilio"""
        try:
            data = json.loads(message)
            message_type = data.get('type')
            
            logger.info(f"Received message type: {message_type}")
            
            if message_type == 'setup':
                await self.handle_setup(websocket, data)
            elif message_type == 'prompt':
                await self.handle_prompt(websocket, data)
            elif message_type == 'interrupt':
                await self.handle_interrupt(websocket, data)
            elif message_type == 'dtmf':
                await self.handle_dtmf(websocket, data)
            elif message_type == 'error':
                await self.handle_error(websocket, data)
            else:
                logger.warning(f"Unknown message type: {message_type}")
                
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse JSON message: {e}")
        except Exception as e:
            logger.error(f"Error handling message: {e}")
    
    async def handle_setup(self, websocket, data):
        """Handle setup message from Twilio"""
        session_id = data.get('sessionId')
        caller = data.get('from')
        logger.info(f"Setup session {session_id} for caller {caller}")
        
        # Store session info if needed
        # You could store this in a database or memory for session tracking
    
    async def handle_prompt(self, websocket, data):
        """Handle voice prompt (user speech) from caller"""
        voice_prompt = data.get('voicePrompt', '').strip()
        is_last = data.get('last', True)
        
        if not voice_prompt:
            return
            
        logger.info(f"User said: {voice_prompt}")
        
        # Get response from MTG knowledge base
        response = await self.mtg_knowledge.get_response(voice_prompt)
        
        # Send response back to caller
        await self.send_text_response(websocket, response)
    
    async def handle_interrupt(self, websocket, data):
        """Handle interruption from caller"""
        logger.info("Caller interrupted")
        # You might want to stop current response and prepare for new input
    
    async def handle_dtmf(self, websocket, data):
        """Handle DTMF key press"""
        digit = data.get('digit')
        logger.info(f"Caller pressed: {digit}")
        
        # You could implement menu navigation here
        if digit == '1':
            await self.send_text_response(websocket, "You pressed 1. Let me help you with card rules.")
        elif digit == '2':
            await self.send_text_response(websocket, "You pressed 2. I can explain game mechanics.")
        elif digit == '0':
            await self.send_text_response(websocket, "Thanks for using the MTG assistant. Have a great day!")
            await self.end_session(websocket)
    
    async def handle_error(self, websocket, data):
        """Handle error message from Twilio"""
        error_description = data.get('description')
        logger.error(f"Twilio error: {error_description}")
    
    async def send_text_response(self, websocket, text):
        """Send text response to be converted to speech"""
        # Split long responses into chunks for better streaming
        words = text.split()
        chunk_size = 10  # Send ~10 words at a time
        
        for i in range(0, len(words), chunk_size):
            chunk = ' '.join(words[i:i+chunk_size])
            is_last = i + chunk_size >= len(words)
            
            message = {
                "type": "text",
                "token": chunk + (" " if not is_last else ""),
                "last": is_last,
                "interruptible": True,
                "preemptible": False
            }
            
            await websocket.send(json.dumps(message))
            # Small delay for natural speech pacing
            if not is_last:
                await asyncio.sleep(0.1)
    
    async def end_session(self, websocket):
        """End the conversation session"""
        message = {
            "type": "end",
            "handoffData": json.dumps({"reason": "session_ended"})
        }
        await websocket.send(json.dumps(message))

async def main():
    """Start the WebSocket server"""
    handler = ConversationRelayHandler()
    port = int(os.getenv("WEBSOCKET_PORT", 8001))
    
    logger.info(f"Starting WebSocket server on port {port}")
    
    async with serve(
        handler.handle_websocket,
        "0.0.0.0",
        port,
        ping_interval=20,
        ping_timeout=10
    ):
        logger.info(f"WebSocket server running on ws://localhost:{port}/websocket")
        await asyncio.Future()  # Run forever

if __name__ == "__main__":
    asyncio.run(main())