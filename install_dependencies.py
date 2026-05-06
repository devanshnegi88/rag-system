#!/usr/bin/env python3
"""
Setup script to install all dependencies for RAG System.
Run: python install_dependencies.py
"""

import subprocess
import sys
from pathlib import Path


def run_command(cmd, description):
    """Run a pip install command and show progress."""
    print(f"\n{'='*60}")
    print(f"Installing: {description}")
    print(f"{'='*60}")
    
    try:
        subprocess.check_call([sys.executable, "-m", "pip"] + cmd)
        print(f"✓ {description} installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ Failed to install {description}: {e}")
        return False


def main():
    print("\n" + "="*60)
    print("RAG SYSTEM - DEPENDENCY INSTALLATION")
    print("="*60)
    
    # List of packages to install
    packages = [
        (["install", "--upgrade", "pip"], "pip upgrade"),
        (["install", "pandas", "numpy"], "Core data packages"),
        (["install", "sentence-transformers"], "Sentence Transformers"),
        (["install", "torch", "torchvision", "torchaudio", "--index-url", "https://download.pytorch.org/whl/cpu"], "PyTorch (CPU)"),
        (["install", "transformers"], "Transformers"),
        (["install", "faiss-cpu"], "FAISS"),
        (["install", "scikit-learn"], "Scikit-learn"),
        (["install", "flask"], "Flask"),
        (["install", "-r", "requirements.txt"], "All requirements from requirements.txt"),
    ]
    
    failed = []
    
    for cmd, description in packages:
        if not run_command(cmd, description):
            failed.append(description)
    
    print("\n" + "="*60)
    print("INSTALLATION COMPLETE")
    print("="*60)
    
    if failed:
        print(f"\n⚠ Failed packages ({len(failed)}):")
        for pkg in failed:
            print(f"  - {pkg}")
        print("\nTry installing manually:")
        print("  pip install sentence-transformers faiss-cpu transformers")
    else:
        print("\n✓ All dependencies installed successfully!")
    
    print("\nNext steps:")
    print("1. Process your data:")
    print("   python main.py --csv data/conversations.csv --output results --no-api")
    print("\n2. Or launch the API:")
    print("   python main.py --csv data/conversations.csv --port 5000")
    print("\n3. Then query the API in another terminal:")
    print("   python example_client.py")
    print("\n" + "="*60 + "\n")


if __name__ == "__main__":
    main()
