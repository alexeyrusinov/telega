import requests, json, pytz
from datetime import datetime

url_binance = "https://api.binance.com/api/v3/ticker/price"


def get_time():
    data_time_ekb = datetime.now(pytz.timezone('Asia/Yekaterinburg'))
    now_data_time_ekb = data_time_ekb.strftime("%H:%M:%S %A %d/%m/%y")
    return now_data_time_ekb


def get_json_btc_usdt(url):
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


def pars_bus():
    now = datetime.now()  # get date and time
    now_day = str(now.day)
    now_month = str(now.month)
    data_time_ekb = datetime.now(pytz.timezone('Asia/Yekaterinburg'))
    data_time_ekb = data_time_ekb.strftime('%H:%M')
    data_time_ekb = datetime.strptime(data_time_ekb, '%H:%M')
    id = '1331'

    # past now day and month
    url = "https://autovokzal.org/upload/php/result.php?id=" + id + "&date=%272021-" + now_month + "-" + now_day + "%27&station=ekb"

    def get_json(url):
        global dic
        try:
            response = requests.get(url)
            response.raise_for_status()
            dic = response.json()
        except Exception:
            print(">>>>--------> Errors with getting json <--------<<<<")
        return dic
    get_json(url)

    # write json file
    with open('data.json', 'w', encoding='utf8') as f:
        json.dump(dic, f, ensure_ascii=False, indent=4)

    # Read json file
    with open('data.json') as f:
        data = json.load(f)

    # Rename json
    items_to_keep = []
    for item in data["rasp"]:
        item["time_otpr"] = datetime.strptime(item["time_otpr"], '%H:%M') # convert str to class 'datetime
        item["name_route"] = item["name_route"].replace('г.Екатеринбург (Южный АВ) -<br/>', 'Екб (Южный АВ) -')  # rename value
        item["name_bus"] = item["name_bus"].replace('YUTONG ZK 6122 H9', 'YUTONG')
        item["name_bus"] = item["name_bus"].replace('YUTONG ZK 6129 H', 'YUTONG')
        item["name_bus"] = item["name_bus"].replace('YUTONG 6121', 'YUTONG')
        item["name_bus"] = item["name_bus"].replace('ПАЗ-4234', 'ПАЗ')
        item["cancel"] = item["cancel"].replace("Отмена", "canceled")  # rename value
        item["status"] = item.pop("cancel")  # rename key
        if item["time_otpr"] > data_time_ekb:
            items_to_keep.append(item)

    # write json file
    with open('new_data.json', 'w', encoding='utf8') as f:
        json.dump(items_to_keep, f, ensure_ascii=False, indent=4, sort_keys=True, default=str)

    next_bus = ''
    next_bus_time = ''
    for i in items_to_keep:  # print time to the next bus
        if i["status"] == "" and i["name_bus"] == "НЕФАЗ" or i["name_bus"] == "ПАЗ":
            time = i["time_otpr"] - data_time_ekb
            time = datetime.strptime(str(time), '%H:%M:%S').strftime('%H:%M')
            if time[:2] == '00':
                time = time[3:] + ' min'
            else:
                time.replace(" min", "")  #### код для елсе которое стиает мин если до след автобуса больше чем час
                # если что вот это смотри
            free_place = i["free_place"]
            name_bus = i["name_bus"]
            next_bus_time = str('The next bus in ' + str(time) + ' \nbus: ' + str(name_bus) + ' free places: ' + str(free_place) +'\n')
            break
        elif i["status"] == "":
            time = i["time_otpr"] - data_time_ekb
            time = datetime.strptime(str(time), '%H:%M:%S').strftime('%H:%M')
            if time[:2] == '00':
                time = time[3:] + ' min'
            else:
                time.replace(" min", "")  #### код для елсе которое стиает мин если до след автобуса больше чем час
                # если что вот это смотри
            free_place = i["free_place"]
            next_bus_time = str('The next bus in ' + str(time) + ' \nfree places: ' + str(free_place) + '\n')
            break

    for i in items_to_keep:  # convert class 'datetime.time to string deleting seconds
        i["time_otpr"] = i["time_otpr"].strftime("%H:%M")

    for i in reversed(items_to_keep):  # revers list
        next_bus += i["time_otpr"]
        next_bus += i["status"] + ' '
        next_bus += i["free_place"] + ' '
        next_bus += i["name_bus"] + ' '
        next_bus += i["name_route"] + '\n\n'

    next_bus += next_bus_time  # add in end output

    return next_bus
