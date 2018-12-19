import pandas as pd
import numpy as np
from Alcohol import *
import matplotlib.pyplot as plt

date = ["2013", "2014", "2015", "2016", "All years"]
d = {'Country name': pd.Series(countries_by_codes),
     "2013": pd.Series(countries_2013),
     "2014": pd.Series(countries_2014),
     "2015": pd.Series(countries_2015),
     "2016": pd.Series(countries_2016),
     'All years': pd.Series(countries)}
pd_alcohol = pd.DataFrame(d)
pd_alcohol.index.name = 'Country code'
pd_alcohol = pd_alcohol.replace(np.nan, 0)
pd_alcohol.to_csv('DataFrames/Summary.csv')

drinks = ['Beer', 'Wine', 'Vermut', 'Sider', 'Alcohol', 'Alcohol drinks']
d1 = {'Country name': pd.Series(countries_by_codes), 'Sider': pd.Series(sider), 'Wine': pd.Series(wine),
      'Vermut': pd.Series(vermut), 'Beer': pd.Series(beer), 'Alcohol': pd.Series(alcohol),
      'Alcohol drinks': pd.Series(alcohol_drinks),
      'Summary': pd.Series(countries)}
pd_drinks = pd.DataFrame(d1)
pd_drinks.index.name = 'Country code'
pd_drinks = pd_drinks.replace(np.nan, 0)
pd_drinks.to_csv('DataFrames/Summary by drinks.csv')


def alc_each_year(year):  # Функция суммирует объемы поставок за каждый год
    yearsum = pd_alcohol[year].sum()
    return yearsum


all_imports = alc_each_year("All years")  # Общий бъем импорта за 2013-2016


def per_cent(df):  # Функция вычисляет долю импорта от всего импорта
    if "All years" in df.columns.values.tolist():
        imports = df["All years"]
        percent_list = np.array([float((i / all_imports) * 100) for i in imports])
        df["Percent"] = pd.Series(percent_list, index=df.index)
    else:
        drink = df.columns.values.tolist()[1]  # Вычисление доли импорта определенного напитка
        imports = df[drink]
        percent_list = np.array([float((i / fourth_graph["Volume"][drink]) * 100) for i in imports])
        df["Percent of " + drink] = pd.Series(percent_list, index=df.index)
    return df


pd_alcohol_wperc = per_cent(pd_alcohol)
pd_alcohol_wperc["Percent"] = pd_alcohol['Percent']
pd_alcohol_wperc['Percent'] = pd_alcohol_wperc['Percent'].apply(lambda x: round(x, 6))
# print(pd_alcohol_wperc)

pd_alcohol_wperc = per_cent(pd_alcohol).sort_values(by="Percent", ascending=False)  # Общий датафрейм с процентами

# Построение 1 графика: общие объемы поставок за каждый год

first_graph = pd.DataFrame({"Volume": np.array([alc_each_year(i) for i in date])}, index=date)  # Датафрейм объемов
# импорта по годам и долей поставок каждого года от общего импорта за 2013-2016

imports = first_graph["Volume"]  # Ищем объем всего импорта и процент каждого года от объема поставок за 4 года
percent_list = np.array([float((i / all_imports) * 100) for i in imports])  # Проценты
first_graph["Percent"] = pd.Series(percent_list, index=first_graph.index)

cmap = plt.get_cmap("Pastel2")  # Устанавливаем цветовую палитру
col = cmap.colors
colours = [i for i in col]

fig, ax1 = plt.subplots()
x1 = date[0:4]
y1 = first_graph["Percent"][0:4].tolist()
ax1.bar(x1, y1, color=colours[1])
ax1.spines['top'].set_visible(False)  # Делаем невидимыми контуры области графика
ax1.spines['right'].set_visible(False)
ax1.yaxis.set_major_formatter(plt.FuncFormatter('{:.0f}%'.format))
ax1.spines['left'].set_visible(False)
plt.tick_params(axis='both', which='both', bottom=False, top=False,
                labelbottom=True, left=False, right=False, labelleft=True)
plt.grid(True, 'major', 'y', ls='-', lw=.3, c='k', alpha=.4)
plt.title("Import per years for 2013-2016")
fig.savefig('Graphs/Import per years.png')
plt.show()

# Построение 2 графика: объёмы поставок за каждый год у стран-лидеров

