""" This file opens a browser window, asks you to log in to Instagram and then starts
scraping user information for the post_urls in file_name_post_info. """
import os
import sys
import time

import selenium.webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

sys.path.insert(1, os.path.join(sys.path[0], ".."))  # allow import from parent dir
import settings as s
from utils import get_list_of_col_values, extract_email_from_string, append_dict_to_csv


def get_user_info_selenium(
        webdriver: selenium.webdriver, post_url: str, file_name_user_info: str
) -> None:
    user_info = {"post_url": post_url}

    webdriver.get(post_url)
    webdriver.find_element(
        By.XPATH,
        "//div[@id='react-root']/section/main/div/div/article/header/div[2]/div/div/span/a",
    ).click()
    WebDriverWait(webdriver, 10).until(
        expected_conditions.visibility_of_element_located((By.CSS_SELECTOR, ".fKFbl"))
    )
    try:
        user_info["user_name"] = webdriver.find_element(By.CSS_SELECTOR, ".fKFbl").text
    except NoSuchElementException:
        user_info["user_name"] = None
    try:
        user_info["full_name"] = webdriver.find_element(By.XPATH, "//h1").text
    except NoSuchElementException:
        user_info["full_name"] = None
    try:
        user_info["follower_count"] = webdriver.find_element(
            By.CSS_SELECTOR, ".Y8-fY:nth-child(2) .g47SY"
        ).text
    except NoSuchElementException:
        user_info["follower_count"] = None
    try:
        user_info["biography"] = webdriver.find_element(By.XPATH, "//div[2]/span").text
    except NoSuchElementException:
        user_info["biography"] = None
    try:
        user_info["email"] = extract_email_from_string(user_info["biography"])
    except TypeError:
        user_info["email"] = None
    append_dict_to_csv(file_name=file_name_user_info, data_dict=user_info)


def main_loop_get_user_info_selenium(
        num_first_post: int = 1,
        num_last_post: int = None,
        login_first: bool = True,
        login_pause: int = 60,
        scrape_pause: int = 10,
        file_name_post_info: str = s.FILE_NAME_POST_INFO,
        file_name_user_info: str = s.FILE_NAME_USER_INFO,
):
    """This function opens a browser window, asks you to log in to Instagram and then
    starts scraping user information for the post_urls in file_name_post_info."""
    webdriver = Chrome(s.CHROMEDRIVER_PATH)
    if login_first:
        webdriver.get("https://www.instagram.com")
        time.sleep(login_pause)
    url_list = get_list_of_col_values(file_name_post_info, "post_url")
    url_list = url_list[num_first_post - 1: num_last_post]
    for num_iteration, url in enumerate(url_list):
        print(f"Scraping user info for post {num_iteration + 1} of {len(url_list)}...")
        get_user_info_selenium(
            webdriver=webdriver, post_url=url, file_name_user_info=file_name_user_info
        )
        time.sleep(scrape_pause)
    webdriver.quit()
    print("Done.")


if __name__ == "__main__":
    main_loop_get_user_info_selenium(
        num_first_post=1,  # Set this if scraping was interrupted for any reason
        num_last_post=None,
        login_first=True,
        login_pause=30,
        scrape_pause=10,
        file_name_post_info=s.FILE_NAME_POST_INFO,
        file_name_user_info=s.FILE_NAME_USER_INFO,
    )
