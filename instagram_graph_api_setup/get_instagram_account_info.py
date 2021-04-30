""" This file returns instagram account info for a user authorized with the application,
i.e. usually yourself. """
from defines import get_creds, make_api_call


def get_istagram_account_info(params: dict) -> dict:
    """Get instagram account
    API Endpoint:
        https://graph.facebook.com/{graph-api-version}/{page-id}?access_token={your-access-token}&fields=instagram_business_account
    Returns:
        object: data from the endpoint
    """
    endpoint_params = {
        "access_token": params["access_token"],
        "fields": "instagram_business_account",
    }
    url = params["endpoint_base"] + params["page_id"]
    response = make_api_call(url, endpoint_params, params["debug"])
    return response


def extract_relevant_instagram_account_info(response: dict) -> dict:
    response_clean = {
        "page_id": response["json_data"]["id"],
        "instagram_business_account_id": response["json_data"]["instagram_business_account"]["id"],
    }
    return response_clean


if __name__ == "__main__":
    params = get_creds()
    params["debug"] = False
    response = get_istagram_account_info(params)
    response_clean = extract_relevant_instagram_account_info(response)
    print(response_clean)
