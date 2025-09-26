import requests



def get_exchange_rates():
    url = "https://api.fxratesapi.com/latest?api_key=fxr_live_a6422b3277f2e5ca0d89df00941809c49adc"
    params = {"base": "GBP"}
    response = requests.get(url, params=params,
                            headers={"Authorization": "access_token fxr_live_a6422b3277f2e5ca0d89df00941809c49adc"})
    response_JSON = response.json()
    exchange_rates = {"GGP":(response_JSON["success"],response_JSON["rates"])}
    return exchange_rates