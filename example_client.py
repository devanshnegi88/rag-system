"""
Example client for querying the RAG system API.

Shows how to interact with the chatbot REST API.
"""

import requests
import json
from typing import Dict, List, Optional


class RAGClient:
    """Client for RAG system API."""
    
    def __init__(self, base_url: str = "http://localhost:5000"):
        """
        Initialize client.
        
        Args:
            base_url: Base URL of RAG API
        """
        self.base_url = base_url
        self.session = requests.Session()
    
    def health_check(self) -> bool:
        """Check if API is running."""
        try:
            response = self.session.get(f"{self.base_url}/health", timeout=5)
            return response.status_code == 200
        except:
            return False
    
    def chat(self, query: str) -> Dict:
        """
        Send a chat query.
        
        Args:
            query: Query string
            
        Returns:
            Response dict with keys: query, intent, response, sources, confidence
        """
        response = self.session.post(
            f"{self.base_url}/chat",
            json={"query": query},
            timeout=30
        )
        response.raise_for_status()
        return response.json()
    
    def get_topics(self) -> Dict:
        """Get list of detected topics."""
        response = self.session.get(
            f"{self.base_url}/topics",
            timeout=10
        )
        response.raise_for_status()
        return response.json()
    
    def get_persona(self) -> Dict:
        """Get extracted persona."""
        response = self.session.get(
            f"{self.base_url}/persona",
            timeout=10
        )
        response.raise_for_status()
        return response.json()
    
    def close(self):
        """Close session."""
        self.session.close()


def example_usage():
    """Example usage of RAG client."""
    
    # Create client
    client = RAGClient("http://localhost:5000")
    
    # Check if API is running
    if not client.health_check():
        print("API is not running!")
        return
    
    print("✓ Connected to RAG API\n")
    
    # Example 1: Get topics
    print("=" * 60)
    print("EXAMPLE 1: Detecting Topics")
    print("=" * 60)
    topics = client.get_topics()
    print(f"Found {topics['total']} topics:\n")
    for topic in topics['topics'][:3]:
        print(f"  • {topic['label']}")
        print(f"    Messages {topic['start_idx']}-{topic['end_idx']} ({topic['message_count']} messages)")
    
    # Example 2: Query persona
    print("\n" + "=" * 60)
    print("EXAMPLE 2: Persona Extraction")
    print("=" * 60)
    persona = client.get_persona()
    
    if 'personal_facts' in persona:
        print(f"Personal Facts ({len(persona['personal_facts'])}):")
        for fact in persona['personal_facts'][:3]:
            print(f"  • {fact['category'].capitalize()}: {fact['fact']}")
    
    if 'communication_style' in persona:
        style = persona['communication_style']
        print(f"\nCommunication Style:")
        print(f"  • Verbosity: {style.get('verbosity', 'N/A')}")
        print(f"  • Formality: {style.get('formality', 'N/A')}")
        print(f"  • Uses emojis: {style.get('emoji_usage', False)}")
    
    # Example 3: Chat with different intents
    print("\n" + "=" * 60)
    print("EXAMPLE 3: Chat Queries")
    print("=" * 60)
    
    queries = [
        "Tell me about yourself",
        "What are your habits?",
        "What did we discuss?",
    ]
    
    for query in queries:
        print(f"\nQuery: {query}")
        response = client.chat(query)
        
        print(f"Intent: {response['intent']}")
        print(f"Confidence: {response['confidence']}")
        print(f"Response:\n  {response['response'][:100]}...")
        
        print(f"Sources: {len(response['sources'])} source(s)")
    
    client.close()


if __name__ == '__main__':
    print("RAG System API Client Example\n")
    
    try:
        example_usage()
    except requests.exceptions.ConnectionError:
        print("✗ Could not connect to API.")
        print("Make sure the API is running:")
        print("  python main.py --csv example_data.csv")
    except Exception as e:
        print(f"Error: {e}")
