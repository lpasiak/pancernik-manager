# Pandas Selection and Filtering

def clean_sku_ean_columns(df, *args):
    """Standardize and clean a column in a DataFrame.
    Args:
        df (pd.DataFrame): The DataFrame to clean.
        args (str): Column names to clean.
    Returns:
        pd.DataFrame: The cleaned DataFrame.
    """
    for col in args:
        if col in df.columns:
            df = df[df[col].notna() & df[col].ne('') & df[col].ne('#N/A')]

    return df