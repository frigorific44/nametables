import csv
import io
import json
import pycountry
# This generates the JSON of country populations from the population csv sourced
# at github.com/datasets/population.


population = {}
data_year = {}

with io.open('population.csv', 'r', newline='', encoding='utf8') as f:
    reader = csv.reader(f, delimiter=',', quotechar='"')
    next(reader)
    for row in reader:
        name = row[0]
        alpha3 = row[1]
        year = int(row[2])
        value = int(row[3])

        country = pycountry.countries.get(alpha_3=alpha3)
        if country == None:
            continue
        alpha2 = country.alpha_2

        if alpha2 in population:
            if year > data_year[alpha2]:
                population[alpha2] = value
                data_year[alpha2] = year
        else:
            population[alpha2] = value
            data_year[alpha2] = year

with io.open('population.json', 'w', newline='', encoding='utf8') as f:
    json.dump(population, f, indent=4)
