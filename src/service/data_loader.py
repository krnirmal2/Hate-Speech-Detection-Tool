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
    df = pd.read_csv(
        file_path,
        engine="python",  # use Python engine (handles malformed CSV better)
        on_bad_lines="skip",  # skip lines like row 337
        quoting=1,  # handle quoted strings safely
        encoding="utf-8",
    )
    # Drop rows with missing or empty username/text
    df.dropna(subset=["username", "tweets"], inplace=True)

    # Remove retweets, duplicate entries
    df.drop_duplicates(subset=["username", "tweets"], inplace=True)

    # Remove bot-like users (e.g., usernames with @ symbols or repeated chars)
    df = df[df["username"].str.contains("@") == False]

    # Reset index
    df.reset_index(drop=True, inplace=True)

    return df
