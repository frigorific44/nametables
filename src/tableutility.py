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
class MacroType(Enum):
    CHAT = 'chat'
    SCRIPT = 'script'

def generate_id(size=16, chars=string.ascii_uppercase + string.digits, seed=None):
    random.seed(seed)
    return ''.join(random.choice(chars) for _ in range(size))

def get_rranges(weights):
    rranges = []
    i = 0
    for weight in weights:
        lower = i + 1
        i += weight
        rranges.append([lower, i])
    return rranges

def make_macro(name, tableId, type=MacroType.SCRIPT.value):
    cmd = (
'''
const num = 10

const pack = game.packs.get("who-in-the-world.witw-user-tables")
'''
f'const table = await pack.getDocument("{tableId}")'
'''
const roll = await table.drawMany(num, {displayChat: false})
const subdivisions = subdivide(roll.results, num)
const nameStrings = subdivisions.map(x => x.map(y => y.data.text).join(" "))
const formattedStrings = nameStrings.map(x => `<p>${x}</p>`)
const rString = formattedStrings.join(" ")
fPrintMessage(rString)


function fPrintMessage(message) {
  let chatData = {
    user: game.user._id,
    content: message,
  };
  ChatMessage.create(chatData,{})
}

function subdivide(arr, numGroups) {
  const perGroup = Math.ceil(arr.length / numGroups);
  return new Array(numGroups)
    .fill('')
    .map((_, i) => arr.slice(i * perGroup, (i + 1) * perGroup));
}
'''
    )
    m = {
        '_id': generate_id(seed=name+"m"),
        'name': name,
        'type': type,
        'author': '0hNxyZp41uLKpCTW',
        'scope': 'global',
        'command': cmd,
    }
    return m


def make_table(tname, results, formula, replace=True, display=False, seed=None):
    rolltable = {
        '_id': generate_id(seed=seed),
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
    rranges = get_rranges(apportionment)
    for name, weight, range in zip(names, apportionment, rranges):
        r = {
            '_id': generate_id(seed=tname+name),
            'type': ResultType.TEXT.value,
            'text': name,
            'weight': weight,
            'range': range
        }
        results.append(r)

    return make_table(tname, results, f'1d{sum(apportionment)}', seed=tname+"c")

def from_comp_tables(tname, tables, collectionName, weights=None):
    if weights:
        rranges = get_rranges(weights)
    else:
        weights = [1 for i in range(len(tables))]
        rranges = [[1, 1] for i in range(len(tables))]
    results = []
    for table, weight, rrange in zip(tables, weights, rranges):
        r = {
            '_id': generate_id(seed=tname+table['name']),
            'type': ResultType.COMPENDIUM.value,
            'text': table['name'],
            'collection': collectionName,
            'resultId': table['_id'],
            'weight': weight,
            'range': rrange
        }
        results.append(r)

    return make_table(tname, results, f'1d{rranges[-1][-1]}', seed=tname+"t")
