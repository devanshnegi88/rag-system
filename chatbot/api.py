from flask import Flask, request, jsonify, render_template
import logging
import numpy as np
from typing import Dict, List

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# =========================================================
# NUMPY-SAFE JSON CONVERSION
# =========================================================

def clean_json(obj):
    """
    Convert NumPy types to standard Python types for JSON serialization.
    """
    if isinstance(obj, (np.int_, np.intc, np.intp, np.int8,
        np.int16, np.int32, np.int64, np.uint8,
        np.uint16, np.uint32, np.uint64)):
        return int(obj)
    elif isinstance(obj, (np.float_, np.float16, np.float32, np.float64)):
        return float(obj)
    elif isinstance(obj, (np.ndarray,)):
        return obj.tolist()
    elif isinstance(obj, dict):
        return {k: clean_json(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [clean_json(i) for i in obj]
    return obj


# =========================================================
# CHATBOT API CLASS
# =========================================================

class ChatbotAPI:
    def __init__(self, rag_indexer, persona_extractor):
        self.rag_indexer = rag_indexer
        self.persona_extractor = persona_extractor
        self.app = Flask(__name__)
        self._register_routes()

    def _register_routes(self):
        @self.app.route('/health')
        def health():
            return jsonify({'status': 'healthy'})

        @self.app.route('/chat', methods=['POST'])
        def chat():
            try:
                data = request.get_json()
                query = data.get('query', '').strip()
                response = self._handle_chat(query)
                return jsonify(clean_json(response)), 200
            except Exception as e:
                logger.error(f"Error in /chat: {e}")
                return jsonify({'error': str(e)}), 500

    # =====================================================
    # MAIN CONVERSATIONAL HANDLER
    # =====================================================

    def _handle_chat(self, query: str) -> Dict:
        query_lower = query.lower().strip()

        # 1. CONVERSATIONAL HANDLING (NO RETRIEVAL)
        greetings = ["hi", "hello", "hey", "good morning", "good evening"]
        thanks = ["thanks", "thank you", "thx"]
        goodbyes = ["bye", "goodbye", "see you"]

        if any(word == query_lower for word in greetings):
            logger.info(f"Intent detected: GREETING")
            return {
                'query': query,
                'intent': 'greeting',
                'response': "Hello! Ask me about the user's conversations, habits, persona, or topics.",
                'sources': [],
                'confidence': 1.0
            }

        if any(word in query_lower for word in thanks):
            logger.info(f"Intent detected: THANKS")
            return {
                'query': query,
                'intent': 'thanks',
                'response': "You're welcome! Feel free to ask more questions.",
                'sources': [],
                'confidence': 1.0
            }

        if any(word in query_lower for word in goodbyes):
            logger.info(f"Intent detected: GOODBYE")
            return {
                'query': query,
                'intent': 'goodbye',
                'response': "Goodbye! Have a great day.",
                'sources': [],
                'confidence': 1.0
            }

        # 2. PHRASE-BASED INTENT ROUTING
        intent = self._classify_intent(query_lower)
        logger.info(f"Intent detected: {intent.upper()}")

        # 3. ROUTE TO SPECIALIZED HANDLERS
        if intent == "persona":
            response, sources = self._answer_persona_query(query)
        elif intent == "habits":
            response, sources = self._answer_habits_query(query)
        elif intent == "topic":
            response, sources = self._answer_topic_query(query)
        else:
            # 4. GENERAL RETRIEVAL (FALLBACK)
            response, sources = self._answer_general_query(query)

        return {
            'query': query,
            'intent': intent,
            'response': response,
            'sources': sources,
            'confidence': 0.9
        }

    def _classify_intent(self, query: str) -> str:
        # Persona phrases
        persona_phrases = ["what kind of person", "describe the user", "personality", "communication style", "what is this user like"]
        # Habits phrases
        habits_phrases = ["habits", "routine", "patterns"]
        # Topic phrases
        topic_phrases = ["topics", "subjects discussed", "conversation themes"]

        if any(p in query for p in persona_phrases):
            return "persona"
        if any(p in query for p in habits_phrases):
            return "habits"
        if any(p in query for p in topic_phrases):
            return "topic"
        
        return "general"

    # =====================================================
    # SPECIALIZED RESPONSE GENERATORS
    # =====================================================

    def _answer_persona_query(self, query: str) -> tuple:
        """Synthesize persona response in third person."""
        persona = self.persona_extractor
        
        traits = [t.get('trait', '') for t in persona.get('personality_traits', [])[:3]]
        facts = [f.get('fact', '') for f in persona.get('personal_facts', [])[:2]]
        style = persona.get('communication_style', {})
        formality = style.get('formality', 'casual')

        response_parts = []
        if traits:
            response_parts.append(f"The user appears to be {', '.join(traits)}.")
        if facts:
            response_parts.append(f"They mentioned details such as {', '.join(facts)}.")
        
        response_parts.append(f"Their communication style is generally {formality}.")
        
        response = " ".join(response_parts)
        return response, [{'type': 'persona'}]

    def _answer_habits_query(self, query: str) -> tuple:
        """Synthesize habits response in third person."""
        persona = self.persona_extractor
        habits = persona.get('habits', [])

        if not habits:
            return "No strong habits were detected in the user's conversations.", []

        habit_list = []
        for h in habits[:3]:
            if isinstance(h, dict):
                habit_list.append(h.get('trait', ''))
            else:
                habit_list.append(str(h))

        response = f"The system detected recurring habits such as {', '.join(habit_list)} and discussing daily routines frequently."
        return response, [{'type': 'habits'}]

    def _answer_topic_query(self, query: str) -> tuple:
        """List detected conversation themes."""
        topics = self.rag_indexer.topics
        if not topics:
            return "No conversation topics have been detected yet.", []

        labels = [t.get('label', 'Unknown') for t in topics[:5]]
        response = f"The conversations mainly covered themes like: {', '.join(labels)}."
        return response, [{'type': 'topics'}]

    def _answer_general_query(self, query: str) -> tuple:
        """Retrieve and synthesize general answers in third person."""
        results = self.rag_indexer.query(query, k=5)
        if not results:
            return "I couldn't find any information in the conversations to answer that.", []

        # Format context as dialogue for the summarizer
        context = "\n".join([f"{r.get('sender', 'User')}: {r.get('content', '')}" for r in results])

        try:
            prompt = (
                f"Question: {query}\n\n"
                f"Based on these messages, explain what the user says about the question in the third person. "
                f"Be concise.\n\n"
                f"Messages:\n{context}"
            )
            synthesized = self.rag_indexer.summarizer.summarize_text(prompt, max_length=100)
            
            if synthesized and len(synthesized) > 30:
                response = synthesized
            else:
                # Use first relevant message as a clean fallback
                content = results[0].get('content', '')
                response = f"In the conversations, the user mentioned that '{content}'."
        except Exception as e:
            logger.error(f"Summarization error: {e}")
            content = results[0].get('content', '')
            response = f"According to the chat logs, the user said: '{content}'."

        sources = []
        for r in results[:3]:
            sources.append({
                'type': 'message',
                'message_index': int(r.get('message_index', 0)),
                'sender': str(r.get('sender', 'unknown'))
            })

        return response, sources

    # =====================================================
    # SYSTEM RUNNERS
    # =====================================================

    def run(self, host='0.0.0.0', port=5000, debug=False):
        logger.info(f"Starting API on {host}:{port}")
        self.app.run(host=host, port=port, debug=debug)

    def get_app(self):
        return self.app
