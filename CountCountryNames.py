import csv
from collections import Counter
import io
import json
import sys
from math import ceil
from pathlib import Path

# Female first names.
f_counts = Counter()
# Male first names.
m_counts = Counter()
# Last names.
l_counts = Counter()
# Unknow gender names.
u_counts = Counter()

p = Path('data')
for q in p.glob('*.csv'):
    country = str(q).split('.')[-2].split('\\')[-1]
    print(country)
    f_counts.clear()
    m_counts.clear()
    l_counts.clear()
    u_counts.clear()

    # Get our counts.
    with q.open(newline='', encoding='utf8') as f:
        namereader = csv.reader(f, delimiter=',', quotechar='"')
        for row in namereader:
            first = row[0]
            last = row[1]
            gender = row[2]

            # TODO: Spanish and Latin American naming conventions?
            if gender == 'F':
                f_counts[first] += 1
            elif gender == 'M':
                m_counts[first] += 1
            else:
                u_counts[first] += 1
            l_counts[last] += 1
        del f_counts['']
        del m_counts['']
        del l_counts['']
        del u_counts['']
        # Distribute genderless given names.
        for n, count in u_counts.items():
            fcount = f_counts[n]
            mcount = m_counts[n]
            denominator = fcount + mcount
            if denominator > 0:
                f_counts[n] += ceil(count * (fcount/(denominator)))
                m_counts[n] += ceil(count * (mcount/(denominator)))
        f_counts = +f_counts
        m_counts = +m_counts
        l_counts = +l_counts

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
