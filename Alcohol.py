import csv
import requests
from lxml import html

alcohol_names = []
with open('ALCOHOL_NAMES.txt', 'r', encoding='utf-8') as file:
    for row in file:
        alcohol_names = row.split(',')

# print(alcohol_names)

alcohol_indexes = []
with open('tnved.csv', 'r', encoding='utf-8') as file:
    reader = csv.reader(file)
    for row in reader:
        for i in range(len(alcohol_names)):
            if alcohol_names[i] in row[1]:
                alcohol_indexes.append(row[0])
                break

for i in range(len(alcohol_indexes)):
    alcohol_indexes[i] = alcohol_indexes[i][:4]

alcohol_indexes = set(alcohol_indexes)


# print(alcohol_indexes)


def add_country(row):
    if row[0] == 'ЭК' or row[3] not in alcohol_indexes:
        return
    if row[2] in countries:
        countries[row[2]] += float(row[7])
    elif float(row[6]) != 0.0:
        countries.update({row[2]: float(row[7])})
        return

def add_country_by_year(row):
    if row[0] == 'ЭК' or row[3] not in alcohol_indexes:
        return
    if row[1] == '2013':
        if row[2] in countries_2013:
            countries_2013[row[2]] += float(row[7])
        elif float(row[6]) != 0.0:
            countries_2013.update({row[2]: float(row[7])})
            return
    elif row[1] == '2014':
        if row[2] in countries_2014:
            countries_2014[row[2]] += float(row[7])
        elif float(row[6]) != 0.0:
            countries_2014.update({row[2]: float(row[7])})
            return
    elif row[1] == '2015':
        if row[2] in countries_2015:
            countries_2015[row[2]] += float(row[7])
        elif float(row[6]) != 0.0:
            countries_2015.update({row[2]: float(row[7])})
            return
    elif row[1] == '2016':
        if row[2] in countries_2016:
            countries_2016[row[2]] += float(row[7])
        elif float(row[6]) != 0.0:
            countries_2016.update({row[2]: float(row[7])})
            return


# https://docs.python.org/2.4/lib/standard-encodings.html

countries = {}
countries_2013 = {}
countries_2014 = {}
countries_2015 = {}
countries_2016 = {}

with open('TCBT.csv', 'r', encoding='cp866') as file:
    reader = csv.reader(file)
    for row in reader:
        if row[0].startswith('NAPR'):
            continue
        add_country(row)
        add_country_by_year(row)


def int_countries(countr):
    for key in countr:
        if int(countr[key]) != 0:
            countr[key] = int(countr[key])
    return


int_countries(countries)
int_countries(countries_2013)
int_countries(countries_2014)
int_countries(countries_2015)
int_countries(countries_2016)








print(countries)
# print(countries_2013)
# print(countries_2014)
# print(countries_2015)
# print(countries_2016)
# print()



countries_by_codes = {}

url = 'https://www.artlebedev.ru/country-list/tab/'
r = requests.get(url)
with open('countries.csv', 'w', encoding='utf-8') as file:
    file = file.write(r.text)

with open('countries.csv', 'r', encoding='utf-8') as file:
    reader = csv.reader(file)
    for row in reader:
        if row[0].startswith('name'):
            continue
        code = row[0].split('\t')
        try:
            countries_by_codes.update({code[3]: code[2]})
        except:
            continue
# print(countries_by_codes)
countries_pop = []
for key in countries_by_codes:
    if key not in countries:
        countries_pop.append(key)
# print(countries_pop)
for key in countries_pop:
    countries_by_codes.pop(key)
# print(countries_by_codes)
# print(countries_by_codes)
