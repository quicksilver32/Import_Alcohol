import pandas as pd
import numpy as np
from Alcohol import *
import matplotlib.pyplot as plt

d = {'Country name':pd.Series(countries_by_codes), 2013: pd.Series(countries_2013), 2014: pd.Series(countries_2014),
     2015: pd.Series(countries_2016), 2016: pd.Series(countries_2016),
     'All years': pd.Series(countries)}
pd_alcohol = pd.DataFrame(d)
pd_alcohol.index.name = 'Country code'
pd_alcohol = pd_alcohol.replace(np.nan, 0)
# print(pd_alcohol)
print(pd_alcohol)
pd_alcohol.to_csv('pd_alc.csv')
