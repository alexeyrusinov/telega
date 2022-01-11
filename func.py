import requests
import json
import pytz
from datetime import datetime

# from bs4 import BeautifulSoup

# url_binance = "https://api.binance.com/api/v3/ticker/price"


# текущее время и дата в ЕКБ
def get_data_time_ekb():
    data_time_ekb = datetime.now(pytz.timezone('Asia/Yekaterinburg'))
    return data_time_ekb


# btn Текущее время и дата
def get_time():
    now_data_time_ekb = get_data_time_ekb()
    now_data_time_ekb = now_data_time_ekb.strftime("%H:%M:%S %A %d/%m/%y")
    print("get_time done")
    return now_data_time_ekb


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
        print("get_json_btc_usdt done")
        return result
    except Exception:
        print(">>>>--------> Errors with getting json <--------<<<<")


# btn Расписание автобуса
def get_bus_time():
    now_time = get_data_time_ekb()
    now_day, now_month, now_year = str(now_time.day), str(now_time.month), str(now_time.year)
    # now_day = str(now_time.day)
    # now_month = str(now_time.month)
    # now_year = str(now_time.year)

    # past now day and month
    url_bus = f"https://autovokzal.org/upload/php/result.php?id=1331&date=%27{now_year}-{now_month}-{now_day}%27&station=ekb"

    now_time = now_time.strftime('%H:%M')
    now_time = datetime.strptime(now_time, '%H:%M')

    def get_json(url_bus): # --- удалить саму функцию а тело оставить
        global dict_json_bus
        try:
            response = requests.get(url_bus)
            response.raise_for_status()
            dict_json_bus = response.json()
            return dict_json_bus
        except Exception:
            print(">>>>--------> Errors with getting json <--------<<<<")

    get_json(url_bus)
    my_bus = dict()
    # write json file
    with open('data.json', 'w', encoding='utf8') as f:
        json.dump(dict_json_bus, f, ensure_ascii=False, indent=4)

    # Read json file
    with open('data.json') as f:
        all_buses = json.load(f)

    # Rename json
    buses_schedule, buses_dispatched, buses_canceled = ([] for i in range(3))  # create lists
    # buses_schedule = []
    # buses_dispatched = []
    # buses_canceled = []
    for item in all_buses["rasp"]:
        item["time_otpr"] = datetime.strptime(item["time_otpr"], '%H:%M')  # convert str to class 'datetime
        item["name_route"] = item["name_route"].replace('г.Екатеринбург (Южный АВ) -<br/>',
                                                        'Екб (Южный АВ) -')  # rename value
        item["name_bus"] = item["name_bus"].replace('YUTONG ZK 6122 H9', 'YUTONG')
        item["name_bus"] = item["name_bus"].replace('YUTONG ZK 6129 H', 'YUTONG')
        item["name_bus"] = item["name_bus"].replace('YUTONG 6121', 'YUTONG')
        item["name_bus"] = item["name_bus"].replace('ПАЗ-4234', 'ПАЗ')
        item["cancel"] = item["cancel"].replace("Отмена", "canceled")  # rename value
        item["status"] = item.pop("cancel")  # rename key
        if item["time_otpr"] > now_time and item["status"] != "canceled": ### тут now_time переделать под выбор дня
            buses_schedule.append(item)
        elif item["status"] == "Отправлен":
            buses_dispatched.append(item)
        elif item["status"] == "canceled":
            buses_canceled.append(item)

    # write json file
    with open('new_data.json', 'w', encoding='utf8') as f:
        json.dump(buses_schedule, f, ensure_ascii=False, indent=4, sort_keys=True, default=str)

    next_bus_time = ''
    for i in buses_schedule:  # print time to the next bus
        if i["status"] == "" and i["name_bus"] == "НЕФАЗ" or i["name_bus"] == "ПАЗ":
            time = i["time_otpr"] - now_time
            time = datetime.strptime(str(time), '%H:%M:%S').strftime('%H:%M')
            if time[:2] == '00':
                time = time[3:] + ' min'
            else:
                time.replace(" min", "")  #### код для елсе которое стиает мин если до след автобуса больше чем час
                # если что вот это смотри
            free_place = i["free_place"]
            name_bus = i["name_bus"]
            next_bus_time = str(
                'The next bus in ' + str(time) + ' \nbus: ' + str(name_bus) + ' free places: ' + str(free_place) + '\n')
            break
        elif i["status"] == "":
            time = i["time_otpr"] - now_time
            time = datetime.strptime(str(time), '%H:%M:%S').strftime('%H:%M')
            if time[:2] == '00':
                time = time[3:] + ' min'
            else:
                time.replace(" min", "")  #### код для елсе которое стиает мин если до след автобуса больше чем час
                # если что вот это смотри
            free_place = i["free_place"]
            next_bus_time = str('The next bus in ' + str(time) + ' \nfree places: ' + str(free_place) + '\n')
            break

    for i in all_buses["rasp"]:  # convert class 'datetime.time to string deleting seconds
        i["time_otpr"] = i["time_otpr"].strftime("%H:%M")

    next_bus = ''
    for i in reversed(buses_schedule):  # revers list, and output next bus
        next_bus += i["time_otpr"]
        next_bus += i["status"] + ' '
        next_bus += i["free_place"] + ' '
        next_bus += i["name_bus"] + ' '
        next_bus += i["name_route"] + '\n\n'

    next_bus += next_bus_time

    # a = str(len(buses_dispatched))

    # add to dict for output
    # my_bus['buses'] = all_buses["rasp"]
    # my_bus['buses_dispatched'] = buses_dispatched
    # my_bus['buses_schedule'] = items_to_keep
    # my_bus['buses_canceled'] = buses_canceled
    buses = ""
    buses += str(len(all_buses["rasp"]))

    print(f"all_buses - {buses}")
    print(f"buses_dispatched - {str(len(buses_dispatched))}")
    print(f"buses_schedule - {len(buses_schedule)}")
    print(f"buses_canceled - {len(buses_canceled)}")

    print("get_bus_time done")

    if len(next_bus) == 0:
        return f"No buses for today."
    else:
        return next_bus


