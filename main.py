#!/usr/bin/env python3
"""
Main orchestration script for RAG-based Conversation Intelligence System.

This script:
1. Loads conversation data from CSV
2. Builds the RAG system (topic detection + summarization)
3. Extracts persona from conversations
4. Launches chatbot API

Usage:
    python main.py --csv path/to/data.csv --port 5000
"""

import argparse
import logging
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from processing.loader import ConversationLoader
from rag.indexing import RAGIndexer
from persona.extractor import PersonaExtractor
from chatbot.api import ChatbotAPI
from config import RAG_CONFIG


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="RAG-based Conversation Intelligence System"
    )
    parser.add_argument(
        '--csv',
        required=True,
        help='Path to CSV file with conversation data'
    )
    parser.add_argument(
        '--output',
        default='outputs',
        help='Output directory for results'
    )
    parser.add_argument(
        '--port',
        type=int,
        default=5000,
        help='Port for chatbot API'
    )
    parser.add_argument(
        '--host',
        default='0.0.0.0',
        help='Host for chatbot API'
    )
    parser.add_argument(
        '--no-api',
        action='store_true',
        help='Skip launching API (only process data)'
    )
    parser.add_argument(
        '--debug',
        action='store_true',
        help='Enable debug mode'
    )
    
    args = parser.parse_args()
    
    # Create output directory
    output_dir = Path(args.output)
    output_dir.mkdir(exist_ok=True)
    
    try:
        # Step 1: Load conversation data
        logger.info(f"Loading conversation data from {args.csv}...")
        loader = ConversationLoader(args.csv)
        conversations = loader.load()
        all_messages = loader.get_all_messages()
        
        logger.info(f"Loaded {len(all_messages)} messages from {len(conversations)} conversation(s)")
        
        # Step 2: Build RAG system
        logger.info("Building RAG system...")
        rag_indexer = RAGIndexer(
            embedding_model=RAG_CONFIG['embedding_model'],
            summarization_model=RAG_CONFIG['summarization_model'],
            window_size=RAG_CONFIG['topic_window_size'],
            checkpoint_size=RAG_CONFIG['checkpoint_size'],
            gemini_api_key=RAG_CONFIG.get('gemini_api_key')
        )
        
        rag_result = rag_indexer.build_rag_system(
            all_messages,
            save_summaries=str(output_dir / 'topic_summaries.json'),
            save_index=str(output_dir / 'faiss_index')
        )
        
        logger.info(f"RAG system built:")
        logger.info(f"  - Topics: {rag_result['topic_count']}")
        logger.info(f"  - Checkpoints: {rag_result['checkpoint_count']}")
        
        # Step 3: Extract persona
        logger.info("Extracting persona...")
        persona_extractor = PersonaExtractor(min_repetitions=2)
        persona = persona_extractor.extract(all_messages)
        
        persona_extractor.save_persona(
            persona,
            str(output_dir / 'persona.json')
        )
        
        logger.info("Persona extraction complete")
        
        # Step 4: Launch chatbot API (if requested)
        if not args.no_api:
            logger.info(f"Launching chatbot API on {args.host}:{args.port}...")
            chatbot = ChatbotAPI(rag_indexer, persona)
            chatbot.run(host=args.host, port=args.port, debug=args.debug)
        else:
            logger.info("Data processing complete. Outputs saved to:")
            logger.info(f"  - {output_dir / 'topic_summaries.json'}")
            logger.info(f"  - {output_dir / 'topic_summaries_checkpoints.json'}")
            logger.info(f"  - {output_dir / 'persona.json'}")
            logger.info(f"  - {output_dir / 'faiss_index'}/")
    
    except FileNotFoundError as e:
        logger.error(f"File not found: {e}")
        sys.exit(1)
    except ValueError as e:
        logger.error(f"Invalid input: {e}")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Unexpected error: {e}", exc_info=True)
        sys.exit(1)


if __name__ == '__main__':
    main()
