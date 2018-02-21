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


from EDdata import EDdata

pmED = EDdata('pmth')

pmED.status()

pmED._name

portsmouth_cols = {
'pas_id':'dept_patid',
'nhs_number':'hosp_patid',
'age':'age',
'gender':'gender',
'department':'site',
'date_of_attendance':'arrival_date',
'time_of_attendance':'arrival_time',
'mode_of_arrival':'arrival_mode',
'triage_time':'first_triage_time',
'dr1_seen':'first_dr_time',
'referred_to__first_referral':'first_adm_request_time',
'referred_to_at_point_of_discharge':'adm_referral_loc',
'departure_method':'departure_method',
'left_dept_time':'leaving_time',
'departure_method':'departure_method'
}

### import data
pmED.loadRAW('./../../3_Data/Patient Journey ED Data 22.01.2014 to 31.10.2015.csv',portsmouth_cols)

pmED.status()

pmED._name

### apply manual edits - and replace _dataRAW in pmED
df_temp = pmED._dataRAW #get df out of pmED
# filter out only admissions to QA
df_temp = df_temp[df_temp.site == 'Queen Alexandra Hospital ED']
df_temp.reset_index(inplace=True, drop=True)
#df_temp = df_temp[0:100] ### delete this later on! made for quicker processing
pmED._dataRAW  = df_temp # replace df to pmED

pmED._dataRAW.shape # check size has reduced from 233,000

#### create datetime columns foe leaving and entering dept from arrival day and time
pmED.create_datetime_columns() #temp!


# temp workaround for quick working on datetime cols:
pmED.create_auto_columns()

#### create admission flag
df_temp = pmED._dataRAW #get df out of pmED
df_temp['adm_flag'] = 0
df_temp.loc[df_temp.departure_method == 'Admitted to QAH','adm_flag'] = 1
print ('no. of admissions in dataset: ', df_temp.adm_flag.sum())
pmED._dataRAW  = df_temp # replace df to pmED
pmED._dataRAW.head(2)

#### calculate total patinet time for each day - in transformation function?

#### print
pmED.saveRAW()





pmED.loadCLEAN()
#pmED.saveCLEAN()

print('\n Script success.')
# Fix list
# issue with reimporting - functions do not re-import after changes
# importlib.reload() should do it but need to automate?
