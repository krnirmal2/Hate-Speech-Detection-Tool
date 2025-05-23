# src/data_loader.py

import pandas as pd

def load_data(file_path: str) -> pd.DataFrame:
    """
    Loads Twitter dataset and performs initial cleaning.

    Args:
        file_path (str): Path to the CSV file

    Returns:
        pd.DataFrame: Cleaned tweet data
    """
    df = pd.read_csv("E:\cursorAi\PYTHON\Hate-Speech-Detection-Tool\tweets_1.csv")

    # Drop rows with missing or empty username/text
    df.dropna(subset=["username", "text"], inplace=True)

    # Remove retweets, duplicate entries
    df.drop_duplicates(subset=["username", "text"], inplace=True)

    # Remove bot-like users (e.g., usernames with @ symbols or repeated chars)
    df = df[df['username'].str.contains('@') == False]

    # Reset index
    df.reset_index(drop=True, inplace=True)

    return df
