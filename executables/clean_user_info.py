""" This file merges Instagram Graph API output and Selenium scrape output and
preprocesses the resulting dataframe. """
import pandas as pd
import os
import numpy as np
import re
import string
import unicodedata
import sys
sys.path.insert(1, os.path.join(sys.path[0], ".."))  # allow import from parent dir
import settings as s


def clean_follower_count_col(df: pd.DataFrame, delimiter: str = ",") -> pd.DataFrame:
    """Instagram shows follower counts like so:
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


def make_small_uppercase_letters_mapping() -> dict:
    """This function is not used but shows how the mapping in small_uppercase_letters()
    is generated."""
    uppercase_letters = [i for i in string.ascii_uppercase]
    mapping = {
        unicodedata.lookup("LATIN LETTER SMALL CAPITAL " + i): i
        for i in uppercase_letters
        if i != "X"
    }
    return mapping


def small_uppercase_letters() -> dict:
    """The mapping is generated in make_small_uppercase_letters_mapping(). Small
    uppercase letters cannot be normalized by unicodedata and need to be mapped manually."""
    return {
        "ᴀ": "A",
        "ʙ": "B",
        "ᴄ": "C",
        "ᴅ": "D",
        "ᴇ": "E",
        "ꜰ": "F",
        "ɢ": "G",
        "ʜ": "H",
        "ɪ": "I",
        "ᴊ": "J",
        "ᴋ": "K",
        "ʟ": "L",
        "ᴍ": "M",
        "ɴ": "N",
        "ᴏ": "O",
        "ᴘ": "P",
        "ꞯ": "Q",
        "ʀ": "R",
        "ꜱ": "S",
        "ᴛ": "T",
        "ᴜ": "U",
        "ᴠ": "V",
        "ᴡ": "W",
        "ʏ": "Y",
        "ᴢ": "Z",
    }


def make_mathematical_monospace_digit_mapping() -> dict:
    """This function is not used but shows how the mapping in
    mathematical_monospace_digits() is generated."""
    digits = {
        0: "ZERO",
        1: "ONE",
        2: "TWO",
        3: "THREE",
        4: "FOUR",
        5: "FIVE",
        6: "SIX",
        7: "SEVEN",
        8: "EIGHT",
        9: "NINE",
    }
    mapping = {
        unicodedata.lookup("MATHEMATICAL MONOSPACE DIGIT " + text): i
        for i, text in digits.items()
    }
    return mapping


def mathematical_monospace_digits() -> dict:
    """The mapping is generated in make_mathematical_monospace_digit_mapping().
    Monospace digits cannot be normalized by unicodedata and need to be mapped manually."""
    return {
        "𝟶": 0,
        "𝟷": 1,
        "𝟸": 2,
        "𝟹": 3,
        "𝟺": 4,
        "𝟻": 5,
        "𝟼": 6,
        "𝟽": 7,
        "𝟾": 8,
        "𝟿": 9,
    }


def clean_letterlike_characters(string_input: str, email: bool = False) -> str:
    """Helpful lookup for investigating unicode characters: https://unicode.scarfboy.com
    This function cleans a string with  unicode characters.
    >>> clean_letterlike_characters('𝓕𝓲𝓻𝓼𝓽𝓷𝓪𝓶𝓮 𝓛𝓪𝓼𝓽𝓷𝓪𝓶𝓮🦄💪')
    'Firstname Lastname'
    >>> clean_letterlike_characters("ᴛᴇꜱᴛ𝟿𝟶@ɢᴍᴀɪʟ.ᴄᴏᴍ")
    'TEST90@GMAIL.COM'
    >>> clean_letterlike_characters("normal_string")
    'normal_string'
    """
    if string_input in (np.NaN, "nan"):
        return string_input
    string_output = ""  # start with an empty string
    for letter in string_input:
        if letter in mathematical_monospace_digits().keys():
            string_output += str(mathematical_monospace_digits()[letter])
        elif letter in small_uppercase_letters().keys():
            string_output += small_uppercase_letters()[letter]
        else:
            string_output += unicodedata.normalize("NFKD", letter)
    if email:  # remove non email characters
        string_output = re.sub(r"[^a-zA-Z0-9-_+@.]", "", string_output)
    else:  # extract words
        string_output = " ".join(re.findall(r"[\w-]+|\$[\.-]+", string_output))
    string_output = string_output.lstrip().rstrip()  # remove whitespace from left and right end
    string_output = re.sub(" +", " ", string_output)  # remove multiple whitespace
    return string_output


def preprocess_instagram_data(
    file_name_post_info: str = s.FILE_NAME_POST_INFO,
    file_name_user_info: str = s.FILE_NAME_USER_INFO,
    file_name_output: str = s.FILE_NAME_USER_INFO_CLEAN,
    delimiter: str = ","
) -> None:
    df_posts = pd.read_csv(file_name_post_info)
    df_users = pd.read_csv(file_name_user_info)

    print(f"Preprocessing {len(df_posts)} posts...")
    df = df_posts.merge(df_users, how="inner", on="post_url")
    df = clean_follower_count_col(df, delimiter=delimiter)
    df["full_name_clean"] = df["full_name"].apply(lambda x: clean_letterlike_characters(x))
    df["full_name_clean"] = df["full_name_clean"].str.title()
    df["email_clean"] = df["email"].apply(lambda x: clean_letterlike_characters(x, email=True))
    df["email_clean"] = df["email_clean"].str.lower()
    df = df.drop_duplicates(subset="user_name")
    df = df[[
        "post_id",
        "post_url",
        "user_name",
        "full_name",
        "full_name_clean",
        "follower_count",
        "email",
        "email_clean"
    ]]
    print(f"Done. Remaining unique users: {len(df)}")
    df.to_csv(file_name_output, index=False)


if __name__ == "__main__":
    preprocess_instagram_data(
        file_name_post_info=s.FILE_NAME_POST_INFO,
        file_name_user_info=s.FILE_NAME_USER_INFO,
        file_name_output=s.FILE_NAME_USER_INFO_CLEAN,
        delimiter=","
    )
