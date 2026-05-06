"""Load and parse conversation data from CSV."""
import pandas as pd
import json
from typing import List, Dict, Tuple
from datetime import datetime


class ConversationLoader:
    """Load conversation data from CSV files."""
    
    def __init__(self, csv_path: str):
        """
        Initialize loader with CSV file.
        
        Args:
            csv_path: Path to CSV file containing conversations
        """
        self.csv_path = csv_path
        self.raw_data = None
        self.conversations = {}
        
    def load(self) -> Dict[str, List[Dict]]:
        """
        Load CSV and parse conversations.
        
        Expected CSV format:
        - Column 'conversation': JSON array of messages or newline-separated messages
        - Column 'date': Date of conversation (optional)
        
        Returns:
            Dict mapping date to list of message dicts with keys:
            {timestamp, sender, content, message_index}
        """
        try:
            df = pd.read_csv(self.csv_path)
            self.raw_data = df
        except FileNotFoundError:
            raise FileNotFoundError(f"CSV file not found: {self.csv_path}")
        except Exception as e:
            raise ValueError(f"Error reading CSV: {e}")
        
        # Process each row
        for idx, row in df.iterrows():
            conversation_key = row.get('date', f"conversation_{idx}")
            messages = self._parse_conversation(row, idx)
            self.conversations[conversation_key] = messages
        
        return self.conversations
    
    def _parse_conversation(self, row: pd.Series, row_idx: int) -> List[Dict]:
        """
        Parse a single conversation row.
        
        Handles multiple formats:
        1. JSON array: [{"sender": "...", "content": "..."}, ...]
        2. Newline-separated messages: "user: msg1\nbot: msg2"
        3. Raw text in 'conversation' or 'messages' column
        
        Args:
            row: DataFrame row
            row_idx: Row index for fallback naming
            
        Returns:
            List of parsed messages with metadata
        """
        messages = []
        message_index = 0
        
        # Try to get conversation data from various column names
        conv_text = None
        for col_name in ['conversation', 'messages', 'text', 'content']:
            if col_name in row and pd.notna(row[col_name]):
                conv_text = row[col_name]
                break
        
        if conv_text is None:
            return messages
        
        conv_text = str(conv_text)
        
        # Try to parse as JSON
        try:
            if conv_text.startswith('[') or conv_text.startswith('{'):
                parsed = json.loads(conv_text)
                if isinstance(parsed, list):
                    for msg in parsed:
                        if isinstance(msg, dict):
                            messages.append(self._normalize_message(msg, message_index))
                            message_index += 1
                elif isinstance(parsed, dict):
                    messages.append(self._normalize_message(parsed, message_index))
                    message_index += 1
                return messages
        except (json.JSONDecodeError, ValueError):
            pass
        
        # Parse as newline-separated messages
        lines = conv_text.split('\n')
        for line in lines:
            if line.strip():
                msg = self._parse_message_line(line, message_index)
                if msg:
                    messages.append(msg)
                    message_index += 1
        
        return messages
    
    def _parse_message_line(self, line: str, msg_idx: int) -> Dict:
        """
        Parse a single message line (format: "sender: content").
        
        Args:
            line: Message line
            msg_idx: Message index for tracking
            
        Returns:
            Normalized message dict
        """
        line = line.strip()
        
        # Handle "sender: content" format
        if ':' in line:
            parts = line.split(':', 1)
            sender = parts[0].strip()
            content = parts[1].strip()
        else:
            # Assume whole line is content
            sender = 'unknown'
            content = line
        
        return {
            'sender': sender,
            'content': content,
            'timestamp': None,
            'message_index': msg_idx
        }
    
    def _normalize_message(self, msg: Dict, msg_idx: int) -> Dict:
        """
        Normalize message to standard format.
        
        Args:
            msg: Raw message dict
            msg_idx: Message index
            
        Returns:
            Normalized message dict
        """
        return {
            'sender': msg.get('sender') or msg.get('author') or 'unknown',
            'content': msg.get('content') or msg.get('text') or msg.get('message') or '',
            'timestamp': msg.get('timestamp'),
            'message_index': msg_idx
        }
    
    def get_all_messages(self) -> List[Dict]:
        """Get all messages from all conversations as flat list."""
        all_messages = []
        for conv_messages in self.conversations.values():
            all_messages.extend(conv_messages)
        return all_messages
