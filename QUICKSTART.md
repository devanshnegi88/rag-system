"""
Configuration and example files for RAG System.

The example_data.csv contains a sample conversation that demonstrates:
1. Topic shifts (weekend activities → work → interests → personal facts)
2. Repeated habits (hiking every weekend, coffee every morning)
3. Personality traits (enthusiastic about AI, enjoys outdoors)
4. Personal facts (name: Alex, age: 28, location: San Francisco, job: engineer)

This file can be used to test the system before using your own data.

QUICK START:
============

1. Install dependencies:
   pip install -r requirements.txt

2. Test with example data:
   python main.py --csv example_data.csv --output test_results --port 5000

3. In another terminal, test the API:
   curl http://localhost:5000/health
   curl http://localhost:5000/topics
   curl -X POST http://localhost:5000/chat \
     -H "Content-Type: application/json" \
     -d '{"query": "Tell me about yourself"}'

4. Check outputs in test_results/:
   - topic_summaries.json (topic detection)
   - topic_summaries_checkpoints.json (100-message checkpoints)
   - persona.json (extracted persona)
   - faiss_index/ (retrieval index)

CSV FORMAT REQUIREMENTS:
=======================

The system supports multiple conversation formats:

Format 1: JSON Array (Recommended)
----------------------------------
[{"sender": "user", "content": "message here"}, {"sender": "assistant", "content": "response"}]

Format 2: Simple Text with "sender: message"
---------------------------------------------
user: First message here
assistant: Response here
user: Another message

Format 3: JSON Objects
----------------------
{"sender": "user", "content": "message"}
{"sender": "assistant", "content": "response"}

COLUMN REQUIREMENTS:
===================
- Required: One column containing conversation (named 'conversation', 'messages', 'text', or 'content')
- Optional: 'date' column for conversation date (used as key if provided)

EXAMPLE CSV STRUCTURE:
======================
date,conversation
2024-01-01,"[{""sender"":""user"",""content"":""Hi""},{""sender"":""assistant"",""content"":""Hello""}]"
2024-01-02,"user: Hello
assistant: Hi there!"

IMPORTANT NOTES:
================
1. Each row = one full conversation
2. Messages are processed in order (chronological)
3. Minimum 20 messages recommended for good topic detection
4. 100+ messages recommended for stable persona extraction
5. CSV must be UTF-8 encoded
6. Escape quotes properly in JSON strings
"""

# This file is for documentation only. See example_data.csv for actual sample data.
