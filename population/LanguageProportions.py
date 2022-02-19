import csv
from collections import Counter
import io
import json
from pathlib import Path
import pycountry
import unicodedata2

MAXNAMES = 1000

sproportions = {}

p = Path('..\counts')
for q in p.glob('*.csv'):
    country, type = str(q).split('\\')[-1][:-len('.csv')].split('-')
    print(country)

    scripts = Counter()

    with q.open(newline='', encoding='utf8') as f:
        countreader = csv.reader(f, delimiter=',', quotechar='"')
        countreader.__next__()
        majority = Counter()
        for i, row in enumerate(countreader):
            name, count = row

            majority.clear()
            for c in name:
                script = unicodedata2.script_cat(c)[0]
                if script != 'Common':
                    majority[script] += 1
            scripts[majority.most_common(1)[0][0]] += int(count)

            if i >= MAXNAMES:
                break

    if country not in sproportions:
        sproportions[country] = {}
    sproportions[country][type] = dict(scripts)


with io.open('countryscripts.json', 'w', newline='', encoding='utf8') as f:
    json.dump(sproportions, f, indent=4)
