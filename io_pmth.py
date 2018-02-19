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


# import raw data
rawED = EDimport('./../../3_Data/Patient Journey ED Data 22.01.2014 to 31.10.2015.csv')
#### possible additional cols in pmth ED dataset
#presenting_complaint
#reason_for_attendance
#diagnosis__primary
# roles_of_discharging_user

#### filter out only admissions to
rawED = rawED[rawED.site == 'Queen Alexandra Hospital ED']
rawED.reset_index(inplace=True)

#### create datetime columns foe leaving and entering dept
rawED = create_datetime_col(rawED)

#### create waitingtime column
rawED = make_waitingtime_column(rawED)

#### create breach flags
rawED['breach'] = (rawED['waiting_time'] > 4*60).astype(int)

#### create: day of week, time of day, month of year columns
rawED = make_callender_columns(rawED,'arrival_datetime','arr')
rawED = make_callender_columns(rawED,'leaving_datetime','leaving')

#### create admission flag
rawED['adm_flag'] = 0
rawED.loc[rawED.departure_method == 'Admitted to QAH','adm_flag'] = 1
print ('no. of admissions in dataset: ', rawED.adm_flag.sum())

#### calculate minutes in ED for each attendance


#### calculate total patinet time for each day - in transformation function?

#### print
print('-'*40)
print('Saving rawED df to csv.')
rawED.to_csv('../../3_Data/processed/pmthED.csv',index=False)

print('\n Script success.')
# Fix list
# issue with reimporting - functions do not re-import after changes
# importlib.reload() should do it but need to automate?



#
