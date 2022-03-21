import requests


# Курсы валют
def get_exchange_rate(currency: int, slice_price: int, currency_sign: str):
    url_binance = "https://api.binance.com/api/v3/ticker/price"
    try:
        response = requests.get(url_binance)
        response.raise_for_status()
        dic = response.json()
        res = dic[currency]
        result = str(res["symbol"] + " - *" +  res["price"][:slice_price] + f"* {currency_sign}")
        return result
    except Exception:
        print(">>>>--------> Errors with getting json <--------<<<<")
        return 'ошибка получения курса, напиши -> @rusinov'