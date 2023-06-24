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
            json.dump(messages_admin, json_file, ensure_ascii=False, indent=4)
    else:
        print('Файла нет')
    messages = open_json_admins()


def read_json_admin_file_add_user_admin(user_id):
    if os.path.exists(JSON_FILE_ADMIN):
        with open(JSON_FILE_ADMIN, 'r', encoding='utf-8') as file:
            messages_admin = json.load(file)

        messages_admin["admins"].append(int(user_id))

        with open(JSON_FILE_ADMIN, 'w', encoding='utf-8') as json_file:
            json.dump(messages_admin, json_file, ensure_ascii=False, indent=4)
    else:
        print('Файла нет')
    messages = open_json_admins()


def save_json_admins(role, data):     # roles_dict
    if os.path.exists(JSON_FILE_ADMIN):
        with open(JSON_FILE_ADMIN, 'r', encoding='utf-8') as file:
            messages_admin = json.load(file)

        messages_admin.get('roles_dict', {})[role] = data

        with open(JSON_FILE_ADMIN, 'w', encoding='utf-8') as json_file:
            json.dump(messages_admin, json_file, ensure_ascii=False, indent=4)

        messages = open_json_admins()
    else:
        print('Файла нет')


def del_json_user(user):
    if os.path.exists(JSON_FILE_ADMIN):
        with open(JSON_FILE_ADMIN, 'r', encoding='utf-8') as file:
            messages_admin = json.load(file)
        try:

            del messages_admin.get('granted_users_is', {})[str(user)]

        except Exception as e:
            print(e)
            pass

        try:

            messages_admin.get('granted_users', []).remove(int(user))

        except Exception as e:
            print(e)
            pass

        with open(JSON_FILE_ADMIN , 'w' , encoding='utf-8') as json_file:
            json.dump(messages_admin , json_file , ensure_ascii=False , indent=4)

        messages = open_json_admins()

    else:
        print('Файла нет')


def del_json_admin(user):
    if os.path.exists(JSON_FILE_ADMIN):
        with open(JSON_FILE_ADMIN, 'r', encoding='utf-8') as file:
            messages_admin = json.load(file)

        try:
            messages_admin['admins'].remove(int(user))
        except Exception as e:
            print(e)
            pass

        with open(JSON_FILE_ADMIN , 'w' , encoding='utf-8') as json_file:
            json.dump(messages_admin , json_file , ensure_ascii=False , indent=4)

        messages = open_json_admins()

    else:
        print('Файла нет')


def add_granted_users_is_data(userid, name, surname, phone):
    if os.path.exists(JSON_FILE_ADMIN):
        with open(JSON_FILE_ADMIN, 'r', encoding='utf-8') as file:
            messages_admin = json.load(file)

        try:
            messages_admin.get('granted_users_is', {})[str(userid)] = {
                "Name": str(name),
                "Surname": str(surname),
                "phone_number": str(phone)
            }
            print(messages_admin.get('granted_users_is', {})[str(userid)])
        except Exception as e:
            print(e)
            pass

        with open(JSON_FILE_ADMIN , 'w' , encoding='utf-8') as json_file:
            json.dump(messages_admin , json_file , ensure_ascii=False , indent=4)

        messages = open_json_admins()