second_graph = pd_alcohol.sort_values(by=["All years"], ascending=False).head(6)  # 6 крупнейших поставщиков
other_countries = pd_alcohol.sort_values(by=["All years"], ascending=False).iloc[6:, 0:]  # Остальные страны

other_countries_perc = other_countries["Percent"].sum()  # Процент импорта остальных стран
leaders = [i for i in second_graph["Country name"]]  # Список 6 лидеров по импорту


def perc_for_leaders(daft, country):  # Функция вычисляет долю импорта от всех поставок за определенный год
    imports = daft[country]
    percent_list = np.array([float((i / all_imports) * 100) for i in imports])
    return percent_list


sg1 = sg2 = sg3 = sg4 = sg5 = sg6 = None

for row in range(len(leaders)):  # Создаем датафреймы стран-лидеров с долей импорта за каждый год
    if row == 0:
        sg1 = pd.DataFrame({leaders[row]: np.array([second_graph[i][row] for i in date])}, index=date)
        sg1[leaders[row]] = pd.Series(perc_for_leaders(sg1, leaders[row]), index=date)
    elif row == 1:
        sg2 = pd.DataFrame({leaders[row]: np.array([second_graph[i][row] for i in date])}, index=date)
        sg2[leaders[row]] = pd.Series(perc_for_leaders(sg2, leaders[row]), index=date)
    elif row == 2:
        sg3 = pd.DataFrame({leaders[row]: np.array([second_graph[i][row] for i in date])}, index=date)
        sg3[leaders[row]] = pd.Series(perc_for_leaders(sg3, leaders[row]), index=date)
    elif row == 3:
        sg4 = pd.DataFrame({leaders[row]: np.array([second_graph[i][row] for i in date])}, index=date)
        sg4[leaders[row]] = pd.Series(perc_for_leaders(sg4, leaders[row]), index=date)
    elif row == 4:
        sg5 = pd.DataFrame({leaders[row]: np.array([second_graph[i][row] for i in date])}, index=date)
        sg5[leaders[row]] = pd.Series(perc_for_leaders(sg5, leaders[row]), index=date)
    elif row == 5:
        sg6 = pd.DataFrame({leaders[row]: np.array([second_graph[i][row] for i in date])}, index=date)
        sg6[leaders[row]] = pd.Series(perc_for_leaders(sg6, leaders[row]), index=date)

second_graph1 = pd.merge(sg1, sg2, left_index=True, right_index=True)  # Объединяем в 1 датафрейм
second_graph11 = pd.merge(second_graph1, sg3, left_index=True, right_index=True)
second_graph12 = pd.merge(second_graph11, sg4, left_index=True, right_index=True)
second_graph13 = pd.merge(second_graph12, sg5, left_index=True, right_index=True)
second_graph2 = pd.merge(second_graph13, sg6, left_index=True, right_index=True)

# print(second_graph2)

cmap1 = plt.get_cmap("Set3")  # Устанавливаем цветовую палитру
coll = cmap1.colors
colours1 = [i for i in coll]

ctr = second_graph2.columns.values.tolist()
fig, ax2 = plt.subplots()
clr = [colours1[0], colours1[2], colours1[3], colours1[4], colours1[5], colours1[7]]
x2 = date[0:4]
for i in range(len(ctr)):
    y2 = second_graph2[ctr[i]].values.tolist()[0:4]
    ax2.plot(x2, y2, lw=2.5, color=clr[i])
ax2.spines['top'].set_visible(False)
ax2.spines['bottom'].set_visible(False)
ax2.spines['right'].set_visible(False)
ax2.spines['left'].set_visible(False)
ax2.set_ylim(0, 10)
ax2.set_xlim("2013", "2016")
ax2.legend(leaders, frameon=False)
plt.grid(True, 'major', 'y', ls='--', lw=.3, c='k', alpha=.4)
ax2.get_xaxis().tick_bottom()
ax2.get_yaxis().tick_left()
ax2.yaxis.set_major_formatter(plt.FuncFormatter('{:.0f}%'.format))
plt.tick_params(axis='both', which='both', bottom=False, top=False,
                labelbottom=True, left=False, right=False, labelleft=True)
plt.title("Leaders' dynamics of imports for 2013-2016")
fig.savefig("Graphs/Leaders summary.png")
plt.show()

# Построение 3 графика: доли импорта стран-лидеров и других стран за 2013-2016

perc_all_years = second_graph2.loc["All years"]
perc_all_years["Other countries"] = other_countries_perc  # Серия с процентами импорта за 2013-2016

