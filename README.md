# Magic: The Gathering Chatbot with Twilio Conversation Relay + OpenAI

A voice-powered Magic: The Gathering assistant that you can call to get information about MTG mechanics, rules, strategies, and more using Twilio's Conversation Relay powered by OpenAI's intelligent responses.

## Features

- 📞 **Voice-activated**: Call a phone number to talk to the MTG assistant
- 🤖 **OpenAI-powered**: Dynamic, intelligent responses using GPT models
- 🎲 **Comprehensive MTG Knowledge**: Ask about any MTG topic - cards, mechanics, rules, strategies
- 🗣️ **Natural Conversation**: Uses Twilio's Conversation Relay for smooth speech-to-text and text-to-speech
- ⚡ **Real-time Responses**: Fast, streaming responses for natural conversation flow
- 🔧 **Easy Setup**: Python-based with simple configuration

## What You Can Ask

With OpenAI integration, you can ask about virtually anything Magic-related:

- **Mechanics**: "What is flying?" "Explain trample" "How does cascade work?"
- **Rules**: "How does combat work?" "What is the stack?" "Explain the London mulligan"
- **Formats**: "What is Standard?" "Tell me about Commander" "How does Draft work?"
- **Strategy**: "Give me aggro tips" "How do I play control?" "What beats combo decks?"
- **Specific Cards**: "Tell me about Lightning Bolt" "How good is Teferi?" "What's Black Lotus?"
- **Deck Building**: "How many lands should I run?" "What's a good mana curve?" "Sideboard advice?"
- **Current Meta**: "What's popular in Standard?" "Best Modern decks?" "Commander staples?"

## Prerequisites

- Python 3.8 or higher
- A Twilio account with a phone number
- An OpenAI API account with API key
- ngrok (for local development) or a public server

## Quick Setup

1. **Clone and setup**:
   ```bash
   git clone <your-repo-url>
   cd twilio-mtg-chatbot
   python setup.py
   ```

2. **Configure credentials**:
   Edit `.env` file with your Twilio Account SID, Auth Token, and OpenAI API Key

3. **Start the servers**:
   ```bash
   python run_servers.py
   ```

4. **Expose your local server** (for development):
   ```bash
   ngrok http 8000
   ```

5. **Configure your Twilio phone number**:
   Set the webhook URL to: `https://your-ngrok-url.ngrok.io/voice`

## Detailed Setup

### 1. Get API Keys

