import json
import os
from config import BOT_TOKEN, CHEKICHAT, ADMINS, JSON_FILE

def open_json():
    global MY_CONTACT
    if os.path.exists(JSON_FILE):
        with open(JSON_FILE, 'r', encoding='utf-8') as file:
            MY_CONTACT = json.load(file)
    else:
        MY_CONTACT = {}


def save_json():
    with open(JSON_FILE, 'w', encoding='utf-8') as file:
        json.dump(MY_CONTACT, file, ensure_ascii=False, indent=4)


def add_to_dict(userbtn, phone):
    userbtn = str(userbtn).replace('[', '')
    userbtn = str(userbtn).replace(']', '')
    userbtn = str(userbtn).replace('"', '')
    userbtn = str(userbtn).replace('\'', '')
    userbtn = f'[\'{userbtn}\']'
    MY_CONTACT.update({f'{userbtn}': f'{phone}'})
    save_json()

