"""
Run both the HTTP and WebSocket servers for the MTG Chatbot
"""
import asyncio
import subprocess
import sys
import os
import signal
from dotenv import load_dotenv

load_dotenv()

def run_http_server():
    """Run the FastAPI HTTP server"""
    port = os.getenv("HTTP_PORT", 8000)
    cmd = [
        sys.executable, "-m", "uvicorn", 
        "main:app", 
        "--host", "0.0.0.0", 
        "--port", str(port),
        "--reload"
    ]
    return subprocess.Popen(cmd)

def run_websocket_server():
    """Run the WebSocket server"""
    cmd = [sys.executable, "websocket_server.py"]
    return subprocess.Popen(cmd)

def main():
    """Start both servers"""
    print("🎲 Starting MTG Chatbot servers...")
    
    # Start HTTP server
    print(f"🌐 Starting HTTP server on port {os.getenv('HTTP_PORT', 8000)}...")
    http_process = run_http_server()
    
    # Start WebSocket server  
    print(f"🔌 Starting WebSocket server on port {os.getenv('WEBSOCKET_PORT', 8001)}...")
    ws_process = run_websocket_server()
    
    print("\n✅ Both servers are running!")
    print(f"📱 HTTP Server: http://localhost:{os.getenv('HTTP_PORT', 8000)}")
    print(f"🔗 WebSocket Server: ws://localhost:{os.getenv('WEBSOCKET_PORT', 8001)}")
    print(f"🎯 TwiML Endpoint: http://localhost:{os.getenv('HTTP_PORT', 8000)}/voice")
    print("\n💡 Configure your Twilio phone number to point to the TwiML endpoint")
    print("⚡ Press Ctrl+C to stop both servers")
    
    try:
        # Wait for keyboard interrupt
        while True:
            asyncio.run(asyncio.sleep(1))
    except KeyboardInterrupt:
        print("\n🛑 Shutting down servers...")
        http_process.terminate()
        ws_process.terminate()
        
        # Wait for processes to finish
        http_process.wait()
        ws_process.wait()
        
        print("✅ Servers stopped successfully!")

if __name__ == "__main__":
    main()