labels = "Ukraine", "Spain", "Italy", "France", "Germany", "Belarus", "Other countries"
fig3, ax3 = plt.subplots(1, 1)
patches3, texts3, autotexts3 = ax3.pie(perc_all_years.tolist(), labels=labels, autopct='%1.1f%%',
                                       wedgeprops=dict(width=1, edgecolor='w'),
                                       shadow=False, explode=(0.03, 0, 0, 0, 0, 0, 0), pctdistance=0.76,
                                       colors=colours)
plt.setp(autotexts3, size=8.9)
plt.title("Leaders' percents of import for 2013-2016")
fig3.savefig("Graphs/Leaders percentage.png")
plt.show()

# Построение 4 графика: объёмы и доли импорта отдельных видов алкоголя за 2013-2016

fourth_graph = pd.DataFrame({"Volume": np.array([pd_drinks[i].sum() for i in drinks])}, index=drinks)
imports1 = fourth_graph["Volume"]  # Ищем объем всего импорта и процент каждого года от объема поставок за 4 года
percent_list1 = np.array([float((i / all_imports) * 100) for i in imports1])  # Проценты
fourth_graph["Percent"] = pd.Series(percent_list1, index=fourth_graph.index)  # Добавляем в датафрейм столбец с %

fig, ax4 = plt.subplots()
x = drinks
y = fourth_graph["Percent"].tolist()
ax4.bar(x, y, color=colours)
xax = ax4.xaxis
plt.grid(True, 'major', 'y', ls='--', lw=.3, c='k', alpha=.4)
xlabels = xax.get_ticklabels()
for label in xlabels:
    label.set_rotation(20)
ax4.spines['top'].set_visible(False)  # Делаем невидимыми контуры области графика
ax4.spines['right'].set_visible(False)
ax4.yaxis.set_major_formatter(plt.FuncFormatter('{:.0f}%'.format))
ax4.spines['left'].set_visible(False)
plt.tick_params(axis='both', which='both', bottom=False, top=False,
                labelbottom=True, left=False, right=False, labelleft=True)
plt.grid(True, 'major', 'y', ls='-', lw=.3, c='k', alpha=.4)
plt.title("Drinks' percents of all import for 2013-2016")
fig.savefig("Graphs/Drinks percentage.png")
plt.show()

# Построение 5 графика: доля лидеров в импорте каждого вида плкоголя от общего объёма поставок

pd_drinks["Total percent"] = pd_alcohol_wperc["Percent"]
pd_drinks = pd_drinks.sort_values(by="Total percent", ascending=False)
wine_leaders = pd_drinks.sort_values(by="Wine", ascending=False).head(6)
wine_leaders.drop(['Beer', 'Vermut', 'Sider', 'Alcohol', 'Alcohol drinks'], inplace=True, axis=1)

beer_leaders = pd_drinks.sort_values(by="Beer", ascending=False).head(6)
beer_leaders.drop(['Wine', 'Vermut', 'Sider', 'Alcohol', 'Alcohol drinks'], inplace=True, axis=1)

sider_leaders = pd_drinks.sort_values(by="Sider", ascending=False).head(6)
sider_leaders.drop(['Wine', 'Beer', 'Vermut', 'Alcohol', 'Alcohol drinks'], inplace=True, axis=1)

vermut_leaders = pd_drinks.sort_values(by="Vermut", ascending=False).head(6)
vermut_leaders.drop(['Wine', 'Beer', 'Sider', 'Alcohol', 'Alcohol drinks'], inplace=True, axis=1)

alcohol_leaders = pd_drinks.sort_values(by="Alcohol", ascending=False).head(6)
alcohol_leaders.drop(['Wine', 'Beer', 'Vermut', 'Sider', 'Alcohol drinks'], inplace=True, axis=1)

alcoholdr_leaders = pd_drinks.sort_values(by="Alcohol drinks", ascending=False).head(6)
alcoholdr_leaders.drop(['Wine', 'Beer', 'Vermut', 'Sider', 'Alcohol'], inplace=True, axis=1)



per_cent(wine_leaders)  # Рассчет роцента импорта
per_cent(beer_leaders)
per_cent(sider_leaders)
per_cent(vermut_leaders)
per_cent(alcohol_leaders)
per_cent(alcoholdr_leaders)

