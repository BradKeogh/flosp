#%% Change working directory from the workspace root to the ipynb file location. Turn this addition off with the DataScience.changeDirOnImportExport setting
import os
try:
	os.chdir(os.path.join(os.getcwd(), 'example'))
	print(os.getcwd())
except:
	pass
#%% [markdown]
# # Example workflow for using flosp to import and clean ED data
#%% [markdown]
# Get to directory above to import flosp

#%%
# get_ipython().run_line_magic('load_ext', 'autoreload')
# get_ipython().run_line_magic('autoreload', '2')


#%%
# get_ipython().run_line_magic('ls', '')


#%%
# get_ipython().run_line_magic('cd', '".\\..')


#%%
import flosp


#%%


#%% [markdown]
# ## initialise flosp
# 
# You must provide the path to the setup file, which you should edit to your project specifics.

#%%
from flosp import Interface


#%%
hosp = Interface(setup_file_path='./setup.py')


#%%
hosp = Interface(setup_file_path='./ff/setup.py')


#%%
from example.setup import HOSPITAL_NAME

#%% [markdown]
# setup_file_path = './setup.py'
#%% [markdown]
# from setup_file_path import HOSPITAL_NAME
#%% [markdown]
# ### Importing ED data
#%% [markdown]
# load raw data

#%%
hosp.load_dataED('./example/example_data_ED.csv') #,nrows=1500) # limit number of rows for quick runtime during dev

#%% [markdown]
# look at the dataframe at any stage of processing

#%%
hosp.extract_data('ED').head()

#%% [markdown]
# subsampling method - for quicker inital runtime during development of cleaning (some of the datetime conversions can take some time on larger data sets
#%% [markdown]
# ## Import IP data

#%%
hosp.load_dataIP('./example/example_data_IP.csv')


#%%
hosp.extract_data('IP').head()


#%%



#%%


#%% [markdown]
# # Make aggregated tables at hourly and daily level

#%%
get_ipython().run_line_magic('matplotlib', 'inline')


#%%
hosp.make_new_tables()


#%%
hosp.data.HOURLY.plot()


#%%
hosp.data.HOURLY2.sum()


#%%
hosp.data.ED.ARRIVAL_DTTM.max()


#%%
hosp.data.HOURLY2.sum()


#%%
hosp.


#%%
hosp.data.HOURLY


#%%
hosp.data.HOURLY.plot()


#%%
hosp.data.ED.shape


#%%
hosp.data.HOURLY


#%%
hosp.data.ED.shape


#%%



#%%



#%%
hosp.data.ED.columns


#%%
def count_hourly_occupancy(df,arrival_col,departure_col,count_name):
    """
    inputs:
    df with attendance number as index,
    arrival, departure datetime col names (must be datetime format)
    ouptut:
    df, contains many-to-many link between the arrival_
    """
    df1 = df[[arrival_col,departure_col]].head(1000).copy()
    df1[arrival_col] = df1[arrival_col].apply(lambda x : x.replace(second=0,minute=0)) # round arrival hour down
    df1[departure_col] = df1[departure_col].apply(lambda x : x.replace(second=0,minute=0)) +pd.Timedelta(hours=1) # round leaving tim up
    
    #### create col with number of hours active 
    df1['n_hours'] = ((df1[departure_col] - df1[arrival_col])/pd.Timedelta(1,'h')).astype(int)
    df1 = df1.drop(df1[df1['n_hours'] <=0].index) # must drop the negative n_hour rows as otherwise messes up my size of array initilisation (was getting an error that the index i was assinging to in ids was out of bounds).
    
    #### time efficient (i hope) function for cycling through and finding all combinations of active hours for attednaces - create a (long format) list of links between attendance numbers and 

    # function for list comp which finds list of datetimes (for each hour)
    date_func = lambda datetime , offset : datetime + pd.Timedelta(offset,'h')

    # iterate over rows in df
    df1 = df1.reset_index() # reset so have the new index to itereate over

    ids = np.empty(shape=(df1['n_hours'].sum()),dtype='int64') # initilise array - change to np.empty() to speed up
    timestamps = np.empty(shape=(df1['n_hours'].sum()),dtype='datetime64[s]')
    row_count = 0

    for row in df1.itertuples():
        atten_id = [row[1]]
        hour_list = [date_func(row[2],i) for i in np.arange(row[4])] # creates list of hour datetimes

        # create array of list for all combinations of timestamp
        for i in itertools.product(atten_id,hour_list):
            ids[row_count] = i[0] # assign patient numbers
            timestamps[row_count] = i[1]
            row_count += 1 # add to row count for new array    
    # put into df
    data = {'atten_id':ids}
    df_new = pd.DataFrame(data=data,index=timestamps)#,columns=[count_name])

    return(df_new)


#%%
test =count_hourly_occupancy(hosp.data.ED,'ARRIVAL_DTTM','DEPARTURE_DTTM','test')


