import os
import shutil
import logging
import pandas as pd
from PDF.square_tag import start as square_tag
from PDF.horizon_tag import start as horizon_tag

stop_word = 'nan'

color_type = {
    'ГАБА': '#CD7F32',
    'УЛУН': '#E75C21',
    'КРАСНЫЙ': '#FF0033',
    'СВЕТЛЫЕ УЛУНЫ': '#77DDE7',
    'СВ УЛУН': '#77DDE7',
    'ЗЕЛЕНЫЙ': '#7ED957',
    'ЖЕЛТЫЙ': '#FFED00',
    'БЕЛЫЙ': '#FFFFFF',
    'ФХДЦ': '#8A6642',
    'ДХП': '#CC7722',
    'ХЕЙ ЧА': '#FFFFFF'
}


def start_logic():
    xls = pd.ExcelFile(os.path.abspath('PDF/counter.xlsx'))
    sheets = xls.sheet_names
    try:
        # Проходим по каждому листу в файле
        for sheet in sheets:
            # Читаем данные с текущего листа
            data = pd.read_excel(xls, sheet)
            print('*'*100)
            print(sheet)
            # Итерируемся по каждой строке данных
            for index, row in data.iterrows():
                if str(str(row['Наименование'])) in str(stop_word):
                    break
                # print(row)
                # Получаем нужный цвет из словаря
                # print(df.columns)
                # Обработка цены
                price = str(convert_to_appropriate_type(row['Цена']))
                if float(row['Цена']) < 20:
                    price = price + 'ρ (A)'
                elif float(row['Цена']) <= 35:
                    price = price + 'ρ (A+)'
                elif float(row['Цена']) <= 55:
                    price = price + 'ρ (A++)'
                else:
                    price = price + 'ρ'
                print(
                    color_type.get(str(row['Тип чая']).upper(), '#E75C21'),
                    str(row['Тип чая']),
                    str(row['Наименование']).replace('/', '\\'),
                    price
                )
                # Здесь вставьте вызовы функций модулей horizon и square в соответствии с именем листа
                if sheet.lower() == 'horizon':
                    horizon_tag(color_type=color_type.get(str(row['Тип чая']).upper(), '#E75C21'),
                                color_name='#FFFFFF',
                                color_price='#FFB12A',
                                tea_type=str(row['Тип чая']),
                                name_of_tea=str(row['Наименование']).replace('/', '\\'),
                                price_tea=price)

                elif sheet.lower() == 'square':
                    square_tag(color_type=color_type.get(str(row['Тип чая']).upper(), '#E75C21'),
                               color_name='#FFFFFF',
                               color_price='#FFB12A',
                               tea_type=str(row['Тип чая']),
                               name_of_tea=str(row['Наименование']).replace('/', '\\'),
                               price_tea=price)
    except Exception as e:
        print(e)


def clear_subdirectories(path):
    try:
        # Проверяем, существует ли заданный путь
        if os.path.exists(path) and os.path.isdir(path):
            # Проходим по всем поддиректориям
            for root_dir, dirs, files in os.walk(path):
                for dir in dirs:
                    dir_path = os.path.join(root_dir, dir)
                    # Удаляем все файлы и поддиректории в текущей поддиректории
                    for filename in os.listdir(dir_path):
                        if '1' in filename:
                            continue
                        file_path = os.path.join(dir_path, filename)
                        try:
                            if os.path.isfile(file_path) or os.path.islink(file_path):
                                os.unlink(file_path)
                            elif os.path.isdir(file_path):
                                shutil.rmtree(file_path)
                        except Exception as e:
                            print(f'Не удалось удалить {file_path}. Причина: {e}')
        else:
            print(f'Путь {path} не существует или не является директорией')
    except Exception as e:
        print(e)


def convert_to_appropriate_type(num):
    if num.is_integer():
        return int(num)
    return num


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    logger.info("Информационное сообщение")
    logger.warning("Предупреждение")
    logger.error("Ошибка")
    clear_subdirectories(os.path.abspath('output'))
    start_logic()