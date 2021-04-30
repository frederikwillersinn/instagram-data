import datetime

from defines import get_creds, make_api_call


def debug_access_token(params: dict) -> dict:
    """Get info on an access token
    API Endpoint:
        https://graph.facebook.com/debug_token?input_token={input-token}&access_token={valid-access-token}
    Returns:
        object: data from the endpoint
    """
    endpoint_params = {
        "input_token": params["access_token"],  # input token is the access token
        "access_token": params["access_token"],  # access token to get debug info on
    }
    url = params["graph_domain"] + "/debug_token"
    response = make_api_call(url, endpoint_params, params["debug"])
    return response


def extract_relevant_access_token_data(response: dict) -> dict:
    response_clean = {
        "data_access_expiry_date": str(datetime.datetime.fromtimestamp(response["json_data"]["data"]["data_access_expires_at"])),
        "token_expiry_date": str(datetime.datetime.fromtimestamp(response["json_data"]["data"]["expires_at"])),
    }
    return response_clean


if __name__ == "__main__":
    params = get_creds()
    params["debug"] = True
    response = debug_access_token(params)
    response_clean = extract_relevant_access_token_data(response)
    print(response_clean)
