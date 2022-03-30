import csv
from collections import Counter
import io
from math import ceil


class NameCounter(object):
    """docstring NameCounter."""

    def __init__(self, country):
        self.country = country
        self.f = Counter()
        self.m = Counter()
        self.l = Counter()
        self.u = Counter()

    def count_csv(
            self, file, skipfirst=False,
            count_f=lambda t:('',0), count_m=lambda t:('',0),
            count_l=lambda t:('',0), count_u=lambda t:('',0)):
        namereader = csv.reader(file, delimiter=',', quotechar='"')
        if skipfirst:
            namereader.__next__()
        for row in namereader:
            f_tup = count_f(row)
            m_tup = count_m(row)
            l_tup = count_l(row)
            u_tup = count_u(row)
            self.f[ f_tup[0] ] += int(f_tup[1])
            self.m[ m_tup[0] ] += int(m_tup[1])
            self.l[ l_tup[0] ] += int(l_tup[1])
            self.u[ u_tup[0] ] += int(u_tup[1])

    def distribute_unknown(self):
        for name, count in self.u.items():
            fcount = f_counts[name]
            mcount = m_counts[name]
            denominator = fcount + mcount
            if denominator > 0:
                self.f[name] += ceil(count * (fcount/(denominator)))
                self.m[name] += ceil(count * (mcount/(denominator)))

    def cleanup(self):
        del self.f['']
        del self.m['']
        del self.l['']
        del self.u['']
        self.f = +self.f
        self.m = +self.m
        self.l = +self.l
        self.u = +self.u

    def write_counts(self, par_dir='counts'):
        with io.open(par_dir+f'/{self.country}-F.csv', 'w', newline='', encoding='utf8') as file:
            writer = csv.writer(file)
            writer.writerow(('Total', self.f.total()))
            writer.writerows(list(self.f.most_common()))
        # Save male names.
        with io.open(par_dir+f'/{self.country}-M.csv', 'w', newline='', encoding='utf8') as file:
            writer = csv.writer(file)
            writer.writerow(('Total', self.m.total()))
            writer.writerows(list(self.m.most_common()))
        #Save last names.
        with io.open(par_dir+f'/{self.country}-L.csv', 'w', newline='', encoding='utf8') as file:
            writer = csv.writer(file)
            writer.writerow(('Total', self.l.total()))
            writer.writerows(list(self.l.most_common()))
