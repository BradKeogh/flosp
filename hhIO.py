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

hh = hosp('hh')

hh_cols = {
'PSEUDONYMISED_PATIENT_ID':'dept_patid',
'PSEUDONYMISED_PATIENT_ID':'hosp_patid',
'AGE_AT_ARRIVAL':'age',
'GENDER_NATIONAL_DESCRIPTION':'gender',
'SITE':'site',
'ARRIVAL_DTTM':'arrival_date',
'ARRIVAL_DTTM':'arrival_time',
'ARRIVAL_MODE_NATIONAL_CODE':'arrival_mode',
'INITIAL_ASSESSMENT_DTTM':'first_triage_time',
'SEEN_FOR_TREATMENT_DTTM':'first_dr_time',
'SPECIALTY_REQUEST_TIME':'first_adm_request_time',
'SPECIALTY_REFERRED_TO_CODE':'adm_referral_loc',
'ADMISSION_FLAG':'departure_method',
'ATTENDANCE_CONCLUSION_DTTM':'leaving_time',
'STREAM_LOCAL_CODE':'stream'
}

### import data
hh.ioED.load_hosp_csv('./../../3_Data/HH_ED_Flow_Study.csv',hh_cols)



hh.ioED.checks()

#
#
#
# ### apply manual edits - and replace _dataRAW in pmED
df_temp = hh.ioED.get_EDraw() #get df out of pmED
# # filter out only admissions to QA
# df_temp = df_temp[df_temp.site == 'Queen Alexandra Hospital ED']
# df_temp.reset_index(inplace=True, drop=True)
#df_temp = df_temp[0:200] ###! delete this later on! made for quicker processing
# df_temp = create_datetime_col(df_temp) #### create datetime columns foe leaving and entering dept from arrival day and time
# #### crete_datetime_col warnings leaves pink errors. should tidy at some point.
df_temp['arrival_datetime'] = df_temp.arrival_time.apply(lambda x : pd.to_datetime(x)) #convert to datetime and create arrival datetime col

df_temp['leaving_datetime'] =df_temp.arrival_time.apply(lambda x : pd.to_datetime(x))

df_temp['adm_flag'] = df_temp['departure_method'] #' this takes HHFT breach flag column directly'






hh.ioED.replace_EDraw(df_temp)   # replace df to pmED
#

hh.ioED.checks() # check size has reduced from 233,000
#
# # temp workaround for quick working on datetime cols:
hh.ioED.create_auto_columns()

hh.ioED.create_aggregates()

hh.ioED.saveRAWasCLEAN()
#
#
#
# #### create admission flag
# df_temp = pmth.ioED.get_EDraw() #get df out of pmED
# df_temp['adm_flag'] = 0
# df_temp.loc[df_temp.departure_method == 'Admitted to QAH','adm_flag'] = 1
# print ('no. of admissions in dataset: ', df_temp.adm_flag.sum())
#
# pmth.ioED.replace_EDraw(df_temp) # replace df to pmED
#
# pmth.ioED.checks()
#
# pmth.ioED.get_EDraw().head(2)
#
# #### calculate total patinet time for each day - in transformation function?
#
# pmth.ioED.create_aggregates()
#
# #### print
# pmth.ioED.saveRAWasRAW()
#
# pmth.ioED.saveRAWasCLEAN()
#
#
#
# #pmED.loadCLEAN()
# #pmED.saveCLEAN()
#
# print('\n Script success.')
# # Fix list
# # issue with reimporting - functions do not re-import after changes
# # importlib.reload() should do it but need to automate?



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
