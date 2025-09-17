#!/usr/bin/env python3
"""
Fast Track Academy - DutyBot Core

This module contains the core functionality for the DutyBot, a virtual character
capable of interacting with users across various social media platforms.
"""

import json
import logging
from datetime import datetime
from typing import Dict, List, Optional

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class DutyBot:
    """
    Core DutyBot class for handling interactions and responses.
    """
    
    def __init__(self, name: str = "DutyBot", personality: str = "helpful"):
        """
        Initialize the DutyBot with a name and personality.
        
        Args:
            name: The name of the bot
            personality: The personality type (helpful, friendly, professional)
        """
        self.name = name
        self.personality = personality
        self.created_at = datetime.now()
        self.interaction_count = 0
        self.responses = self._load_default_responses()
        
        logger.info(f"DutyBot '{self.name}' initialized with {self.personality} personality")
    
    def _load_default_responses(self) -> Dict[str, List[str]]:
        """Load default response templates."""
        return {
            "greeting": [
                f"Hello! I'm {self.name}, your virtual assistant.",
                f"Hi there! {self.name} here, ready to help!",
                f"Greetings! I'm {self.name}, how can I assist you today?"
            ],
            "help": [
                "I can help you with academy resources, answer questions, and guide you through the platform.",
                "I'm here to assist with your learning journey and platform navigation.",
                "Feel free to ask me about courses, achievements, or any academy-related topics!"
            ],
            "farewell": [
                "Goodbye! Have a great learning experience!",
                "See you later! Keep up the great work!",
                "Farewell! Don't hesitate to reach out if you need help."
            ]
        }
    
    def generate_response(self, message: str, category: str = "general") -> str:
        """
        Generate a response based on the input message and category.
        
        Args:
            message: The input message from the user
            category: The category of the message (greeting, help, farewell, general)
            
        Returns:
            A response string
        """
        self.interaction_count += 1
        
        message_lower = message.lower().strip()
        
        # Determine response category
        if any(word in message_lower for word in ["hello", "hi", "hey", "greetings"]):
            category = "greeting"
        elif any(word in message_lower for word in ["help", "assist", "support"]):
            category = "help"
        elif any(word in message_lower for word in ["bye", "goodbye", "farewell", "see you"]):
            category = "farewell"
        
        # Get response from templates
        if category in self.responses:
            import random
            response = random.choice(self.responses[category])
        else:
            response = f"Thank you for your message: '{message}'. How can I help you with the Fast Track Academy platform?"
        
        logger.info(f"Generated response for category '{category}': {response[:50]}...")
        return response
    
    def add_custom_response(self, category: str, responses: List[str]) -> None:
        """
        Add custom response templates for a specific category.
        
        Args:
            category: The response category
            responses: List of response templates
        """
        self.responses[category] = responses
        logger.info(f"Added {len(responses)} custom responses for category '{category}'")
    
    def get_stats(self) -> Dict:
        """Get bot statistics."""
        return {
            "name": self.name,
            "personality": self.personality,
            "created_at": self.created_at.isoformat(),
            "interaction_count": self.interaction_count,
            "response_categories": list(self.responses.keys())
        }
    
    def interact(self, message: str) -> Dict:
        """
        Main interaction method that returns structured response data.
        
        Args:
            message: The input message from the user
            
        Returns:
            A dictionary containing the response and metadata
        """
        response = self.generate_response(message)
        
        return {
            "bot_name": self.name,
            "user_message": message,
            "bot_response": response,
            "timestamp": datetime.now().isoformat(),
            "interaction_number": self.interaction_count
        }


def main():
    """Main function to run the DutyBot interactively."""
    print("=== Fast Track Academy - DutyBot ===")
    print("Welcome to the DutyBot interactive session!")
    print("Type 'quit' or 'exit' to end the session.\n")
    
    # Initialize the bot
    bot = DutyBot()
    
    try:
        while True:
            user_input = input("You: ").strip()
            
            if user_input.lower() in ['quit', 'exit', 'q']:
                print(f"\n{bot.name}: {bot.generate_response('goodbye')}")
                break
            
            if not user_input:
                continue
            
            # Get bot response
            interaction = bot.interact(user_input)
            print(f"{bot.name}: {interaction['bot_response']}")
    
    except KeyboardInterrupt:
        print(f"\n\n{bot.name}: Goodbye! Session ended.")
    
    # Print session stats
    stats = bot.get_stats()
    print(f"\nSession Statistics:")
    print(f"- Total interactions: {stats['interaction_count']}")
    print(f"- Bot personality: {stats['personality']}")


if __name__ == "__main__":
    main()