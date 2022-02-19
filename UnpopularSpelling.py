import numpy as np
import csv
import json
import jellyfish


metaphone_map = {}
soundex_map = {}
nysiis_map = {}
mrc_map = {}

with open("baby-names.csv", newline='') as csvfile:
    namereader = csv.reader(csvfile, delimiter=',', quotechar='"')

    i = 0
    for row in namereader:
        # "year","name","percent","sex"
        year = row[0]
        gender = row[3]
        if year != '2008' or gender != 'girl':
            continue

        i += 1
        name = row[1]
        percent = row[2]
        entry = (name, percent)

        m = jellyfish.metaphone(name)
        if m in metaphone_map:
            metaphone_map[m].append(entry)
        else:
            metaphone_map[m] = [entry]

        s = jellyfish.soundex(name)
        if s in soundex_map:
            soundex_map[s].append(entry)
        else:
            soundex_map[s] = [entry]

        n = jellyfish.nysiis(name)
        if n in nysiis_map:
            nysiis_map[n].append(entry)
        else:
            nysiis_map[n] = [entry]

        mrc = jellyfish.match_rating_codex(name)
        if mrc in mrc_map:
            mrc_map[mrc].append(entry)
        else:
            mrc_map[mrc] = [entry]

    print(i)


metaphone_pop = {tuples[0][0]: [t[0] for t in tuples] for k, tuples in metaphone_map.items()}
soundex_pop = {tuples[0][0]: [t[0] for t in tuples] for k, tuples in soundex_map.items()}
nysiis_pop = {tuples[0][0]: [t[0] for t in tuples] for k, tuples in nysiis_map.items()}
# MRC performs poorly, as it's intended for a different task.
mrc_pop = {tuples[0][0]: [t[0] for t in tuples] for k, tuples in mrc_map.items()}


print(json.dumps(soundex_pop, indent=4))

print(len(metaphone_pop))
print(len(soundex_pop))
print(len(nysiis_pop))
print(len(mrc_pop))
