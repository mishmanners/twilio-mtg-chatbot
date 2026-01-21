"""
Main HTTP server for serving TwiML responses for the MTG Chatbot
"""
import os
from fastapi import FastAPI, Request, Form
from fastapi.responses import Response
from dotenv import load_dotenv
import uvicorn

# Load environment variables
load_dotenv()

app = FastAPI(title="MTG Chatbot - TwiML Server")

@app.post("/voice")
async def handle_voice_call(request: Request):
    """
    Handle incoming voice calls and return TwiML with ConversationRelay
    """
    # Get the WebSocket URL for ConversationRelay
    websocket_url = f"wss://{os.getenv('HOST', 'localhost')}:{os.getenv('WEBSOCKET_PORT', '8001')}/websocket"
    
    twiml = f"""<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Connect action="/connect_action">
        <ConversationRelay 
            url="{websocket_url}" 
            welcomeGreeting="Hello! I'm your Magic: The Gathering assistant. Ask me about cards, mechanics, rules, or strategies!" 
            voice="alice"
            dtmfDetection="true"
            debug="true" />
    </Connect>
</Response>"""
    
    return Response(content=twiml, media_type="application/xml")

@app.post("/connect_action")
async def handle_connect_action(request: Request):
    """
    Handle the action callback after ConversationRelay ends
    """
    form_data = await request.form()
    print(f"Connect action callback: {dict(form_data)}")
    
    # You can handle different scenarios here based on handoffData
    twiml = """<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Say>Thanks for using the Magic: The Gathering assistant! Goodbye!</Say>
</Response>"""
    
    return Response(content=twiml, media_type="application/xml")

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "mtg-chatbot-twiml"}

if __name__ == "__main__":
    port = int(os.getenv("HTTP_PORT", 8000))
    uvicorn.run(
        "main:app", 
        host="0.0.0.0", 
        port=port, 
        reload=True,
        log_level="info"
    )