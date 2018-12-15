import pandas as pd
import numpy as np
from Alcohol import *
import matplotlib.pyplot as plt

pd.options.display.max_rows = 105

d = {'Country name': pd.Series(countries_by_codes), 2013: pd.Series(countries_2013), 2014: pd.Series(countries_2014),
     2015: pd.Series(countries_2015), 2016: pd.Series(countries_2016),
     'All years': pd.Series(countries)}
pd_alcohol = pd.DataFrame(d)
pd_alcohol.index.name = 'Country code'
pd_alcohol = pd_alcohol.replace(np.nan, 0)

d = {'Country name': pd.Series(countries_by_codes), 'Beer': pd.Series(beer), 'Wine': pd.Series(wine),
     'Vermut': pd.Series(vermut), 'Sider': pd.Series(sider), 'Alcohol': pd.Series(alcohol),
     'Alcohol drinks': pd.Series(alcohol_drinks)}
pd_drinks = pd.DataFrame(d)
pd_drinks.index.name = 'Country code'
pd_drinks = pd_drinks.replace(np.nan, 0)

print(pd_alcohol)
pd_alcohol.to_csv('pd_alc.csv')

print(pd_drinks)
pd_drinks.to_csv('pd_drinks.csv')
