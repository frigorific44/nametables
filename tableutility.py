import apportionment.apportionment.methods as apportion
import csv
import io
import json
import pycountry
import random
import string


def generate_id(size=16, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def make_macro():
    pass

def make_table(tname, entries, weights, type):
    results = []
    i = 0
    for name, weight in zip(entries, weights):
        lower = i + 1
        i += weight
        upper = i + weight
        r = {
            '_id': generate_id(),
            'type': type,
            'text': name,
            'weight': weight,
            'range': [lower, i]
        }
        results.append(r)

    rolltable = {
        '_id': generate_id(),
        'name': tname,
        'descriptiion': '?',
        'results': results,
        'formula': f'1d{sum(weights)}',
        'replacement': True,
        'displayRoll': False,
        # 'permission': {},
        'flags': {}
    }
    return rolltable

def from_csv(f, tname, type, size=1000, votes=2000):
    reader = csv.reader(f)
    names = []
    counts = []

    reader.__next__()
    for i, row in enumerate(reader):
        names.append(row[0])
        counts.append(int(row[1]))
        if i >= size:
            break
    apportionment = apportion.compute(
        'hill', counts, votes, parties=names, verbose=False, fractions=False
    )

    return make_table(tname, names, apportionment, type)
    # results = []
    # i = 0
    # for name, weight in zip(names, apportionment):
    #     lower = i + 1
    #     i += weight
    #     upper = i + weight
    #     r = {
    #         '_id': generate_id(),
    #         'type': type,
    #         'text': name,
    #         'weight': weight,
    #         'range': [lower, i]
    #     }
    #     results.append(r)
    #
    # rolltable = {
    #     '_id': generate_id(),
    #     'name': tname,
    #     'descriptiion': '?',
    #     'results': results,
    #     'formula': f'1d{votes}',
    #     'replacement': True,
    #     'displayRoll': False,
    #     # 'permission': {},
    #     'flags': {}
    # }
    # return rolltable
