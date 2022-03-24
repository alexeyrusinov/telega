import requests


# Курсы валют
def get_exchange_rate(currency: int, currency_sign: str):
    url_binance = "https://api.binance.com/api/v3/ticker/price"
    try:
        response = requests.get(url_binance)
        response.raise_for_status()
        dic = response.json()
        result_currency = dic[currency]
        my_slice = result_currency["price"].split(".")
        currency_pair = result_currency["symbol"]
        total = f"{currency_pair} - *{my_slice[0]}.{my_slice[1][:2]}* {currency_sign}"
        return total
    except Exception:
        print(">>>>--------> Errors with getting json <--------<<<<")
        return 'ошибка получения курса, напиши -> @rusinov'