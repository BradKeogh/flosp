
class timeseries():
    """ contains functions for processing time series data """

    def create_timeseries_from_events(df, col_start, col_end, col_to_split=None, start=None, end=None,freq='H'):
        """
        Input:
        df, df, with event data
        col_start, str, column name with datetime of the start of the event
        col_end, str, column ame with dateitme of the end of hte event
        start, str, datetime of when to start time series from. e.g. '3/1/2015'
        end, str, datetime of when to end timeseries.
        col_to_split, str, column name of optional sub-splitting of data.


        Output: df, with timeseries index with counts of events for each period.
        """
        import pandas as pd
        import numpy as np
        from flosp import basic_tools

        #### set default vals if none given
        if start == None:
            start = df[col_start].min() # could use col_end here to ensure that all events are finished.
        if end == None:
            end = df[col_start].max()
        if col_to_split != None:
            #### get list to interate if a split column is given
            cols_clean = {}
            for i in df[col_to_split].unique():
                if type(i) == np.str:
                    j = basic_tools.tidy_string(i)
                else:
                    j = i
                cols_clean[i] = j

        #### create new df with timeseries index
        index = pd.date_range(start=start,end=end,freq=freq) #make index
        occ = pd.DataFrame(index=index) # make df


        #### interat over each rowin occ df
        dftemp = df

        if col_to_split == None:
            for index, row in occ.iterrows():
                index_time = index
                #get df with patients currently within trust
                mask = (dftemp[col_start] < index_time) & (dftemp[col_end] > index_time)
                dftemp2 = dftemp[mask]
                # calc size of df
                occ.loc[index,'count_all'] = dftemp2.shape[0]

        if col_to_split != None:

            for index, row in occ.iterrows():
                index_time = index
                #get df with patients currently within trust
                mask = (dftemp[col_start] < index_time) & (dftemp[col_end] > index_time)
                dftemp2 = dftemp[mask]
                # calc size of df after queries
                for i in cols_clean:
                    #print(i)
                    filter_val = cols_clean[i]
                    occ.loc[index,filter_val] = dftemp2[dftemp2[col_to_split] == i].shape[0]

            # problem inmplementing when column names do not exist in occ.
            #occ['count_all'] = 0
            #for k in cols_clean:
            #    occ['count_all'] += occ[i]


        return(occ)
