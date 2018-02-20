####

import json
import pandas as pd



class EDdata:
    """
    This is a test class to attempt EDdata analysis.

    Input
    name: string, name of hospital
    """

    def __init__(self,name):
        self._name = name

        # check for logfile for metadata
        from pathlib import Path
        myfile = Path('./logs/' + name +'.py')
        if 1 == 1: #myfile.exists():
            # load file and vars within _path_*, _check_*
            #https://pythonspot.com/json-encoding-and-decoding-with-python/
            print('file exists')
        else:
            # create log file - write to it whenever save a df etc
            for_log = {'name':self._name}
            print(json.dumps(for_log))


    def status(self):
        """
        Method to print details about class instance.
        """
        print(self._name)
        return

    def checks(self):
        """
        Run all checks we currently have on current progress.
        """
        print('checing.')

        return

    def importRAW(self,path,col_mapping):
        """
        Function imports ED data and extracts columns of interest into generic column namings.

        Inputs
        path: string, path to RAW ED csv file
        cols_select: dict, dictionary of columns to use {'name of col in input df':'new column name'}

        Output
        Pandas dataframe of ED patient level data.
        """

        print('-'*40)
        #print(importRAW)
        #### import dataframe
        print('importing ED data to dataframe')
        df = pd.read_csv(path,
        low_memory=False)
        print('Dataframe shape: ', df.shape)

        #### tidy column names
        from Fcleaning import pd_tidy_column_heads
        df = pd_tidy_column_heads(df) # how do i call this inslide function?

        #### select columns

        # define basic columns to include


        if col_mapping == None:
            print('Only usual columns will be added.')
            # should add a check here that all the column names are required
        else:
            print('User defined columns are okay.')
        # rename columns to standard format
        df.rename(columns = col_mapping,inplace=True)
        df = df[list(col_mapping.values())]

        self._dataRAW = df
        return #df

    def saveRAW(self):
        print('-'*40)
        print('Saving rawED df to csv.')
        self._dataRAW.to_csv('../../3_Data/processed/'+ self._name + 'ED.csv',index=False)
        return

    def importCLEAN(self):
        """

        """
        return

    def create_datetime_columns(self):
        self._dataRAW = create_datetime_col(self._dataRAW)

    def create_auto_columns(self):
        """
        Function creates additional colums which are automatic inc:
        - waiting time (minutes)
        - breach flag
        - callender columns
        """
        #### create waitingtime column
        self._dataRAW = make_waitingtime_column(self._dataRAW)
        #### create breach flags
        self._dataRAW['breach'] = (self._dataRAW['waiting_time'] > 4*60).astype(int)
        #### create: day of week, time of day, month of year columns
        self._dataRAW = make_callender_columns(self._dataRAW,'arrival_datetime','arr')
        self._dataRAW = make_callender_columns(self._dataRAW,'leaving_datetime','leaving')

    def __call__(self):
        return self.status()


######################################################
#### seperate functions ####
######################################################

def checkmissing(x):
    """
    input: df, for checking
    output: info about missing values
    """
    return df.isnull().sum()

def check_standard_colsED(x):
    """
    Function to check if standard columsn are present and flag warning if arn't.
    input
    x (df): for checking
    output: print statement of warnings
    """
    standard_colsED = [
    'dept_patid',
    'hosp_patid',
    'age',
    'gender',
    'site',
    'arrival_date',
    'arrival_time',
    'arrival_mode',
    'first_triage_time',
    'first_dr_time',
    'first_adm_request_time',
    'adm_referral_loc',
    'departure_method',
    'leaving_time',
    'flag_adm'
    ]
    # Loop check
    for i in standard_colsED:
        if i not in x.columns:
            print('WARNING: standard column missing in ED data: ', i)
    return()


def pd_tidy_column_heads(x):
    """
    Function makes all column names lowercase and replaces any whitespace with _'s. Removes wild characters.

    Input
    df for cleaning

    Returns
    tidy dataframe for assignment to variable name
    """
    rename_cols = dict() # make dictionary of old column names and new ones
    for i in x.columns:
        j = i.lower()
        j = j.strip()
        j = j.replace(' ','_')
        j = j.replace('.','_')
        j = j.replace('?','_')
        j = j.replace('&','_')
        j = j.replace('%','perc')
        j = j.replace('(','')
        j = j.replace(')','')
        j = j.replace(':','')
        j = j.replace(';','')
        j = j.replace('-','')
        j = j.replace('/','')
        #j = j.replace('\','')
        rename_cols[i] = j

    x = x.rename(columns=rename_cols)
    return(x)

def create_datetime_col(x):
    """
    Function creates datetime column from separate date and time columns.
    Input: df
    Output: df with additional columns
    """
    print('-'*40)
    print(create_datetime_col)
    # Create arrival datetime column
    print('Creating arrival datetime column...(make take some time)')
    f = lambda i: pd.to_datetime(i.arrival_date + ' ' + i.arrival_time)
    x['arrival_datetime'] = x.apply(f,axis=1)

    #Create dishcarge datetime column
    print('Creating leaving datetime column...(make take some time)')
    f = lambda j: pd.to_datetime(j.arrival_date + ' ' + j.leaving_time)
    x['leaving_datetime'] = x.apply(f,axis=1)

    # correct negative stay times in ED (these are people who have rolled past midnight). There is an assumption here that LOS !> 24hours
    datetime_values = x[(x.leaving_datetime - x.arrival_datetime) < pd.Timedelta(0)].leaving_datetime + pd.Timedelta('1 days')

    x.leaving_datetime.iloc[datetime_values.index] = datetime_values.values

    #### there are 8 people who were in there for > 24 hours. we have no way of picking up how long they were in there.
    #df[(df.discharge_time - df.arrival_time) == pd.Timedelta('1 days')].shape

    return(x)

def make_waitingtime_column(x):
    """
    Function to create datetime column with arrival and discharge datetime columns
    Input: df of rawED data
    Ouput: new df with additional column of waiting time in minutes
    """
    print('-'*40)
    print(make_waitingtime_column)
    x['waiting_time'] = (x['leaving_datetime'] - x['arrival_datetime']) / pd.Timedelta('1 minute')
    return(x)

def make_callender_columns(x,column,prefix):
    """
    Function to take a datetime column and create: hour of day, day of week, month of year columns.
    Input
    x(df): dataframe
    column (string): name of datetime column to work from
    prefix (string): give prefix for column names

    Output
    x(df): new df with additional columns with numerical indicators for callender vars.
    """
    print('-'*40)
    print(make_callender_columns)
    x[prefix + '_hour'] = x[column].dt.hour.astype(object)
    x[prefix + '_dayofweek'] = x[column].dt.dayofweek.astype(object)
    x[prefix + '_month'] = x[column].dt.month.astype(object)
    return(x)
