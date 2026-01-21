"""
Setup script to help configure the MTG Chatbot
"""
import os
import shutil
import subprocess
import sys

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        return False
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} detected")
    return True

def setup_environment():
    """Set up environment file"""
    if not os.path.exists('.env'):
        if os.path.exists('.env.example'):
            shutil.copy('.env.example', '.env')
            print("✅ Created .env file from template")
            print("📝 Please edit .env file with your Twilio credentials")
        else:
            print("❌ .env.example file not found")
            return False
    else:
        print("✅ .env file already exists")
    return True

def install_dependencies():
    """Install Python dependencies"""
    print("📦 Installing dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError:
        print("❌ Failed to install dependencies")
        return False

def setup_ngrok():
    """Provide instructions for ngrok setup"""
    print("\n🌐 For local development, you'll need to expose your server to the internet.")
    print("📱 We recommend using ngrok:")
    print("1. Install ngrok from https://ngrok.com/")
    print("2. Run: ngrok http 8000")
    print("3. Use the https URL provided by ngrok for your Twilio webhook")

def print_next_steps():
    """Print next steps for the user"""
    print("\n🎯 Next Steps:")
    print("1. Get your Twilio Account SID and Auth Token from https://console.twilio.com/")
    print("2. Get your OpenAI API Key from https://platform.openai.com/api-keys")
    print("3. Edit the .env file with your credentials")
    print("4. Set up ngrok or deploy to a cloud service")
    print("5. Configure your Twilio phone number webhook to point to your server")
    print("6. Test the OpenAI integration with: python test_knowledge.py")
    print("7. Run the servers with: python run_servers.py")
    print("\n📖 See README.md for detailed setup instructions")

def main():
    """Run the setup process"""
    print("🎲 MTG Chatbot Setup")
    print("=" * 50)
    
    if not check_python_version():
        return
    
    if not setup_environment():
        return
        
    if not install_dependencies():
        return
        
    setup_ngrok()
    print_next_steps()
    
    print("\n✅ Setup completed successfully!")

if __name__ == "__main__":
    main()