#!/usr/bin/env python3
"""
Test script to validate RAG system installation and functionality.

Run this after installing dependencies to ensure everything works.

Usage:
    python test_system.py

Or with example data:
    python test_system.py --csv example_data.csv
"""

import argparse
import sys
import logging
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def test_imports():
    """Test that all required modules can be imported."""
    logger.info("Testing imports...")
    
    try:
        import pandas as pd
        logger.info("✓ pandas")
    except ImportError as e:
        logger.error(f"✗ pandas: {e}")
        return False
    
    try:
        import numpy as np
        logger.info("✓ numpy")
    except ImportError as e:
        logger.error(f"✗ numpy: {e}")
        return False
    
    try:
        from sentence_transformers import SentenceTransformer
        logger.info("✓ sentence-transformers")
    except ImportError as e:
        logger.error(f"✗ sentence-transformers: {e}")
        return False
    
    try:
        import faiss
        logger.info("✓ faiss")
    except ImportError as e:
        logger.error(f"✗ faiss: {e}")
        return False
    
    try:
        from transformers import pipeline
        logger.info("✓ transformers")
    except ImportError as e:
        logger.error(f"✗ transformers: {e}")
        return False
    
    try:
        from flask import Flask
        logger.info("✓ flask")
    except ImportError as e:
        logger.error(f"✗ flask: {e}")
        return False
    
    return True


def test_modules():
    """Test that all project modules can be imported."""
    logger.info("\nTesting project modules...")
    
    try:
        from processing.loader import ConversationLoader
        logger.info("✓ processing.loader")
    except ImportError as e:
        logger.error(f"✗ processing.loader: {e}")
        return False
    
    try:
        from rag.topic_detection import TopicDetector
        logger.info("✓ rag.topic_detection")
    except ImportError as e:
        logger.error(f"✗ rag.topic_detection: {e}")
        return False
    
    try:
        from rag.summarization import SummarizationEngine
        logger.info("✓ rag.summarization")
    except ImportError as e:
        logger.error(f"✗ rag.summarization: {e}")
        return False
    
    try:
        from rag.retrieval import HybridRetriever
        logger.info("✓ rag.retrieval")
    except ImportError as e:
        logger.error(f"✗ rag.retrieval: {e}")
        return False
    
    try:
        from rag.indexing import RAGIndexer
        logger.info("✓ rag.indexing")
    except ImportError as e:
        logger.error(f"✗ rag.indexing: {e}")
        return False
    
    try:
        from persona.extractor import PersonaExtractor
        logger.info("✓ persona.extractor")
    except ImportError as e:
        logger.error(f"✗ persona.extractor: {e}")
        return False
    
    try:
        from chatbot.api import ChatbotAPI
        logger.info("✓ chatbot.api")
    except ImportError as e:
        logger.error(f"✗ chatbot.api: {e}")
        return False
    
    return True


def test_models():
    """Test that models can be downloaded and loaded."""
    logger.info("\nTesting model loading (this may take a minute)...")
    
    try:
        logger.info("  Loading sentence-transformer model...")
        from sentence_transformers import SentenceTransformer
        model = SentenceTransformer('all-MiniLM-L6-v2')
        
        # Test encoding
        embeddings = model.encode(["Hello world"])
        logger.info(f"  ✓ Model loaded, embedding shape: {embeddings.shape}")
    except Exception as e:
        logger.error(f"✗ Failed to load sentence-transformer: {e}")
        return False
    
    return True


def test_example_csv(csv_path):
    """Test system with example CSV."""
    logger.info(f"\nTesting system with {csv_path}...")
    
    try:
        from processing.loader import ConversationLoader
        
        loader = ConversationLoader(csv_path)
        conversations = loader.load()
        messages = loader.get_all_messages()
        
        logger.info(f"✓ Loaded {len(messages)} messages")
        
        if len(messages) == 0:
            logger.error("✗ No messages loaded!")
            return False
        
        # Test topic detection
        logger.info("  Testing topic detection...")
        from rag.topic_detection import TopicDetector
        detector = TopicDetector()
        topics = detector.detect_topics(messages)
        logger.info(f"  ✓ Detected {len(topics)} topics")
        
        # Test persona extraction
        logger.info("  Testing persona extraction...")
        from persona.extractor import PersonaExtractor
        extractor = PersonaExtractor()
        persona = extractor.extract(messages)
        
        habits = persona.get('habits', [])
        facts = persona.get('personal_facts', [])
        traits = persona.get('personality_traits', [])
        
        logger.info(f"  ✓ Extracted {len(habits)} habits, {len(facts)} facts, {len(traits)} traits")
        
        # Test FAISS indexing
        logger.info("  Testing FAISS indexing...")
        from rag.retrieval import HybridRetriever
        retriever = HybridRetriever()
        retriever.build_index(messages)
        logger.info("  ✓ FAISS index built")
        
        # Test retrieval
        logger.info("  Testing retrieval...")
        results = retriever.retrieve("hello", k=3)
        logger.info(f"  ✓ Retrieved {len(results)} results")
        
        logger.info("✓ All tests passed!")
        return True
        
    except Exception as e:
        logger.error(f"✗ Test failed: {e}", exc_info=True)
        return False


def main():
    """Run all tests."""
    parser = argparse.ArgumentParser(description="Test RAG system installation")
    parser.add_argument('--csv', default='example_data.csv', help='CSV file to test with')
    parser.add_argument('--skip-models', action='store_true', help='Skip model loading test')
    
    args = parser.parse_args()
    
    logger.info("=" * 60)
    logger.info("RAG System Test Suite")
    logger.info("=" * 60)
    
    all_passed = True
    
    # Test imports
    if not test_imports():
        logger.error("\n✗ Import tests failed. Please run: pip install -r requirements.txt")
        return False
    
    # Test modules
    if not test_modules():
        logger.error("\n✗ Module tests failed. Check your project structure.")
        return False
    
    # Test models
    if not args.skip_models:
        if not test_models():
            logger.error("\n✗ Model loading failed. Check your internet connection.")
            all_passed = False
    
    # Test with CSV
    csv_path = Path(args.csv)
    if csv_path.exists():
        if not test_example_csv(str(csv_path)):
            all_passed = False
    else:
        logger.warning(f"\nSkipping CSV test: {csv_path} not found")
        logger.info("To test with the example CSV, run:")
        logger.info("  python test_system.py --csv example_data.csv")
    
    logger.info("\n" + "=" * 60)
    if all_passed:
        logger.info("✓ All tests PASSED!")
        logger.info("\nYou can now run the system with:")
        logger.info("  python main.py --csv example_data.csv --port 5000")
        return True
    else:
        logger.info("⚠ Some tests failed. Check logs above.")
        return False


if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
