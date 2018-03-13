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
'ARRIVAL_DTTM':'arrive_datetime',
'ARRIVAL_MODE_NATIONAL_CODE':'arrive_mode',
'INITIAL_ASSESSMENT_DTTM':'first_triage_datetime',
'SEEN_FOR_TREATMENT_DTTM':'first_dr_datetime',
'SPECIALTY_REQUEST_TIME':'first_adm_request_time',
'SPECIALTY_REFERRED_TO_CODE':'adm_referral_loc',
'ADMISSION_FLAG':'adm_flag',
'ATTENDANCE_CONCLUSION_DTTM':'depart_datetime',
'STREAM_LOCAL_CODE':'stream'
}

### import data
hh.ioED.load_hosp_csv('./../../3_Data/HH_ED_Flow_Study.csv',hh_cols)



hh.ioED.checks()

####! cut down sample size for testing
# df = hh.ioED.get_EDraw()
# df = df[0:500]
# hh.ioED.replace_EDraw(df)

#### problem with datetime conversion means need to specifiy dt_format of strings. Some datetimes are also not in this format - so need to tidy these. e.g. one has seconds included (but seems erroneus anyway Y1899)

df = hh.ioED.get_EDraw()
df.loc[df.first_triage_datetime == '1899-12-30 00:00:00.000000', 'first_triage_datetime'] = np.nan
hh.ioED.replace_EDraw(df)

hh.ioED.convert_cols_datetime(dt_format="%d/%m/%Y %H:%M")

hh.ioED.checks()

hh.ioED.create_auto_columns()

hh.ioED.checks() # check size has reduced from 233,000

hh.ioED.saveRAWasCLEAN()

# hh.ioED.create_aggregates()
#

#
# #
# #
# # #### create admission flag
# # df_temp = pmth.ioED.get_EDraw() #get df out of pmED
# # df_temp['adm_flag'] = 0
# # df_temp.loc[df_temp.departure_method == 'Admitted to QAH','adm_flag'] = 1
# # print ('no. of admissions in dataset: ', df_temp.adm_flag.sum())
# #
# # pmth.ioED.replace_EDraw(df_temp) # replace df to pmED
# #
# # pmth.ioED.checks()
# #
# # pmth.ioED.get_EDraw().head(2)
# #
# # #### calculate total patinet time for each day - in transformation function?
# #
# # pmth.ioED.create_aggregates()
# #
# # #### print
# # pmth.ioED.saveRAWasRAW()
# #
# # pmth.ioED.saveRAWasCLEAN()
# #
# #
# #
# # #pmED.loadCLEAN()
# # #pmED.saveCLEAN()
# #
# # print('\n Script success.')
# # # Fix list
# # # issue with reimporting - functions do not re-import after changes
# # # importlib.reload() should do it but need to automate?
#
#
#
# #pmth.loadCLEAN()
#
#
# #print(pmth._name)
# #print(pmth._pathCLEAN)
#
#
#
# ###############################################################
# #### IO uses
# #pmth.EDio.loadRAW()
# #pmth.EDio.create_datetime_columns()
# #pmth.EDio.get_df() # for manual changes/checks (need a replace_df() method?)
# #pmth.EDio.status() # gives update on what needs to be done (checks)
# #pmth.EDio.saveCLEAN()
#
# #### pmth
# #pmth.loadCLEAN() # loads all clean pkls available and instantiates classes associated with each .e.g. pmth.ED.pat, pmth.ED.daily
# #pmth.status() # gives update of which CLEAN files available
#
# #### ED uses
# #pmth.ED.pat.create_daily() # makes daily df & instantiates
# #............create_weekly()
#
# #pmth.ED.pat.plot_ts() # possibly higher functions somewhere upstream but edited to suit column names at pat level.
#
# #pmth.ED.pat.get_df()
#







#
