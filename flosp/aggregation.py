import itertools

import numpy as np
import pandas as pd
from functools import reduce

class Aggregate:
    """ 
    Aggregates new tables from record data. i.e. takes ED attendance table and produces hourly or/and daily tables.
    """

    def __init__(self,data,metadata):
        """ """
        # get data
        self.data = data
        self.metadata = metadata
        # check if ED and IP present, create flag 
        self.metadata.list_record_level_dfs = []
        if hasattr(self.data, 'ED'):
            self.metadata.list_record_level_dfs.append('ED')
        
        if hasattr(self.data,'IP'):
            self.metadata.list_record_level_dfs.append('IP')
        # run hourly and daily methods.
        self.make_hourly_table()
        self.make_daily_table()

        return

    def make_hourly_table(self):
        """ Takes record level dfs and makes aggregate HOURLY table.
        Assigns output as DATA class attribute.
        """
        # get data range, create DT index
        master_index = self.make_masterDT_index()
        #### Aggregate ED columns
        # Count events - 
        ED_arrivals = count_hourly_events(self.data.ED,'ARRIVAL_DTTM','ED_arrivals')
        ED_departures = count_hourly_events(self.data.ED,'DEPARTURE_DTTM','ED_departures')
        # occupancy counting
        ED_occ_total = count_hourly_occupancy(self.data.ED,'ARRIVAL_DTTM','DEPARTURE_DTTM','ED_occ_total')


        #### Aggregate IP columns
        # events
        IP_admissions_total = count_hourly_events(self.data.IP,'ADM_DTTM','IP_admissions_total')
        IP_discharges_total = count_hourly_events(self.data.IP,'DIS_DTTM','IP_discharges_total')
        # occupancy
        IP_occ_total = count_hourly_occupancy(self.data.IP,'ADM_DTTM','DIS_DTTM','IP_occ_total')

        # df_new = count_hourly_occupancy2(self.data.ED,'ARRIVAL_DTTM','DEPARTURE_DTTM','new_col')


        #### combine aggregations:
        # Events - merge, reindex, fill zeros
        events_dfs = [ED_arrivals,ED_departures,IP_admissions_total,IP_discharges_total]
        events_df_merged = merge_series_with_datetime_index(events_dfs)
        events_df_merged = events_df_merged.resample('H').sum() # fills in missing hours from datetime index. using .sum() puts zeroes into the missing values of the index.
        events_df_merged.fillna(value=0, inplace=True)

        # reindex, 
        events_df_merged2 = events_df_merged.reindex(index=master_index) # No ED counts when do this; this looks like a problem, but actually example ED dataset is lacking any data for this period.
        
        # Occupancies - merge, reindex, ffill

        occ_dfs = [ED_occ_total, IP_occ_total]
        occ_df_merged = merge_series_with_datetime_index(occ_dfs)
        occ_df_merged = occ_df_merged.resample('H').ffill() # fill missing hours in datetime index. ffill from previous occupancy that has been calculated.
        events_df_merged.fillna(value='ffill', inplace=True)



        # Merge into one table, assign to data class
        hourly = merge_series_with_datetime_index([events_df_merged, occ_df_merged])
        self.data.HOURLY = hourly
        # self.data.HOURLY2 = occ_df_merged
        return
    

    def count_hourly_occupancy2(self,df,datetime_col_start,datetime_column_end):
        """
        inputs: df, col_name, new_col_name
        returns: df, with datetime index at hourly level, index not complete
        """
        #### setup data to be easier to compute, 
        df['event_column_name_rounded'] = df[event_column_name].apply(lambda x : x.replace(second=0, minute=0)) # round to lower hour
        
        #### make array and find counts of uniques datetimes
        times = df['event_column_name_rounded'].values
        unique, counts = np.unique(times, return_counts=True)
        
        # put into df
        event_counts = pd.DataFrame(data = counts, index= unique, columns = [new_col_name])
        #### 

        return

    def aggregate_columns(self,dt_index):
        """ takes a """
        # 
        return

    def make_daily_table(self):
        """ Takes hourly level df and aggregates to DAILY table.
        Assigns output as a DATA class attribute.
        """
        # check that hourly table exists. (superfluous?, only called above.)

        # find date range (from hourly table), make DT index.

        # perform groupby on each column in houlry status

        # perform groupby on some filtered columns, i.e. discharges pre-noon

        # combine into new table, assign to data class
        pass

    def make_masterDT_index(self):
        """ Takes dataframes which are available. Returns datetime index which spans all records. """
        dt_mins = []
        dt_maxs = []

        for i in self.metadata.list_record_level_dfs:
            df = getattr(self.data,i)
            i_metadata = getattr(self.metadata,i)
            col_name = i_metadata.dataRAW_first_datetime_col
            dt_mins.append(find_min_value_in_dataframe_col(df,col_name)) # add min value of first datetime col to list
            col_name = i_metadata.dataRAW_second_datetime_col
            dt_maxs.append(find_max_value_in_dataframe_col(df,col_name))
        print(dt_mins)
        startDT = np.amin(dt_mins).round('D')
        endDT = np.amax(dt_maxs).round('D')

        datetimeindex = pd.DatetimeIndex(start=startDT,end=endDT,freq='H')

        return datetimeindex


