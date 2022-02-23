import csv
import io
import json
from pathlib import Path


SCRIPT_THRESHOLD = 0.01

with io.open('population/countrydata.json', 'r', encoding='utf8') as f:
    countrydata = json.load(f)
countrytables = set(countrydata.keys())

transliterations = {}



def getGenderDiff(country):
    f = countrydata[country]['names']['F']
    m = countrydata[country]['names']['M']
    return (f - m) / m

def getTypeDiff(country):
    f = countrydata[country]['names percentage']['F']
    l = countrydata[country]['names percentage']['L']
    m = countrydata[country]['names percentage']['M']
    return ((f + m) - l) / l



# Filter on whether each gender is sufficiently represented.
def genderRepresentationFilter(country):
    return abs(getGenderDiff(country)) < 0.5

# Filter on whether the scripts present are representative
# of the country's languages.
def languageRepresentationFilter(country):
    pass

# Filter on whether there are sufficient numbers or at least
# a sufficient percentage compared to the actual population.
def quantityFilter(country):
    p = countrydata[country]['names percentage']['L']
    c = countrydata[country]['names']['L']
    return p > 0.01 and c > 100000

# Filter on whether scripts present are supported by the current pipeline.
def scriptSupportFilter(country):
    for scripts in countrydata[country]['scripts percentage'].values():
        for s, p in scripts.items():
            if p > SCRIPT_THRESHOLD and s not in transliterations and s != 'Latin':
                return False
    return True

# Filter on whether there is not too great a disparity
# between representation of each name type.
def typeRepresentationFilter(country):
    return abs(getTypeDiff(country)) < 0.01



# print(*sorted([(k,getGenderDiff(k)) for k in countrytables], key=lambda y:y[1]), sep='\n')
genderPassed = set(filter(genderRepresentationFilter, countrytables))
genderFailed = countrytables - genderPassed
# print(sorted(genderFailed))

quantityPassed = set(filter(quantityFilter, countrytables))
quantityFailed = countrytables - quantityPassed
# print(sorted(quantityFailed))

scriptPassed = set(filter(scriptSupportFilter, countrytables))
scriptFailed = countrytables - scriptPassed
# print(sorted(scriptFailed))

# print(*sorted([(k,getTypeDiff(k)) for k in countrytables], key=lambda y:y[1]), sep='\n')
typePassed = set(filter(typeRepresentationFilter, countrytables))
typeFailed = countrytables - typePassed
# print(sorted(typeFailed))

testFailures = [genderFailed, quantityFailed, scriptFailed, typeFailed]
print('    G Q S T')
for c in sorted(countrytables):
    s = c + ' ' * 2
    for t in testFailures:
        s += 'x' if c in t else ' '
        s += ' '
    print(s)

with io.open('datachecks.csv', 'w', newline='', encoding='utf8') as f:
    writer = csv.writer(f)
    writer.writerow(('Country', 'Gender', 'Quantity', 'Script', 'Type'))
    for c in sorted(countrytables):
        r = (c, *('x' if c in t else '' for t in testFailures))
        writer.writerow(r)


# When iterating, keep track of the timestamp for when files we process were
# last modified, so we can check if this gets run again to only process new files.
