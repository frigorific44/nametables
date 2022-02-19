import apportionment.apportionment.methods as apportion
import csv
import io
import json
import matplotlib as mpl
import numpy as np
import time
from fractions import Fraction
import warnings
warnings.filterwarnings('error')

TABLE_SIZE = 1000
names = []
counts = []
methods = [
    'quota',
    'largest_remainder',
    'dhondt',
    'saintelague',
    'modified_saintelague',
    'huntington', # gives at least 1
    'adams', # gives at least 1
    'dean' # gives at least 1
]

with io.open('counts/US-L.csv', encoding='utf8') as f:
    reader = csv.reader(f)
    reader.__next__()
    i = 0
    for row in reader:
        names.append(row[0])
        counts.append(int(row[1]))
        i += 1
        if i >= TABLE_SIZE:
            break

# counts = np.array(counts)

# a = [Fraction(8, 12), Fraction(1, 7), Fraction(99, 100), Fraction(1, 999999999)]
# print(np.sum(a))
# print(apportion.compute(methods[7], counts, 999, names, verbose=False))
# 420 seconds
start = time.time()
for m in methods:
    print(m)
    apportion.compute(m, counts, 2000, parties=names, verbose=False, fractions=False)
# apportion.compute('quota', counts, 100, verbose=False, fractions=True)
print(time.time() - start)