# # pars bus 91-------------------------------------------------------------
#
# url = "http://www.urbus.ru/win/popup/bl114/dy2021/dm12/dd29/su/92/"
# url = "https://www.autovokzal.org/"
#
# page = requests.get(url)
# print(page.status_code)
# filteredNews = []
#
# days = []
# soup = BeautifulSoup(page.text, "html.parser")
# # allNews = soup.findAll("td")
# day = soup.findAll("pmu-days")
# print(day)
# for data in day:
#     if data is not None:
#         days.append(data)
#
# for data in days:
#     print(data)
#
# for data in allNews:
#     if data.findAll("td") is not None:
#         # filteredNews.append(data.text.replace("\xa0", ""))
#         filteredNews.append(data.get_text().replace("\xa0", ""))
#
#
# filteredNews = list(filter(None, filteredNews)) # dell empty str in list
#
#
#
# # for data in filteredNews:
# #     print(data)
#
# #  index
# indexMetroBotanicheskaya = filteredNews.index('Метро Ботаническая')
# indexTcDirijabl = filteredNews.index('ТЦДирижабль')
# indexBulvarMalahova = filteredNews.index('Бульвар Малахова')
# indexSomocvetniyBulvar = filteredNews.index('Самоцветный бульвар')
# indexUvelirnaya = filteredNews.index('Ювелирная')
# indexPerRigskiy = filteredNews.index('Рижскийпер.')
# indexSuxologskaya = filteredNews.index('Сухоложская')
# indexVtorjermet = filteredNews.index('Вторчермет')
# indexPoliklinika = filteredNews.index('Поликлиника')
# indexObshegitiye = filteredNews.index('Общежитие')
# indexStKeramik = filteredNews.index('Ст. Керамик')
# indexYugnayaPodstanciya = filteredNews.index('Южная подстанция')
# indexSady = filteredNews.index('Сады')
# indexSadRodnijok = filteredNews.index('Сад «Родничок»')
# indexPolevodstvo = filteredNews.index('Полеводство')
# index17KlPolevskogoTrakta = filteredNews.index('17км Полевского тракта')
# indexZelenaya = filteredNews.index('Зеленая')
# indexSrednaya = filteredNews.index('Средняя')
# indexZeleniyBor = filteredNews.index('Зеленый Бор')
# indexPovNaZeleniyBor = filteredNews.index('Пов. наЗеленый Бор')
# indexEkodole1 = filteredNews.index('Экодолье 1')
# indexPovNaZeleniyBor2 = filteredNews.index('Пов. наЗеленый Бор')
# indexSrednaya2 = filteredNews.index('Средняя')
# indexGorniyShit = filteredNews.index('Горный Щит')
# indexShirokayaRejka = filteredNews.index('Широкая Речка')
