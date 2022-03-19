from datetime import *
from bot import clean_on_space
import openpyxl
import asyncio
import random
import aioschedule


# Import data from excel
book = openpyxl.open('CHI.xlsx', read_only=True)
sheet_clean_cchi = book['clean_cchi']
sheet_clean_pyshk = book['clean_pyshk']
word_book = book['word']
kpi = book['KPI']


# For KPI

async def KPI_lines():
    k = 1
    i = 1
    KPI = []
    while i != 0:
        line = kpi[f'A{k}'].value
        k += 1
        if line == None:
            KPI.pop()
            i = 0
        else:
            KPI.append(line)
            # print(KPI)



# Продаванские мудрости
# def word_send(Words):
#     # print(type(Words))
#     global a_send_message
#     a_send_message = random.choice(Words)
    # a_send_message = [a_send_message]
    # print(a)
    # return a_send_message

# def word_mentor():
#     k = 1
#     i = 1
#     global Words
#     Words = []
#     while i != 0:
#         line = word_book[f'A{k}'].value
#         k += 1
#         # print(line)
#         Words.append(line)
#         if line == None:
#             i = 0
#             # a_send_message = random.choice(Words)
#             # print(a_send_message)

# class send_mess():
#     a_send_message = random.choice(Words)



########################################################


# Уборка ЦЧИ
async def do_cleaning_cchi(day):
    if day.strftime("%A") == 'Monday':
        Monday = {}
        k = 1
        i = 1
        while i != 0:
            line = sheet_clean_cchi[k][0].value
            k += 1
            print(line)
            Monday['Monday'] = [line]
            if line == None:
                i = 0
        await clean_on_space(clean=Monday.values())
        print(day.strftime("%A"))
    elif day.strftime("%A") == 'Tuesday':
        Tuesday = {}
        k = 1
        i = 1
        while i != 0:
            line = sheet_clean_cchi[k][1].value
            k += 1
            print(line)
            Tuesday['Tuesday'] = [line]
            if line == None:
                i = 0
        await clean_on_space(clean=Tuesday.values())
        print(day.strftime("%A"))
    elif day.strftime("%A") == 'Wednesday':
        Wednesday = {}
        k = 1
        i = 1
        while i != 0:
            line = sheet_clean_cchi[k][2].value
            k += 1
            print(line)
            Wednesday['Wednesday'] = [line]
            if line == None:
                i = 0
        await clean_on_space(clean=Wednesday.values())
    elif day.strftime("%A") == 'Thursday':
        Thursday = {}
        k = 1
        i = 1
        while i != 0:
            line = sheet_clean_cchi[k][3].value
            k += 1
            print(line)
            Thursday['Thursday'] = [line]
            if line == None:
                i = 0
        await clean_on_space(clean=Thursday.values())
    elif day.strftime("%A") == 'Friday':
        Friday = {}
        k = 1
        i = 1
        while i != 0:
            line = sheet_clean_cchi[k][4].value
            k += 1
            print(line)
            Friday['Friday'] = [line]
            if line == None:
                i = 0
        await clean_on_space(clean=Friday.values())
    elif day.strftime("%A") == "Saturday":
        Saturday = {}
        k = 1
        i = 1
        while i != 0:
            line = sheet_clean_cchi[k][5].value
            k += 1
            print(line)
            Saturday['Saturday'] = [line]
            if line == None:
                i = 0
        await clean_on_space(clean=Saturday.values())

    elif day.strftime("%A") == 'Sunday':
        Sunday = {}
        k = 1
        i = 1
        while i != 0:
            line = sheet_clean_cchi[k][6].value
            k += 1
            print(line)
            Sunday['Sunday'] = [line]
            if line == None:
                i = 0
        await clean_on_space(clean=Sunday.values())


# Уборка Пушка
async def do_cleaning_pyshk(day):
    if day.strftime("%A") == 'Monday':
        Monday = {}
        k = 1
        i = 1
        while i != 0:
            line = sheet_clean_cchi[k][0].value
            k += 1
            print(line)
            Monday['Monday'] = [line]
            if line == None:
                i = 0
        await clean_on_space(clean=Monday.values())
        print(day.strftime("%A"))
    elif day.strftime("%A") == 'Tuesday':
        Tuesday = {}
        k = 1
        i = 1
        while i != 0:
            line = sheet_clean_cchi[k][1].value
            k += 1
            print(line)
            Tuesday['Tuesday'] = [line]
            if line == None:
                i = 0
        await clean_on_space(clean=Tuesday.values())
        print(day.strftime("%A"))
    elif day.strftime("%A") == 'Wednesday':
        Wednesday = {}
        k = 1
        i = 1
        while i != 0:
            line = sheet_clean_cchi[k][2].value
            k += 1
            print(line)
            Wednesday['Wednesday'] = [line]
            if line == None:
                i = 0
        await clean_on_space(clean=Wednesday.values())
    elif day.strftime("%A") == 'Thursday':
        Thursday = {}
        k = 1
        i = 1
        while i != 0:
            line = sheet_clean_cchi[k][3].value
            k += 1
            print(line)
            Thursday['Thursday'] = [line]
            if line == None:
                i = 0
        await clean_on_space(clean=Thursday.values())
    elif day.strftime("%A") == 'Friday':
        Friday = {}
        k = 1
        i = 1
        while i != 0:
            line = sheet_clean_cchi[k][4].value
            k += 1
            print(line)
            Friday['Friday'] = [line]
            if line == None:
                i = 0
        await clean_on_space(clean=Friday.values())
    elif day.strftime("%A") == "Saturday":
        Saturday = {}
        k = 1
        i = 1
        while i != 0:
            line = sheet_clean_cchi[k][5].value
            k += 1
            print(line)
            Saturday['Saturday'] = [line]
            if line == None:
                i = 0
        await clean_on_space(clean=Saturday.values())

    elif day.strftime("%A") == 'Sunday':
        Sunday = {}
        k = 1
        i = 1
        while i != 0:
            line = sheet_clean_cchi[k][6].value
            k += 1
            print(line)
            Sunday['Sunday'] = [line]
            if line == None:
                i = 0
        await clean_on_space(clean=Sunday.values())


# day = date.weekday(weekday)
# print(day)
day = datetime.now()
print(day.strftime("%A"))


async def po_tochkam(tochka):
    central = 'Центральная Чайная история'
    if tochka == central:
        await do_cleaning_cchi(day)
    else:
        await do_cleaning_pyshk(day)
