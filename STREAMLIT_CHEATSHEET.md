# 📱 Streamlit UI Cheat Sheet

## Interface Overview

```
┌─────────────────────────────────────────────────────────────┐
│  🤖 RAG Chatbot System              [🔄] [Settings]    [⚙️]  │
└─────────────────────────────────────────────────────────────┘

┌──────────────────┐  ┌──────────────────────────────────────┐
│  Sidebar         │  │  Main Content Area                   │
│                  │  │                                      │
│ Navigation:      │  │  💬 Chat                            │
│ 💬 Chat          │  │  ✅ Persona                         │
│ 👤 Persona       │  │  📚 Topics                          │
│ 📚 Topics        │  │  ℹ️  About                          │
│ ℹ️  About         │  │                                      │
│                  │  │  [Chat Messages displayed here]     │
│ Settings:        │  │                                      │
│ ✓ Show Metadata  │  │  User: What are your habits?        │
│ ✓ Show Sources   │  │                                      │
│                  │  │  Bot: Here are your habits...       │
│ System Status:   │  │  └─ Intent: Habits                  │
│ ✅ Ready         │  │     Confidence: 0.85                │
│ Messages: 1,200  │  │     Sources: [View]                 │
│ Topics: 8        │  │                                      │
└──────────────────┘  └──────────────────────────────────────┘
```

---

## 💬 Chat Tab Features

### User Message
```
┌─────────────────────────────────────┐
│ 👤 You:                             │
│                                     │
│ What are the main personality       │
│ traits?                             │
└─────────────────────────────────────┘
```

### Bot Response
```
┌─────────────────────────────────────┐
│ 🤖 Chatbot:                         │
│                                     │
│ Based on the conversation, here     │
│ are the main traits found:          │
│ • Friendly (0.92 score)             │
│ • Curious (0.87 score)              │
│ • Enthusiastic (0.79 score)         │
│                                     │
│ 👤 Intent: Persona                  │
│ 🎯 Confidence: 0.89                 │
│ 📚 Sources: 3                       │
│    [📖 View Sources]                │
└─────────────────────────────────────┘
```

### Sidebar Chat Options
```
Settings
☑ Show Message Metadata
☑ Show Source Details
  └─ Shows full message text when expanding

[🗑️ Clear Chat History]
  └─ Resets all messages
```

---

## 👤 Persona Tab Layout

```
┌─────────────────────────────────────┐
│ 🎯 Habits                           │
│ • Drinks coffee daily (Evidence: 7) │
│ • Exercises on weekends (Ev: 4)     │
│                                     │
├─────────────────────────────────────┤
│ 📝 Communication Style              │
│ • Verbosity: Moderate               │
│ • Formality: Casual                 │
│ • Emoji Usage: Yes                  │
│                                     │
├─────────────────────────────────────┤
│ 💭 Traits                           │
│ • Sentiment: Positive (0.78)        │
│ • Curiosity: High (0.82)            │
│ • Enthusiasm: High (0.74)           │
│                                     │
├─────────────────────────────────────┤
│ 📋 Facts                            │
│ • Lives in San Francisco            │
│ • Works as a software engineer      │
│ • Has 2 dogs                        │
└─────────────────────────────────────┘
```

---

## 📚 Topics Tab Layout

```
┌─────────────────────────────────────┐
│ Total Topics: 8                     │
│                                     │
│ 📌 Topic 1: Weekend Plans           │
│   ├─ Messages: 15                   │
│   ├─ Range: 0-15                    │
│   ├─ Keywords: weekend, hiking,     │
│   │              plans              │
│   └─ Summary: Discussion about...   │
│                                     │
│ 📌 Topic 2: Work Updates            │
│   ├─ Messages: 23                   │
│   ├─ Range: 16-39                   │
│   ├─ Keywords: project, deadline,   │
│   │              team                │
│   └─ Summary: Discussed ongoing...  │
│                                     │
│ 📌 Topic 3: Tech Topics             │
│   └─ [Click to expand]              │
└─────────────────────────────────────┘
```

---

## Example Questions & Responses

### Question Type 1: Persona
```
Input: "Tell me about their communication style"

Output:
✓ Intent: Persona
✓ Confidence: 0.87
✓ Response: "Their communication style shows:
   - Moderate verbosity (average message: 45 words)
   - Casual formality level
   - Frequent emoji usage (48% of messages)
   - Friendly and approachable tone"
```

### Question Type 2: Habits
```
Input: "What are repeated patterns?"

Output:
✓ Intent: Habits
✓ Confidence: 0.92
✓ Response: "Repeated patterns identified:
   - Morning coffee mentions (8 times)
   - Weekend hiking trips (5 times)
   - Weekly gym visits (7 times)
   - Evening gaming sessions (12 times)"
```

### Question Type 3: General
```
Input: "Summarize everything"

Output:
✓ Intent: General
✓ Confidence: 0.81
✓ Response: "This conversation covered 8 main topics:
   1. Weekend plans and hobbies
   2. Work projects and deadlines
   3. Tech discussions
   4. Personal achievements
   ..."
```

---

## 🎮 Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `Enter` | Send message in chat |
| `Ctrl+C` | Stop Streamlit server |
| `R` | Rerun app |
| `C` | Clear app cache |

---

## 🎨 UI Colors & Meanings

| Color | Meaning |
|-------|---------|
| 🔵 Blue | Your messages (user input) |
| ⚫ Gray | Bot responses |
| 🟡 Yellow | System messages |
| 🟣 Purple | Persona cards |
| 🔴 Pink | Topic cards |
| 🟢 Green | Success indicators |
| 🔴 Red | Errors/warnings |

---

## ⚡ Quick Actions

### Clear Chat
```
Sidebar → [🗑️ Clear Chat History]
```

### View Source Messages
```
Message → [📖 View Sources] → [View full message]
```

### Toggle Metadata
```
Sidebar → ☑ Show Message Metadata (check/uncheck)
```

### Explore a Topic
```
Topics Tab → [📌 Topic Name] → [Expand card]
```

### View Persona Details
```
Persona Tab → Scroll through sections
```

---

## 📊 Sidebar Metrics

```
System Status
├─ Status: ✅ Ready or ❌ Error
├─ Messages Indexed: 1,234
└─ Topics Detected: 8
```

What it tells you:
- ✅ = System fully loaded and ready
- Number = Amount of data processed
- Helps verify everything is working

---

## 🚨 Common Issues & Quick Fixes

| Issue | Fix |
|-------|-----|
| "Failed to load system" | Check all data files exist |
| Port 8501 busy | Use different port (see guide) |
| Slow first load | Normal! Building indexes |
| No responses | Check data file format |
| Sources not showing | Enable "Show Message Metadata" |

---

## 📝 Tips & Tricks

1. **Ask follow-up questions** - Bot remembers chat history
2. **View sources** - Click to see original message references
3. **Check intent** - Shows if bot understood your category
4. **Explore topics** - Expand cards to see summaries
5. **Toggle metadata** - Hide details for cleaner chat
6. **Clear history** - Fresh start anytime
7. **Check status** - Sidebar shows if ready

---

## 🔗 Documentation Links

Quick Links from UI:
- **About Tab** → Full system documentation
- **Source badges** → Original message references
- **Topic cards** → Keyword and summary details
- **Persona sections** → Evidence counts for each item

---

## 🎯 Pro Tips

✨ **For best experience:**
- Keep metadata on to see intent classification
- Expand sources to understand how bot answered
- Use the About tab to learn feature
- Check Topics first to understand data
- Ask specific questions for better responses

---

**Need help?** See STREAMLIT_GUIDE.md for complete documentation