labels_w = "Spain", "Italy", "Ukraine", "France", "South Africa", "Georgia", "Other Countries"
labels_b = "Ukraine", "Belarus", "Germany", "Czech Republic", "Belgium ", "United Kingdom", "Other Countries"
labels_s = "Lithuania", "Italy", "Belarus", "Bulgaria", "Other Countries"
labels_v = "Italy", "Bulgaria", "Germany", "Spain", "Other Countries"
labels_a = "Kazakhstan", "Belarus", "Spain", "Germany", "Switzerland", "Other Countries"
labels_ad = "United Kingdom", "Armenia", "France", "Ukraine", "Belarus", "Other Countries"


def pie_builder(df):
    drink = df.columns.values.tolist()[1]
    other_countries = 100 - df["Percent of " + drink].sum()
    xx = df["Percent of " + drink].values.tolist()
    xx = np.append(xx, other_countries)
    labels = ''
    if drink is "Wine":
        labels = labels_w
    elif drink is "Beer":
        labels = labels_b
    fig, ax5 = plt.subplots()
    patches5, texts5, autotexts5 = ax5.pie(xx, labels=labels, autopct='%1.1f%%',
                                           shadow=False, explode=(0.03, 0, 0, 0, 0, 0, 0),
                                           wedgeprops=dict(width=1, edgecolor='w'),
                                           startangle=90, colors=colours, pctdistance=0.76)
    ax5.set_title(drink)
    plt.setp(autotexts5, size=8.9)
    ax5.set(aspect="equal", title=drink + " import for 2013-2016")
    fig.savefig('Graphs/'+drink+" leaders.png")
    plt.show()


pie_builder(wine_leaders)
pie_builder(beer_leaders)

# График для спиртных напитков
alcdr_resh = alcoholdr_leaders.loc['GB':'BY', 'Percent of Alcohol drinks']
other_country = 100 - alcdr_resh.sum()
xx = alcdr_resh.values.tolist()
xx = np.append(xx, other_country)
fig, ax5 = plt.subplots()
patches5, texts5, autotexts5 = ax5.pie(xx, labels=labels_ad, autopct='%1.1f%%',
                                       shadow=False, explode=(0.03, 0, 0, 0, 0, 0),
                                       wedgeprops=dict(width=1, edgecolor='w'),
                                       colors=colours, pctdistance=0.76)
plt.setp(autotexts5, size=8.9)
ax5.set(aspect="equal", title="Alcohol drinks import for 2013-2016")
fig.savefig("Graphs/Alcohol drinks leaders.png")
plt.show()

# График для сидра
sider_resh = sider_leaders.loc['LT':'BG', 'Percent of Sider']
other_country1 = 100 - sider_resh.sum()
xx1 = sider_resh.values.tolist()
xx1 = np.append(xx1, other_country1)
fig6, ax6 = plt.subplots()
patches6, texts6, autotexts6 = ax6.pie(xx1, labels=labels_s, autopct='%1.1f%%',
                                       shadow=False, explode=(0.03, 0, 0, 0, 0),
                                       wedgeprops=dict(width=1, edgecolor='w'),
                                       colors=colours, pctdistance=0.76)
plt.setp(autotexts6, size=8.9)
ax6.set(aspect="equal", title='Sider import for 2013-2016')
fig6.savefig("Graphs/Sider leaders.png")
plt.show()

# График для вермута
vermut_resh = vermut_leaders.loc['IT':'ES', 'Percent of Vermut']
other_country2 = 100 - vermut_resh.sum()
xx1 = vermut_resh.values.tolist()
xx1 = np.append(xx1, other_country2)
fig7, ax7 = plt.subplots()
patches7, texts7, autotexts7 = ax7.pie(xx1, labels=labels_v, autopct='%1.1f%%',
                                       shadow=False, explode=(0.03, 0, 0, 0, 0),
                                       wedgeprops=dict(width=1, edgecolor='w'),
                                       colors=colours, pctdistance=0.76)
plt.setp(autotexts7, size=8.9)
ax7.set(aspect="equal", title='Vermut import for 2013-2016')
fig7.savefig("Graphs/Vermut leaders.png")
plt.show()

#  График для спирта
alcd_resh = alcohol_leaders.loc['KZ':'CH', 'Percent of Alcohol']
other_country = 100 - alcd_resh.sum()
xx = alcd_resh.values.tolist()
xx = np.append(xx, other_country)
fig8, ax8 = plt.subplots()
patches8, texts8, autotexts8 = ax8.pie(xx, labels=labels_a, autopct='%1.1f%%',
                                       shadow=False, explode=(0.03, 0, 0, 0, 0, 0),
                                       wedgeprops=dict(width=1, edgecolor='w'),
                                       colors=colours, pctdistance=0.76)
