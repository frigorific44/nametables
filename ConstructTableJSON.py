import apportionment.apportionment.methods as apportion
import csv
import io
import json
import pycountry

names = []
counts = []

fname = 'US-L.csv'

with io.open(fname, encoding='utf8') as f:
    reader = csv.reader(f)
    # reader.__next__()
    for row in reader:
        names.append(row[0])
        counts.append(int(row[1]))
n = 2000
apportionment = apportion.compute('hill', counts, n, parties=names, verbose=False, fractions=False)

# Get the country name.
countrycode = fname.split('/')[-1].split('.')[-2].split('-')[0]
country = pycountry.countries.get(alpha_2=countrycode)
countryname = country.name

results = []
i = 0
for name, count in zip(names, apportionment):
    lower = i + 1
    i += count
    upper = i + count
    r = {
        'text': name,
        'weight': count,
        'range': [lower, i]
    }
    results.append(r)

rolltable = {
    'name': countryname,
    'results': results,
    'formula': f'1d{n}'
}

newfname = fname.split('/')[-1].split('.')[0] + '.json'
with io.open(newfname, 'w', newline='', encoding='utf8') as f:
    json.dump(rolltable, f, separators=(',',':'))
