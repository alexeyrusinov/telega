import pytz
from datetime import datetime

# текущее время и дата в ЕКБ
def get_data_time_ekb():
    data_time_ekb = datetime.now(pytz.timezone('Asia/Yekaterinburg'))
    return data_time_ekb


# btn Текущее время и дата
def get_convert_date_time():
    now_data_time_ekb = get_data_time_ekb()
    now_data_time_ekb = now_data_time_ekb.strftime("%H:%M:%S %A %d/%m/%y")
    print("get_time done")
    return now_data_time_ekb


def get_convert_date():
    now_data_time_ekb = get_data_time_ekb()
    now_data_time_ekb = now_data_time_ekb.strftime("%d/%m/%y %A")
    print("get_convert_date done")
    return now_data_time_ekb


# convert format time for calculate
def get_now_time():
    now_time = get_data_time_ekb()
    now_time = now_time.strftime('%H:%M')
    now_time = datetime.strptime(now_time, '%H:%M')
    return now_time
