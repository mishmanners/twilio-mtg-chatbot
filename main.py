import os
import json
import uvicorn
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Form
from fastapi.responses import Response
from openai import OpenAI
from dotenv import load_dotenv
from fastapi import Request
import inspect

# Load environment variables from .env file
load_dotenv()

# Configuration
PORT = int(os.getenv("PORT", "8080"))
DOMAIN = "a222b0333acd.ngrok.app"  # Replace with your actual domain, no https://
WS_URL = f"wss://{DOMAIN}/ws"
MODEL = "gpt-4o-mini"
WELCOME_GREETING = "Jace Beleren, at your service. What Magic The Gathering guidance or knowledge do you seek?"
SYSTEM_PROMPT = "Your name is Jace Beleren, you are a human planeswalker who is intelligent, curious, and specialises in magic , telepathy, clairvoyance, and illusion, and thus you should respond to questions in this manner. You are here to be a helpful assistant to the human Magic The Gathering players. This conversation is being translated to voice, so answer carefully. When you respond, please spell out all numbers, for example twenty not 20. Do not include emojis in your responses. Do not include bullet points, asterisks, or special symbols. You can include Magic The Gathering specific references and terminology to make things interesting, and highlight your knowledge of the game and personality. Keep your responses concise and to the point. Ignore the semi-colon in Magic: The Gathering, and just say Magic The Gathering. Once you've said Magic the Gathering once in the conversation, you can refer to it as Magic. You can also include some flavour text or quotes from the game to make things more engaging."

# Initialise OpenAI client so we can tap into the multiverse of knowledge
openai = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Store active sessions to keep track of the conversation
sessions = {}

# Create FastAPI app, this is where the interactions happen
app = FastAPI()

async def ai_response(messages):
    """Get a response from OpenAI API"""
    completion = openai.chat.completions.create(
        model=MODEL,
        messages=messages
    )
    return completion.choices[0].message.content


# You can choose the voice from ElevenLabs here: https://www.twilio.com/docs/voice/conversationrelay/voice-configuration
@app.post("/twiml") # Twilio calls this endpoint to get TwiML instructions (XML) that tells Twilio to connect to the WebSocket
async def twiml_endpoint(request: Request):
        
        # parse Host header from the request to construct WS_URL dynamically
        host = request.headers.get("host")

        """Endpoint that returns TwiML for Twilio to connect to the WebSocket. Accepts form data from Twilio."""
        xml_response = f"""<?xml version="1.0" encoding="UTF-8"?>
        <Response>
            <Connect>
                <ConversationRelay url="wss://{host}/ws" welcomeGreeting="{WELCOME_GREETING}" ttsProvider="ElevenLabs" voice="EkK5I93UQWFDigLMpZcX" />
            </Connect>

        </Response>"""
        return Response(content=xml_response, media_type="text/xml")

@app.websocket("/ws") # This is where the magic happens, handling real-time communication
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket endpoint for real-time communication"""
    await websocket.accept() # Accept the WebSocket connection
    call_sid = None
    
    try:
        while True:
            data = await websocket.receive_text()
            message = json.loads(data)
            
            if message["type"] == "setup": # New session created for the caller
                call_sid = message["callSid"]
                print(f"Setup for call: {call_sid}")
                websocket.call_sid = call_sid
                sessions[call_sid] = [{"role": "system", "content": SYSTEM_PROMPT}]
                
            elif message["type"] == "prompt":
                print(f"Processing prompt: {message['voicePrompt']}") # The user's voice input is added to the conversation
                conversation = sessions[websocket.call_sid]
                conversation.append({"role": "user", "content": message["voicePrompt"]})
                
                try:
                    response = await ai_response(conversation) # The AI responds with knowledge, flavor, and quotes
                    conversation.append({"role": "assistant", "content": response})
                    
                    await websocket.send_text( # Sending the answer back through the WebSocket
                        json.dumps({
                            "type": "text",
                            "token": response,
                            "last": True
                        })
                    )
                    print(f"Sent response: {response}") # Log the response sent back to the user
                    
                except Exception as e:
                    print(f"Error getting AI response: {e}")
                    error_response = "Our connection to the Blind Eternities has been disrupted. I can’t reach the knowledge you seek right now. Try again soon."
                    
                    await websocket.send_text(
                        json.dumps({
                            "type": "text", 
                            "token": error_response,
                            "last": True
                        })
                    )
                    print(f"Sent error response due to: {e}") # Log the error response sent back to the user
                
            elif message["type"] == "interrupt":
                print("Handling interruption.")
                
            else:
                print(f"Unknown message type received: {message['type']}") 
                
    except WebSocketDisconnect:
        print("WebSocket connection closed")
        if call_sid:
            sessions.pop(call_sid, None)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=PORT)
    print(f"Server running at http://localhost:{PORT} and {WS_URL}")