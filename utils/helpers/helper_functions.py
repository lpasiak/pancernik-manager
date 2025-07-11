import json
import pandas as pd
import config
from pathlib import Path

# Pandas Selection and Filtering

def clean_sku_ean_columns(df: pd.DataFrame, *args: str) -> pd.DataFrame:
    """Standardize and clean a column in a DataFrame.
    Args:
        df (pd.DataFrame): The DataFrame to clean.
        args (str): One or more column names to clean.
    Returns:
        pd.DataFrame: The cleaned DataFrame.
    """
    filtered = df.copy()
    for col in args:
        if col in filtered.columns:
            filtered = filtered[filtered[col].notna() & filtered[col].ne('') & filtered[col].ne('#N/A')]
    return filtered

# Export Data

def export_to_json(data: dict | list, filename: str) -> None:
    """Export data to a JSON file (Saved to exports directory).
    Args:
        data (dict | list): The data to export.
        filename (str): The name of the file to export to.
    Returns:
        None
    """
    filepath = config.EXPORTS_DIR / Path(filename)
    filepath.parent.mkdir(parents=True, exist_ok=True)

    with open(filepath, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)