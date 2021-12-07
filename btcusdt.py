import requests
from key import url_binance

def get_json_btcusdt(url):
    global result
    try:
        response = requests.get(url_binance)
        response.raise_for_status()
        dic = response.json()
        res = dic[11]
        result = str(res["symbol"] + " - " + res["price"])
        result = result[:-6] + " $"
    except Exception:
        print(">>>>--------> Errors with getting json <--------<<<<")
    return result


# get_json_btcusdt(url_binance)
# str.rstrip(str[-1])