def find_max_value_in_dataframe_col(df,col_name):
    " given a dataframe and name of datetime column. return the max and min dates."
    max_val = df[col_name].max()
    return max_val

def find_min_value_in_dataframe_col(df,col_name):
    " given a dataframe and name of datetime column. return the max and min dates."
    min_val = df[col_name].max()
    return min_val


def count_hourly_events(df,event_column_name,new_col_name):
    """
    Takes a df at patient record level, counts number of events (records) at hourly level. Event is taken to happen when event_column_name datetime occurs.
    Input
    =====
    df, dataframe, 
    event_column_name, str, 
    new_column_name, str, 

    Output
    ======
    even_counts, dataframe, single column with count of events, datetime index (hourly & potentially non-continuous). 


    """
    #### set up data to make calc easier
    df['event_column_name_rounded'] = df[event_column_name].apply(lambda x : x.replace(second=0, minute=0)) # round to lower hour
    
    #### make array and find counts of uniques datetimes
    times = df['event_column_name_rounded'].values
    unique, counts = np.unique(times, return_counts=True)
    
    # put into df
    event_counts = pd.DataFrame(data = counts, index= unique, columns = [new_col_name])
    return event_counts

    
def count_hourly_occupancy(df,datetime_col_start,datetime_column_end, new_column_name):
    """
    Function takes patient record level dataframe and calculates the occupancy/activity for each hour of the day.
    The activity is defined based on the two datetime columns being provided.
    e.g. if 'attendnace datetime' and 'departure datetime' were given then the 'activity' would be the occupancy of the department.

    Inputs
    ======
    df, pandas dataframe, with patient-record level activity.
    datetime_col_start, str, name of column in df when the activity begins. Column must be in datetime format.
    datetime_col_end, str, name of column in df when the activity ends. Column must be in datetime format.
    new_col_name, str, name to assign the new column that is produced.

    Output
    ======
    df, pandas dataframe, datetime index at hourly level, single column containing the count of activity in that hour
    (index potentially not continuous).
    """
    #### setup data to be easier to compute, 
#         df['event_column_name_rounded'] = df[event_column_name].apply(lambda x : x.replace(second=0, minute=0)) # round to lower hour
    df1 = df[[datetime_col_start,datetime_column_end]].copy()
    df1[datetime_col_start] = df1[datetime_col_start].apply(lambda x : x.replace(second=0,minute=0)) # round arrival hour down
    df1[datetime_column_end] = df1[datetime_column_end].apply(lambda x : x.replace(second=0,minute=0)) +pd.Timedelta(hours=1)
    
    
    #### create col with number of hours active 
    df1['n_hours'] = ((df1[datetime_column_end] - df1[datetime_col_start])/pd.Timedelta(1,'h')).astype(int)
    df1 = df1.drop(df1[df1['n_hours'] <=0].index) # must drop the negative n_hour rows as otherwise messes up my size of array initilisation (was getting an error that the index i was assinging to in ids was out of bounds).

    #### time efficient (i hope) function for cycling through and finding all combinations of active hours for attednaces 
    # - create a (long format) list of links between attendance numbers and 
    # function for list comp which finds list of datetimes (for each hour)
    date_func = lambda datetime , offset : datetime + pd.Timedelta(offset,'h')

    # iterate over rows in df
    df1 = df1.reset_index() # reset so have the new index to itereate over

    ids = np.empty(shape=(df1['n_hours'].sum()),dtype='int64') # initilise array - change to np.empty() to speed up
    timestamps = np.empty(shape=(df1['n_hours'].sum()),dtype='datetime64[s]')
    row_count = 0 # initialise row counter for empty arrays
    
    # iterate through rows of df
    for row in df1.itertuples():
        atten_id = [row[1]] # get attendance id
        hour_list = [date_func(row[2],i) for i in np.arange(row[4])] # make a list datetimes for each hour that patient is active.

        # populate empty arrays with seperate list of ids and timestamps.  
        for i in itertools.product(atten_id,hour_list):
            ids[row_count] = i[0] # assign patient number to array
            timestamps[row_count] = i[1] # 
            row_count += 1 # add to row count for new id-> hour pair
    
    # put ids and timestamps into df
    data = {'atten_id':ids,'hours':timestamps}
    df_new = pd.DataFrame(data=data)
    
    # count isntances for each hour
    df_new = df_new.groupby(['hours']).count()
    
    # Tidy colum names
#     df_new.set_index('hours', inplace=True)
    df_new.index.name = '' # remove 'hours' as index name
    
    df_new.rename(columns = {'atten_id' : new_column_name}, inplace = True) # rename to final column name.

    return df_new



def merge_series_with_datetime_index(dfs_to_merge):
    "take list of dfs and merge all on index. returns merged df."

    events_df_merged = reduce(lambda  left, right: pd.merge(left, right ,left_index=True, right_index=True, how='outer'), dfs_to_merge)

    return events_df_merged