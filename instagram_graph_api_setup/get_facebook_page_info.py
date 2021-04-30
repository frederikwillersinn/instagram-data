""" This file returns the facebook page for a user authorized with the application,
i.e. usually yourself, using the Instagram Graph API. """
from defines import get_creds, make_api_call


def get_user_pages_info(params: dict) -> dict:
    """Get facebook pages for a user
    API Endpoint:
    https://graph.facebook.com/{graph-api-version}/me/accounts?access_token={access-token}
    Returns:
        object: data from the endpoint
    """
    endpoint_params = {"access_token": params["access_token"]}
    url = params["endpoint_base"] + "me/accounts"
    response = make_api_call(url, endpoint_params, params["debug"])
    return response


def extract_relevant_user_pages_info(response: dict) -> dict:
    response_clean = {
        "id": response["json_data"]["data"][0]["id"],
        "name": response["json_data"]["data"][0]["name"],
        "category": response["json_data"]["data"][0]["category"],
    }
    return response_clean


if __name__ == "__main__":
    params = get_creds()
    params["debug"] = False
    response = get_user_pages_info(params)
    response_clean = extract_relevant_user_pages_info(response)
    print(response_clean)
