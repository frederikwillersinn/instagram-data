# Instagram data

### Description:

This repository contains code for extracting different Instagram data:
1. **Get post info by hashtag name<br>**
Input: Instagram hashtag name<br>
Output: Instagram post info (post_url, caption, like_count, media_type, media_url etc.)<br>
Tool: [Hashtag Search](https://developers.facebook.com/docs/instagram-api/guides/hashtag-search/?locale=en_US)
which is a feature of the official [Instagram Graph API](https://developers.facebook.com/docs/instagram-api/?locale=en_US)
Code: executables/get_hashtag_info_graph_api.py<br>
2. **Get user info by post url**<br>
Input: Instagram post urls<br>
Output: Instagram user info (user_name, full_name, biography, follower_count)<br>
Tool: Selenium<br>
Code: executables/get_user_info_selenium.py<br>
3. **Get post info by user name**<br>
Input: Instagram user name<br>
Output: Latest post info (user_name, full_name, upload_date, caption, likes, tagged_users, hashtags)<br>
Tool: Instascrape<br>
Code: executables/get_user_posts_instascrape.py<br>

### Requirements

Instagram Graph API:
- An [Instagram Business Account](https://help.instagram.com/502981923235522)
or [Instagram Creator Account](https://help.instagram.com/1158274571010880).
You can easily switch your account type.
- A [Facebook Page](https://developers.facebook.com/docs/instagram-api/overview#pages)
connected to that account.
- A Facebook Developer account that can perform.
[Tasks on that Page](https://developers.facebook.com/docs/instagram-api/overview#tasks).
- A registered [Facebook App](https://developers.facebook.com/docs/development#register)
with Basic settings configured (app must be a Business app).

Selenium:
- A webdriver, e.g. ChromeDriver (click [here](https://sites.google.com/chromium.org/driver/)
for ChromeDriver documentation and download).

Instascrape:
- A webdriver, e.g. ChromeDriver (click [here](https://sites.google.com/chromium.org/driver/)
for ChromeDriver documentation and download).
- An Instagram session id (click [here](http://valvepress.com/how-to-get-instagram-session-cookie/)
for instructions on how to get the session id).

### Instructions:

A. Setup

1. Run ```pip install -r requirements.txt``` in CLI<br>
This installs required packages from ```requirements.txt```.

B. Excecutables:

1. **Get post info by hashtag name<br>**
a. Ensure the Instagram Graph API is set up, credentials need to be added to
```defines.py```. Tutorial: [Instagram Graph API Access Tokens with Python](https://www.youtube.com/watch?v=c8i4CaELPME). <br>
b. In ```settings.py```, define HASHTAG_NAME, NUM_PAGES to request and MEDIA_TYPE.<br>
c. Run ```python executables/get_hashtag_info_graph_api.py``` in CLI. This writes post
info for an Instagram hashtag to a csv.<br>

2. **Get user info by post url**<br>
a. In ```settings.py```, define CHROMEDRIVER_PATH and POST_URL_LIST.
By default, the post urls from the previous step are used.<br>
b. Run ```python executables/get_user_info_selenium.py``` in CLI. This writes user info
from Instagram posts to a csv.<br>
c. Optional: Run ```python executables/preprocess_instagram_data.py``` in CLI to get a
cleaned csv.<br>

3. **Get post info by user name**<br>
a. In ```settings.py```, define Instagram USER_NAME_LIST, CHROMEDRIVER_PATH and
Instagram SESSION_ID.<br>
b. Run ```python executables/get_user_posts_instascrape.py``` in CLI. This writes recent
posts of one or more Instagram users to a csv.<br>

### Limitations

- Instagram Graph API can only access posts from Business and Creator accounts.
- Getting user info is only possible with the Instagram Graph API for users which authorized
with your app, so you can get an access token which allows you access to their content.

### Disclaimer

This is just a private side project and I am not responsible for how you use
it. Independently, this code is designed to be responsible and respectful and it is up
to you to decide what you do with it.
