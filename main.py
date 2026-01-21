import os
import json
import uvicorn
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import Response
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configuration
PORT = int(os.getenv("PORT", "8080"))
DOMAIN = os.getenv("NGROK_URL")
WS_URL = f"wss://{DOMAIN}/ws"
MODEL = "gpt-4o-mini" # You can change this to any OpenAI model you prefer
WELCOME_GREETING = "Jace Beleren, at your service. What Magic: The Gathering guidance or knowledge do you seek?"
SYSTEM_PROMPT = "You are a helpful assistant. This conversation is being translated to voice, so answer carefully. When you respond, please spell out all numbers, for example twenty not 20. Do not include emojis in your responses. Do not include bullet points, asterisks, or special symbols. You can include Magic: The Gathering specific references and terminology to make things interesting."

# Initialise OpenAI client
openai = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Store active sessions
sessions = {}

# Create FastAPI app
app = FastAPI()

async def ai_response(messages):
    """Get a response from OpenAI API"""
    completion = openai.chat.completions.create(
        model=MODEL,
        messages=messages
    )
    return completion.choices[0].message.content

@app.post("/twiml")
# You can choose the voice from ElevenLabs here: https://www.twilio.com/docs/voice/conversationrelay/voice-configuration
async def twiml_endpoint():
    """Endpoint that returns TwiML for Twilio to connect to the WebSocket"""
    xml_response = f"""<?xml version="1.0" encoding="UTF-8"?>
    <Response>
      <Connect>
        <ConversationRelay url="{WS_URL}" welcomeGreeting="{WELCOME_GREETING}" ttsProvider="ElevenLabs" voice="EkK5I93UQWFDigLMpZcX" />
      </Connect>
    </Response>"""
    
    return Response(content=xml_response, media_type="text/xml")

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket endpoint for real-time communication"""
    await websocket.accept()
    call_sid = None
    
    try:
        while True:
            data = await websocket.receive_text()
            message = json.loads(data)
            
            if message["type"] == "setup":
                call_sid = message["callSid"]
                print(f"Setup for call: {call_sid}")
                websocket.call_sid = call_sid
                sessions[call_sid] = [{"role": "system", "content": SYSTEM_PROMPT}]
                
            elif message["type"] == "prompt":
                print(f"Processing prompt: {message['voicePrompt']}")
                conversation = sessions[websocket.call_sid]
                conversation.append({"role": "user", "content": message["voicePrompt"]})
                
                try:
                    response = await ai_response(conversation)
                    conversation.append({"role": "assistant", "content": response})
                    
                    await websocket.send_text(
                        json.dumps({
                            "type": "text",
                            "token": response,
                            "last": True
                        })
                    )
                    print(f"Sent response: {response}")
                    
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
                    print(f"Sent error response due to: {e}")
                
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