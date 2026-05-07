# 🚀 Quick Start - Streamlit Chatbot UI

Get your interactive chatbot UI running in 2 minutes!

## Installation & Launch

### Windows Users
```bash
run_streamlit.bat
```

### Mac/Linux/Python Users
```bash
python run_streamlit.py
```

### Manual Setup
```bash
pip install -r requirements.txt
streamlit run streamlit_app.py
```

The app opens automatically at: **http://localhost:8501** 🌐

---

## First Time Using It?

### 1️⃣ Chat Tab (💬)
- Type a question in the input box
- Examples:
  - "What are the main habits?"
  - "What topics were discussed?"
  - "Tell me about their personality"

### 2️⃣ Persona Tab (👤)
- See extracted personality traits
- View habits with evidence count
- Check communication style
- Read key facts

### 3️⃣ Topics Tab (📚)
- Explore detected topics
- See keywords and summaries
- Check message ranges

---

## Example Questions

**About Personality**
- "What are this person's main traits?"
- "How do they communicate?"
- "What habits did you detect?"

**About Topics**
- "What topics were discussed?"
- "Summarize each conversation topic"
- "What were the main subjects?"

**General Questions**
- "Tell me everything you know"
- "What patterns did you find?"
- "Give me a summary"

---

## Tips

✅ Clear chat to start fresh: Click "🗑️ Clear Chat History"  
✅ See sources: Click "📖 View Sources" to see original messages  
✅ Toggle details: Use sidebar checkboxes  
✅ Check status: Sidebar shows if system is ready  

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| Port 8501 busy | Run: `streamlit run streamlit_app.py --server.port 8502` |
| Missing dependencies | Run: `pip install -r requirements.txt` |
| Slow first load | Normal! Index building takes 30-60 seconds |
| App crashes | Check logs in terminal, ensure data files exist |

---

## What's Happening Behind the Scenes?

1. **Loads Your Data** ✓
2. **Builds Retrieval Indexes** ✓
3. **Extracts Personality** ✓
4. **Ready for Questions** ✓

---

## Want to Learn More?

📖 Full guide: See `STREAMLIT_GUIDE.md`  
📚 System details: See `README.md`  
🏗️ Setup help: See `INSTALLATION_GUIDE.md`  

---

**Happy chatting!** 🎉
