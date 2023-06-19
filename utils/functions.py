import os
import json
from config.config import BOT_TOKEN, CHEKICHAT, ADMINS, JSON_FILE, manager


def open_json():
    if os.path.exists(JSON_FILE):
        with open(JSON_FILE, 'r', encoding='utf-8') as file:
            MY_CONTACT = json.load(file)
    else:
        MY_CONTACT = {}
    return MY_CONTACT


def save_json(MY_CONTACT):
    # with open(JSON_FILE, 'r', encoding='utf-8') as file:
    #     read = json.load(file, ensure_ascii=False, indent=4)

    with open(JSON_FILE, 'w', encoding='utf-8') as file:
        json.dump(MY_CONTACT, file, ensure_ascii=False, indent=4)


def add_to_dict(MY_CONTACT, userbtn, phone):

    MY_CONTACT[userbtn] = phone
    save_json(MY_CONTACT)


def read_KPI_lines(counter):
    with open('jsons/kpi_json', 'r') as kpi:
        kpi = '\n'.join(json.load(kpi).get(counter, []))
    return kpi


def write_KPI_lines(kpi_list, counter, city):
    with open('jsons/kpi_json', 'r') as kpi_read:
        kpi_read = json.load(kpi_read)
    kpi_read[city][counter] = kpi_list

    with open('jsons/kpi.json', 'w') as kpi_write:
        json.dump(kpi_read, kpi_write)

