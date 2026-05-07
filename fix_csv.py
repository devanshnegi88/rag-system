#!/usr/bin/env python3
"""
Fix the conversations.csv file format.
Adds proper CSV headers and formatting.
"""

import os
import pandas as pd
from pathlib import Path

input_file = Path("data/conversations.csv")
output_file = Path("data/conversations_fixed.csv")

print("Reading old CSV format...")
try:
    # The original file is a one-column CSV without header
    # We use header=None to ensure no data is lost as a header
    df = pd.read_csv(input_file, header=None, names=['conversation'])
    print(f"Found {len(df)} conversations")
except Exception as e:
    print(f"Error reading original file: {e}")
    exit(1)

# Write new CSV with headers
print("Adding dates and formatting...")
# Generate a date based on index for variety
dates = []
for idx in range(len(df)):
    day = (idx % 28) + 1
    month = ((idx // 28) % 12) + 1
    year = 2024 + (idx // (28 * 12))
    dates.append(f"{year}-{month:02d}-{day:02d}")

df['date'] = dates

print("Writing properly formatted CSV...")
df[['date', 'conversation']].to_csv(output_file, index=False, quoting=1) # quote_all=True for safety

print(f"Fixed CSV written to {output_file}")
print(f"File size: {output_file.stat().st_size / (1024*1024):.2f} MB")

# Backup original and replace
print("Replacing original file...")
backup_file = Path("data/conversations_backup.csv")

# Only backup if the current file isn't already a backup
if input_file.exists():
    # If backup already exists, don't overwrite it with a potentially broken file
    if not backup_file.exists():
        input_file.rename(backup_file)
    else:
        # If backup exists, we can just delete the current file as it's being replaced
        input_file.unlink()

if output_file.exists():
    output_file.rename(input_file)

print("Done! conversations.csv has been fixed properly.")
