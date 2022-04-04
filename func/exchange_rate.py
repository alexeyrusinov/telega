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


def get_exchange_rate_for_admin(currency1: int, currency_sign1: str, currency2: int, currency_sign2: str):
    url_binance = "https://api.binance.com/api/v3/ticker/price"
    try:
        response = requests.get(url_binance)
        response.raise_for_status()
        dic = response.json()
        result_currency1 = dic[currency1]
        result_currency2 = dic[currency2]
        my_slice1 = result_currency1["price"].split(".")
        my_slice2 = result_currency2["price"].split(".")
        currency_pair1 = result_currency1["symbol"]
        currency_pair2 = result_currency2["symbol"]
        total = f"{currency_pair1} - *{my_slice1[0]}.{my_slice1[1][:2]}* {currency_sign1}"
        total += f"\n{currency_pair2} - *{my_slice2[0]}.{my_slice2[1][:2]}* {currency_sign2}"
        return total
    except Exception:
        print(">>>>--------> Errors with getting json <--------<<<<")
        return 'ошибка получения курса, напиши -> @rusinov'


get_exchange_rate_for_admin(11, '$', 688, '₽')