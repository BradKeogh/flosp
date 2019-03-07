import itertools

import numpy as np
import pandas as pd
from functools import reduce

from flosp.basic_tools import make_callender_columns

class Aggregate:
    """ 
    Aggregates new tables from record-level data. i.e. takes ED attendance table and produces hourly or/and daily tables.
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
        self.make_IPSPELL_table()
        self.make_hourly_table()
        self.make_daily_table()

        return

    def make_IPSPELL_table(self):
        """ 
        Takes record-level IP data at location level (i.e. multiple records for a single spell/hospital stay, either FCE or ward) and makes SPELL level record.
        """
        #### Get IP data and filter for first location record for each spell/hospital stay 
        df = self.data.IP.query('LOCATION_NUMBER == "1"').copy()
        #### remove LOCATION columns that are now not of interest
        df.drop(['LOCATION_END','LOCATION_START','LOCATION_NUMBER'],axis=1,inplace=True)
        #### rename LOCATION_NAME to 'FIRST_LOCATION'
        df.rename(columns={'LOCATION_NAME':'FIRST_LOCATION'},inplace=True)
        self.data.IPSPELL = df
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
        # ED_admissions # query for admitted patients,'DEPARTURE DTTM'
        # ED_breaches # query: breach patients, 'BREACH DTTM'
        #  
        # occupancy counting
        EDocc_total = count_hourly_occupancy(self.data.ED,'ARRIVAL_DTTM','DEPARTURE_DTTM','EDocc_total')

        # col with breach time -> so can count events
        # optional query for count_hourly_events

        # Definitions found here: https://www.datadictionary.nhs.uk/data_dictionary/attributes/a/add/admission_method_de.asp?shownav=1?query=%22admission+type%22&rank=3.012927&shownav=1

        ## IP queries
        nonelec_query = "ADM_METHOD in ['21','22','23','24','25','2A','2B','2C','2D','28','81']"
        elec_query = "ADM_METHOD in ['11','12','13']" # 11,12,13
        elec_nonelec_query = "ADM_METHOD in ['21','22','23','24','25','2A','2B','2C','2D','28','81','11','12','13']"
        excludingdaycases_query = "ADM_TYPE in ['Non-Elective','Elective']"
        onlydaycases_query = "ADM_TYPE in ['Day Case']"
        ## ED queries
        breach_query = "BREACH_FLAG in [1]" # lookat records with only patients who breach.
        admission_query = "ADMISSION_FLAG in [1]" # look at records with only patients who are admitted.



        #### Aggregate IP columns
        # events
        IP_admissions_total = count_hourly_events(self.data.IPSPELL,'ADM_DTTM','IP_admissions_total')
        IP_discharges_total = count_hourly_events(self.data.IPSPELL,'DIS_DTTM','IP_discharges_total')

        IP_admissions_nonelec = count_hourly_events(self.data.IPSPELL,'ADM_DTTM','IP_admissions_nonelec', query=nonelec_query)
        IP_admissions_elec = count_hourly_events(self.data.IPSPELL,'ADM_DTTM','IP_admissions_elec', query=elec_query)
        IP_admissions_elec_nonelec = count_hourly_events(self.data.IPSPELL,'ADM_DTTM','IP_admissions_elec_nonelec', query=elec_nonelec_query)
        IP_admissions_excludingdaycases = count_hourly_events(self.data.IPSPELL,'ADM_DTTM','IP_admissions_excludingdaycases', query=excludingdaycases_query)
        
        IP_discharges_nonelec = count_hourly_events(self.data.IPSPELL,'DIS_DTTM','IP_discharges_nonelec', query=nonelec_query)
        IP_discharges_elec = count_hourly_events(self.data.IPSPELL,'DIS_DTTM','IP_discharges_elec', query=elec_query)
        IP_discharges_elec_nonelec = count_hourly_events(self.data.IPSPELL,'DIS_DTTM','IP_discharges_elec_nonelec', query=elec_nonelec_query)

        

        # occupancy
        
        EDocc_total = count_hourly_occupancy(self.data.ED,'ARRIVAL_DTTM','DEPARTURE_DTTM','EDocc_total')
        EDocc_breaching_patients = count_hourly_occupancy(self.data.ED,'ARRIVAL_DTTM','DEPARTURE_DTTM','EDocc_breaching_patients', query=breach_query)
        EDocc_awaiting_adm = count_hourly_occupancy(self.data.ED,'ADM_REQUEST_DTTM','DEPARTURE_DTTM','EDocc_awaiting_adm', query=admission_query)

        IPocc_total = count_hourly_occupancy(self.data.IPSPELL,'ADM_DTTM','DIS_DTTM','IPocc_total')

        IPocc_elec_nonelec = count_hourly_occupancy(self.data.IPSPELL,'ADM_DTTM','DIS_DTTM','IPocc_elec_nonelec', query = elec_nonelec_query)

        IPocc_elec = count_hourly_occupancy(self.data.IPSPELL,'ADM_DTTM','DIS_DTTM','IPocc_elec', query = elec_query)

        IPocc_excludingdaycases = count_hourly_occupancy(self.data.IPSPELL,'ADM_DTTM','DIS_DTTM','IPocc_excludingdaycases', query = excludingdaycases_query)

        IPocc_daycases = count_hourly_occupancy(self.data.IPSPELL,'ADM_DTTM','DIS_DTTM','IPocc_daycases', query = onlydaycases_query)
        
        # df_new = count_hourly_occupancy2(self.data.ED,'ARRIVAL_DTTM','DEPARTURE_DTTM','new_col')


        #### combine aggregations:
        ## Events - merge, reindex, fill zeros
        events_dfs = [
            ED_arrivals,
            ED_departures,

            IP_admissions_total,
            IP_admissions_excludingdaycases,
            IP_admissions_elec,
            IP_admissions_elec_nonelec,
            IP_admissions_nonelec,

            IP_discharges_total,
            IP_discharges_nonelec,
            IP_discharges_elec,
            IP_discharges_elec_nonelec,
            ]

        events_df_merged = merge_dfs_with_datetime_index(events_dfs)
        events_df_merged = events_df_merged.resample('H').sum() # fills in missing hours from datetime index. using .sum() puts zeroes into the missing values of the index.
        events_df_merged.fillna(value=0, inplace=True)

        # reindex events - commented out post as assigned variables is never used.
        # events_df_merged2 = events_df_merged.reindex(index=master_index) # No ED counts when do this; this looks like a problem, but actually example ED dataset is lacking any data for this period.
        
        ## Occupancies - merge, reindex, ffill

        occ_dfs = [
            EDocc_total,
            EDocc_breaching_patients,
            EDocc_awaiting_adm,

            IPocc_total,
            IPocc_elec,
            IPocc_elec_nonelec,
            IPocc_excludingdaycases,
            IPocc_daycases,
            ]

        occ_df_merged = merge_dfs_with_datetime_index(occ_dfs)
        occ_df_merged = occ_df_merged.resample('H').ffill() # fill missing hours in datetime index. ffill from previous occupancy that has been calculated.
        events_df_merged.fillna(value='ffill', inplace=True)


        # Merge into one table, assign to data class
        hourly = merge_dfs_with_datetime_index([events_df_merged, occ_df_merged])
        # create final columns as necessary
        hourly['IPadm_minus_dis_elec_nonelec'] = hourly['IP_admissions_elec_nonelec'] - hourly['IP_discharges_elec_nonelec']
        self.data.HOURLY = hourly
        # self.data.HOURLY2 = occ_df_merged
        return
    
    def make_daily_table(self):
        """ 
        Takes hourly level df and aggregates to DAILY table.
        Different columns require different aggregation. Seperate loops used to compute each.
        Assigns output df as a data.DAILY class attribute.
        """
        #### perform index resample (to daily) on each column in hourly status
        # SUMMED COLUMNS
        daily_columns_list = []
        for column in ['ED_arrivals','ED_departures','IP_admissions_excludingdaycases']:
            daily_series = self.data.HOURLY[column].resample('D').sum()
            daily_df = pd.DataFrame(daily_series) # make series into dataframe so can use merge_dfs_with_datetime_index 
            daily_columns_list.append(daily_df)
        
        # MEAN columns
        for column in ['IPocc_elec_nonelec','IPocc_total']:
            daily_series = self.data.HOURLY[column].resample('D').mean()
            daily_df = pd.DataFrame(daily_series) # make series into dataframe so can use merge_dfs_with_datetime_index
            daily_df.rename(columns={column:column + '_MEAN'},inplace=True) # add suffix to column name in daily df
            daily_columns_list.append(daily_df)


        # MAX columns
        for column in ['IPocc_total','IPocc_elec_nonelec','EDocc_total','IPocc_excludingdaycases']:
            daily_series = self.data.HOURLY[column].resample('D').max()
            daily_df = pd.DataFrame(daily_series) # make series into dataframe so can use merge_dfs_with_datetime_index
            daily_df.rename(columns={column:column + '_MAX'},inplace=True) # add suffix to column name in daily df
            daily_columns_list.append(daily_df)


        # perform groupby on some filtered columns, i.e. discharges pre-noon #  'IPdis_pre12_elec_nonelec'
        for column in ['IP_discharges_elec_nonelec']:
            daily_series = self.data.HOURLY.between_time('0:00', '12:01')[column].resample('D').sum()
            daily_df = pd.DataFrame(daily_series) # make series into dataframe so can use merge_dfs_with_datetime_index
            daily_df.rename(columns={column:column + '_PRE12'},inplace=True) # add suffix to column name in daily df
            daily_columns_list.append(daily_df)

        # combine into new table, assign to data class
        daily_dfs_merged = merge_dfs_with_datetime_index(daily_columns_list)

        # make callender columns
        daily_dfs_merged['date'] = daily_dfs_merged.index

        make_callender_columns(daily_dfs_merged,'date','date')

        self.data.DAILY = daily_dfs_merged
        return

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
        startDT = np.amin(dt_mins).round('D')
        endDT = np.amax(dt_maxs).round('D')

        datetimeindex = pd.DatetimeIndex(start=startDT,end=endDT,freq='H')

        return datetimeindex


def find_max_value_in_dataframe_col(df,col_name):
    " given a dataframe and name of datetime column. return the max and min dates in the column."
    max_val = df[col_name].max()
    return max_val

def find_min_value_in_dataframe_col(df,col_name):
    " given a dataframe and name of datetime column. return the max and min dates in the column."
    min_val = df[col_name].max()
    return min_val


def count_hourly_events(df,event_column_name,new_col_name, query = None):
    """
    Takes a df at patient record level, counts number of events (records) at hourly level. Event is taken to happen when event_column_name datetime occurs.
    
    Input
    =====
    df, dataframe, 
    event_column_name, str, 
    new_column_name, str, 
    query, str, optional, sql-style query called on df using df.query('input string query here')

    Output
    ======
    even_counts, dataframe, single column with count of events, datetime index (hourly & potentially non-continuous). 


    """
    #### filter for query if present
    if query != None:
        df = df.query(query)# .copy() -required to remove pink warning of copying when user calls method "make_new_tables()"

    #### set up data to make calc easier
    df['event_column_name_rounded'] = df[event_column_name].apply(lambda x : x.replace(second=0, minute=0)) # round to lower hour
    
    #### make array and find counts of uniques datetimes
    times = df['event_column_name_rounded'].values
    unique, counts = np.unique(times, return_counts=True)
    
    # put into df
    event_counts = pd.DataFrame(data = counts, index= unique, columns = [new_col_name])
    return event_counts

    
def count_hourly_occupancy(df,datetime_col_start,datetime_column_end, new_column_name,query = None):
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
    query, str, optional, sql-style query called on df using df.query('input string query here')

    Output
    ======
    df, pandas dataframe, datetime index at hourly level, single column containing the count of activity in that hour
    (index potentially not continuous).
    """
    # if query present filter dataframe with it
    if query != None:
        df = df.query(query)
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



def merge_dfs_with_datetime_index(dfs_to_merge):
    "take list of dfs and merge all on index. returns merged df."

    events_df_merged = reduce(lambda  left, right: pd.merge(left, right ,left_index=True, right_index=True, how='outer'), dfs_to_merge)

    return events_df_merged