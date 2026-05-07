# 🤖 Streamlit UI Guide - RAG Chatbot System

## Overview

The Streamlit UI provides a modern, interactive web interface for users to interact with your RAG-based chatbot system. Users can chat with the bot, explore extracted persona information, and view detected conversation topics.

## Features

### 💬 Chat Interface
- **Interactive chat** with real-time responses
- **Intent classification** showing whether queries are about persona, habits, or general topics
- **Source attribution** with message references
- **Chat history** maintained in the session
- **Confidence scoring** for query responses
- **Clear chat** functionality to reset conversation

### 👤 Persona Dashboard
- **Extracted habits** with evidence references
- **Communication style** including verbosity, formality, and emoji usage
- **Personality traits** like sentiment, curiosity, enthusiasm
- **Key facts** extracted from conversations
- **Evidence-based insights** (no hallucinations)

### 📚 Topics Explorer
- **Detected topics** from conversation data
- **Topic statistics** (message count, keyword analysis)
- **Summaries** for each detected topic
- **Keywords** associated with each topic
- **Message ranges** showing where topics occur

### ℹ️ About & System Info
- System status and health indicators
- Feature overview and how the system works
- Real-time metrics (messages processed, topics found)

## Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Quick Start

#### Option 1: Batch Script (Windows)
```bash
run_streamlit.bat
```

#### Option 2: Python Script
```bash
python run_streamlit.py
```

#### Option 3: Manual Installation
```bash
# Install dependencies
pip install -r requirements.txt

# Run Streamlit
streamlit run streamlit_app.py
```

## Usage Guide

### Starting the Application

1. Navigate to the project directory
2. Run one of the startup scripts above
3. The app will automatically open in your default browser at `http://localhost:8501`

### The Chat Interface

#### Asking Questions

The chatbot supports three types of queries:

**1. Persona Queries**
- "What are the main habits?"
- "Tell me about their communication style"
- "What traits does this person have?"
- Keywords: personality, traits, habits, characteristics, style

**2. Habits Queries**
- "What habits were detected?"
- "How often do they mention X?"
- "What patterns emerged?"
- Keywords: habits, patterns, repeated, frequently

**3. General Queries**
- "What topics were discussed?"
- "Summarize the conversation"
- "What was the main topic?"
- Keywords: anything else

#### Understanding Responses

Each response includes:

- **Message Content**: The bot's answer to your query
- **Intent**: Classification (Persona/Habits/General)
- **Confidence**: How confident the system is in the response
- **Sources**: Click to view the specific message references used

### Exploring Persona Information

Navigate to the **👤 Persona** tab to see:

- **Habits**: Repeated behaviors with message counts showing evidence
- **Communication Style**: How they write (formal/informal, verbose/concise)
- **Traits**: Personality characteristics (sentiment, curiosity, etc.)
- **Facts**: Key information explicitly mentioned

### Analyzing Topics

Go to the **📚 Topics** tab to:

- View all detected conversation topics
- Click topic cards to expand details
- See message ranges and counts
- Review keywords and summaries for each topic

## Configuration

### Sidebar Settings

**Show Message Metadata**
- Toggle to display/hide intent, confidence, and source information
- Default: On

**Show Source Details**
- Enable to see full source messages when expanding sources
- Default: On

### System Status

The sidebar displays:
- System readiness (✅ Ready or ❌ Error)
- Messages indexed count
- Topics detected count

## API Endpoints (for Flask integration)

If you're also running the Flask API, these endpoints are available:

- `POST /chat` - Send a query and get a response
- `GET /health` - Health check
- `GET /persona` - Get persona data
- `GET /topics` - Get topics list

## Performance Tips

1. **First Load**: The system builds indexes on first load. This may take a minute depending on data size.
2. **Caching**: Streamlit caches the system components, so subsequent page refreshes are fast.
3. **Large Datasets**: For conversations with 10,000+ messages, index building may take several minutes.

## Troubleshooting

### Issue: "Failed to load chatbot system"

**Solution**: Check that all required files are present:
- `config.py`
- `main.py`
- `rag/indexing.py`
- `persona/extractor.py`
- `chatbot/api.py`

Run from the project root directory.

### Issue: Missing dependencies

**Solution**: Install all dependencies:
```bash
pip install -r requirements.txt
```

### Issue: Port 8501 already in use

**Solution**: Use a different port:
```bash
streamlit run streamlit_app.py --server.port 8502
```

### Issue: Slow responses

**Solution**: 
- This is normal on first use while indexes build
- Increase Streamlit's timeout if needed:
```bash
streamlit run streamlit_app.py --client.toolbarMode=minimal
```

## Customization

### Styling

The UI includes custom CSS for a modern look. To modify colors and styles, edit the CSS section in `streamlit_app.py`:

```python
st.markdown("""
<style>
    .chat-message { ... }
    .persona-card { ... }
    .topic-card { ... }
</style>
""", unsafe_allow_html=True)
```

### Adding New Pages

To add a new tab/page:

1. Add a new option in the sidebar radio button
2. Create a new conditional block with your content
3. Example:
```python
elif page == "🔍 Search":
    st.markdown("## 🔍 Advanced Search")
    # Your content here
```

## Advanced Usage

### Running with Custom Configuration

Create a custom config and pass it:

```python
from config import Config
config = Config()
config.DATA_FILE = "path/to/your/data.csv"
# Then modify load_system() to use this config
```

### Integrating with External Systems

The Streamlit UI can be modified to:
- Fetch data from external APIs
- Save chat histories to a database
- Send messages to a messaging platform
- Log analytics for usage tracking

## Browser Compatibility

Tested on:
- Chrome/Chromium 90+
- Firefox 88+
- Safari 14+
- Edge 90+

## Keyboard Shortcuts

- `Ctrl+C` - Stop the server
- `R` - Rerun the app
- `C` - Clear cache

## File Structure

```
rag system/
├── streamlit_app.py      # Main Streamlit application
├── run_streamlit.bat     # Windows batch launcher
├── run_streamlit.py      # Python launcher (cross-platform)
├── requirements.txt      # Updated with streamlit dependency
└── ... (other project files)
```

## Performance Metrics

Typical performance (on 1,000 messages):
- Initial load: 30-60 seconds (building indexes)
- Subsequent loads: 2-5 seconds (cached)
- Query response: 1-3 seconds

## Support

For issues or questions:
1. Check the troubleshooting section above
2. Review logs in the terminal running Streamlit
3. Ensure all dependencies are correctly installed
4. Check that data files are in the correct location

## Next Steps

1. **Deploy**: See `DEPLOYMENT.md` for cloud deployment options
2. **Customize**: Modify the UI to match your branding
3. **Integrate**: Connect to your own data sources
4. **Extend**: Add new analysis features to the persona and topics sections

---

Happy chatting! 🚀