1. **Twilio**: Sign up for a [Twilio account](https://www.twilio.com/try-twilio)
2. Go to the [Twilio Console](https://console.twilio.com/)
3. Find your Account SID and Auth Token on the dashboard
4. Buy a phone number in the Phone Numbers section

5. **OpenAI**: Sign up for an [OpenAI account](https://platform.openai.com/signup)
6. Go to [API Keys](https://platform.openai.com/api-keys)
7. Create a new API key and copy it

### 2. Configure Twilio Features

1. In the Twilio Console, navigate to Voice → Settings → General
2. Enable "Predictive and Generative AI/ML Features Addendum"
3. Go to Voice → Manage → TwiML Apps
4. Create a new TwiML App or select an existing one
5. Set the Voice URL to your server endpoint (see step 4)

### 3. Environment Setup

```bash
# Install dependencies
pip install -r requirements.txt

# Copy environment template
cp .env.example .env

# Edit .env with your credentials
TWILIO_ACCOUNT_SID=ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
TWILIO_AUTH_TOKEN=your_auth_token_here
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxx
HTTP_PORT=8000
WEBSOCKET_PORT=8001
HOST=localhost  # Change to your domain for production
```

### 4. Local Development with ngrok

For local testing, you need to expose your server to the internet:

```bash
# Install ngrok from https://ngrok.com/
# Then run:
ngrok http 8000
```

This will give you a URL like `https://abc123.ngrok.io` - use this as your webhook URL.

### 5. Configure Twilio Webhook

1. In your TwiML App settings, set the Voice URL to:
   ```
   https://your-ngrok-url.ngrok.io/voice
   ```

2. Set the Voice Method to `POST`

3. Assign this TwiML App to your Twilio phone number

## Running the Application

### Development Mode

```bash
# Test the OpenAI integration first
python test_knowledge.py

# Then run both servers
python run_servers.py

# Or run individually:
# Terminal 1:
python main.py

# Terminal 2:
python websocket_server.py
```

### Production Deployment

For production, deploy to a cloud service like:

- **Heroku**: Use the included `Procfile`
- **AWS**: Deploy on EC2 or use Elastic Beanstalk
- **Google Cloud**: Use App Engine or Compute Engine
- **DigitalOcean**: Deploy on a Droplet

Update your `.env` file with your production domain:
```
HOST=your-domain.com
```

## Project Structure

```
twilio-mtg-chatbot/
├── main.py                 # HTTP server for TwiML
├── websocket_server.py     # WebSocket server for ConversationRelay
├── mtg_knowledge.py        # MTG knowledge base
├── run_servers.py          # Script to run both servers
├── setup.py               # Setup and configuration script
├── requirements.txt       # Python dependencies
├── .env.example          # Environment template
├── .env                  # Your configuration (create from .env.example)
└── README.md             # This file
```

## How It Works

1. **Incoming Call**: User calls your Twilio number
2. **TwiML Response**: Twilio hits your `/voice` endpoint, gets TwiML with ConversationRelay instructions
3. **WebSocket Connection**: Twilio establishes WebSocket connection to your server
4. **Speech Recognition**: User's speech is converted to text and sent via WebSocket
5. **OpenAI Processing**: Your server sends the question to OpenAI's GPT model for intelligent MTG responses
6. **Response Generation**: Server sends the OpenAI response back via WebSocket
7. **Text-to-Speech**: Twilio converts text to speech and plays it to the caller

## Customization

### Adding More MTG Intelligence

The OpenAI integration gives you access to vast MTG knowledge automatically! But you can customize the system prompt in `mtg_knowledge.py` to:
- Focus on specific MTG areas
- Adjust response length and style
- Add custom instructions or personality
- Include specific tournament meta information

### Modifying Voice Settings

In `main.py`, you can customize the ConversationRelay settings:
```python
<ConversationRelay 
    url="{websocket_url}" 
    welcomeGreeting="Your custom greeting here!"
    voice="alice"  # or "man", "woman", etc.
    dtmfDetection="true"
    debug="true" />
```

### Adding Menu Navigation

The WebSocket server supports DTMF (keypad) input. Customize the `handle_dtmf` method in `websocket_server.py`.

## Troubleshooting

### Common Issues

1. **"Invalid signature" errors**: Check your Auth Token in `.env`
2. **WebSocket connection failed**: Ensure your server is publicly accessible
3. **TwiML not loading**: Verify your webhook URL is correct and server is running
4. **Poor voice quality**: Check your internet connection and server performance

### Debugging

Enable debug mode in the ConversationRelay TwiML:
```xml
<ConversationRelay url="..." debug="true" />
```

Check the server logs for WebSocket messages and errors.

### Testing

Test your webhook URL directly:
```bash
curl -X POST https://your-domain.com/voice
```

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `TWILIO_ACCOUNT_SID` | Your Twilio Account SID | Required |
| `TWILIO_AUTH_TOKEN` | Your Twilio Auth Token | Required |
| `OPENAI_API_KEY` | Your OpenAI API Key | Required |
| `HTTP_PORT` | Port for the HTTP server | 8000 |
| `WEBSOCKET_PORT` | Port for WebSocket server | 8001 |
| `HOST` | Your server hostname | localhost |

## Security

- The WebSocket server validates Twilio signatures for security
- Keep your Auth Token secret and never commit it to version control
- Use HTTPS/WSS in production
- Consider rate limiting for production deployments

## Contributing

1. Fork the repository
2. Create a feature branch
3. Add your improvements
4. Test thoroughly
5. Submit a pull request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

- [Twilio Docs](https://www.twilio.com/docs/voice/conversationrelay)
- [MTG Rules](https://magic.wizards.com/en/rules)
- Create an issue for bugs or feature requests

---

🎲 **May your draws be favorable and your mana curve smooth!** 🎲