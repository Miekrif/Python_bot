import xlrd
from datetime import *
import random
import openpyxl

day = datetime.now()
book = openpyxl.open('CHI.xlsx', read_only=True)
word_book = book['word']
sheet_clean_cchi = book['clean_cchi']



# a = 'Monday'
#
#
# if a == 'Monday':
#     Monday = {}
#     k = 1
#     i = 1
#     while i != 0:
#         line = sheet_clean_cchi[k][0].value
#         k += 1
#         print(line)
#         Monday['Monday'] = [line]
#         if line == None:
#             i = 0
# from bot import lines
# #открываем файл
# rb = xlrd.open_workbook(r'userid=name.xls')
#
# #выбираем активный лист
# sheet = rb.sheet_by_index(0)
#
# # lines = []
# b = len(lines)
# print(b)
#
# def che():
#     for i in range(b):
#         for j in range(0, 1):
#             # Print the cell values with tab space
#             lines.append(sheet.cell_value(i, j))
#             # print(i + 1, sheet.cell_value(i, j), end = '\t')
#     print('')
#
#
# print(random.choice(lines))
kpi = book['KPI']
#For KPI
def KPI_lines():
    k = 1
    i = 1
    global KPI
    KPI = []
    while i != 0:
        line = kpi[f'A{k}'].value
        k += 1
        KPI.append(line)
        if line == None:
            i = 0
            print(KPI)


KPI_lines()
print(KPI)
def word_send(Words):
    print(type(Words))
    a = random.choice(Words)
    print(a)


def word_mentor():
    k = 1
    i = 1
    Words = []
    while i != 0:
        line = word_book[f'A{k}'].value
        k += 1
        print(line)
        Words.append(line)
        if line == None:
            i = 0
            word_send(Words)

    # word_send(Word)

