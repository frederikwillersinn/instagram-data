""" This file queries top posts for the specified Instagram hashtag, using the
Instagram Graph API and writes the repsonse to csv. """
import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], ".."))  # allow import from parent dir
import settings as s
from utils import append_dict_to_csv
from instagram_graph_api_setup.defines import get_creds, make_api_call


def get_hashtag_info_graph_api(params: dict) -> dict:
    """Get info on a hashtag
    API Endpoint:
        https://graph.facebook.com/{graph-api-version}/ig_hashtag_search?user_id={user-id}&q={hashtag-name}&fields={fields}
    Returns:
        object: data from the endpoint
    """
    endpoint_params = {
        "user_id": params["instagram_account_id"],
        "q": params["hashtag_name"],
        "fields": "id,name",  # fields to get back
        "access_token": params["access_token"],
    }
    url = params["endpoint_base"] + "ig_hashtag_search"
    response = make_api_call(url, endpoint_params, params["debug"])
    return response


def get_hashtag_posts_graph_api(params: dict, paging_url: str = "") -> dict:
    """Get posts for a hashtag
    API Endpoints:
        https://graph.facebook.com/{graph-api-version}/{ig-hashtag-id}/top_media?user_id={user-id}&fields={fields}
        https://graph.facebook.com/{graph-api-version}/{ig-hashtag-id}/recent_media?user_id={user-id}&fields={fields}
    Returns:
        object: data from the endpoint
    Docs:
    https://developers.facebook.com/docs/instagram-api/reference/ig-hashtag/top-media,
    https://developers.facebook.com/docs/instagram-api/reference/ig-hashtag/recent-media
    """
    endpoint_params = {
        "user_id": params["instagram_account_id"],
        "fields": "id,children,caption,comment_count,like_count,media_type,media_url,permalink",  # fields to get back
        "access_token": params["access_token"],
    }
    if paging_url == "":  # get first page
        url = params["endpoint_base"] + params["hashtag_id"] + "/" + params["type"]
    else:  # get specific page
        url = paging_url
    response = make_api_call(url, endpoint_params, params["debug"])
    return response


def main_loop_get_hashtag_info_graph_api(
    hashtag_name: str = s.HASHTAG_NAME,
    num_pages: int = s.NUM_PAGES,
    file_name: str = s.FILE_NAME_POST_INFO,
) -> None:
    """
    Args:
        hashtag_name: hashtag to request
        num_pages: number of pages to request
        file_name: filename of output csv file
    Returns:
    """
    params = get_creds()
    params["hashtag_name"] = hashtag_name
    hashtag_info_response = get_hashtag_info_graph_api(params)
    params["hashtag_id"] = hashtag_info_response["json_data"]["data"][0]["id"]
    params["type"] = "top_media"
    for num_page in range(1, num_pages + 1):  # loop over pages
        print(f"Collecting #{hashtag_name} posts from page {num_page}...")
        if num_page == 1:
            url_next_page = ""
        else:
            url_next_page = hashtag_top_media_response["json_data"]["paging"]["next"]
        hashtag_top_media_response = get_hashtag_posts_graph_api(params, paging_url=url_next_page)
        for post in hashtag_top_media_response["json_data"]["data"]:  # loop over posts
            data = {
                "post_id": post["id"],
                "post_url": post["permalink"],
                "caption": post["caption"],
                "media_type": post["media_type"],
                "like_count": post["like_count"],
            }
            append_dict_to_csv(file_name=file_name, data_dict=data)
    print("Done.")


if __name__ == "__main__":
    main_loop_get_hashtag_info_graph_api(
        hashtag_name=s.HASHTAG_NAME,
        num_pages=s.NUM_PAGES,
        file_name=s.FILE_NAME_POST_INFO,
    )
