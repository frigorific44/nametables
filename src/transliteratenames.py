from namecounter import NameCounter
import io
import qazaq_transliterator
from population import unicodedata2


def transliterate_country(country, translit):
    translit_row = lambda t:(translit(t[0]), t[1])
    nc = NameCounter(country)
    with io.open(f'counts/{country}-F.csv', 'r', newline='', encoding='utf8') as f:
        nc.count_csv(f, skipfirst=True, count_f=translit_row)
    with io.open(f'counts/{country}-L.csv', 'r', newline='', encoding='utf8') as f:
        nc.count_csv(f, skipfirst=True, count_l=translit_row)
    with io.open(f'counts/{country}-M.csv', 'r', newline='', encoding='utf8') as f:
        nc.count_csv(f, skipfirst=True, count_m=translit_row)
    nc.cleanup()
    nc.write_counts()

transliterated = []

# Kazakhstan
kz = 'KZ'
def kz_translit(s):
    script = unicodedata2.string_script(s)
    if script == 'Latin':
        return s
    elif script == 'Cyrillic':
        return qazaq_transliterator.translit(s)
    else:
        return ''
        

if __name__ == "__main__":
    transliterate_country(kz, kz_translit)
    transliterated.append(kz)
