import apportionment.apportionment.methods as apportion
import csv
from enum import Enum
import io
import json
import pycountry
import random
import string

class ResultType(Enum):
    TEXT = 0
    DOCUMENT = 1
    COMPENDIUM = 2


def generate_id(size=16, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def make_macro(id):
    return (
        f'const table = game.tables.find(t => t._id === {id})'
        '''
        const results = await table.draw().results
        const rString = results.reduce(concatResult, "")

        function  concatResult(s, result) {
            return s + "\n" + result.data.text
        }

        function fPrintMessage(message) {
            let chatData = {
                user: game.user._id,
                content: message,
            };
            ChatMessage.create(chatData,{})
        }
        '''
    )

def make_table(tname, entries, weights, type=ResultType.TEXT.value):
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
    }
    return rolltable

def make_table(tname, results, formula, replace=True, display=False):
    rolltable = {
        '_id': generate_id(),
        'name': tname,
        'descriptiion': '',
        'results': results,
        'formula': formula,
        'replacement': replace,
        'displayRoll': display,
    }
    return rolltable

def from_csv(f, tname, size=1000, votes=2000):
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

    results = []
    i = 0
    for name, weight in zip(names, apportionment):
        lower = i + 1
        i += weight
        upper = i + weight
        r = {
            '_id': generate_id(),
            'type': ResultType.TEXT.value,
            'text': name,
            'weight': weight,
            'range': [lower, i]
        }
        results.append(r)

    return make_table(tname, results, f'1d{sum(apportionment)}')

def from_comp_tables(tname, tables, collectionName):
    results = []
    for table in tables:
        r = {
            '_id': generate_id(),
            'type': ResultType.COMPENDIUM.value,
            'text': table['name'],
            'collection': collectionName,
            'resultId': table['_id'],
            'weight': 1,
            'range': [1, 1]
        }
        results.append(r)

    return make_table(tname, results, '1d1')
