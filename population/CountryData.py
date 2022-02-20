import csv
from collections import Counter
import io
import json
from pathlib import Path
import unicodedata2
# Generates a JSON file to be used in a decision-making process on each country.
# {
# ...
#     "Country": {
#         "scripts": {},
#         "size": {"F": int, "L": int, "M": int},
#         "pop_percent": {"F": int, "L": int, "M": int}
#     }
# ...
# }

MAXNAMES = 1000

populations = None
with io.open('population.json', 'r', encoding='utf8') as f:
    populations = json.load(f)

data = {}

p = Path('..\counts')
for q in p.glob('*.csv'):
    country, type = str(q).split('\\')[-1][:-len('.csv')].split('-')
    print(country)
    scripts = Counter()

    with q.open(newline='', encoding='utf8') as f:
        countreader = csv.reader(f, delimiter=',', quotechar='"')
        total = int(countreader.__next__()[1])

        for i, row in enumerate(countreader):
            name, count = row
            for c in name:
                script = unicodedata2.script_cat(c)[0]
                if script != 'Common':
                    scripts[script] += int(count)
                    break
            if i >= MAXNAMES:
                break

    if country not in data:
        data[country] = {
            'scripts': {},
            'size': {},
            'pop_percent': {}
        }
    data[country]['scripts'][type] = dict(scripts)
    data[country]['size'][type] = total
    data[country]['pop_percent'][type] = total / populations[country]

with io.open('countrydata.json', 'w', newline='', encoding='utf8') as f:
    json.dump(data, f, indent=4)
