""" This file contains the credentials for Instagram Graph Api and the main function
for making an API call"""
import json
import requests


def get_creds():
    """Get creds required for use in the applications
    Returns:
        dictonary: credentials needed globally
    """
    creds = {
        "access_token": "ACCESS-TOKEN",  # access token for use with all api calls (initially from debug_access_token.py, replaced with response from get_long_lived_access_token.py)
        "client_id": "FB-APP-CLIENT-ID",  # client id from Facebook app (from developers.facebook.com)
        "client_secret": "FB-APP-CLIENT-SECRET",  # client secret from Facebook app (from developers.facebook.com)
        "graph_domain": "https://graph.facebook.com/",  # base domain for api calls
        "graph_version": "v6.0",  # version of the api we are hitting
        "endpoint_base" "https://graph.facebook.com/v6.0/"  # base endpoint with domain and version
        "page_id": "FB-PAGE-ID",  # user"s Facebook page id (from get_user_pages.py)
        "instagram_account_id": "INSTAGRAM-BUSINESS-ACCOUNT-ID",  # user"s Instagram account id (from get_instagram_account.py)
        "ig_username": "IG-USERNAME"  # user"s Instagram user name
    }
    return creds


def make_api_call(url: str, endpoint_params: dict, debug: bool = False) -> dict:
    """Request data from endpoint with params
    Args:
        url: string of the url endpoint to make request from
        endpoint_params: dictionary keyed by the names of the url parameters
        debug: boolean parameter to define whether response info should be display only
    Returns:
        object: data from the endpoint
    """
    data = requests.get(url, endpoint_params)

    response = {
        "url": url,
        "endpoint_params": endpoint_params,
        "endpoint_params_pretty": json.dumps(endpoint_params, indent=4),
        "json_data": json.loads(data.content),
    }
    response["json_data_pretty"] = json.dumps(response["json_data"], indent=4)

    if debug:
        display_api_call_data(response)
    return response


def display_api_call_data(response: dict) -> None:
    """ Print out to cli response from api call """
    print("\nURL: ")
    print(response["url"])
    print("\nEndpoint Params: ")
    print(response["endpoint_params_pretty"])
    print("\nResponse: ")
    print(response["json_data_pretty"])


if __name__ == "__main__":
    creds = get_creds()
    print(creds)
