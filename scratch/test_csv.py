
import pandas as pd
from pathlib import Path

csv_path = "data/conversations.csv"
try:
    df = pd.read_csv(csv_path)
    print(f"Columns: {df.columns.tolist()}")
    print(f"First row: {df.iloc[0].values[0][:100]}...")
    print(f"Shape: {df.shape}")
except Exception as e:
    print(f"Error: {e}")
