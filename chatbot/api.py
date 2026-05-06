"""Flask-based chatbot API."""
import logging
import json
from typing import Dict, List
from flask import Flask, request, jsonify, render_template
from functools import wraps
import numpy as np

logger = logging.getLogger(__name__)
def clean_json(obj):

    if isinstance(obj, np.integer):
        return int(obj)

    if isinstance(obj, np.floating):
        return float(obj)

    if isinstance(obj, np.ndarray):
        return obj.tolist()

    if isinstance(obj, dict):
        return {
            k: clean_json(v)
            for k, v in obj.items()
        }

    if isinstance(obj, list):
        return [clean_json(i) for i in obj]

    return obj


class ChatbotAPI:
    """
    Flask-based chatbot API with intent classification.
    
    Endpoints:
    POST /chat - Submit query and get response
    GET /health - Health check
    """
    
    def __init__(self, rag_indexer, persona_extractor):
        """
        Initialize chatbot API.
        
        Args:
            rag_indexer: RAGIndexer instance (with built RAG system)
            persona_extractor: PersonaExtractor instance (already extracted persona)
        """
        self.app = Flask(
    __name__,
    template_folder="templates",
    static_folder="static"
)
        self.rag_indexer = rag_indexer
        self.persona_extractor = persona_extractor
        
        # Setup logging
        self._setup_logging()
        
        # Register routes
        self._register_routes()
        
    
    def _setup_logging(self):
        """Configure Flask logging."""
        handler = logging.StreamHandler()
        handler.setLevel(logging.INFO)
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)
        self.app.logger.addHandler(handler)
    
    def _register_routes(self):
        """Register Flask routes."""

        @self.app.route('/')
        def home():
           return render_template("index.html")


        @self.app.route('/persona-ui')
        def persona_ui():
           return render_template(
                "persona.html",
               persona=self.persona_extractor
           )


        @self.app.route('/topics-ui')
        def topics_ui():
           return render_template(
                "topics.html",
                topics=self.rag_indexer.topics
            )
        
        @self.app.route('/health', methods=['GET'])
        def health():
            return jsonify({'status': 'ok'}), 200
        
        @self.app.route('/chat', methods=['POST'])
        def chat():
            try:
                data = request.get_json()
                
                if not data or 'query' not in data:
                    return jsonify({
                        'error': 'Missing query parameter'
                    }), 400
                
                query = data['query']
                response = self._handle_chat(query)
                
                return jsonify(clean_json(response)), 200
            
            except Exception as e:
                logger.error(f"Error in /chat: {e}", exc_info=True)
                return jsonify({
                    'error': str(e)
                }), 500
        
        @self.app.route('/topics', methods=['GET'])
        def get_topics():
            """Get list of detected topics."""
            try:
                topics = []
                for topic in self.rag_indexer.topics:
                    topics.append({
                        'topic_id': topic['topic_id'],
                        'label': topic.get('label', ''),
                        'start_idx': topic['start_idx'],
                        'end_idx': topic['end_idx'],
                        'message_count': len(topic.get('messages', []))
                    })
                
                return jsonify({
                    'total': len(topics),
                    'topics': topics
                }), 200
            
            except Exception as e:
                logger.error(f"Error in /topics: {e}", exc_info=True)
                return jsonify({'error': str(e)}), 500
        
        @self.app.route('/persona', methods=['GET'])
        def get_persona():
            """Get extracted persona."""
            try:
                return jsonify(self.persona_extractor), 200
            except Exception as e:
                logger.error(f"Error in /persona: {e}", exc_info=True)
                return jsonify({'error': str(e)}), 500
    
    def _handle_chat(self, query: str) -> Dict:
        """
        Handle chat query with intent classification.
        
        Returns dict with:
        {
            'query': str,
            'intent': str (persona, habits, general),
            'response': str,
            'sources': [...],
            'confidence': float
        }
        """
        # Step 1: Classify intent
        intent = self._classify_intent(query)
        
        # Step 2: Retrieve relevant information
        if intent == 'persona':
            response, sources = self._answer_persona_query(query)
        elif intent == 'habits':
            response, sources = self._answer_habits_query(query)
        else:  # general
            response, sources = self._answer_general_query(query)
        
        return {
            'query': query,
            'intent': intent,
            'response': response,
            'sources': sources,
            'confidence': 0.8  # Simple confidence
        }
    
    def _classify_intent(self, query: str) -> str:
        """
        Classify query intent into: persona, habits, general.
        
        Args:
            query: User query
            
        Returns:
            Intent classification
        """
        query_lower = query.lower()
        
        # Persona intent keywords
        persona_keywords = [
            'who', 'about you', 'personality', 'traits', 'type of person',
            'describe yourself', 'tell me about', 'name', 'age', 'live',
            'work', 'like', 'love', 'hate', 'communication'
        ]
        
        # Habits intent keywords
        habits_keywords = [
            'habit', 'usually', 'always', 'routine', 'daily', 'often',
            'typical', 'do you', 'how do you', 'pattern'
        ]
        
        # Check persona intent
        for keyword in persona_keywords:
            if keyword in query_lower:
                return 'persona'
        
        # Check habits intent
        for keyword in habits_keywords:
            if keyword in query_lower:
                return 'habits'
        
        # Default to general
        return 'general'
    
    def _answer_persona_query(self, query: str) -> tuple:
        """
        Answer persona-related query using extracted persona.
        
        Returns (response_text, sources_list).
        """
        persona = self.persona_extractor
        
        # Extract persona information
        facts_text = self._format_personal_facts(persona.get('personal_facts', []))
        traits_text = self._format_personality_traits(persona.get('personality_traits', []))
        style_text = self._format_communication_style(persona.get('communication_style', {}))
        
        response_parts = []
        
        if facts_text:
            response_parts.append(f"**Personal Facts:**\n{facts_text}")
        
        if traits_text:
            response_parts.append(f"**Personality Traits:**\n{traits_text}")
        
        if style_text:
            response_parts.append(f"**Communication Style:**\n{style_text}")
        
        response = "\n\n".join(response_parts) if response_parts else "Unable to determine persona traits."
        
        sources = [
            {
                'type': 'persona',
                'component': 'extracted_traits'
            }
        ]
        
        return response, sources
    
    def _answer_habits_query(self, query: str) -> tuple:
        """
        Answer habits-related query using extracted habits.
        
        Returns (response_text, sources_list).
        """
        persona = self.persona_extractor
        habits = persona.get('habits', [])
        
        if not habits:
            return "No habits detected in conversations.", []
        
        # Format habits with evidence
        habit_texts = []
        for habit in habits[:5]:  # Top 5 habits
            evidence_info = f" (mentioned {habit['frequency']} times)"
            habit_texts.append(f"- {habit['trait']}{evidence_info}")
        
        response = "**Identified Habits:**\n" + "\n".join(habit_texts)
        
        sources = [
            {
                'type': 'persona',
                'component': 'habits',
                'habit_count': len(habits)
            }
        ]
        
        return response, sources
    
    def _answer_general_query(self, query: str) -> tuple:
        """
        Answer general query using RAG retrieval.
        
        Returns (response_text, sources_list).
        """
        # Retrieve relevant messages
        results = self.rag_indexer.query(query, k=3)
        
        if not results:
            return "No relevant information found.", []
        
        # Format response
        response_parts = ["Based on the conversation:"]
        sources = []
        
        for result in results:
            response_parts.append(f"- {result['content'][:100]}...")
            sources.append({
                'type': 'message',
                'message_index': result['message_index'],
                'sender': result['sender'],
                'score': round(result['score'], 2)
            })
        
        response = "\n".join(response_parts)
        
        return response, sources
    
    def _format_personal_facts(self, facts: List[Dict]) -> str:
        """Format personal facts for display."""
        if not facts:
            return ""
        
        lines = []
        for fact in facts[:5]:  # Top 5 facts
            fact_text = fact.get('fact', '')
            category = fact.get('category', '')
            if fact_text:
                lines.append(f"- **{category.capitalize()}**: {fact_text}")
        
        return "\n".join(lines) if lines else ""
    
    def _format_personality_traits(self, traits: List[Dict]) -> str:
        """Format personality traits for display."""
        if not traits:
            return ""
        
        lines = []
        for trait in traits[:5]:  # Top 5 traits
            trait_name = trait.get('trait', '')
            strength = trait.get('strength', 0)
            strength_pct = int(strength * 100)
            if trait_name:
                lines.append(f"- **{trait_name}**: {strength_pct}%")
        
        return "\n".join(lines) if lines else ""
    
    def _format_communication_style(self, style: Dict) -> str:
        """Format communication style for display."""
        lines = []
        
        if style.get('verbosity'):
            lines.append(f"- **Verbosity**: {style['verbosity']}")
        
        if style.get('formality'):
            lines.append(f"- **Formality**: {style['formality']}")
        
        if style.get('emoji_usage'):
            lines.append("- **Uses emojis**: Yes")
        
        avg_len = style.get('avg_message_length', 0)
        if avg_len:
            lines.append(f"- **Average message length**: {avg_len} characters")
        
        return "\n".join(lines) if lines else ""
    
    def run(self, host: str = '0.0.0.0', port: int = 5000, debug: bool = False):
        """
        Run Flask app.
        
        Args:
            host: Host to bind to
            port: Port to bind to
            debug: Enable debug mode
        """
        logger.info(f"Starting chatbot API on {host}:{port}")
        self.app.run(host=host, port=port, debug=debug)
    
    def get_app(self):
        """Get Flask app instance (for WSGI servers)."""
        return self.app




