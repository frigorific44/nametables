import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import csv
from math import ceil
import json

def huntingtonHill(arr, n):
    portions = np.full((arr.size,), 1)
    while np.sum(portions) < n:
        rank = arr / np.sqrt(portions*(portions + 1))
        portions[np.argmax(rank)] += 1
    return portions

def jefferson(arr, n):
    portions = np.full((arr.size,), 1)
    quot = arr / 2
    while np.sum(portions) < n:
        next = np.argmax(quot)
        portions[next] += 1
        quot[next] = arr[next] / (quot[next] + 1)
    return portions

def webster(arr, n):
    portions = np.full((arr.size,), 1)
    quot = arr / 2
    while np.sum(portions) < n:
        next = np.argmax(quot)
        portions[next] += 1
        quot[next] = arr[next] / ((2 * quot[next]) + 1)
    return portions

def hamilton(arr, n):
    portions = np.full((arr.size,), 1)
    leftover = n - np.sum(portions)
    quota = (arr * leftover)
    for i in range(leftover):
        next = np.argmax(quota)
        portions[next] += 1
        quota[next] = 0

apportionmentMethods = {
    'hamilton': hamilton,
    'huntington-hill': huntingtonHill,
    'jefferson': jefferson,
    'webster': webster
}

with open("baby-names.csv", newline='') as csvfile:
    year = '2008'
    gender = 'girl'
    methodName = 'huntington-hill'

    namereader = csv.reader(csvfile, delimiter=',', quotechar='"')
    percents = []
    i = 0;
    for row in namereader:
        if row[0] == year and row[3] == gender:
            percents.append(row[2])
    print(len(percents))
    arr = np.array(percents)
    arr = arr.astype(float)
    # Normalize the percentages.
    arr = arr / (np.sum(arr))
    arr_std = []
    arr_mean = []

    min_n = len(arr)
    max_n = ceil(1 / arr[-1])

    method = apportionmentMethods[methodName]
    for i in range(min_n, max_n):
        result = method(arr, i)
        big = arr * i

        relative_diff = np.absolute(result - big) / result
        arr_mean.append(np.mean(relative_diff))
        arr_std.append(np.std(relative_diff))

    xaxis = [*range(min_n, max_n)]
    with open(f"{year}-{gender}-{methodName}.json", 'w') as f:
        json.dump([arr_mean, arr_std, xaxis], f, separators=(',', ':'))

    # fig, ax = plt.subplots()
    # xaxis = [*range(min_n, max_n)]
    # ax.plot(xaxis, arr_mean, label="mean")
    # ax.plot(xaxis, arr_std, label="std")
    # ax.legend()
    # ax.set_title("Jefferson Method")
    # plt.show()
