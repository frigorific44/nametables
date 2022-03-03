import tableutility as tu
import csv
import io
import json
from pathlib import Path
import pycountry
import sys


symbol_category = {
    'F': 'F Given',
    'M': 'M Given',
    'L': 'Surname'
}

OUTPUT_PATH = Path(sys.argv[1])
if not OUTPUT_PATH.is_dir():
    raise Exception("The path argument does not point to a directory.")
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
# print('    G Q S T')
# for c in sorted(countrytables):
#     s = c + ' ' * 2
#     for t in testFailures:
#         s += 'x' if c in t else ' '
#         s += ' '
#     print(s)

with io.open('datachecks.csv', 'w', newline='', encoding='utf8') as f:
    writer = csv.writer(f)
    writer.writerow(('Country', 'Gender', 'Quantity', 'Script', 'Type'))
    for c in sorted(countrytables):
        r = (c, *('x' if c in t else '' for t in testFailures))
        writer.writerow(r)


# When iterating, keep track of the timestamp for when files we process were
# last modified, so we can check if this gets run again to only process new files.
passed = sorted(countrytables.difference(*testFailures))

src_tables = []
user_tables = []
user_macros = []
packs_dir_path = (OUTPUT_PATH / 'packs').resolve()
packs_dir_path.mkdir(exist_ok=True)
counts_dir_path = Path('counts')
for c in passed:
    c_name = pycountry.countries.get(alpha_2=c).name
    c_tables = {}
    for q in counts_dir_path.glob(f'{c}-*.csv'):
        cat_symbol = q.stem.split('-')[-1]
        category = symbol_category[cat_symbol]
        tablename = f'{c_name} - {category}'
        with q.open(newline='', encoding='utf8') as f:
            table = tu.from_csv(f, tablename)
            c_tables[cat_symbol] = table
            table_json = json.dumps(table, separators=(',', ':'))
            src_tables.append(table_json)
    f_table = tu.from_comp_tables(
        f'{c_name} - F', [c_tables['F'], c_tables['L']], 'who-in-the-world.witw-src-tables'
    )
    m_table = tu.from_comp_tables(
        f'{c_name} - M', [c_tables['M'], c_tables['L']], 'who-in-the-world.witw-src-tables'
    )
    c_table = tu.from_comp_tables(
        c_name, [f_table, m_table], 'who-in-the-world.witw-user-tables'
    )
    user_tables.extend(map(lambda t:json.dumps(t,separators=(',',':')),[f_table,m_table,c_table]))
    # tu.from_csv(f, tname, type, size=2)


src_tables_path = (packs_dir_path / 'witw-src-tables.db').resolve()
src_tables_path.write_text('\n'.join(src_tables), encoding='utf8')

user_tables_path = (packs_dir_path / 'witw-user-tables.db').resolve()
user_tables_path.write_text('\n'.join(user_tables), encoding='utf8')

user_macros_path = (packs_dir_path / 'witw-user-macros.db').resolve()
user_macros_path.write_text('\n'.join(user_macros), encoding='utf8')
