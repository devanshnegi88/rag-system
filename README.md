# RAG-Based Conversation Intelligence System

An AI-powered conversation intelligence platform that performs:

- Topic-aware RAG retrieval
- Chronological topic segmentation
- Persona extraction
- Hybrid semantic search
- Interactive chatbot interface

The system processes conversation datasets message-by-message, detects topic transitions dynamically, generates summaries, extracts user persona traits, and provides a browser-based chatbot interface for querying conversations.

---

# Features

## Topic-Aware RAG
- Chronological message processing
- Dynamic topic segmentation
- Topic checkpoint summaries
- 100-message checkpoint summaries
- Hybrid retrieval:
  - Dense embeddings
  - Keyword overlap scoring

## Persona Extraction
Extracts:
- Habits
- Personal facts
- Personality traits
- Communication style

All persona traits are evidence-backed and derived from actual conversation signals.

## Interactive Web Interface
Includes:
- Chatbot interaction page
- Persona dashboard
- Topic exploration dashboard

---

# Project Structure

```bash
rag system/
│
├── processing/
│   ├── __init__.py
│   └── loader.py
│
├── rag/
│   ├── __init__.py
│   ├── topic_detection.py
│   ├── summarization.py
│   ├── retrieval.py
│   └── indexing.py
│
├── persona/
│   ├── __init__.py
│   └── extractor.py
│
├── chatbot/
│   ├── __init__.py
│   ├── api.py
│   │
│   ├── templates/
│   │   ├── index.html
│   │   ├── persona.html
│   │   └── topics.html
│   │
│   └── static/
│       ├── style.css
│       └── app.js
│
├── outputs/
│   ├── topic_summaries.json
│   ├── topic_summaries_checkpoints.json
│   ├── persona.json
│   └── faiss_index/
│
├── main.py
├── config.py
├── requirements.txt
├── example_data.csv
├── example_client.py
├── test_system.py
├── README.md
├── QUICKSTART.md
└── DEPLOYMENT.md
