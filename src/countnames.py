import csv
from collections import Counter
from namecounter import NameCounter
import io
from pathlib import Path
from tqdm import tqdm


def CountNameDataset():
    count_f = lambda t: (t[0],1) if (t[2] == 'F') else ('', 0)
    count_m = lambda t: (t[0],1) if (t[2] == 'M') else ('', 0)
    count_l = lambda t: (t[1],1)
    count_u = lambda t: (t[0],1) if (t[2] != 'F' and t[2] != 'M') else ('', 0)

    p = Path('data/name-dataset')
    for q in tqdm(sorted(p.glob('*.csv'))):
        country = str(q).split('.')[-2].split('\\')[-1]
        print(country)
        nc = NameCounter(country)

        # Get our counts.
        with q.open(newline='', encoding='utf8') as f:
            nc.count_csv(f, count_f, count_m, count_l, count_u)
        nc.cleanup()
        nc.distribute_unknown()
        nc.write_counts()

def CountChineseNames():
    cn_nc = NameCounter('CN')

    with io.open('data/chinese-names/familyname.csv', 'r', newline='', encoding='utf8') as f:
        cn_nc.count_csv(f, count_l=lambda t: (t[0], t[4]), skipfirst=True)
    with io.open('data/chinese-names/top1000name.prov.csv', 'r', newline='', encoding='utf8') as f:
        cn_nc.count_csv(f, count_f=lambda t:(t[0],t[2]), count_m=lambda t:(t[0],t[1]), skipfirst=True)

    cn_nc.cleanup()
    cn_nc.distribute_unknown()
    cn_nc.write_counts()

if __name__ == "__main__":
    CountNameDataset()
    CountChineseNames()
