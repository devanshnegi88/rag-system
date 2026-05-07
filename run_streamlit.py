#!/usr/bin/env python3
"""
Streamlit UI launcher for RAG Chatbot System.

This script handles:
1. Dependency installation
2. Configuration validation
3. Streamlit app launch
"""

import subprocess
import sys
import os
from pathlib import Path


def check_python_version():
    """Ensure Python 3.8 or higher is installed."""
    if sys.version_info < (3, 8):
        print(f"Error: Python 3.8+ required. You have {sys.version}")
        sys.exit(1)
    print(f"✓ Python version: {sys.version.split()[0]}")


def install_dependencies():
    """Install required packages."""
    print("\n[1/3] Installing dependencies...")
    
    packages = [
        'streamlit>=1.28.0',
        'pandas>=1.3.0',
        'numpy>=1.21.0',
        'sentence-transformers>=2.2.0',
        'transformers>=4.30.0',
        'torch>=1.9.0',
        'faiss-cpu>=1.7.3',
        'scikit-learn>=1.0.0',
        'flask>=2.0.0',
        'werkzeug>=2.0.0',
        'python-dotenv>=0.19.0'
    ]
    
    try:
        subprocess.check_call([
            sys.executable, '-m', 'pip', 'install', '-q'
        ] + packages)
        print("✓ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ Error installing dependencies: {e}")
        return False


def validate_project_structure():
    """Validate required project files exist."""
    print("\n[2/3] Validating project structure...")
    
    required_files = [
        'config.py',
        'main.py',
        'streamlit_app.py',
        'requirements.txt',
        'rag/indexing.py',
        'persona/extractor.py',
        'chatbot/api.py'
    ]
    
    missing_files = []
    for file in required_files:
        if not Path(file).exists():
            missing_files.append(file)
    
    if missing_files:
        print(f"✗ Missing files: {', '.join(missing_files)}")
        return False
    
    print("✓ Project structure valid")
    return True


def launch_streamlit():
    """Launch the Streamlit application."""
    print("\n[3/3] Starting Streamlit UI...")
    print("\n" + "="*50)
    print("RAG Chatbot - Streamlit UI")
    print("="*50)
    print("\nThe UI will open in your browser at:")
    print("👉 http://localhost:8501")
    print("\nPress Ctrl+C to stop the server")
    print("="*50 + "\n")
    
    try:
        subprocess.run([
            sys.executable, '-m', 'streamlit', 'run', 
            'streamlit_app.py',
            '--logger.level=info'
        ])
    except KeyboardInterrupt:
        print("\n\n✓ Streamlit server stopped")
        sys.exit(0)
    except Exception as e:
        print(f"\n✗ Error launching Streamlit: {e}")
        sys.exit(1)


def main():
    """Main entry point."""
    print("="*50)
    print("RAG Chatbot - Streamlit UI Launcher")
    print("="*50)
    
    # Check Python version
    check_python_version()
    
    # Install dependencies
    if not install_dependencies():
        sys.exit(1)
    
    # Validate project
    if not validate_project_structure():
        print("\nPlease ensure all project files are in the correct location.")
        sys.exit(1)
    
    # Launch Streamlit
    launch_streamlit()


if __name__ == '__main__':
    main()
