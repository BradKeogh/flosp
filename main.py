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
pd.read_csv('./../../4_analysis/processed/pmthED.csv')



print('\n Script success.')
# Fix list
# issue with reimporting - functions do not re-import after changes
# importlib.reload() should do it but need to automate?



#ddqd
