# Magic: The Gathering Chatbot with Twilio Conversation Relay + OpenAI

A voice-powered Magic: The Gathering assistant that you can call to get information about MTG mechanics, rules, strategies, and more using [Twilio Voice](https://www.twilio.com/docs/voice), [Twilio's Conversation Relay](https://www.twilio.com/docs/voice/twiml/connect/conversationrelay) and by [OpenAI's intelligent responses](https://platform.openai.com/docs/api-reference/introduction).

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
- A Twilio account with a phone number ([read the instructions for purchasing a number number](https://support.twilio.com/hc/en-us/articles/223180928-How-to-Buy-a-Twilio-Phone-Number)), and you can [sign up for a free trial](https://www.twilio.com/docs/usage/tutorials/how-to-use-your-free-trial-account)
- An [OpenAI API account with API key](https://platform.openai.com/api-keys)
- ngrok (for local development) or a public server

## Quick Setup

1. **Clone and setup**:
   ```bash
   git clone <your-repo-url>
   cd twilio-mtg-chatbot
   python setup.py
   ```

2. Install the required dependencies: `pip  install  -r  requirements.txt`

3. **Configure credentials**:
   Edit `.env` file with your Twilio Account SID, Auth Token, OpenAI API Key, and NGROK URL

4. **Start the servers**:
   ```bash
   ngrok  http  8080
   ```

5. Update `NGROK_URL` in your `.env` file with new URL from ngrok

6. Run the application: `python  main.py`

7. **Configure your Twilio phone number to use twiml endpoint as webhook for incoming calls**:
   Set the webhook URL to: `https://your-ngrok-url.ngrok.io/twiml`

8. Call number to interact

### Configuring the Twilio Features

1. In the Twilio Console, navigate to Voice → Settings → General
2. Enable "Predictive and Generative AI/ML Features Addendum"
3. Go to Voice → Manage → TwiML Apps
4. Create a new TwiML App or select an existing one
5. Set the Voice URL to your server endpoint (see step 4)

### Local Development with ngrok

For local testing, you need to expose your server to the internet:

```bash
# Install ngrok from https://ngrok.com/
# Then run:
ngrok http 8000
```

This will give you a URL like `https://abc123.ngrok.io` - use this as your webhook URL.

### Configure Twilio Webhook

1. In your TwiML App settings, set the Voice URL to:
   ```
   https://your-ngrok-url.ngrok.io/twiml
   ```

2. Set the Voice Method to `POST`

3. Assign this TwiML App to your Twilio phone number

## How It Works

1. **Incoming Call**: User calls your Twilio number
2. **TwiML Response**: Twilio hits your `/twiml` endpoint, gets TwiML with ConversationRelay instructions
3. **WebSocket Connection**: Twilio establishes WebSocket connection to your server
4. **Speech Recognition**: User's speech is converted to text and sent via WebSocket
5. **OpenAI Processing**: Your server sends the question to OpenAI's GPT model for intelligent MTG responses
6. **Response Generation**: Server sends the OpenAI response back via WebSocket
7. **Text-to-Speech**: Twilio converts text to speech and plays it to the caller

## Customisation

### Adding More MTG Intelligence

The OpenAI integration gives you access to vast MTG knowledge automatically. However, you can customise the system prompt in `mtg_knowledge.py` to:
- Focus on specific MTG areas
- Adjust response length and style
- Add custom instructions or personality
- Include specific tournament meta information

### Modifying Voice Settings

In `main.py`, you can customise the ConversationRelay settings:
```python
<ConversationRelay 
    url="{websocket_url}" 
    welcomeGreeting="Your custom greeting here!"
    voice="alice"  # or "man", "woman", you can see a list of voices on the [Twilio Docs](https://www.twilio.com/docs/voice/conversationrelay/voice-configuration)
    dtmfDetection="true"
    debug="true" />
```

### Debugging

Enable debug mode in the ConversationRelay TwiML:
```xml
<ConversationRelay url="..." debug="true" />
```

Check the server logs for WebSocket messages and errors.

### Testing

Test your webhook URL directly:
```bash
curl -X POST https://your-domain.com/twiml
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