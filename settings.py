from utils import get_list_of_col_values

# Required for Instagram Graph API (get_hashtag_info_graph_api.py)
HASHTAG_NAME = "HASHTAG-OF-INTEREST"  # Hashtag of interest
NUM_PAGES = 2  # Number of Instagram pages to request, 1 page contains 25 posts
MEDIA_TYPE = "top_media"  # Type of media to request, options: "top_media", "recent_media"

FILE_NAME_POST_INFO = f"instagram_post_info_{HASHTAG_NAME}_{MEDIA_TYPE}.csv"  # Output file name

# Required for Selenium (get_user_info_selenium.py)
CHROMEDRIVER_PATH = "PATH-TO-CHROMEDRIVER"
URL_LIST = get_list_of_col_values(FILE_NAME_POST_INFO, col_name="post_url")  # List of post urls

FILE_NAME_USER_INFO = f"instagram_user_info_{HASHTAG_NAME}_{MEDIA_TYPE}.csv"  # Output file name
FILE_NAME_USER_INFO_CLEAN = f"instagram_user_info_{HASHTAG_NAME}_{MEDIA_TYPE}_clean.csv"  # Output file name

# Required for Insta-scrape (get_user_posts_instascrape.py)
SESSION_ID = "INSTAGRAM-SESSION-ID"
USER_NAME_LIST = ["USER-NAMES-OF-INTEREST"]

FILE_NAME_USER_POSTS = f"instagram_user_posts.csv"  # Output file name
