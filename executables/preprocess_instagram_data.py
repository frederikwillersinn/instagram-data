""" This file merges Instagram Graph API output and Selenium scrape output and
preprocesses the resulting dataframe. """
import pandas as pd
import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], ".."))  # allow import from parent dir
import settings as s


def clean_follower_count_col(df: pd.DataFrame, delimiter: str = ",") -> pd.DataFrame:
    """ Instagram shows follower counts like so:
    German format: 101, 1.001, 10,1k, 101k, 1,1m, 101m
    English format: 101, 1,001, 10.1k, 101k, 1.1m, 101m
    This function cleans the string type follower_count and returns them as integer.
    >>> df = pd.DataFrame({"id": [1,2,3,4,5,6], "follower_count": ["101", "1.001", "10,1k", "101k", "1,1m", "101m"]})
    >>> df = clean_follower_count_col(df, delimiter=",")
    >>> df
       id  follower_count
    0   1             101
    1   2            1001
    2   3           10100
    3   4          101000
    4   5         1100000
    5   6       101000000
    """
    if delimiter == ",":
        thousands_separator = "."
    elif delimiter == ".":
        thousands_separator = ","
    else:
        raise ValueError(f"Delimiter '{delimiter}' not supported.")
    df["follower_count"] = df["follower_count"].map(
        lambda x: str(x).replace(delimiter, "").replace("k", "00")
        if "k" in str(x) and delimiter in str(x)
        else str(x).replace("k", "000")
        if "k" in str(x) and delimiter not in str(x)
        else str(x).replace(delimiter, "").replace("m", "00000")
        if "m" in str(x) and delimiter in str(x)
        else str(x).replace("m", "000000")
        if "m" in str(x) and delimiter not in str(x)
        else str(x).replace(thousands_separator, "")
    )
    df["follower_count"] = df["follower_count"].astype(int)
    return df


def preprocess_instagram_data(
    file_name_post_info: str = s.FILE_NAME_POST_INFO,
    file_name_user_info: str = s.FILE_NAME_USER_INFO,
    file_name_output: str = s.FILE_NAME_OUTPUT,
    delimiter: str = ","
) -> None:
    df_posts = pd.read_csv(file_name_post_info)
    df_users = pd.read_csv(file_name_user_info)

    print(f"Preprocessing {len(df_posts)} posts...")
    df = df_posts.merge(df_users, how="inner", on="post_url")
    df = clean_follower_count_col(df, delimiter=delimiter)
    df = df.drop_duplicates(subset="user_name")
    df = df[["post_id", "post_url", "user_name", "full_name", "follower_count", "email"]]
    print(f"Done. Remaining unique users: {len(df)}")
    df.to_csv(file_name_output, index=False)


if __name__ == "__main__":
    preprocess_instagram_data(
        file_name_post_info=s.FILE_NAME_POST_INFO,
        file_name_user_info=s.FILE_NAME_USER_INFO,
        file_name_output=s.FILE_NAME_OUTPUT,
        delimiter=","
    )
