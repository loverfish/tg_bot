import requests

from datetime import datetime as dt
from datetime import timedelta
from time import sleep


from tg_bot.setup_list import *


base_params_vk = {
        'v': version_api_vk,
        'access_token': api_token_vk,
        'fields': 'online',
    }


def get_user_info_vk(person=user_id_vk):
    additional_params = {'user_id': person}
    params = {**base_params_vk, **additional_params}    # vk_params | additional_params  v3.9+
    return requests.get(root_url_vk + 'users.get', params=params).json().get('response')[0]


def get_user_fullname(person=user_id_vk):
    info = get_user_info_vk(person)
    return f"{info.get('first_name')} {info.get('last_name')}"


def user_online_info(list_info, person=user_id_vk):
    info = get_user_info_vk(person)
    if info.get('online'):
        list_info.append(dt.now())


def create_online_report(person=user_id_vk, duration=1):
    report = []
    end_time = dt.now() + timedelta(minutes=duration)
    sleep_time = 62
    while dt.now() < end_time:
        user_online_info(report, person)
        sleep(sleep_time)

    if report:
        header = f"Пользователь {get_user_fullname(person)} был в сети:\n"
        result_report = [f'{report[0].strftime("%Y-%m-%d   %H:%M:%S")}']
        t = ''
        for i in range(1, len(report) - 1):
            if report[i] - report[i-1] <= timedelta(seconds=sleep_time+1):
                if report[i + 1] - report[i] >= timedelta(seconds=sleep_time + 1):
                    result_report.append(f'- {report[i].strftime("%H:%M:%S")}')
                    t = ''
                else:
                    t = '- '
            else:
                result_report.append(f'\n{report[i].strftime("%Y-%m-%d   %H:%M:%S")}')
        if len(report) > 1:
            if t:
                result_report.append(f'{t}{report[-1].strftime("%H:%M:%S")}')
            else:
                result_report.append(f'\n{report[-1].strftime("%Y-%m-%d   %H:%M:%S")}')

        return header + ' '.join(result_report)
