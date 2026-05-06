@echo off
REM Setup script for RAG System on Windows

echo Installing RAG System dependencies...
echo.

cd /d "%~dp0"

echo Upgrading pip...
python -m pip install --upgrade pip

echo.
echo Installing required packages (this may take 2-5 minutes)...
echo.

pip install pandas numpy
echo ✓ Core data packages installed

pip install sentence-transformers
echo ✓ Sentence transformers installed

pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
echo ✓ PyTorch installed

pip install transformers
echo ✓ Transformers installed

pip install faiss-cpu
echo ✓ FAISS installed

pip install scikit-learn
echo ✓ Scikit-learn installed

pip install flask
echo ✓ Flask installed

echo.
echo ======================================================
echo Dependencies installed successfully!
echo.
echo To process your data, run:
echo   python main.py --csv data/conversations.csv --output results --no-api
echo.
echo To launch the API, run:
echo   python main.py --csv data/conversations.csv --port 5000
echo ======================================================
echo.

pause