plt.setp(autotexts8, size=8.9)
ax8.set(aspect="equal", title="Alcohol import for 2013-2016")
fig8.savefig("Graphs/Alcohol leaders.png")
plt.show()

# Сводка датафреймов

pd_alcohol_wperc = pd_alcohol_wperc.to_string(formatters={'Percent': '{:.8f}%'.format})
print(pd_alcohol_wperc)  # Общий датафрейм по годам с процентами
print()

# for i in pd_drinks.columns.values:
#     if i != "Country name" and i != "Total percent":
#         pd_drinks[i] = pd_drinks[i].astype(np.int64)

pd_drinks = pd_drinks.to_string(formatters={'Total percent': '{:.8f}%'.format})
print(pd_drinks)  # По напиткам

first_graph["Percent"] = first_graph['Percent'].apply(lambda x: round(x, 2))
first_graph["Volume"] = first_graph['Volume'].astype(np.int64)
first_graph.to_csv('DataFrames/Import per years.csv')
first_graph = first_graph.to_string(formatters={'Percent': '{:.2f}%'.format})
print(first_graph)  # Объем импорта по годам и доля поставок каждого года от общего импорта за 2013-2016 (для 1 графика)
print()

second_graph["Percent"] = second_graph['Percent'].apply(lambda x: round(x, 2))
second_graph = second_graph.set_index("Country name")
second_graph.index.name = None
for i in date:
    second_graph[i] = second_graph[i].astype(np.int64)
second_graph.to_csv('DataFrames/Leaders summary.csv')
second_graph = second_graph.to_string(formatters={'Percent': '{:.2f}%'.format})
print(second_graph)  # 6 стран-лидеров по импорту, объём и % от общих поставок за 2013-2016
print()

second_graph2 = second_graph2.applymap(lambda x: round(x, 2))
second_graph2.to_csv('Leaders percentage.csv')
second_graph2 = second_graph2.applymap("{:.2f}%".format)
print(second_graph2)  # Доля импорта стран-лидеров по годам и общая(для 2 графика)
print()

fourth_graph["Percent"] = fourth_graph["Percent"].apply(lambda x: round(x, 3))
fourth_graph["Volume"] = fourth_graph['Volume'].astype(np.int64)
fourth_graph.to_csv('DataFrames/Drinks percentage.csv')
fourth_graph = fourth_graph.to_string(formatters={'Percent': '{:.3f}%'.format})
print(fourth_graph)  # Общий объём импорта по каждому виду алкоголя (для 4 графика)
print()

wine_leaders["Wine"] = wine_leaders["Wine"].astype(np.int64)
sider_leaders["Sider"] = sider_leaders["Sider"].astype(np.int64)
beer_leaders["Beer"] = beer_leaders["Beer"].astype(np.int64)
vermut_leaders["Vermut"] = vermut_leaders["Vermut"].astype(np.int64)
alcoholdr_leaders["Alcohol drinks"] = alcoholdr_leaders["Alcohol drinks"].astype(np.int64)
alcohol_leaders["Alcohol"] = alcohol_leaders["Alcohol"].astype(np.int64)
leaders_df = [wine_leaders, sider_leaders, beer_leaders, vermut_leaders, alcohol_leaders, alcoholdr_leaders]
for i in leaders_df:
    del i["Summary"]
    i["Total percent"] = i["Total percent"].apply(lambda x: round(x, 2))

wine_leaders.to_csv('DataFrames/Wine leaders.csv')
sider_leaders.to_csv('DataFrames/Sider leader.csv')
beer_leaders.to_csv('DataFrames/Beer leaders.csv')
vermut_leaders.to_csv('DataFrames/Vermut leaders.csv')
alcohol_leaders.to_csv('DataFrames/Alcohol leaders.csv')
alcoholdr_leaders.to_csv('DataFrames/Alcohol drinks leaders.csv')


def format_alc(df):
    drink = df.columns.values.tolist()[1]
    df = df.set_index("Country name")
    df.index.name = None
    df = df.to_string(formatters={'Percent of ' + drink: '{:.2f}%'.format,
                                  'Total percent': '{:.2f}%'.format})
    return df


for i in leaders_df:
    print(format_alc(i))
    print()
