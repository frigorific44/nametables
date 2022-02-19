import csv
from collections import Counter
import io
import json
from pathlib import Path
import pycountry

population = None
with io.open('population.json', 'r', encoding='utf8') as f:
    population = json.load(f)

def elaborateRow(row):
    percent = row[1] / population[row[0]]
    return (row[0], row[1], percent)

country_totals = Counter()

p = Path('..\counts')
for q in p.glob('*.csv'):
    if '-L' not in str(q):
        continue

    country = str(q).split('-')[-2].split('\\')[-1]
    print(country)
    # Get the total.
    with q.open(newline='', encoding='utf8') as f:
        namereader = csv.reader(f, delimiter=',', quotechar='"')
        for row in namereader:
            total = row[1]
            country_totals[country] = int(total)
            break

# Save as CSV ordered by total count.
with io.open('CountryTotals.csv', 'w', newline='', encoding='utf8') as f:
    writer = csv.writer(f)
    writer.writerows(map(elaborateRow, list(country_totals.most_common())))
