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


        #### combine aggregations:
        # Events - merge, reindex, fill zeros
        events_dfs = [ED_arrivals,ED_departures,IP_admissions_total,IP_discharges_total]
        events_df_merged = merge_series_with_datetime_index(events_dfs)

        # reindex, 
        events_df_merged2 = events_df_merged.reindex(index=master_index) # No ED counts when do this; this looks like a problem, but actually example ED dataset is lacking any data for this period.
        
        # Occupancies - merge, reindex, ffill

        occ_dfs = [ED_occ_total]


        # Merge into one table, assign to data class
        self.data.HOURLY = events_df_merged
        self.data.HOURLY2 = ED_occ_total
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



def count_hourly_occupancy(df,arrival_col,departure_col,count_name):
    """
    inputs:
    df with attendance number as index,
    arrival, departure datetime col names (must be datetime format)
    ouptut:
    df, contains many-to-many link between the arrival_
    NOTE: re-write required: very slow.
    """
    import itertools
    df1 = df[[arrival_col,departure_col]].copy()
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
    df_new = pd.DataFrame(data=data,index=timestamps,columns=[count_name])

    return(df_new)

def count_hourly_events(df,event_column_name,new_col_name):
    """
    Count number of events (records) at hourly level, given datetime column.
    input: df, column_name.
    """
    #### set up data to make calc easier
    df['event_column_name_rounded'] = df[event_column_name].apply(lambda x : x.replace(second=0, minute=0)) # round to lower hour
    
    #### make array and find counts of uniques datetimes
    times = df['event_column_name_rounded'].values
    unique, counts = np.unique(times, return_counts=True)
    
    # put into df
    event_counts = pd.DataFrame(data = counts, index= unique, columns = [new_col_name])
    return event_counts

def merge_series_with_datetime_index(dfs_to_merge):
    "take list of dfs and merge all on index. returns merged df."

    events_df_merged = reduce(lambda  left, right: pd.merge(left, right ,left_index=True, right_index=True, how='outer'), dfs_to_merge)

    return events_df_merged