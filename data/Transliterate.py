from namecounter import NameCounter
import io
from qazaq_transliterator import translit as qazaq_translit
from nametables.population import unicodedata2


def transliterate_country(country, translit):
    translit_row = lambda t:(translit(t[0]), t[1])
    nc = NameCounter(country)
    with io.open(f'../counts/{country}-F.csv', 'r', newline='', encoding='utf8') as f:
        nc.count_csv(f, skipfirst=True, count_f=translit_row)
    with io.open(f'../counts/{country}-L.csv', 'r', newline='', encoding='utf8') as f:
        nc.count_csv(f, skipfirst=True, count_l=translit_row)
    with io.open(f'../counts/{country}-M.csv', 'r', newline='', encoding='utf8') as f:
        nc.count_csv(f, skipfirst=True, count_m=translit_row)
    nc.cleanup()
    nc.write_counts()

transliterated = []

# Kazakhstan
kz = 'KZ'
def kz_translit(s):
    cat = script_cat(s[0])
    if cat == 'Latin':
        return s
    elif cat == 'Cyrillic':
        return qazaq_translit(s)
    else:
        return ''
transliterate_country(kz, kz_translit)
transliterated.append(kz)