#%%
def count_hourly_events(df,event_column_name,new_col_name):
    """
    Count number of events (records) at hourly level, given datetime column.
    input: df, column_name
    """
    #### set up data to make calc easier
    df['event_column_name_rounded'] = df[event_column_name].apply(lambda x : x.replace(second=0,minute=0)) # round to lower hour
    
    #### make array and find counts of uniques datetimes
    times = df['event_column_name_rounded'].values
    unique, counts = np.unique(times, return_counts=True)
    
    # put into df
    event_counts = pd.DataFrame(data = counts, index= unique,columns =[new_col_name] )
    return event_counts

count_hourly_events(hosp.data.ED,'ARRIVAL_DTTM','new_col')


#%%
a = np.array([0, 3, 0, 1, 0, 1, 2, 1, 0, 0, 0, 0, 1, 3, 4])
unique, counts = np.unique(a, return_counts=True)


#%%
counts


#%%
a = np.array(df1.index)
unique, counts = np.unique(a, return_counts=True)


#%%
df1.index


#%%
df1.col1.values


#%%
pd.Series(df1.index)


#%%

hosp.data.ED['ARRIVAL_DTTM'].apply(lambda x : x.replace(second=0,minute=0))


#%%
get_ipython().run_line_magic('matplotlib', 'inline')
test.plot()


#%%
test['atten_id'].value_counts()


#%%



#%%



#%%



#%%
break

#%% [markdown]
# # Dev

#%%
import pandas as pd
import numpy as np


#%%
pd.datetime.now()


#%%
master_index = pd.DatetimeIndex(start=pd.datetime(2019,1,1),periods=20,freq='D').round('D')
master_index


#%%
df1 = pd.DataFrame([3,5],master_index[0:2],columns=['col1'])
df1


#%%
df2 = pd.DataFrame([8,9],master_index[8:10],columns=['col2'])
df2


#%%
df3 = pd.DataFrame([1,2,3],master_index[1:4],columns=['col3'])
df3


#%%
concat = pd.concat([df1,df2,df3],sort=True)
concat


#%%
concat.reindex()


#%%
pd.master_index


#%%



#%%
from functools import reduce
data_frames = [df1, df3, df2]
df_merged = reduce(lambda  left,right: pd.merge(left,right,left_index=True,right_index=True,
                                            how='outer'), data_frames)
df_merged.ffill()
df_merged


#%%
df_merged.reindex(index=master_index)


#%%



#%%



#%%


#%% [markdown]
# ### mapping columns to standard naming convention
#%% [markdown]
# unless your columns are already named using the required names - use column mapping method

#%%
#### define dictionary for mapping
col_map = {
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
'SPECIALTY_REFERRED_TO_DESCRIPTION':'adm_referral_loc',
'ADMISSION_FLAG':'adm_flag',
'DEPARTURE_DTTM':'depart_datetime',
'STREAM_LOCAL_CODE':'stream'
}


#%%
len(col_map)


#%%
EDdata.map_columns(col_map)

#%% [markdown]
# required column names can be found: 

#%%
flosp._expected_file_structures.dataRAW_expected_cols.keys()


#%%



#%%
EDdata.get_EDraw().head(3)


#%%


#%% [markdown]
# ### bespoke user cleaning operations 
#%% [markdown]
# if at any stage manual edits to the data are required (e.g. cleaning a spurious datetime)... get data out of class, edit and replace:

#%%
#### get data out
df = EDdata.get_EDraw()

#### make changes to df
# my changes here

#### replace data into EDdata
EDdata.replace_EDraw(df)


#%%



#%%



#%%



#%%


#%% [markdown]
# ### converting datetimes
# #### datetime formats are often non-standard...some attention is needed but there are some built in methods to help.
#%% [markdown]
# convert columns to datetime formats (by default anything with 'datetime' in column name will be transformed.

#%%
EDdata.convert_cols_datetime("%Y/%m/%d %H:%M")

#%% [markdown]
# create a datetime column from seperate time and date columns.

#%%
EDdata.create_datetime_from_time('first_adm_request_time','arrive_datetime','first_adm_request_datetime')

#%% [markdown]
# ### automated cleaning
#%% [markdown]
# check what else needs doing to get data into normalised format:

#%%
EDdata.run_tests()

#%% [markdown]
# #### run as much automated cleaning as possible using: 

#%%
EDdata.autoclean()

#%% [markdown]
# run tests again:

#%%
EDdata.run_tests()

#%% [markdown]
# #### alternativly to autoclean,  step through the process using various methods:

#%%
EDdata.make_callender_columns()


#%%
EDdata.make_wait_columns()


#%%
EDdata.make_breach_columns()


#%%
EDdata.make_age_group_column()


#%%



#%%
EDdata.run_tests()


#%%



#%%


#%% [markdown]
# ## saving
# #### ioED (and flosp) will automate the structure of your saving folder in the root dir you provided when you created the EDdata instance of ioED

#%%
EDdata.save_path


#%%


#%% [markdown]
# #### at any stage save your data out to come back to later..

#%%
EDdata.saveRAWasRAW()


#%%



#%%


#%% [markdown]
# #### once your data is cleaned, save cleaned data out to .pkl file

#%%
EDdata.saveRAWasCLEAN()


#%%


#%% [markdown]
# #### load your data back from cleaned file again if you are using ioED:

#%%
EDdata.loadPKLasRAW()


#%%



#%%



