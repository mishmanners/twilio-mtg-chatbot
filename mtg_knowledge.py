"""
Magic: The Gathering knowledge base for the chatbot using OpenAI
"""
import re
import logging
from typing import Dict, List
from openai import AsyncOpenAI
from dotenv import load_dotenv

load_dotenv()
logger = logging.getLogger(__name__)

class MTGKnowledge:
    def __init__(self):
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY environment variable is required")
        
        self.client = AsyncOpenAI(api_key=api_key)
        self.system_prompt = """You are an expert Magic: The Gathering assistant. You help players with:

1. Game rules and mechanics (flying, trample, combat, stack, priority, etc.)
2. Card interactions and rulings
3. Format information (Standard, Modern, Legacy, Commander, Draft, etc.)
4. Strategy and deck building advice
5. Meta game insights and tips

Guidelines:
- Give accurate, helpful responses based on current MTG rules
- Keep responses conversational and friendly for voice interaction
- Explain complex concepts in simple terms
- If asked about specific cards, provide accurate information
- For rules questions, cite the comprehensive rules when helpful
- Be encouraging and positive about the game
- Keep responses under 100 words for voice clarity

Remember: You're talking to someone over the phone, so be clear and concise!"""

    async def get_response(self, user_input: str) -> str:
        """
        Get a Magic: The Gathering response using OpenAI
        """
        try:
            response = await self.client.chat.completions.create(
                model="gpt-3.5-turbo",  # You can upgrade to gpt-4 if needed
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": user_input}
                ],
                max_tokens=200,  # Keep responses concise for voice
                temperature=0.7,
                top_p=1,
                frequency_penalty=0.2,
                presence_penalty=0.1
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            logger.error(f"OpenAI API error: {e}")
            return self._get_fallback_response(user_input)
    
    def _get_fallback_response(self, user_input: str) -> str:
        """Fallback response if OpenAI API fails"""
        user_input_lower = user_input.lower()
        
        if any(word in user_input_lower for word in ['hello', 'hi', 'hey']):
            return "Hello! I'm your Magic: The Gathering assistant. I'm having some technical difficulties, but I'll try to help!"
        
        if any(word in user_input_lower for word in ['bye', 'goodbye', 'thanks']):
            return "You're welcome! Happy gaming!"
        
        # Basic mechanic responses as fallback
        basic_mechanics = {
            "flying": "Flying creatures can only be blocked by other flying creatures or creatures with reach.",
            "trample": "Trample lets excess combat damage carry over to the player if blockers are destroyed.",
            "first strike": "First strike creatures deal combat damage before regular creatures.",
            "deathtouch": "Any damage from a deathtouch creature destroys the creature it damages.",
            "lifelink": "Damage from lifelink creatures also heals you for that amount."
        }
        
        for mechanic, explanation in basic_mechanics.items():
            if mechanic in user_input_lower:
                return explanation
        
        return "I'm sorry, I'm having trouble connecting to my knowledge base right now. Please try asking about basic Magic mechanics like flying, trample, or deathtouch, or try again in a moment!"