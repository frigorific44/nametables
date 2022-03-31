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

SCRIPT_KEY = 'scripts' # The counts for the scripts used in names by type.
NAME_KEY = 'names' # The total counts for names by type.
SCRIPT_PERC_KEY = 'scripts percentage' # The proportion of each script in dataset by type.
NAME_PERC_KEY = 'names percentage' # The percentage of total population for name count by type.
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
            scripts[unicodedata2.string_script(name)] += int(count)

            if i >= MAXNAMES:
                break

    stotal = sum(scripts.values())
    if country not in data:
        data[country] = {
            NAME_KEY: {},
            NAME_PERC_KEY: {},
            SCRIPT_KEY: {},
            SCRIPT_PERC_KEY: {}
        }
    data[country][NAME_KEY][type] = total
    data[country][NAME_PERC_KEY][type] = total / populations[country]
    data[country][SCRIPT_KEY][type] = dict(scripts)
    data[country][SCRIPT_PERC_KEY][type] = {k: v/stotal for k, v in scripts.items()}

with io.open('countrydata.json', 'w', newline='', encoding='utf8') as f:
    json.dump(data, f, indent=4)
