import xlrd
import random
from bot import lines
#открываем файл
rb = xlrd.open_workbook(r'userid=name.xls')

#выбираем активный лист
sheet = rb.sheet_by_index(0)

# lines = []
b = len(lines)
print(b)

def che():
    for i in range(b):
        for j in range(0, 1):
            # Print the cell values with tab space
            lines.append(sheet.cell_value(i, j))
            # print(i + 1, sheet.cell_value(i, j), end = '\t')
    print('')


print(random.choice(lines))