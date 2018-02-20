# Script to call other scripts whilst dev

# Magic needed for reloading in changes to imports automatically
# after changing .py files
from IPython import get_ipython
ipython = get_ipython()
ipython.magic("load_ext autoreload") # %load_ext autoreload
ipython.magic("autoreload 2") # %autoreload 2

#import dep
import numpy as np
import pandas as pd

#import hospital-flow scripts here
from Fcleaning import *
from Ftest import *
from Ftransform import *
from Fplot import *
from Fio import *


# import ED data
cleanED = pd.read_csv('./../../3_Data/processed/pmthED.csv')

cleanED.columns




import matplotlib.pyplot as plt
fig = plt.figure(figsize=(12,4))
ax1 = fig.add_subplot(121)
df[['ed_arrivals','arr_month']].boxplot(by='month',ax=ax1)
ax2 = fig.add_subplot(122)
df[['ed_arrivals','arr_dayofweek']].boxplot(by='dayofweek',ax=ax2);


print('\n Script success.')
