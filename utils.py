import pandas as pd
import re
import os
from csv import DictWriter
from typing import Union


def get_list_of_col_values(file_name: str, col_name: str) -> list:
    df = pd.read_csv(file_name)
    url_list = df[col_name].values.tolist()
    return url_list


def extract_email_from_string(input_str: str) -> Union[str, None]:
    try:
        email = re.search(r'[\w.-]+@[\w.-]+', input_str).group(0)
    except AttributeError:
        email = None
    return email


def append_dict_to_csv(file_name: str, data_dict: dict) -> None:
    """ Appends a row to an existing or a new csv file, using a dict as input. """
    if file_name not in os.listdir():
        add_header = True
    else:
        add_header = False
    with open(file_name, "a+", newline="") as write_obj:
        dict_writer = DictWriter(write_obj, fieldnames=data_dict.keys())
        if add_header:
            dict_writer.writeheader()
        dict_writer.writerow(data_dict)
