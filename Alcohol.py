from lxml import etree
import requests
import csv


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


def add_country_by_name(row):
    if row[0] == 'ЭК' or row[3] not in alcohol_indexes:
        return
    if row[3] == '2203':
        if row[2] in beer:
            beer[row[2]] += float(row[7])
        elif float(row[6]) != 0.0:
            beer.update({row[2]: float(row[7])})
            return
    elif row[3] == '2204':
        if row[2] in wine:
            wine[row[2]] += float(row[7])
        elif float(row[6]) != 0.0:
            wine.update({row[2]: float(row[7])})
            return
    elif row[3] == '2205':
        if row[2] in vermut:
            vermut[row[2]] += float(row[7])
        elif float(row[6]) != 0.0:
            vermut.update({row[2]: float(row[7])})
            return
    elif row[3] == '2206':
        if row[2] in sider:
            sider[row[2]] += float(row[7])
        elif float(row[6]) != 0.0:
            sider.update({row[2]: float(row[7])})
            return
    elif row[3] == '2207':
        if row[2] in alcohol:
            alcohol[row[2]] += float(row[7])
        elif float(row[6]) != 0.0:
            alcohol.update({row[2]: float(row[7])})
            return
    else:
        if row[2] in alcohol_drinks:
            alcohol_drinks[row[2]] += float(row[7])
        elif float(row[6]) != 0.0:
            alcohol_drinks.update({row[2]: float(row[7])})
            return


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

# https://docs.python.org/2.4/lib/standard-encodings.html

countries = {}
countries_2013 = {}
countries_2014 = {}
countries_2015 = {}
countries_2016 = {}

beer = {}
wine = {}
vermut = {}
sider = {}
alcohol = {}
alcohol_drinks = {}

with open('TCBT.csv', 'r', encoding='cp866') as file:
    reader = csv.reader(file)
    for row in reader:
        if row[0].startswith('NAPR') or row[2] == 'NNN':
            continue
        add_country(row)
        add_country_by_year(row)
        add_country_by_name(row)


def int_countries(countr):
    for key in countr:
        if int(countr[key]) > 100:
            countr[key] = int(countr[key])
    return


int_countries(countries)
int_countries(countries_2013)
int_countries(countries_2014)
int_countries(countries_2015)
int_countries(countries_2016)
int_countries(beer)
int_countries(wine)
int_countries(vermut)
int_countries(sider)
int_countries(alcohol)
int_countries(alcohol_drinks)

# print(countries)
# print(countries_2013)
# print(countries_2014)
# print(countries_2015)
# print()
# print(wine)
# print(countries_2016)
# print(beer)
# print(vermut)
# print(sider)
# print(alcohol_drinks)
# print(alcohol)

countries_by_codes = {}
url = 'https://www.artlebedev.ru/country-list/xml/'
r = requests.get(url)
text = r.text
text = text.replace('&#160;', ' ')
with open('ctr.xml', 'w', encoding='utf=8') as file:
    file.write(text)

doc = etree.parse('ctr.xml')
root = doc.getroot()
for node in root.iter():
    if node.text == 'Alpha2' or node.text == 'На английском':
        continue
    if node.tag == 'english':
        name = node.text.replace(u'\xa0', ' ')
    if node.tag == 'alpha2':
        nm = node.text.replace(u'\xa0', ' ')
        countries_by_codes.update({nm: name})

# # print(countries_by_codes)
countries_pop = []
for key in countries_by_codes:
    if key not in countries:
        countries_pop.append(key)
# print(countries_pop)
for key in countries_pop:
    countries_by_codes.pop(key)
# print(len(countries_by_codes))
