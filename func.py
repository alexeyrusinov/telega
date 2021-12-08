import requests
from key import url_binance
import json, datetime


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

#----------------------
def pars_bus():
    now = datetime.datetime.now() # get date and time
    now_day = str(now.day)
    now_month = str(now.month)
    times = now.time().replace(microsecond=0) # del millisecond
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


    #write json file
    with open('data.json', 'w', encoding='utf8') as f:
        json.dump(dic, f, ensure_ascii=False, indent=4)

    #Read json file
    with open('data.json') as f:
        data = json.load(f)


    #Rename json
    items_to_keep = []
    for item in data["rasp"]:
        item["time_otpr"] = datetime.datetime.strptime(item["time_otpr"], "%H:%M").time() # convert str to class 'datetime
        item["name_route"] = item["name_route"].replace('г.Екатеринбург (Южный АВ) -<br/>', 'Екб (Южный АВ) -')   # rename value
        item["name_bus"] = item["name_bus"].replace('YUTONG ZK 6122 H9', 'YUTONG')
        item["name_bus"] = item["name_bus"].replace('YUTONG 6121', 'YUTONG')
        item["name_bus"] = item["name_bus"].replace('ПАЗ-4234', 'ПАЗ')
        item["cancel"] = item["cancel"].replace("Отмена", "canceled")  # rename value
        item["status"] = item.pop("cancel") # rename key
        if item["time_otpr"] > times:
            items_to_keep.append(item)


    #write json file
    with open('new_data.json', 'w', encoding='utf8') as f:
        json.dump(items_to_keep, f, ensure_ascii=False, indent=4, sort_keys=True, default=str)


    res = ''
    for i in items_to_keep: # print min to the next bus
        if i["status"] == "" and i["name_bus"] == "НЕФАЗ" or i["name_bus"] == "ПАЗ-4234":
            nex_bus = i["time_otpr"].minute - times.minute
            free_place = i["free_place"]
            name_bus = i["name_bus"]
            # print(f" The next bus in {nex_bus} minutes, bus: {name_bus}, free places: {free_place} ")
            resultNextBus = str('The next bus in ' + str(nex_bus) + ' minutes, bus: ' + str(name_bus) + ' free places: ' + str(free_place) +'\n')
            res = resultNextBus
            break
        elif i["status"] == "":
            nex_bus = i["time_otpr"].minute - times.minute
            free_place = i["free_place"]
            # print(f" The next bus in {nex_bus} minutes, free places: {free_place} ")
            resultNextBus = str('The next bus in ' + str(nex_bus) + ' minutes, free places: ' + str(free_place) +'\n')
            res = resultNextBus
            break


    for i in items_to_keep: # convert class 'datetime.time to string deleting seconds
        i["time_otpr"] = i["time_otpr"].strftime("%H:%M")


    for i in items_to_keep:
        res += i["time_otpr"]
        res += i["status"] + ' '
        res += i["free_place"] + ' '
        res += i["name_bus"] + ' '
        res += i["name_route"] + '\n\n'

    return res










