"""
Configuration and initialization utilities for RAG system.
"""

import os
from pathlib import Path

# Project root
PROJECT_ROOT = Path(__file__).parent

# Output directories
OUTPUT_DIR = PROJECT_ROOT / "outputs"
OUTPUT_DIR.mkdir(exist_ok=True)

# Data directories
DATA_DIR = PROJECT_ROOT / "data"
DATA_DIR.mkdir(exist_ok=True)

# Configuration
RAG_CONFIG = {
    "embedding_model": "all-MiniLM-L6-v2",
    "summarization_model": "facebook/bart-large-cnn",
    "topic_window_size": 5,
    "checkpoint_size": 100,
    "similarity_threshold": 0.6,
    "retrieval_k": 5,
}

# Persona extraction config
PERSONA_CONFIG = {
    "min_habit_repetitions": 2,
    "consider_explicit_only": True,
}

# API configuration
API_CONFIG = {
    "host": "0.0.0.0",
    "port": 5000,
    "debug": False,
    "max_request_size": 16 * 1024 * 1024,  # 16 MB
}

# Logging
LOGGING_CONFIG = {
    "level": "INFO",
    "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
}


def get_output_path(filename: str) -> str:
    """Get path for output file."""
    return str(OUTPUT_DIR / filename)


def get_data_path(filename: str) -> str:
    """Get path for data file."""
    return str(DATA_DIR / filename)
