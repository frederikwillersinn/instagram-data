import os
import re
import sys
import time

import selenium.webdriver
from instascrape import Profile, scrape_posts
from selenium.webdriver import Chrome

sys.path.insert(1, os.path.join(sys.path[0], ".."))  # allow import from parent dir
import settings as s
from utils import append_dict_to_csv


def get_user_posts(
    webdriver: selenium.webdriver,
    user_name: str,
    posts_per_user: int,
    file_name_user_posts: str = s.FILE_NAME_USER_POSTS,
) -> None:
    headers = {
        "user-agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Mobile Safari/537.36 Edg/87.0.664.57",
        "cookie": f"sessionid={s.SESSION_ID};",
    }
    user = Profile(user_name)
    user.scrape(headers=headers)
    posts = user.get_posts(webdriver=webdriver, login_first=False, amount=posts_per_user, scrape_pause=2)
    scraped_posts, unscraped_posts = scrape_posts(posts, headers=headers, pause=2, silent=False)
    for post in scraped_posts:
        post_dict = post.to_dict()
        keys_of_interest = [
            "shortcode",
            "username",
            "full_name",
            "upload_date",
            "caption",
            "likes",
        ]
        post_dict_out = {key: post_dict[key] for key in keys_of_interest}
        post_dict_out[
            "url"
        ] = f"https://www.instagram.com/p/{post_dict_out['shortcode']}/"
        post_dict_out["tagged_users"] = re.findall("\B@\w+", post_dict_out["caption"])
        post_dict_out["hashtags"] = re.findall("\B#\w+", post_dict_out["caption"])
        append_dict_to_csv(file_name_user_posts, post_dict_out)


def main_loop_get_user_posts_instascrape(
    login_first: bool,
    login_pause: int,
    user_name_list: list,
    posts_per_user: int,
    file_name_user_posts: str = s.FILE_NAME_USER_POSTS,
) -> None:
    """This function opens a browser window, asks you to log in to Instagram and then
    scrapes user posts for the specified users."""
    webdriver = Chrome(s.CHROMEDRIVER_PATH)
    if login_first:
        webdriver.get("https://www.instagram.com")
        time.sleep(login_pause)
    for num_iteration, user_name in enumerate(user_name_list):
        print(f"Scraping user posts for user {num_iteration + 1} of {len(user_name_list)}: {user_name}...")
        get_user_posts(
            webdriver=webdriver,
            user_name=user_name,
            posts_per_user=posts_per_user,
            file_name_user_posts=file_name_user_posts,
        )
    webdriver.quit()
    print("Done.")


if __name__ == "__main__":
    main_loop_get_user_posts_instascrape(
        login_first=True,
        login_pause=30,
        user_name_list=s.USER_NAME_LIST,
        posts_per_user=10,
        file_name_user_posts=s.FILE_NAME_USER_POSTS,
    )
