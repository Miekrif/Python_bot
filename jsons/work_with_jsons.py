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