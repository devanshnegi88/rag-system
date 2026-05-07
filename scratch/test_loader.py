import sys
import os
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

import pandas as pd
from processing.loader import ConversationLoader

csv_path = "data/conversations.csv"
loader = ConversationLoader(csv_path)
conversations = loader.load()
all_messages = loader.get_all_messages()

print(f"Total conversations: {len(conversations)}")
print(f"Total messages: {len(all_messages)}")
if all_messages:
    print(f"First message: {all_messages[0]}")
