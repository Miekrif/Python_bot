import xlrd
import random
#открываем файл
rb = xlrd.open_workbook(r'userid=name.xls')

#выбираем активный лист
sheet = rb.sheet_by_index(0)

lines = []

for i in range(3):
    for j in range(0, 1):
        # Print the cell values with tab space
        lines.append(sheet.cell_value(i, j))
        print(i + 1, sheet.cell_value(i, j), end = '\t')
    print('')

print(random.choice(lines))