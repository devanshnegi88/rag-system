"""
Streamlit UI for RAG-based Chatbot System.

This provides an interactive web interface for users to:
- Chat with the intelligent chatbot
- View extracted persona information
- Explore detected topics
- See query sources and reasoning
"""

import streamlit as st
import json
import sys
import os
from typing import Dict, List
import logging

# Setup page configuration
st.set_page_config(
    page_title="RAG Chatbot",
    page_icon="💬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Add project root to path
sys.path.insert(0, os.path.dirname(__file__))

# Import chatbot components
from config import OUTPUT_DIR, DATA_DIR, RAG_CONFIG, PERSONA_CONFIG, get_output_path, PROJECT_ROOT
from processing.loader import ConversationLoader
from rag.indexing import RAGIndexer
from persona.extractor import PersonaExtractor
from chatbot.api import ChatbotAPI
from pathlib import Path

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Custom CSS for better UI
st.markdown("""
<style>
    .chat-message {
        padding: 1.5rem;
        border-radius: 0.8rem;
        margin-bottom: 1rem;
        display: flex;
        flex-direction: column;
    }
    .chat-message.user {
        background-color: #e3f2fd;
        border-left: 4px solid #2196F3;
        color: #0d47a1;
    }
    .chat-message.bot {
        background-color: #f1f8e9;
        border-left: 4px solid #4CAF50;
        color: #1b5e20;
    }
    .chat-message.system {
        background-color: #fff3cd;
        border-left: 4px solid #ffc107;
        color: #856404;
    }
    .message-content {
        margin-top: 0.5rem;
        font-size: 0.95rem;
    }
    .message-metadata {
        margin-top: 0.8rem;
        font-size: 0.85rem;
        color: #666;
        font-style: italic;
    }
    .persona-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 0.8rem;
        margin-bottom: 1rem;
    }
    .topic-card {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        color: white;
        padding: 1rem;
        border-radius: 0.8rem;
        margin-bottom: 0.8rem;
    }
    .source-badge {
        display: inline-block;
        background-color: #e0e0e0;
        color: #333;
        padding: 0.4rem 0.8rem;
        border-radius: 0.4rem;
        font-size: 0.85rem;
        margin-right: 0.5rem;
        margin-bottom: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)


@st.cache_resource
def load_system(csv_filename: str = None):
    """Load RAG system components (cached for performance)."""
    try:
        # Find CSV files in data directory
        data_files = list(DATA_DIR.glob("*.csv"))
        
        # Also check root for example_data.csv if not in data/
        root_example = PROJECT_ROOT / "example_data.csv"
        if root_example.exists() and root_example not in data_files:
            data_files.append(root_example)
            
        if not data_files:
            logger.error(f"No CSV files found in {DATA_DIR}")
            st.error(
                "❌ No data files found!\n\n"
                "Please add a CSV file to the `data/` directory with conversation data.\n\n"
                "Expected CSV format with JSON conversations or simple text format."
            )
            return None
        
        # Use selected file or default to first one
        if csv_filename:
            csv_file = next((f for f in data_files if f.name == csv_filename), data_files[0])
        else:
            # Prioritize example_data.csv if available
            example_file = next((f for f in data_files if f.name == "example_data.csv"), None)
            csv_file = example_file if example_file else data_files[0]
            
        logger.info(f"Loading conversation data from {csv_file}...")
        
        # Step 1: Load conversation data
        loader = ConversationLoader(str(csv_file))
        conversations = loader.load()
        all_messages = loader.get_all_messages()
        
        if not all_messages:
            logger.error("No messages found in CSV file")
            st.error("❌ No messages found in CSV file. Please check the file format.")
            return None
        
        logger.info(f"Loaded {len(all_messages)} messages")
        
        # Step 2: Build RAG system
        logger.info("Building RAG system...")
        rag_indexer = RAGIndexer(
            embedding_model=RAG_CONFIG['embedding_model'],
            summarization_model=RAG_CONFIG['summarization_model'],
            window_size=RAG_CONFIG['topic_window_size'],
            checkpoint_size=RAG_CONFIG['checkpoint_size'],
            gemini_api_key=RAG_CONFIG.get('gemini_api_key')
        )
        
        result = rag_indexer.build_rag_system(
            all_messages,
            save_summaries=str(OUTPUT_DIR / "topic_summaries.json"),
            save_index=str(OUTPUT_DIR / "faiss_index")
        )
        
        logger.info(f"RAG system built successfully")
        
        # Step 3: Extract persona
        logger.info("Extracting persona...")
        persona_extractor = PersonaExtractor()
        personas = persona_extractor.extract(all_messages)
        
        logger.info(f"Persona extracted successfully")
        
        # Step 4: Initialize API
        api = ChatbotAPI(rag_indexer, personas)
        
        return {
            'api': api,
            'rag_indexer': rag_indexer,
            'persona_extractor': persona_extractor,
            'persona_data': personas,
            'all_messages': all_messages
        }
    except Exception as e:
        logger.error(f"Error loading system: {e}", exc_info=True)
        error_msg = (
            "❌ Failed to load chatbot system\n\n"
            f"Error: {str(e)}\n\n"
            "Please ensure:\n"
            "1. CSV file exists in `data/` directory\n"
            "2. All required Python packages are installed\n"
            "3. Run: `pip install -r requirements.txt`"
        )
        st.error(error_msg)
        return None


def display_message(message: str, message_type: str = "bot", metadata: Dict = None):
    """Display a formatted chat message."""
    if message_type == "user":
        st.markdown(f"""
        <div class="chat-message user">
            <strong>👤 You:</strong>
            <div class="message-content">{message}</div>
        </div>
        """, unsafe_allow_html=True)
    elif message_type == "bot":
        st.markdown(f"""
        <div class="chat-message bot">
            <strong>🤖 Chatbot:</strong>
            <div class="message-content">{message}</div>
        </div>
        """, unsafe_allow_html=True)
        if metadata:
            display_metadata(metadata)
    elif message_type == "system":
        st.markdown(f"""
        <div class="chat-message system">
            <strong>ℹ️ System:</strong>
            <div class="message-content">{message}</div>
        </div>
        """, unsafe_allow_html=True)


def display_metadata(metadata: Dict):
    """Display message metadata (intent, sources, confidence)."""
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if 'intent' in metadata:
            intent_emoji = {
                'persona': '👤',
                'habits': '🎯',
                'general': '💭'
            }
            emoji = intent_emoji.get(metadata['intent'], '❓')
            st.caption(f"{emoji} **Intent:** {metadata['intent'].title()}")
    
    with col2:
        if 'confidence' in metadata:
            st.caption(f"🎯 **Confidence:** {metadata['confidence']:.2%}")
    
    with col3:
        if 'sources' in metadata and metadata['sources']:
            st.caption(f"📚 **Sources:** {len(metadata['sources'])}")
    
    # Display sources if available
    if 'sources' in metadata and metadata['sources']:
        with st.expander("📖 View Sources"):
            for i, source in enumerate(metadata['sources'], 1):
                st.markdown(f"**Source {i}:**")
                st.code(source, language="text")


def display_persona_info(persona_data: Dict):
    """Display extracted persona information."""
    st.markdown("### 👤 Extracted Persona")
    
    try:
        persona = persona_data
        
        # Display in columns
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 🎯 Habits")
            if 'habits' in persona and persona['habits']:
                for habit in persona['habits']:
                    if isinstance(habit, dict):
                        st.info(f"• {habit.get('trait', 'N/A')} (Evidence refs: {len(habit.get('evidence', []))})")
                    else:
                        st.info(f"• {habit}")
            else:
                st.info("No habits extracted yet")
        
        with col2:
            st.markdown("#### 📝 Communication Style")
            if 'communication_style' in persona and persona['communication_style']:
                style = persona['communication_style']
                st.write(f"• **Verbosity:** {style.get('verbosity', 'N/A')}")
                st.write(f"• **Formality:** {style.get('formality', 'N/A')}")
                st.write(f"• **Emoji Usage:** {'Yes' if style.get('emoji_usage') else 'No'}")
                st.write(f"• **Avg Length:** {style.get('avg_message_length', 'N/A')} chars")
            else:
                st.info("No communication style data")
        
        col3, col4 = st.columns(2)
        
        with col3:
            st.markdown("#### 💭 Traits")
            if 'personality_traits' in persona and persona['personality_traits']:
                for trait in persona['personality_traits']:
                    strength_pct = int(trait.get('strength', 0) * 100)
                    st.write(f"• **{trait.get('trait', 'N/A').title()}:** {strength_pct}%")
            else:
                st.info("No traits extracted")
        
        with col4:
            st.markdown("#### 📋 Facts")
            if 'personal_facts' in persona and persona['personal_facts']:
                for fact in persona['personal_facts']:
                    st.write(f"• **{fact.get('category', 'N/A').title()}:** {fact.get('fact', 'N/A')}")
            else:
                st.info("No facts extracted")
    
    except Exception as e:
        st.error(f"Error displaying persona: {e}")


def display_topics_info(rag_indexer):
    """Display detected topics."""
    st.markdown("### 📚 Detected Topics")
    
    try:
        topics = rag_indexer.topics
        
        if not topics:
            st.info("No topics detected yet")
            return
        
        st.write(f"**Total Topics:** {len(topics)}")
        
        for topic in topics:
            with st.expander(f"📌 Topic {topic['topic_id']}: {topic.get('label', 'Unlabeled')}"):
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric("Messages", len(topic.get('messages', [])))
                
                with col2:
                    st.metric("Range", f"{topic.get('start_idx', 'N/A')}-{topic.get('end_idx', 'N/A')}")
                
                with col3:
                    st.metric("Keywords", len(topic.get('keywords', [])))
                
                if 'keywords' in topic:
                    st.write("**Keywords:**")
                    keywords_str = ", ".join(topic['keywords'][:10])
                    st.caption(keywords_str)
                
                if 'summary' in topic:
                    st.write("**Summary:**")
                    st.write(topic['summary'])
    
    except Exception as e:
        st.error(f"Error displaying topics: {e}")


def main():
    """Main Streamlit application."""
    # Sidebar
    with st.sidebar:
        st.markdown("## 🤖 RAG Chatbot System")
        
        page = st.radio(
            "Select View:",
            ["💬 Chat", "👤 Persona", "📚 Topics", "ℹ️ About"],
            index=0
        )
        
        st.divider()
        
        st.markdown("### Data Settings")
        # Get list of available CSV files
        available_files = list(DATA_DIR.glob("*.csv"))
        root_example = PROJECT_ROOT / "example_data.csv"
        if root_example.exists() and root_example not in available_files:
            available_files.append(root_example)
            
        file_names = [f.name for f in available_files]
        
        # Try to find example_data.csv index
        default_idx = 0
        if "example_data.csv" in file_names:
            default_idx = file_names.index("example_data.csv")
            
        selected_file = st.selectbox(
            "Select Data File:",
            file_names,
            index=default_idx
        )
        
        st.divider()
        
        st.markdown("### UI Settings")
        show_metadata = st.checkbox("Show Message Metadata", value=True)
        show_sources = st.checkbox("Show Source Details", value=True)
        
        st.divider()
        st.markdown("### System Status")
        
        system = load_system(selected_file)
        if system:
            st.success("✅ System Ready")
            st.metric("Messages Indexed", len(system['all_messages']) if system['all_messages'] else 0)
            st.metric("Topics Detected", len(system['rag_indexer'].topics) if system['rag_indexer'].topics else 0)
        else:
            st.error("❌ System Error")
    
    # Main content area
    system = load_system(selected_file)
    
    if not system:
        st.error("Failed to load chatbot system. Please check the logs.")
        return
    
    # Page routing
    if page == "💬 Chat":
        st.markdown("## 💬 Chat Interface")
        
        # Initialize chat history in session state
        if "messages" not in st.session_state:
            st.session_state.messages = []
        
        # Display chat history
        for msg in st.session_state.messages:
            display_message(
                msg["content"],
                msg["type"],
                msg.get("metadata")
            )
        
        # Chat input
        user_input = st.chat_input("Type your question here...")
        
        if user_input:
            # Display user message
            display_message(user_input, "user")
            st.session_state.messages.append({
                "type": "user",
                "content": user_input
            })
            
            # Get bot response
            with st.spinner("🤔 Thinking..."):
                try:
                    response = system['api']._handle_chat(user_input)
                    bot_message = response.get('response', 'Sorry, I could not generate a response.')
                    
                    # Display bot message
                    metadata = {
                        'intent': response.get('intent'),
                        'confidence': response.get('confidence'),
                        'sources': response.get('sources', [])
                    } if show_metadata else None
                    
                    display_message(bot_message, "bot", metadata)
                    
                    st.session_state.messages.append({
                        "type": "bot",
                        "content": bot_message,
                        "metadata": metadata
                    })
                
                except Exception as e:
                    logger.error(f"Error getting chatbot response: {e}")
                    error_msg = f"An error occurred: {str(e)}"
                    display_message(error_msg, "bot")
                    st.session_state.messages.append({
                        "type": "bot",
                        "content": error_msg
                    })
        
        # Clear chat button
        if st.button("🗑️ Clear Chat History"):
            st.session_state.messages = []
            st.rerun()
    
    elif page == "👤 Persona":
        st.markdown("## 👤 Extracted Persona Information")
        st.markdown("This section shows the personality traits, habits, and communication style extracted from the conversation data.")
        st.divider()
        display_persona_info(system['persona_data'])
    
    elif page == "📚 Topics":
        st.markdown("## 📚 Conversation Topics")
        st.markdown("Topics automatically detected and analyzed from the conversation data.")
        st.divider()
        display_topics_info(system['rag_indexer'])
    
    elif page == "ℹ️ About":
        st.markdown("## 📖 About This System")
        
        st.markdown("""
        ### What is This?
        
        This is a **Retrieval-Augmented Generation (RAG)** based chatbot system that:
        
        1. **Analyzes Conversations** - Processes conversation data to extract meaningful patterns
        2. **Detects Topics** - Identifies topic shifts and semantic boundaries
        3. **Extracts Persona** - Builds a profile of habits, traits, and communication style
        4. **Answers Questions** - Uses RAG to provide context-aware responses
        
        ### Key Features
        
        ✨ **Intelligent Retrieval** - Combines dense and keyword-based search  
        🎯 **Intent Classification** - Understands whether queries are about persona, habits, or general topics  
        📊 **Topic Analysis** - Detects conversation shifts and provides summaries  
        🧠 **Personality Extraction** - Identifies habits, traits, and communication patterns  
        
        ### How It Works
        
        1. **Input Processing** - Loads and parses conversation data
        2. **RAG Pipeline** - Builds topic detection and retrieval indexes
        3. **Persona Extraction** - Analyzes communication for personality insights
        4. **Query Handling** - Routes queries and retrieves relevant information
        
        ### Navigation
        
        - **💬 Chat** - Interact with the chatbot
        - **👤 Persona** - View extracted personality information
        - **📚 Topics** - Explore detected conversation topics
        
        ### Documentation
        
        For more information, see:
        - `README.md` - Technical documentation
        - `QUICKSTART.md` - Quick start guide
        - `INSTALLATION_GUIDE.md` - Setup instructions
        """)
        
        st.divider()
        st.markdown("### System Info")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Messages Processed", len(system['all_messages']) if system['all_messages'] else 0)
        
        with col2:
            st.metric("Topics Found", len(system['rag_indexer'].topics) if system['rag_indexer'].topics else 0)
        
        with col3:
            try:
                if system['all_messages'] and system['rag_indexer'].topics:
                    st.metric("System Status", "✅")
                else:
                    st.metric("System Status", "⚠️")
            except:
                st.metric("System Status", "❌")


if __name__ == "__main__":
    main()
