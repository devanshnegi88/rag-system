"""Topic detection using semantic similarity, keywords, and conversational markers."""
import re
import numpy as np
from typing import List, Dict, Tuple, Set
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from collections import Counter


class TopicDetector:
    """
    Detect topic shifts in conversations using:
    1. Semantic similarity (embeddings)
    2. Keyword shifts
    3. Conversational markers
    
    Uses sliding window approach (window size = 5).
    """
    
    # Conversational markers that indicate topic shifts
    TOPIC_SHIFT_MARKERS = {
        'btw', 'anyway', 'speaking of', 'by the way', 'that reminds me',
        'oh', 'actually', 'wait', 'hold on', 'also', 'meanwhile',
        'on another note', 'else', 'plus', 'besides', 'furthermore',
        'additionally', 'moreover', 'incidentally', 'parenthetically'
    }
    
    def __init__(self, model_name: str = 'all-MiniLM-L6-v2', window_size: int = 5, 
                 similarity_threshold: float = 0.6, keyword_weight: float = 0.3):
        """
        Initialize topic detector.
        
        Args:
            model_name: Sentence transformer model to use
            window_size: Sliding window size for semantic similarity
            similarity_threshold: Cosine similarity threshold for topic shift (0-1)
            keyword_weight: Weight of keyword shift in final score (0-1)
        """
        self.model = SentenceTransformer(model_name)
        self.window_size = window_size
        self.similarity_threshold = similarity_threshold
        self.keyword_weight = keyword_weight
        self.embeddings_cache = {}
        
    def detect_topics(self, messages: List[Dict]) -> List[Dict]:
        """
        Detect topics in conversation messages.
        
        Returns list of topics with structure:
        {
            'topic_id': int,
            'start_idx': int,
            'end_idx': int,
            'messages': List[Dict],
            'keywords': List[str],
            'shift_score': float (confidence of topic shift),
            'shift_type': str ('semantic', 'keyword', 'marker')
        }
        
        Args:
            messages: List of message dicts with 'content' and 'message_index'
            
        Returns:
            List of topic dicts
        """
        if not messages:
            return []
        
        # Filter out empty messages
        messages = [m for m in messages if m.get('content', '').strip()]
        
        if len(messages) <= self.window_size:
            return [{
                'topic_id': 0,
                'start_idx': 0,
                'end_idx': len(messages) - 1,
                'messages': messages,
                'keywords': self._extract_keywords([m['content'] for m in messages]),
                'shift_score': 0.0,
                'shift_type': 'none'
            }]
        
        # Get embeddings for all messages
        message_contents = [m['content'] for m in messages]
        embeddings = self.model.encode(message_contents, show_progress_bar=False)
        
        # Detect shift points
        shift_points = self._detect_shifts(messages, embeddings, message_contents)
        
        # Create topic segments
        topics = []
        topic_id = 0
        last_idx = 0
        
        for shift_idx, shift_info in shift_points:
            if shift_idx > last_idx:
                topic_messages = messages[last_idx:shift_idx]
                topic_contents = message_contents[last_idx:shift_idx]
                
                topics.append({
                    'topic_id': topic_id,
                    'start_idx': last_idx,
                    'end_idx': shift_idx - 1,
                    'messages': topic_messages,
                    'keywords': self._extract_keywords(topic_contents),
                    'shift_score': shift_info.get('score', 0.0),
                    'shift_type': shift_info.get('type', 'semantic')
                })
                topic_id += 1
                last_idx = shift_idx
        
        # Add final topic
        if last_idx < len(messages):
            topic_messages = messages[last_idx:]
            topic_contents = message_contents[last_idx:]
            
            topics.append({
                'topic_id': topic_id,
                'start_idx': last_idx,
                'end_idx': len(messages) - 1,
                'messages': topic_messages,
                'keywords': self._extract_keywords(topic_contents),
                'shift_score': 0.0,
                'shift_type': 'none'
            })
        
        return topics
    
    def _detect_shifts(self, messages: List[Dict], embeddings: np.ndarray, 
                       message_contents: List[str]) -> List[Tuple[int, Dict]]:
        """
        Detect topic shift points using sliding window.
        
        Returns list of (shift_index, shift_info) tuples sorted by index.
        """
        shifts = []
        
        for i in range(self.window_size, len(messages)):
            # Get window before and after current position
            before_window = embeddings[max(0, i - self.window_size):i]
            after_window = embeddings[i:min(len(embeddings), i + self.window_size)]
            
            if len(before_window) == 0 or len(after_window) == 0:
                continue
            
            # Compute average embeddings for each window
            before_avg = np.mean(before_window, axis=0)
            after_avg = np.mean(after_window, axis=0)
            
            # Semantic similarity score (lower = more different)
            semantic_score = float(cosine_similarity(
                before_avg.reshape(1, -1),
                after_avg.reshape(1, -1)
            )[0][0])
            
            # Keyword shift score
            before_kw = set(self._extract_keywords(message_contents[max(0, i - self.window_size):i]))
            after_kw = set(self._extract_keywords(message_contents[i:min(len(message_contents), i + self.window_size)]))
            keyword_score = self._compute_keyword_shift(before_kw, after_kw)
            
            # Conversational marker detection
            marker_score = 1.0 if self._has_marker(message_contents[i]) else 0.0
            
            # Combine scores (invert semantic for consistency - low similarity = high shift)
            combined_score = (
                (1 - semantic_score) * (1 - self.keyword_weight) +
                keyword_score * self.keyword_weight
            )
            
            # Increase score if marker present
            if marker_score > 0:
                combined_score = min(1.0, combined_score + marker_score * 0.2)
                shift_type = 'marker'
            elif keyword_score > 0.5:
                shift_type = 'keyword'
            else:
                shift_type = 'semantic'
            
            # Check if this is a significant shift
            if combined_score >= (1 - self.similarity_threshold):
                shifts.append((i, {
                    'score': combined_score,
                    'type': shift_type,
                    'semantic_score': semantic_score,
                    'keyword_score': keyword_score,
                    'marker_score': marker_score
                }))
        
        return sorted(shifts, key=lambda x: x[0])
    
    def _extract_keywords(self, texts: List[str], top_k: int = 5) -> List[str]:
        """
        Extract keywords using simple frequency analysis.
        
        Args:
            texts: List of text strings
            top_k: Number of top keywords to extract
            
        Returns:
            List of keywords
        """
        # Combine all texts
        combined = ' '.join(texts).lower()
        
        # Remove stop words and special characters
        words = re.findall(r'\b[a-z]{3,}\b', combined)
        
        # Simple stop word list
        stop_words = {
            'the', 'and', 'for', 'are', 'but', 'not', 'you', 'all', 'can', 'her',
            'was', 'one', 'our', 'out', 'day', 'get', 'has', 'him', 'his', 'how',
            'its', 'may', 'old', 'see', 'she', 'two', 'who', 'boy', 'did', 'let',
            'man', 'new', 'now', 'say', 'too', 'use', 'way', 'who', 'why', 'will',
            'with', 'yes', 'been', 'call', 'come', 'made', 'make', 'over', 'such',
            'than', 'them', 'then', 'when', 'where', 'which', 'while', 'that', 'this',
            'from', 'have', 'just', 'some', 'what', 'your', 'about', 'also'
        }
        
        words = [w for w in words if w not in stop_words and len(w) >= 3]
        
        # Get most common words
        if not words:
            return []
        
        counter = Counter(words)
        top_words = [word for word, _ in counter.most_common(top_k)]
        
        return top_words
    
    def _compute_keyword_shift(self, before: Set[str], after: Set[str]) -> float:
        """
        Compute keyword shift between two sets.
        
        Returns value between 0 and 1 (0 = no shift, 1 = complete shift).
        """
        if not before and not after:
            return 0.0
        
        if not before or not after:
            return 1.0
        
        # Jaccard distance (complement of Jaccard similarity)
        union = len(before.union(after))
        intersection = len(before.intersection(after))
        
        if union == 0:
            return 0.0
        
        jaccard_sim = intersection / union
        return 1.0 - jaccard_sim
    
    def _has_marker(self, text: str) -> bool:
        """Check if text contains conversational markers."""
        text_lower = text.lower()
        
        for marker in self.TOPIC_SHIFT_MARKERS:
            # Match as whole words
            if re.search(rf'\b{re.escape(marker)}\b', text_lower):
                return True
        
        return False
