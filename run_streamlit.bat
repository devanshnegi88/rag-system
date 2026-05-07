@echo off
REM Streamlit UI Launcher for RAG Chatbot
REM This script installs dependencies and runs the Streamlit UI

echo ========================================
echo RAG Chatbot - Streamlit UI Launcher
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Error: Python is not installed or not in PATH
    pause
    exit /b 1
)

echo [1/3] Checking and installing dependencies...
pip install -q streamlit pandas numpy sentence-transformers transformers torch faiss-cpu scikit-learn flask python-dotenv

if %errorlevel% neq 0 (
    echo Error: Failed to install dependencies
    pause
    exit /b 1
)

echo [2/3] Dependencies installed successfully!
echo.
echo [3/3] Starting Streamlit UI...
echo.
echo The UI will open in your browser at: http://localhost:8501
echo Press Ctrl+C to stop the server
echo.

REM Run Streamlit app
streamlit run streamlit_app.py --logger.level=info

pause
