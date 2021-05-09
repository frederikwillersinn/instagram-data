# Required for Instagram Graph API (get_hashtag_info_graph_api.py)
HASHTAG_NAME = "HASHTAG-OF-INTEREST"  # Hashtag of interest
NUM_PAGES = 2  # Number of Instagram pages to request, 1 page contains 25 posts
MEDIA_TYPE = "top_media"  # Type of media to request, options: "top_media", "recent_media"

# Required for Selenium (get_user_info_selenium.py)
CHROMEDRIVER_PATH = "PATH-TO-CHROMEDRIVER"

# Required for Insta-scrape (get_user_posts_instascrape.py)
SESSION_ID = "INSTAGRAM-SESSION-ID"
USER_NAME_LIST = ["USER-NAMES-OF-INTEREST"]

# File names
FILE_NAME_USER_INFO = f"instagram_user_info_{HASHTAG_NAME}_{MEDIA_TYPE}.csv"
FILE_NAME_POST_INFO = f"instagram_post_info_{HASHTAG_NAME}_{MEDIA_TYPE}.csv"
FILE_NAME_OUTPUT = f"instagram_user_info_{HASHTAG_NAME}_{MEDIA_TYPE}_cleaned.csv"
FILE_NAME_USER_POSTS = f"instagram_user_posts.csv"
