import csv
import sys
import io


country_code = sys.argv[1]
num = int(sys.argv[2])

with io.open(f'counts/{country_code}-F.csv', 'r', newline='', encoding='utf8') as f:
    reader = csv.reader(f, delimiter=',', quotechar='"')
    total = None
    sum = 0
    i = 1
    for row in reader:
        if total == None:
            total = int(row[1])
        else:
            sum += int(row[1])
        if i > num:
            break
        i += 1
    print(f'F: {sum / total}')

with io.open(f'counts/{country_code}-M.csv', 'r', newline='', encoding='utf8') as f:
    reader = csv.reader(f, delimiter=',', quotechar='"')
    total = None
    sum = 0
    i = 1
    for row in reader:
        if total == None:
            total = int(row[1])
        else:
            sum += int(row[1])
        if i > num:
            break
        i += 1
    print(f'M: {sum / total}')

with io.open(f'counts/{country_code}-L.csv', 'r', newline='', encoding='utf8') as f:
    reader = csv.reader(f, delimiter=',', quotechar='"')
    total = None
    sum = 0
    i = 1
    for row in reader:
        if total == None:
            total = int(row[1])
        else:
            sum += int(row[1])
        if i > num:
            break
        i += 1
    print(f'L: {sum / total}')
