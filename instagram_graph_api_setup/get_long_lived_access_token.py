""" This file generates a long lived access token which is valid for 90 days compared
to the regular access token which is valid only for 1 day. You should teplace the
regular access token with the long lived access token in defines.py"""
from defines import get_creds, make_api_call


def get_long_lived_access_token(params: dict) -> dict:
    """ Get long lived access token
    API Endpoint:
    https://graph.facebook.com/{graph-api-version}/oauth/access_token?grant_type=fb_exchange_token&client_id={app-id}&client_secret={app-secret}&fb_exchange_token={your-access-token}
    Returns:
        object: data from the endpoint
    """
    endpoint_params = {
        "grant_type": "fb_exchange_token",  # tell facebook we want to exchange token
        "client_id": params["client_id"],  # client id from Facebook app
        "client_secret": params["client_secret"],  # client secret from Facebook app
        "fb_exchange_token": params["access_token"],  # access token to get exchange for a long lived token
    }

    url = params["endpoint_base"] + "oauth/access_token"
    response = make_api_call(url, endpoint_params, params["debug"])
    return response


def extract_relevant_long_lived_access_token_info(response: dict) -> dict:
    response_clean = {
        "access_token": response["json_data"]["access_token"]
    }
    return response_clean


if __name__ == "__main__":
    params = get_creds()
    params["debug"] = True
    response = get_long_lived_access_token(params)
    response_clean = extract_relevant_long_lived_access_token_info(response)
    print(response_clean)
