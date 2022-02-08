import requests
import json
from datetime import datetime
from func.date_and_time import get_data_time_ekb, get_convert_date


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
    now_time_with_parm_days = get_data_time_ekb(days)
    now_time_with_parm_days = now_time_with_parm_days.replace(tzinfo=None, microsecond=0)  # удаляем tzinfo чтобы сравнивало

    now_time = get_data_time_ekb()
    now_time = now_time.replace(tzinfo=None, microsecond=0)

    now_day, now_month, now_year = str(now_time_with_parm_days.day), str(now_time_with_parm_days.month), str(now_time_with_parm_days.year)

    # past now day and month
    url_bus = f"https://autovokzal.org/upload/php/result.php?id=1331&date=%27{now_year}-{now_month}-{now_day}%27&station=ekb"

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

    buses_schedule, buses_dispatched, buses_canceled = ([] for i in range(3))  # create 3 lists

    for item in all_data["rasp"]:  # Rename json
        item["time_otpr"] += f' {str(now_time_with_parm_days.date())}'  # добавляем дату ко времени отправления
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
        if item["time_otpr"] > now_time and item["status"] != "❌":  # тут now_time переделать под выбор дня
            buses_schedule.append(item)
        elif item["status"] == "✅" and item["status"]:
            buses_dispatched.append(item)
        elif item["status"] == "❌":
            buses_canceled.append(item)

    # write json file
    with open('new_data.json', 'w', encoding='utf8') as f:
        json.dump(buses_schedule, f, ensure_ascii=False, indent=4, sort_keys=True, default=str)

    next_bus_time = ''
    if days: # parameters func
        next_bus_time = f"date: {now_time_with_parm_days.strftime('%d-%m-%Y')}"
        print(f"date: {now_time_with_parm_days.strftime('%d-%m-%Y')}")
    else:
        for i in buses_schedule:  # print time to the next bus
            if i["status"] == "" and i["name_bus"] == "НЕФАЗ" or i["name_bus"] == "ПАЗ":
                time = i["time_otpr"] - now_time
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
                        free_place) + f"\ndate: {now_time_with_parm_days.strftime('%d-%m-%Y')}" + '\n')
                break
            elif i["status"] == "":
                time = i["time_otpr"] - now_time
                time = datetime.strptime(str(time), '%H:%M:%S').strftime('%H:%M')
                if time[:2] == '00':
                    time = time[3:] + ' min'
                    if time[:1] == '0':
                        time = time[1:]
                else:
                    time.replace(" min", "")  # код для елсе которое стиает мин если до след автобуса больше чем час
                free_place = i["free_place"]
                next_bus_time = str('Next bus in ' + str(time) + '. free places: ' + str(free_place) +
                                    f"\ndate: {now_time_with_parm_days.strftime('%d-%m-%Y')}" + '\n')
                break

    for i in all_data["rasp"]:  # convert class 'datetime.time to string deleting seconds for output
        i["time_otpr"] = i["time_otpr"].strftime("%H:%M")

    schedule = list_schedule_json_to_string(buses_schedule)
    schedule += next_bus_time

    my_bus = dict()  # add to dict for output
    my_bus['buses'] = all_data["rasp"]
    my_bus['buses_dispatched'] = buses_dispatched
    my_bus['buses_schedule'] = buses_schedule
    my_bus['buses_canceled'] = buses_canceled

    buses = ""
    buses += str(len(all_data["rasp"]))

    print(f"all_buses - {buses}, buses_dispatched - {str(len(buses_dispatched))}, "
          f"buses_schedule - {len(buses_schedule)}, buses_canceled - {len(buses_canceled)}")
    return all_data["rasp"], buses_dispatched, schedule, buses_canceled


def get_all_bus_schedule():  # Все автобусы
    all_buses, buses_dispatched, buses_schedule, buses_canceled = get_bus_time()
    entire_schedule_for_today = list_schedule_json_to_string(all_buses)
    entire_schedule_for_today += 'Все автобусы за сегодня: '
    entire_schedule_for_today += get_convert_date()
    return entire_schedule_for_today


def get_current_schedule():  # Расписание автобуса
    all_buses, buses_dispatched, buses_schedule, buses_canceled = get_bus_time()
    if len(buses_schedule) == 0:
        return f"No buses for today: {get_convert_date()}"
    else:
        return buses_schedule


def get_buses_dispatched(): # Отправленные автобусы
    all_buses, buses_dispatched, buses_schedule, buses_canceled = get_bus_time()
    entire_buses_dispatched_for_today = list_schedule_json_to_string(buses_dispatched)
    entire_buses_dispatched_for_today += 'Отправленные автобусы за сегодня: '
    entire_buses_dispatched_for_today += get_convert_date()
    return entire_buses_dispatched_for_today


def get_buses_canceled(): # Отменённые автобусы
    all_buses, buses_dispatched, buses_schedule, buses_canceled = get_bus_time()
    entire_buses_canceled_for_today = list_schedule_json_to_string(buses_canceled)
    if len(entire_buses_canceled_for_today) == 0:
        return f"No canceled buses today: {get_convert_date()}"
    else:
        entire_buses_canceled_for_today += 'Отменённые автобусы за сегодня: '
        entire_buses_canceled_for_today += get_convert_date()
        return entire_buses_canceled_for_today

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
