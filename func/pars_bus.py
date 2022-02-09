import requests
import json
from datetime import datetime
from func.date_and_time import get_data_time_ekb


def list_schedule_json_to_string(list_schedule):
    schedule = ''
    for i in reversed(list_schedule):  # revers list, and output next bus
        schedule += i["time_otpr"] + ' '
        schedule += i["status"] + ' '
        schedule += i["free_place"] + ' '
        schedule += i["name_bus"] + ' '
        schedule += i["name_route"] + '\n\n'
    return schedule


def get_bus_time(days=0):
    now_datetime_with_parm_days = get_data_time_ekb(days)
    now_date_with_parm_days = str(now_datetime_with_parm_days.date())
    now_date_with_parm_days_str = now_datetime_with_parm_days.strftime('%d-%m-%Y')

    now_datetime = get_data_time_ekb()
    now_date_str = now_datetime.strftime('%d-%m-%Y')

    day, month, year = str(now_datetime_with_parm_days.day), str(now_datetime_with_parm_days.month), str(now_datetime_with_parm_days.year)


    # past now day and month
    url_bus = f"https://autovokzal.org/upload/php/result.php?id=1331&date=%27{year}-{month}-{day}%27&station=ekb"

    try:
        response = requests.get(url_bus)
        response.raise_for_status()
        dict_json_bus = response.json()
    except Exception:
        print(">>>>--------> Errors with getting json <--------<<<<")
        raise

    with open('data.json', 'w', encoding='utf8') as f:
        json.dump(dict_json_bus, f, ensure_ascii=False, indent=4)

    with open('data.json') as f:   # Read json file
        all_data = json.load(f)

    bus_schedule, bus_dispatched, bus_canceled = ([] for i in range(3))  # create 3 lists

    for item in all_data["rasp"]:  # Rename json
        item["time_otpr"] += f' {now_date_with_parm_days}'  # добавляем дату ко времени отправления
        item["time_otpr"] = datetime.strptime(item["time_otpr"], '%H:%M %Y-%m-%d')  # convert str to class 'datetime
        item["name_route"] = item["name_route"].replace('г.Екатеринбург (Южный АВ) -<br/>',
                                                        'Южный АВ -')  # rename value
        item["name_route"] = item["name_route"].replace('г.', '')
        item["name_bus"] = item["name_bus"].replace('YUTONG ZK 6122 H9', 'YTNG')
        item["name_bus"] = item["name_bus"].replace('YUTONG ZK 6129 H', 'YTNG')
        item["name_bus"] = item["name_bus"].replace('YUTONG 6121', 'YTNG')
        item["name_bus"] = item["name_bus"].replace('ПАЗ-4234', 'ПАЗ')
        item["cancel"] = item["cancel"].replace("Отмена", "❌")  # rename value
        item["cancel"] = item["cancel"].replace("Отправлен", "✅")
        item["status"] = item.pop("cancel")  # rename key
        if item["time_otpr"] > now_datetime and item["status"] != "❌":  # тут now_time переделать под выбор дня
            bus_schedule.append(item)
        elif item["status"] == "✅" and item["status"]:
            bus_dispatched.append(item)
        elif item["status"] == "❌":
            bus_canceled.append(item)

    with open('new_data.json', 'w', encoding='utf8') as f:  # write json file
        json.dump(bus_schedule, f, ensure_ascii=False, indent=4, sort_keys=True, default=str)

    next_bus_time = ''
    if days:  # parameter func get_bus_time
        next_bus_time = f"date: {now_date_with_parm_days_str}"
    else:
        for i in bus_schedule:  # print time to the next bus
            if i["status"] == "" and i["name_bus"] == "НЕФАЗ" or i["name_bus"] == "ПАЗ":
                time = i["time_otpr"] - now_datetime
                time = datetime.strptime(str(time), '%H:%M:%S').strftime('%H:%M')
                if time[:2] == '00':
                    time = time[3:] + ' min'
                    if time[:1] == '0':
                        time = time[1:]
                else:
                    time.replace(" min", "")  # код для елсе которое стиает мин если до след автобуса больше чем час
                free_place = i["free_place"]
                name_bus = i["name_bus"]
                next_bus_time = str(
                    f'Next bus in ' + str(time) + ' \nbus: ' + str(name_bus) + '. free places: ' + str(
                        free_place) + f"\ndate: {now_date_str}" + '\n')
                break
            elif i["status"] == "":
                time = i["time_otpr"] - now_datetime
                time = datetime.strptime(str(time), '%H:%M:%S').strftime('%H:%M')
                if time[:2] == '00':
                    time = time[3:] + ' min'
                    if time[:1] == '0':
                        time = time[1:]
                else:
                    time.replace(" min", "")  # код для елсе которое стиает мин если до след автобуса больше чем час
                free_place = i["free_place"]
                next_bus_time = str('Next bus in ' + str(time) + '. free places: ' + str(free_place) +
                                    f"\ndate: {now_date_str}" + '\n')
                break

    for i in all_data["rasp"]:  # convert class 'datetime.time to string deleting seconds for output
        i["time_otpr"] = i["time_otpr"].strftime("%H:%M")

    schedule = list_schedule_json_to_string(bus_schedule)
    schedule += next_bus_time

    data_bus = dict()  # add to dict for output
    data_bus['all_bus'] = all_data["rasp"]
    data_bus['bus_dispatched'] = bus_dispatched
    data_bus['bus_schedule'] = schedule
    data_bus['bus_canceled'] = bus_canceled
    data_bus['now_date_with_parm_days'] = now_date_with_parm_days_str
    data_bus['now_date'] = now_date_str

    bus = str(len(all_data["rasp"]))
    print(f"all_bus - {bus}, bus_dispatched - {str(len(bus_dispatched))}, "
          f"bus_schedule - {len(bus_schedule)}, bus_canceled - {len(bus_canceled)}")

    return data_bus


def get_all_bus_schedule():  # Все автобусы
    data_bus = get_bus_time()  # c парметром days
    entire_schedule_for_today = list_schedule_json_to_string(data_bus['all_bus'])
    entire_schedule_for_today += f"Все автобусы за: {data_bus['now_date_with_parm_days']}"
    return entire_schedule_for_today


def get_current_schedule():  # Расписание автобуса
    data_bus = get_bus_time()  # c парметром days
    if len(data_bus['bus_schedule']) == 0:
        return f"No bus for: {data_bus['now_date_with_parm_days']}"
    else:
        return data_bus['bus_schedule']


def get_bus_dispatched():  # Отправленные автобусы
    data_bus = get_bus_time()
    entire_bus_dispatched_for_today = list_schedule_json_to_string(data_bus['bus_dispatched'])
    entire_bus_dispatched_for_today += f"Отправленные автобусы за: {data_bus['now_date']}"
    return entire_bus_dispatched_for_today


def get_bus_canceled():  # Отменённые автобусы
    data_bus = get_bus_time()  # c парметром days
    entire_bus_canceled_for_today = list_schedule_json_to_string(data_bus['bus_canceled'])
    if len(entire_bus_canceled_for_today) == 0:
        return f"No canceled bus: {data_bus['now_date_with_parm_days']}"
    else:
        entire_bus_canceled_for_today += f"Отменённые автобусы за: {data_bus['now_date_with_parm_days']}"
        return entire_bus_canceled_for_today

# %Y-%m-%d
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
