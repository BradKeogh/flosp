import numpy as np
dataframes_list = ['_dataR_EDpat','_dataR_EDdaily','_dataR_EDweekly','_dataR_EDmonthly']

dataRAW_expected_dtypes = {
'dept_patid':np.object,
'hosp_patid':np.float,
'age':np.int,
'gender':np.object,
'site':np.object,
'arrival_date':np.object,
'arrival_time':np.object,
'arrival_mode':np.object,
'first_triage_time':np.object,
'first_dr_time':np.object,
'first_adm_request_time':np.object,
'adm_referral_loc':np.object,
'departure_method':np.object,
'leaving_time':np.object,
'departure_method':np.object,
'arrival_datetime':np.dtype('datetime64[ns]'),
'leaving_datetime':np.dtype('datetime64[ns]'),
'waiting_time':np.float,
'breach_flag':np.int,
'arr_hour':np.object,
'arr_dayofweek':np.object,
'arr_month':np.object,
'leaving_hour':np.object,
'leaving_dayofweek':np.object,
'leaving_month':np.object,
'adm_flag':np.int
}
