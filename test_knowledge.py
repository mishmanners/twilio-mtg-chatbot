"""
Test the MTG knowledge base functionality with OpenAI
"""
import asyncio
import os
from mtg_knowledge import MTGKnowledge
from dotenv import load_dotenv

async def test_knowledge():
    """Test various MTG questions with OpenAI"""
    load_dotenv()
    
    if not os.getenv("OPENAI_API_KEY"):
        print("❌ Please set your OPENAI_API_KEY in the .env file")
        return
    
    try:
        kb = MTGKnowledge()
    except ValueError as e:
        print(f"❌ Configuration error: {e}")
        return
    
    test_questions = [
        "What is flying?",
        "How does trample work?", 
        "Tell me about Standard format",
        "What are some aggro tips?",
        "How do I build a good mana curve?",
        "What is priority?",
        "Explain Lightning Bolt",
        "What's the best strategy against control decks?",
        "Hello there!",
        "Thanks for your help!"
    ]
    
    print("🎲 Testing MTG Knowledge Base with OpenAI")
    print("=" * 60)
    
    for question in test_questions:
        print(f"\nQ: {question}")
        try:
            response = await kb.get_response(question)
            print(f"A: {response}")
        except Exception as e:
            print(f"❌ Error: {e}")
        print("-" * 60)

if __name__ == "__main__":
    asyncio.run(test_knowledge())