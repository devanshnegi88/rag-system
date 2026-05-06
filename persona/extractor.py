"""Persona extraction module."""
import json
import re
from typing import List, Dict, Tuple
from collections import Counter
import logging

logger = logging.getLogger(__name__)


class PersonaExtractor:
    """
    Extract structured persona from conversations with evidence tracking.
    
    Extracts:
    1. Habits (repeated patterns)
    2. Personal facts (explicit mentions only)
    3. Personality traits (behavior signals)
    4. Communication style (message length, tone, emoji usage)
    
    CRITICAL: Every trait includes message indices as evidence. NO hallucination.
    """
    
    def __init__(self, min_repetitions: int = 2):
        """
        Initialize persona extractor.
        
        Args:
            min_repetitions: Minimum repetitions to count as habit
        """
        self.min_repetitions = min_repetitions
    
    def extract(self, messages: List[Dict]) -> Dict:
        """
        Extract complete persona from messages.
        
        Args:
            messages: List of message dicts with 'content' and 'message_index'
            
        Returns:
            Dict with keys: habits, personal_facts, personality_traits, communication_style
        """
        logger.info(f"Extracting persona from {len(messages)} messages...")
        
        persona = {
            'habits': self._extract_habits(messages),
            'personal_facts': self._extract_personal_facts(messages),
            'personality_traits': self._extract_personality_traits(messages),
            'communication_style': self._extract_communication_style(messages)
        }
        
        logger.info(f"Persona extraction complete. Found:")
        logger.info(f"  - {len(persona['habits'])} habits")
        logger.info(f"  - {len(persona['personal_facts'])} personal facts")
        logger.info(f"  - {len(persona['personality_traits'])} personality traits")
        
        return persona
    
    def _extract_habits(self, messages: List[Dict]) -> List[Dict]:
        """
        Extract habits based on repeated patterns.
        
        Looks for repeated:
        - Phrases (e.g., "I usually...", "I always...")
        - Actions/activities mentioned multiple times
        - Time references (e.g., "every morning")
        
        Returns list of dicts with evidence:
        {
            'trait': str,
            'evidence': [msg_indices],
            'frequency': int
        }
        """
        habits = []
        habit_patterns = {}
        
        # Define habit patterns
        habit_keywords = [
            r'always', r'usually', r'never', r'everyday', r'every day',
            r'often', r'rarely', r'sometimes', r'tend to', r'used to',
            r'am used to', r'am accustomed to', r'makes a point to',
            r'regularly', r'frequently', r'hardly ever'
        ]
        
        # Find potential habits
        for msg in messages:
            content = msg['content'].lower()
            msg_idx = msg['message_index']
            
            # Search for habit indicators
            for keyword in habit_keywords:
                if re.search(rf'\b{keyword}\b', content):
                    # Extract the habit phrase (next sentence or clause)
                    habit_phrase = self._extract_habit_phrase(msg['content'], keyword)
                    
                    if habit_phrase:
                        if habit_phrase not in habit_patterns:
                            habit_patterns[habit_phrase] = []
                        habit_patterns[habit_phrase].append(msg_idx)
        
        # Filter by minimum repetitions
        for habit, indices in habit_patterns.items():
            if len(indices) >= self.min_repetitions:
                habits.append({
                    'trait': habit,
                    'evidence': list(dict.fromkeys(indices)),  # Unique indices, preserve order
                    'frequency': len(indices)
                })
        
        # Sort by frequency
        habits = sorted(habits, key=lambda x: x['frequency'], reverse=True)
        
        return habits
    
    def _extract_habit_phrase(self, content: str, keyword: str) -> str:
        """
        Extract the habit phrase from message content.
        
        Args:
            content: Full message content
            keyword: Habit keyword found
            
        Returns:
            Simplified habit phrase or None
        """
        lower_content = content.lower()
        idx = lower_content.find(keyword)
        
        if idx == -1:
            return None
        
        # Get context around keyword (up to 50 chars after)
        end_idx = min(idx + len(keyword) + 50, len(content))
        phrase = content[idx:end_idx].strip()
        
        # Clean up phrase
        period_idx = phrase.find('.')
        if period_idx != -1:
            phrase = phrase[:period_idx].strip()
        
        if len(phrase) < 5:
            return None
        
        return phrase
    
    def _extract_personal_facts(self, messages: List[Dict]) -> List[Dict]:
        """
        Extract personal facts from explicit mentions only.
        
        NO HALLUCINATION: Only extract facts explicitly stated.
        
        Looks for patterns:
        - "I am/was/have..."
        - "My name is..."
        - "I live/work in..."
        - "I have a..."
        - "I like/hate..."
        
        Returns list of dicts:
        {
            'fact': str,
            'evidence': [msg_indices],
            'category': str (age, location, occupation, interest, etc.)
        }
        """
        facts = []
        fact_evidence = {}
        
        # Define fact extraction patterns
        fact_patterns = [
            (r"i(?:'m| am) (\w+)", 'state'),
            (r"i(?:'m| am) (\w+ \w+)", 'state'),
            (r"my name is (\w+)", 'name'),
            (r"i(?:'m| am) (\d+)", 'age'),
            (r"i live in ([^.!?\n]+)", 'location'),
            (r"i live at ([^.!?\n]+)", 'location'),
            (r"i work in ([^.!?\n]+)", 'occupation'),
            (r"i work as (?:a |an )?([^.!?\n]+)", 'occupation'),
            (r"i have a ([^.!?\n]+)", 'possession'),
            (r"i have (\d+ \w+)", 'possession'),
            (r"i like ([^.!?\n]+)", 'interest'),
            (r"i love ([^.!?\n]+)", 'interest'),
            (r"i hate ([^.!?\n]+)", 'dislike'),
            (r"i don't like ([^.!?\n]+)", 'dislike'),
            (r"i'm from ([^.!?\n]+)", 'origin'),
            (r"i was born in ([^.!?\n]+)", 'origin'),
        ]
        
        for msg in messages:
            content = msg['content']
            msg_idx = msg['message_index']
            
            for pattern, category in fact_patterns:
                matches = re.finditer(pattern, content.lower())
                
                for match in matches:
                    # Get the extracted fact
                    fact_value = content[match.start(1):match.end(1)].strip()
                    
                    if fact_value and len(fact_value) > 2:
                        fact_key = f"{category}:{fact_value}"
                        
                        if fact_key not in fact_evidence:
                            fact_evidence[fact_key] = {
                                'value': fact_value,
                                'category': category,
                                'indices': []
                            }
                        
                        fact_evidence[fact_key]['indices'].append(msg_idx)
        
        # Convert to output format
        for fact_key, info in fact_evidence.items():
            facts.append({
                'fact': info['value'],
                'category': info['category'],
                'evidence': list(dict.fromkeys(info['indices']))  # Unique indices
            })
        
        return facts
    
    def _extract_personality_traits(self, messages: List[Dict]) -> List[Dict]:
        """
        Extract personality traits based on behavior signals.
        
        Looks for:
        - Emotional expressions (excited, happy, frustrated, confused)
        - Question frequency (curious?)
        - Enthusiasm/engagement (exclamation marks)
        - Negativity/positivity balance
        - Profanity/politeness indicators
        
        Returns list of dicts:
        {
            'trait': str,
            'evidence': [msg_indices],
            'strength': float (0-1)
        }
        """
        traits = []
        trait_scores = {}
        
        # Emotional indicators
        positive_words = [
            'happy', 'great', 'awesome', 'wonderful', 'excellent', 'love',
            'excited', 'thrilled', 'amazing', 'fantastic', 'brilliant',
            'good', 'fun', 'enjoy', 'pleased', 'glad'
        ]
        
        negative_words = [
            'sad', 'angry', 'frustrated', 'annoyed', 'upset', 'hate',
            'terrible', 'awful', 'hate', 'disgusting', 'horrible',
            'bad', 'dangerous', 'confused', 'worried', 'scared'
        ]
        
        # Initialize counters
        trait_scores = {
            'positive_sentiment': {'count': 0, 'indices': []},
            'negative_sentiment': {'count': 0, 'indices': []},
            'curious_inquisitive': {'count': 0, 'indices': []},
            'enthusiastic': {'count': 0, 'indices': []},
            'polite_respectful': {'count': 0, 'indices': []},
        }
        
        for msg in messages:
            content = msg['content'].lower()
            msg_idx = msg['message_index']
            
            # Positive sentiment
            for word in positive_words:
                if word in content:
                    trait_scores['positive_sentiment']['count'] += 1
                    trait_scores['positive_sentiment']['indices'].append(msg_idx)
            
            # Negative sentiment
            for word in negative_words:
                if word in content:
                    trait_scores['negative_sentiment']['count'] += 1
                    trait_scores['negative_sentiment']['indices'].append(msg_idx)
            
            # Curiosity (questions)
            if '?' in content:
                trait_scores['curious_inquisitive']['count'] += 1
                trait_scores['curious_inquisitive']['indices'].append(msg_idx)
            
            # Enthusiasm (exclamations)
            if '!' in content and len(content) > 0:
                trait_scores['enthusiastic']['count'] += 1
                trait_scores['enthusiastic']['indices'].append(msg_idx)
            
            # Politeness
            polite_phrases = ['please', 'thank', 'sorry', 'appreciate', 'kind of you']
            for phrase in polite_phrases:
                if phrase in content:
                    trait_scores['polite_respectful']['count'] += 1
                    trait_scores['polite_respectful']['indices'].append(msg_idx)
        
        # Convert to traits with scores
        total_messages = len(messages)
        
        for trait_name, data in trait_scores.items():
            count = data['count']
            indices = list(dict.fromkeys(data['indices']))  # Unique indices
            
            if count > 0:
                # Calculate strength as percentage
                strength = count / total_messages
                
                # Only include if meaningful presence
                if strength > 0.1 or count >= 2:
                    traits.append({
                        'trait': trait_name.replace('_', ' '),
                        'evidence': indices,
                        'strength': min(strength, 1.0),
                        'signal_count': count
                    })
        
        return traits
    
    def _extract_communication_style(self, messages: List[Dict]) -> Dict:
        """
        Extract communication style metrics.
        
        Returns dict with:
        {
            'avg_message_length': int,
            'message_length_variance': float,
            'emoji_usage': bool,
            'punctuation_style': str,
            'formality': str,
            'verbosity': str,
            'evidence': dict with stats
        }
        """
        styles = {
            'avg_message_length': 0,
            'message_length_variance': 0,
            'emoji_usage': False,
            'punctuation_style': 'standard',
            'formality': 'informal',
            'verbosity': 'normal',
            'capitalization': 'normal',
            'evidence': {
                'total_messages': len(messages),
                'emoji_messages': 0,
                'all_caps_messages': 0,
                'avg_words_per_message': 0
            }
        }
        
        if not messages:
            return styles
        
        # Calculate message lengths
        lengths = []
        emoji_count = 0
        all_caps_count = 0
        word_counts = []
        exclamation_count = 0
        question_count = 0
        uppercase_count = 0
        
        emoji_pattern = r'[😀-🙏🌀-🗿]'
        
        for msg in messages:
            content = msg['content']
            length = len(content)
            lengths.append(length)
            
            # Emoji detection
            if re.search(emoji_pattern, content):
                emoji_count += 1
            
            # All caps detection
            if content.isupper() and len(content) > 3:
                all_caps_count += 1
            
            # Word count
            words = content.split()
            word_counts.append(len(words))
            
            # Punctuation patterns
            exclamation_count += content.count('!')
            question_count += content.count('?')
            
            # Capitalization
            upper_letters = sum(1 for c in content if c.isupper())
            if len(content) > 0:
                uppercase_count += upper_letters / len(content)
        
        # Calculate statistics
        if lengths:
            styles['avg_message_length'] = int(np.mean(lengths))
            styles['message_length_variance'] = float(np.var(lengths))
        
        if word_counts:
            styles['evidence']['avg_words_per_message'] = int(np.mean(word_counts))
        
        # Determine styles
        if emoji_count > 0:
            styles['emoji_usage'] = True
            styles['evidence']['emoji_messages'] = emoji_count
        
        if all_caps_count > len(messages) * 0.1:
            styles['capitalization'] = 'frequent_caps'
            styles['evidence']['all_caps_messages'] = all_caps_count
        
        # Formality based on pattern
        if all_caps_count > len(messages) * 0.2 or exclamation_count > len(messages) * 0.3:
            styles['formality'] = 'casual'
        elif exclamation_count < len(messages) * 0.1 and question_count < len(messages) * 0.2:
            styles['formality'] = 'formal'
        
        # Verbosity
        avg_word_count = np.mean(word_counts) if word_counts else 0
        if avg_word_count < 3:
            styles['verbosity'] = 'concise'
        elif avg_word_count > 20:
            styles['verbosity'] = 'verbose'
        
        # Punctuation style
        if exclamation_count > question_count:
            styles['punctuation_style'] = 'exclamatory'
        elif question_count > exclamation_count:
            styles['punctuation_style'] = 'interrogative'
        
        return styles
    
    def save_persona(self, persona: Dict, output_path: str) -> None:
        """
        Save persona to JSON file.
        
        Args:
            persona: Persona dict
            output_path: Path to save JSON
        """
        # Convert to JSON-serializable format
        output_data = {
            'habits': persona['habits'],
            'personal_facts': persona['personal_facts'],
            'personality_traits': persona['personality_traits'],
            'communication_style': persona['communication_style']
        }
        
        with open(output_path, 'w') as f:
            json.dump(output_data, f, indent=2)
        
        logger.info(f"Persona saved to {output_path}")


# Add numpy import (missing earlier)
import numpy as np
