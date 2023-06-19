import os
import json

JSON_FILE_ADMIN = 'jsons/message.json'

async def word_mentor():
    slovo = "Здесь были продаванские мудрости"
    print(slovo)
    return slovo


def open_json_admins():
    if os.path.exists(JSON_FILE_ADMIN):
        with open(JSON_FILE_ADMIN, 'r', encoding='utf-8') as file:
            messages_admin = json.load(file)
    else:
        messages_admin = {}
    return messages_admin


def read_json_admin_file_add_user(user_id):
    if os.path.exists(JSON_FILE_ADMIN):
        with open(JSON_FILE_ADMIN, 'r', encoding='utf-8') as file:
            messages_admin = json.load(file)

        messages_admin["granted_users"].append(int(user_id))

        with open(JSON_FILE_ADMIN, 'w', encoding='utf-8') as json_file:
            json.dump(messages_admin, json_file)

    else:
        print('Файла нет')


def save_json_admins(role, data):     # roles_dict
    if os.path.exists(JSON_FILE_ADMIN):
        with open(JSON_FILE_ADMIN, 'r', encoding='utf-8') as file:
            messages_admin = json.load(file)

        messages_admin.get('roles_dict', {})[role] = data

        with open(JSON_FILE_ADMIN, 'w', encoding='utf-8') as json_file:
            json.dump(messages_admin, json_file)

    else:
        print('Файла нет')
