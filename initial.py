import os
import shutil


def copy_initial_file():
    if not os.path.exists('jsons/message.json'):
        shutil.copy('jsons/message.example', 'jsons/message.json')

