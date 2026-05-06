# ⚡ QUICK SETUP - Run These Commands

## Step 1: Install Dependencies (Choose ONE method)

### Method A: Python Script (Recommended)
```powershell
cd "c:\Users\DELL\Downloads\rag system"
python install_dependencies.py
```

### Method B: Batch Script (Windows)
```powershell
cd "c:\Users\DELL\Downloads\rag system"
.\setup.bat
```

### Method C: Manual pip
```powershell
cd "c:\Users\DELL\Downloads\rag system"
pip install -r requirements.txt
```

---

## Step 2: Process Your Data (No API)

```powershell
cd "c:\Users\DELL\Downloads\rag system"
python main.py --csv data/conversations.csv --output results --no-api
```

**This will:**
- Load your 12.6 MB conversation file
- Detect topics dynamically
- Extract persona (habits, facts, traits, communication style)
- Save results to `results/` folder

**Expected output:** 3 files
- `topic_summaries.json` - All detected topics with summaries
- `topic_summaries_checkpoints.json` - 100-message checkpoints
- `persona.json` - Extracted persona from all conversations

---

## Step 3: Launch API (Optional)

After processing, start the chatbot API:

```powershell
cd "c:\Users\DELL\Downloads\rag system"
python main.py --csv data/conversations.csv --port 5000
```

Then in another terminal query it:
```powershell
python example_client.py
```

Or use curl:
```powershell
curl -X POST http://localhost:5000/chat `
  -H "Content-Type: application/json" `
  -d '{"query": "Tell me about yourself"}'
```

---

## ✅ What You'll Get

### From Processing
- **12.6 MB** of conversation data
- **4 conversations** from your CSV
- Topics with labels, keywords, and summaries
- Persona with habits, facts, traits, and communication style
- FAISS retrieval index for searching

### Files Generated
```
results/
├── topic_summaries.json                  # Topics detected
├── topic_summaries_checkpoints.json      # 100-msg checkpoints
├── persona.json                          # Extracted persona
└── faiss_index/                          # Retrieval index
    ├── faiss_index.bin
    └── metadata.json
```

---

## 📋 Requirements Check

Before starting, verify you have:
- ✓ Python 3.8+ (`python --version`)
- ✓ pip installed (`pip --version`)
- ✓ ~6 GB free disk space (for models)
- ✓ ~2 GB RAM available

Check with:
```powershell
python --version
pip --version
```

---

## 🆘 Troubleshooting

### "ModuleNotFoundError: No module named 'sentence_transformers'"
→ Run step 1 again: `python install_dependencies.py`

### "pip: command not found"
→ Use: `python -m pip install ...`

### Port 5000 already in use
→ Use different port: `python main.py --csv data/conversations.csv --port 8000`

### Out of memory
→ Your file is 12.6 MB which should fit. If issues:
- Close other applications
- Try: `python main.py --csv data/conversations.csv --output results --no-api`

### Slow installation
→ First-time model downloads are slow (sentence-transformers: ~100MB, transformers: ~1.5GB)
→ Once downloaded, subsequent runs are much faster

---

## 🚀 After Installation

1. **Check the results:**
   ```powershell
   # View topic summaries
   type results\topic_summaries.json
   
   # View extracted persona
   type results\persona.json
   ```

2. **View in Python:**
   ```python
   import json
   with open('results/persona.json') as f:
       persona = json.load(f)
   print(json.dumps(persona, indent=2))
   ```

3. **Query the API:**
   - Run Step 3 (Launch API)
   - Use `example_client.py`
   - Or make raw HTTP requests

---

## 📞 Need Help?

1. Check **INSTALLATION_GUIDE.md** for detailed instructions
2. Run **test_system.py** to validate setup: `python test_system.py --csv example_data.csv`
3. Review **README.md** for full documentation

---

## 🎯 Summary

Your CSV file is ready at: `c:\Users\DELL\Downloads\rag system\data\conversations.csv`

Run this now:
```powershell
cd "c:\Users\DELL\Downloads\rag system"
python install_dependencies.py
python main.py --csv data/conversations.csv --output results --no-api
```

Then check the `results/` folder!
