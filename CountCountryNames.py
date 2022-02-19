import csv
from collections import Counter
import io
import json
import sys
from pathlib import Path

# Female first names.
f_counts = Counter()
# Male first names.
m_counts = Counter()
# Last names.
l_counts = Counter()

p = Path('data')
for q in p.glob('*.csv'):
    country = str(q).split('.')[-2].split('\\')[-1]
    print(country)
    f_counts.clear()
    m_counts.clear()
    l_counts.clear()

    # Get our counts.
    with q.open(newline='', encoding='utf8') as f:
        namereader = csv.reader(f, delimiter=',', quotechar='"')
        for row in namereader:
            first = row[0]
            last = row[1]
            gender = row[2]

            if gender == 'F':
                f_counts[first] += 1
            elif gender == 'M':
                m_counts[first] += 1
            l_counts[last] += 1
        del f_counts['']
        del m_counts['']
        del l_counts['']

    # Save as CSV ordered by count.
    # Save female names.
    with io.open(f'counts/{country}-F.csv', 'w', newline='', encoding='utf8') as f:
        writer = csv.writer(f)
        writer.writerow(('Total', f_counts.total()))
        writer.writerows(list(f_counts.most_common()))
    # Save male names.
    with io.open(f'counts/{country}-M.csv', 'w', newline='', encoding='utf8') as f:
        writer = csv.writer(f)
        writer.writerow(('Total', m_counts.total()))
        writer.writerows(list(m_counts.most_common()))
    #Save last names.
    with io.open(f'counts/{country}-L.csv', 'w', newline='', encoding='utf8') as f:
        writer = csv.writer(f)
        writer.writerow(('Total', l_counts.total()))
        writer.writerows(list(l_counts.most_common()))
