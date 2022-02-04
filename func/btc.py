import requests


# btn Курс биткоина
def get_btc_usdt_rate():
    url_binance = "https://api.binance.com/api/v3/ticker/price"
    try:
        response = requests.get(url_binance)
        response.raise_for_status()
        dic = response.json()
        res = dic[11]
        result = str(res["symbol"] + " - " + res["price"])
        result = result[:-6] + " $"
        return result
    except Exception:
        print(">>>>--------> Errors with getting json <--------<<<<")
