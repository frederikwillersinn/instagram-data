# Instagram data

### Description:

This repository contains code for gathering Instagram data:
- Step 1: Query Instagram posts (incl. post_url, caption, like_count etc.) by the
hashtag name using [Hashtag Search](https://developers.facebook.com/docs/instagram-api/guides/hashtag-search/?locale=en_US)
which is a feature of the official [Instagram Graph API](https://developers.facebook.com/docs/instagram-api/?locale=en_US).
- Step 2: Scrape the user information (user_name, full_name, biography, follower_count)
related to each post based on the post_urls using Selenium.


### Limitations
- Instagram Graph API can only access posts from Business and Creator accounts.
- Step 2 is only possible with the Instagram Graph API for users which authorized
with your app, so you can get an access token which allows you access to their content.


### Requirements
Instgram Graph API:
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
for ChromeDriver documentation and download)

### Instrutions:
1. ```pip install -r requirements.txt```<br>
Installs required packages from ```requirements.txt```

2. Ensure the Instagram Graph API is set up (credentials need to be added to ```defines.py```)<br>
Tutorial: [Instagram Graph API Access Tokens with Python](https://www.youtube.com/watch?v=c8i4CaELPME)

2. Define hashtag of interest and number of posts to request in ```settings.py```

3. Run ```python executables/get_hashtag_info_graph_api.py``` in CLI<br>
Writes posts info for Instagram hashtag to a csv

4. Run ```python executables/get_user_info_selenium.py``` in CLI<br>
Writes users info from Instagram hashtag posts step 3 to a csv

5. Run ```python executables/preprocess_instagram_data.py``` in CLI<br>
Returns csv with unique Instagram users

Disclaimer: This is just a private side project and I am not responsible for how you use
it. Independently, this code is designed to be responsible and respectful and it is up
to you to decide what you do with it.
