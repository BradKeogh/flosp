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

# local import
from hospital import *

pmth = hosp('pmth')

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
pmth.ioED.load_hosp_csv('./../../3_Data/Patient Journey ED Data 22.01.2014 to 31.10.2015.csv',portsmouth_cols)



pmth.ioED.checks()




### apply manual edits - and replace _dataRAW in pmED
df_temp = pmth.ioED.get_EDraw() #get df out of pmED
# filter out only admissions to QA
df_temp = df_temp[df_temp.site == 'Queen Alexandra Hospital ED']
df_temp.reset_index(inplace=True, drop=True)
#df_temp = df_temp[0:100] ###! delete this later on! made for quicker processing
df_temp = create_datetime_col(df_temp) #### create datetime columns foe leaving and entering dept from arrival day and time
#### crete_datetime_col warnings leaves pink errors. should tidy at some point.

pmth.ioED.replace_EDraw(df_temp)   # replace df to pmED

pmth.ioED.checks() # check size has reduced from 233,000

# temp workaround for quick working on datetime cols:
pmth.ioED.create_auto_columns()



#### create admission flag
df_temp = pmth.ioED.get_EDraw() #get df out of pmED
df_temp['adm_flag'] = 0
df_temp.loc[df_temp.departure_method == 'Admitted to QAH','adm_flag'] = 1
print ('no. of admissions in dataset: ', df_temp.adm_flag.sum())

pmth.ioED.replace_EDraw(df_temp) # replace df to pmED

pmth.ioED.checks()

pmth.ioED.get_EDraw().head(2)

#### calculate total patinet time for each day - in transformation function?

pmth.ioED.create_aggregates()

#### print
pmth.ioED.saveRAWasRAW()

pmth.ioED.saveRAWasCLEAN()



#pmED.loadCLEAN()
#pmED.saveCLEAN()

print('\n Script success.')
# Fix list
# issue with reimporting - functions do not re-import after changes
# importlib.reload() should do it but need to automate?



#pmth.loadCLEAN()


#print(pmth._name)
#print(pmth._pathCLEAN)



###############################################################
#### IO uses
#pmth.EDio.loadRAW()
#pmth.EDio.create_datetime_columns()
#pmth.EDio.get_df() # for manual changes/checks (need a replace_df() method?)
#pmth.EDio.status() # gives update on what needs to be done (checks)
#pmth.EDio.saveCLEAN()

#### pmth
#pmth.loadCLEAN() # loads all clean pkls available and instantiates classes associated with each .e.g. pmth.ED.pat, pmth.ED.daily
#pmth.status() # gives update of which CLEAN files available

#### ED uses
#pmth.ED.pat.create_daily() # makes daily df & instantiates
#............create_weekly()

#pmth.ED.pat.plot_ts() # possibly higher functions somewhere upstream but edited to suit column names at pat level.

#pmth.ED.pat.get_df()








#
