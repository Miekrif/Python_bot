from datetime import *
# from bot import clean_on_space
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
    KPI_it = []
    while i != 0:
        line1 = kpi[f'A{k}'].value
        k += 1
        print(line1)
        KPI_it.append(line1)
        if line1 == None:
            print(KPI_it)
            KPI_it.pop()
            i = 0
            # print(KPI)
    return KPI_it



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
#             i = return
#             # a_send_message = random.choice(Words)
#             # print(a_send_message)

# class send_mess():
#     a_send_message = random.choice(Words)



########################################################


# Уборка ЦЧИ
async def do_cleaning_cchi(day):
    if day.strftime("%A") == 'Monday':
        Monday = []
        k = 1
        i = 1
        while i != 0:
            line = sheet_clean_cchi[f'A{k}'].value
            k += 1
            print(line)
            Monday.append(line)
            if line == None:
                Monday.pop()
                i = 0
        Monday = str(Monday).replace('[', '').replace(']', '').replace(r'\n', '').replace(r"'", '').replace(r",", '\n')
        return Monday
        #await clean_on_space(clean=Monday)
        # print(day.strftime("%A"))
    elif day.strftime("%A") == 'Tuesday':
        Tuesday = []
        k = 1
        i = 1
        while i != 0:
            line = sheet_clean_cchi[f'B{k}'].value
            k += 1
            print(line)
            Tuesday.append(line)
            if line == None:
                Tuesday.pop()
                i = 0
        Tuesday = str(Tuesday).replace('[', '').replace(']', '').replace(r'\n', '').replace(r"'", '').replace(r",", '\n')
        return Tuesday
        #await clean_on_space(clean=Tuesday)
        # print(day.strftime("%A"))
    elif day.strftime("%A") == 'Wednesday':
        Wednesday = []
        k = 1
        i = 1
        while i != 0:
            line = sheet_clean_cchi[f'C{k}'].value
            k += 1
            print(line)
            Wednesday.append(line)
            if line == None:
                Wednesday.pop()
                i = 0
        Wednesday = str(Wednesday).replace('[', '').replace(']', '').replace(r'\n', '').replace(r"'", '').replace(r",", '\n')
        return Wednesday
        #await clean_on_space(clean=Wednesday)
    elif day.strftime("%A") == 'Thursday':
        Thursday = []
        k = 1
        i = 1
        while i != 0:
            line = sheet_clean_cchi[f'D{k}'].value
            k += 1
            print(line)
            Thursday.append(line)
            if line == None:
                Thursday.pop()
                i = 0
        Thursday = str(Thursday).replace('[', '').replace(']', '').replace(r'\n', '').replace(r"'", '').replace(r",", '\n')
        return Thursday
        #await clean_on_space(clean=Thursday)
    elif day.strftime("%A") == 'Friday':
        Friday = []
        k = 1
        i = 1
        while i != 0:
            line = sheet_clean_cchi[f'E{k}'].value
            k += 1
            print(line)
            Friday.append(line)
            if line == None:
                Friday.pop()
                i = 0
        Friday = str(Friday).replace('[', '').replace(']', '').replace(r'\n', '').replace(r"'", '').replace(r",",
                                                                                                                '\n')
        return Friday
        #await clean_on_space(clean=Friday)
    elif day.strftime("%A") == "Saturday":
        Saturday = []
        k = 1
        i = 1
        while i != 0:
            line = sheet_clean_cchi[f'F{k}'].value
            k += 1
            print(line)
            Saturday.append(line)
            if line == None:
                Saturday.pop()
                i = 0
        Saturday = str(Saturday).replace('[', '').replace(']', '').replace(r'\n', '').replace(r"'", '').replace(r",",
                                                                                                            '\n')
        return Saturday
        #await clean_on_space(clean=Saturday)

    elif day.strftime("%A") == 'Sunday':
        Sunday = []
        k = 1
        i = 1
        while i != 0:
            line = sheet_clean_cchi[f'G{k}'].value
            k += 1
            print(line)
            Sunday.append(line)
            if line == None:
                Sunday.pop()
                i = 0
        Sunday = str(Sunday).replace('[', '').replace(']', '').replace(r'\n', '').replace(r"'", '').replace(r",",
                                                                                                                '\n')
        return Sunday
        #await clean_on_space(clean=Sunday)


