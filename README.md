# RAG-Based Conversation Intelligence System

## Overview

This project is a topic-aware Retrieval-Augmented Generation (RAG) system designed to analyze chronological conversation data, detect topic changes, extract user persona information, and provide an interactive chatbot interface for querying conversations.

The system processes conversations message-by-message in chronological order and creates:
- Topic checkpoints
- Topic summaries
- 100-message summaries
- Persona profiles
- Hybrid retrieval indexes

The chatbot allows users to ask questions about:
- Conversation topics
- User habits
- Personality traits
- Communication style
- General conversation content

---

# Features

## Topic-Aware RAG System
- Chronological message processing
- Dynamic topic change detection
- Topic checkpoint creation
- Topic summarization
- Hybrid retrieval pipeline

## Persona Extraction
Extracts:
- Habits
- Personal facts
- Personality traits
- Communication style

## Chatbot
Supports:
- Persona questions
- Habit questions
- Topic queries
- General conversation retrieval

## Hybrid Retrieval
Combines:
- Dense embedding retrieval
- Semantic similarity
- Context synthesis

---

# Project Architecture

```text
CSV Conversations
        ↓
Message Processing
        ↓
Topic Detection
        ↓
Topic Checkpoints
        ↓
Summarization
        ↓
Hybrid Retrieval Index
        ↓
Persona Extraction
        ↓
Chatbot Interface