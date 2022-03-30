import tableutility as tu
import argparse
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

parser = argparse.ArgumentParser(description='Generate roll tables.')
parser.add_argument('-c', '--checks', action='store_true', dest='RUN_CHECKS')
parser.add_argument('-g', '--generate', action='store_true', dest='GENERATE_TABLES')
parser.add_argument('-v', '--verbose', action='store_true', dest='VERBOSE')
parser.add_argument('--output', type=Path, dest='OUTPUT_PATH')
args = parser.parse_args()

if args.GENERATE_TABLES:
    if not args.OUTPUT_PATH.is_dir():
        raise Exception("The path argument does not point to a directory.")
SCRIPT_THRESHOLD = 0.01

with io.open('population/countrydata.json', 'r', encoding='utf8') as f:
    countrydata = json.load(f)
countrytables = set(countrydata.keys())

with io.open('population/population.json', 'r', encoding='utf8') as f:
    population = json.load(f)

transcriptions = {}
class DataChecks(object):
    def gender_representation_filter(country):
        f = countrydata[country]['names']['F']
        m = countrydata[country]['names']['M']
        diff = abs((f - m) / m)
        return diff < 0.5

    # def language_representation_filter(country):
    #     pass

    def quantity_filter(country):
        p = countrydata[country]['names percentage']['L']
        c = countrydata[country]['names']['L']
        return p > 0.01 and c > 100000

    def script_support_filter(country):
        for scripts in countrydata[country]['scripts percentage'].values():
            for s, p in scripts.items():
                if p > SCRIPT_THRESHOLD and s not in transcriptions and s != 'Latin':
                    return False
        return True

    def type_representation_filter(country):
        f = countrydata[country]['names percentage']['F']
        l = countrydata[country]['names percentage']['L']
        m = countrydata[country]['names percentage']['M']
        diff = abs(((f + m) - l) / l)
        return diff < 0.01

checks = filter(lambda x: not x.startswith('__'), dir(DataChecks))
failed = {}
for check in checks:
    p = set(filter(getattr(DataChecks, check), countrytables))
    f = countrytables - p
    failed[check] = f


if args.RUN_CHECKS:
    if args.VERBOSE:
        print('    ' + ' '.join([k.upper()[0] for k in failed.keys()]))
        for c in sorted(countrytables):
            s = c + ' ' * 2
            for t in failed.values():
                s += 'x' if c in t else ' '
                s += ' '
            print(s)
    with io.open('../datachecks.csv', 'w', newline='', encoding='utf8') as f:
        writer = csv.writer(f)
        writer.writerow(('Country', *(k.split('_')[0].capitalize() for k in failed.keys()), 'Population'))
        rows = []
        for c in sorted(countrytables):
            rows.append((c, *('x' if c in t else '' for t in failed.values()), population[c]))
        rows.sort(key=lambda r: r[-1], reverse=True)
        writer.writerows(rows)

if args.GENERATE_TABLES:
    # When iterating, keep track of the timestamp for when files we process were
    # last modified, so we can check if this gets run again to only process new files.
    passed = sorted(countrytables.difference(*failed))

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
            c_name, [f_table, m_table], 'who-in-the-world.witw-user-tables', [1, 1]
        )
        f_macro = tu.make_macro(f_table['name'], f_table['_id'])
        m_macro = tu.make_macro(m_table['name'], m_table['_id'])
        c_macro = tu.make_macro(c_table['name'], c_table['_id'])

        user_tables.extend(map(lambda t:json.dumps(t,separators=(',',':')),[f_table,m_table,c_table]))
        user_macros.extend(map(lambda t:json.dumps(t,separators=(',',':')),[f_macro, m_macro, c_macro]))


    src_tables_path = (packs_dir_path / 'witw-src-tables.db').resolve()
    src_tables_path.write_text('\n'.join(src_tables), encoding='utf8')

    user_tables_path = (packs_dir_path / 'witw-user-tables.db').resolve()
    user_tables_path.write_text('\n'.join(user_tables), encoding='utf8')

    user_macros_path = (packs_dir_path / 'witw-user-macros.db').resolve()
    user_macros_path.write_text('\n'.join(user_macros), encoding='utf8')
