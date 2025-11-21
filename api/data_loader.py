# data_loader.py
import pandas as pd, os
from pathlib import Path

# Module-level variable
df = None

try:
    _dataUrl = Path(os.getcwd()).parent / "data" / "data1.csv"
    df = pd.read_csv(_dataUrl)
    print(f"Data loaded successfully with shape: {df.shape}")
except Exception as error:
    print(f"An exception occurred: {error}")
