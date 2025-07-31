import pytest
import pandas as pd
from src.service.data_loader import load_data


def test_load_data_success(tmp_path):
    # Create a dummy CSV file for testing
    csv_content = "username,tweets,followers,retweet_count,reply_count\nuser1,tweet1,100,10,5\nuser2,tweet2,200,20,10\nuser3,tweet3,NA,30,15\nuser4,tweet4,,40,20\n"
    csv_file = tmp_path / "test_data.csv"
    csv_file.write_text(csv_content)

    df = load_data(str(csv_file))

    assert isinstance(df, pd.DataFrame)
    assert not df.empty
    assert "username" in df.columns
    assert "tweets" in df.columns
    assert "followers" in df.columns
    assert "retweet_count" in df.columns
    assert "reply_count" in df.columns
    assert df.shape[0] == 2  # Expecting 2 rows after dropping NA/empty for followers
    assert "user1" in df["username"].tolist()
    assert "user2" in df["username"].tolist()


def test_load_data_no_file():
    with pytest.raises(FileNotFoundError):
        load_data("non_existent_file.csv")


def test_load_data_empty_file(tmp_path):
    empty_csv = tmp_path / "empty.csv"
    empty_csv.write_text("")
    df = load_data(str(empty_csv))
    assert df.empty


def test_load_data_missing_columns(tmp_path):
    csv_content = "col1,col2\nval1,val2\n"
    csv_file = tmp_path / "missing_cols.csv"
    csv_file.write_text(csv_content)
    with pytest.raises(KeyError):
        load_data(str(csv_file))
