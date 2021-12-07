import requests
from key import url_binance

def get_json_btcusdt(url):
    global result
    try:
        response = requests.get(url_binance)
        response.raise_for_status()
        dic = response.json()
        res = dic[11]
        result = str(res["symbol"] + " - " + res["price"] + " $")
    except Exception:
        print(">>>>--------> Errors with getting json <--------<<<<")
    return result










