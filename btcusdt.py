import requests, json
from key import url_binance

def get_json_btcusdt(url):
    global dic
    try:
        response = requests.get(url_binance)
        response.raise_for_status()
        dic = response.json()
    except Exception:
        print(">>>>--------> Errors with getting json <--------<<<<")
    return  dic[11]