# Уборка Пушка
async def do_cleaning_pyshk(day):
    if day.strftime("%A") == 'Monday':
        Monday = []
        k = 1
        i = 1
        while i != 0:
            line = sheet_clean_cchi[f'A{k}'].value
            k += 1
            print(line)
            Monday.append(line)
            if line == None:
                Monday.pop()
                i = 0
        Monday = str(Monday).replace('[', '').replace(']', '').replace(r'\n', '').replace(r"'", '').replace(r",", '\n')
        return Monday
        #await clean_on_space(clean=Monday)
        # print(day.strftime("%A"))
    elif day.strftime("%A") == 'Tuesday':
        Tuesday = []
        k = 1
        i = 1
        while i != 0:
            line = sheet_clean_cchi[f'B{k}'].value
            k += 1
            print(line)
            Tuesday.append(line)
            if line == None:
                Tuesday.pop()
                i = 0
        Tuesday = str(Tuesday).replace('[', '').replace(']', '').replace(r'\n', '').replace(r"'", '').replace(r",", '\n')
        return Tuesday
        #await clean_on_space(clean=Tuesday)
        # print(day.strftime("%A"))
    elif day.strftime("%A") == 'Wednesday':
        Wednesday = []
        k = 1
        i = 1
        while i != 0:
            line = sheet_clean_cchi[f'C{k}'].value
            k += 1
            print(line)
            Wednesday.append(line)
            if line == None:
                Wednesday.pop()
                i = 0
        Wednesday = str(Wednesday).replace('[', '').replace(']', '').replace(r'\n', '').replace(r"'", '').replace(r",",
                                                                                                              '\n')
        return Wednesday
        #await clean_on_space(clean=Wednesday)
    elif day.strftime("%A") == 'Thursday':
        Thursday = []
        k = 1
        i = 1
        while i != 0:
            line = sheet_clean_cchi[f'D{k}'].value
            k += 1
            print(line)
            Thursday.append(line)
            if line == None:
                Thursday.pop()
                i = 0
        Thursday = str(Thursday).replace('[', '').replace(']', '').replace(r'\n', '').replace(r"'", '').replace(r",",
                                                                                                                  '\n')
        return Thursday
        #await clean_on_space(clean=Thursday)
    elif day.strftime("%A") == 'Friday':
        Friday = []
        k = 1
        i = 1
        while i != 0:
            line = sheet_clean_cchi[f'E{k}'].value
            k += 1
            print(line)
            Friday.append(line)
            if line == None:
                Friday.pop()
                i = 0
        Friday = str(Friday).replace('[', '').replace(']', '').replace(r'\n', '').replace(r"'", '').replace(r",",
                                                                                                                '\n')
        return Friday
        # #await clean_on_space(clean=Friday)
    elif day.strftime("%A") == "Saturday":
        Saturday = []
        k = 1
        i = 1
        while i != 0:
            line = sheet_clean_cchi[f'F{k}'].value
            k += 1
            print(line)
            Saturday.append(line)
            if line == None:
                Saturday.pop()
                i = 0
        Saturday = str(Saturday).replace('[', '').replace(']', '').replace(r'\n', '').replace(r"'", '').replace(r",",
                                                                                                            '\n')
        return Saturday
        #await clean_on_space(clean=Saturday)
    elif day.strftime("%A") == 'Sunday':
        Sunday = []
        k = 1
        i = 1
        while i != 0:
            line = sheet_clean_cchi[f'G{k}'].value
            k += 1
            print(line)
            Sunday.append(line)
            if line == None:
                Sunday.pop()
                i = 0
        Sunday = str(Sunday).replace('[', '').replace(']', '').replace(r'\n', '').replace(r"'", '').replace(r",",
                                                                                                                '\n')
        return Sunday
        #await clean_on_space(clean=Sunday)


# day = date.weekday(weekday)
# print(day)
# day = datetime.now()
# print(day.strftime("%A"))


# async def po_tochkam(tochka):
#     central = 'Центральная Чайная история'
#     if tochka == central:
#         await do_cleaning_cchi(day)
#     else:
#         await do_cleaning_pyshk(day)
