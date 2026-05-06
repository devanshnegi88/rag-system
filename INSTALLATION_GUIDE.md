# Complete Installation & Execution Guide

## Quick Start (5 minutes)

### 1. Install Dependencies
```bash
cd "rag system"
pip install -r requirements.txt
```

### 2. Run with Example Data
```bash
python main.py --csv example_data.csv --port 5000
```

The system will:
- Load conversation data
- Detect topics
- Extract persona
- Start Flask API on port 5000

### 3. Test the API
In another terminal:
```bash
# Health check
curl http://localhost:5000/health

# Chat query
curl -X POST http://localhost:5000/chat \
  -H "Content-Type: application/json" \
  -d '{"query": "Tell me about yourself"}'

# Get topics
curl http://localhost:5000/topics

# Get persona
curl http://localhost:5000/persona
```

## Validation

Run the test suite to verify everything works:
```bash
python test_system.py --csv example_data.csv
```

Expected output:
```
✓ All imports passed
✓ All modules loaded
✓ Models loaded successfully
✓ Example data processed (XX topics, YY habits, ZZ facts extracted)
```

## With Your Own Data

### CSV Format
Provide a CSV file with one of these formats:

**Option 1: JSON Array**
```csv
date,conversation
2024-01-01,"[{""sender"":""user"",""content"":""Hi""},{""sender"":""bot"",""content"":""Hello""}]"
```

**Option 2: Text format (simple)**
```csv
date,conversation
2024-01-01,"user: Hi there
assistant: Hello! How are you?"
```

### Run System
```bash
python main.py --csv your_data.csv --output results/ --port 5000
```

### Check Results
```
results/
├── topic_summaries.json              # Topics with summaries
├── topic_summaries_checkpoints.json  # 100-message checkpoints
├── persona.json                      # Extracted persona
└── faiss_index/                      # Retrieval index
```

## Advanced Options

```bash
# Process without launching API
python main.py --csv data.csv --no-api

# Custom port
python main.py --csv data.csv --port 8000

# Custom host
python main.py --csv data.csv --host 127.0.0.1 --port 5000

# Debug mode
python main.py --csv data.csv --debug
```

## Docker Deployment

### Build Image
```bash
docker build -t rag-system .
```

### Run Container
```bash
docker run -p 5000:5000 \
  -v $(pwd)/data:/app/data \
  rag-system
```

### Using Docker Compose
```bash
docker-compose up
```

## Render Deployment

See DEPLOYMENT.md for complete instructions.

Quick summary:
1. Push code to GitHub
2. Create web service on Render
3. Set build command: `pip install -r requirements.txt`
4. Set start command: `python main.py --csv data/conversations.csv --host 0.0.0.0 --port $PORT`
5. Upload CSV via Render file manager
6. Deploy

## API Client Usage

Use the Python client:
```bash
python example_client.py
```

Or programmatically:
```python
from example_client import RAGClient

client = RAGClient("http://localhost:5000")

# Chat query
response = client.chat("Tell me about yourself")
print(response['response'])

# Get topics
topics = client.get_topics()
print(f"Found {topics['total']} topics")

# Get persona
persona = client.get_persona()
print(persona['habits'])
```

## Performance Tips

1. **First run is slow** (model downloading)
   - Sentence-transformers: ~100 MB
   - Summarization model: ~1.5 GB
   - Total: ~2 GB of models

2. **For faster summarization**, use smaller model:
   ```python
   RAGIndexer(summarization_model='distilbart-cnn-6-6')
   ```

3. **For better accuracy**, use larger model:
   ```python
   RAGIndexer(embedding_model='all-mpnet-base-v2')
   ```

4. **Memory optimization** for large conversations:
   - Process in batches
   - Reduce checkpoint size
   - Use CPU-only (don't install GPU packages)

## Troubleshooting

### Error: "No module named 'sentence_transformers'"
```bash
pip install -r requirements.txt
```

### Error: "FAISS error"
```bash
pip uninstall faiss-cpu
pip install faiss-cpu
```

### Port already in use
```bash
# Use different port
python main.py --csv data.csv --port 8000

# Or kill process on port 5000
lsof -ti:5000 | xargs kill
```

### Out of memory
- Use smaller batch sizes
- Reduce checkpoint size
- Use lighter models
- Process data incrementally

### Models not downloading
```bash
# Check internet connection
# Or manually download:
from sentence_transformers import SentenceTransformer
model = SentenceTransformer('all-MiniLM-L6-v2')
```

## Next Steps

1. **Review documentation**: See README.md for detailed information
2. **Explore outputs**: Check persona.json and topic_summaries.json
3. **Tune parameters**: Adjust window_size, checkpoint_size, thresholds
4. **Add authentication**: Before production
5. **Set up database**: For persistent storage
6. **Deploy to production**: Using Docker / Render

## Support Files

- **README.md** - Complete technical documentation
- **QUICKSTART.md** - Quick reference
- **DEPLOYMENT.md** - Deployment instructions
- **PROJECT_SUMMARY.txt** - Project overview
- **test_system.py** - Validation tests
- **example_client.py** - API client examples

## Key Files

```
Main entry point:
  main.py                          # Run system

Core modules:
  processing/loader.py             # Data loading
  rag/topic_detection.py          # Topic detection
  rag/summarization.py            # Summarization
  rag/retrieval.py                # Retrieval
  rag/indexing.py                 # RAG coordinator
  persona/extractor.py            # Persona extraction
  chatbot/api.py                  # Flask API

Configuration:
  config.py                       # Configuration
  requirements.txt                # Dependencies

Examples:
  example_data.csv               # Sample data
  example_client.py              # API client

Tests:
  test_system.py                 # Validation

Deployment:
  Dockerfile                     # Container image
  docker-compose.yml             # Compose config
  DEPLOYMENT.md                  # Render guide
```

## Summary

✓ Complete production-ready RAG system
✓ Dynamic topic detection
✓ Hybrid retrieval
✓ Evidence-based persona extraction
✓ REST API with intent classification
✓ Full documentation
✓ Docker support
✓ Deployment guides

Ready to process conversations and answer questions!
