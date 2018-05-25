from flosp import _core

def test_fun():
    """ serves no purpose other than debugging """
    _core.message('test')
    return(True, _core.message)

def tidy_column_heads(df):
    """
    Function makes all column names lowercase and replaces any whitespace with _'s. Removes wild characters.
    Input: df, df, df for cleaning
    Return: df, df, dataframe with tidy names
    """
    rename_cols = dict() # make dictionary of old column names and new ones
    for i in df.columns:
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

    df = df.rename(columns=rename_cols)
    return(df)

def convert_cols_datetime(df,dt_format,col_names = None):
    """
    checks for datetime format and converts columns to datetime if not already.
    if no col_names argument list provided will use all columns with datetime in name. othwerwise will only look at columns given in col_names.
    input:
    df, df, dataframe on which to convert dt
    dt_format, str, format of datetime columns, e.g. "%d/%m/%Y %H:%M"
    col_names, list of str, optional containing names of columns to convert

    return: df with new column formattings
    """
    import numpy as np
    import pandas as pd
    _core.message('Converting cols to datetime...(may take some time depedning on size of df)...',size='s')

    #### find column names which have datetime in them, if non columns have been provided
    if col_names == None:
        col_names = search_in_cols(df, "datetime")

    #### find columns that are already in datetime format from the list
    col_names_dt = [i for i in col_names if df[i].dtype == np.dtype('datetime64[ns]')]
    for i in col_names_dt:
        _core.message(i + '...is already datetime format','s')
    #### get list of cols that need converting
    col_names = [i for i in col_names if df[i].dtype != np.dtype('datetime64[ns]')]

    #### do datetime conversion columns that are in list
    for i in col_names:
        _core.message(i + '...converting',size='s')
        df[i] = pd.to_datetime(df[i],format=dt_format)
    return(df)

def search_in_cols(df, search_term):
    """
    search in dataframe for columns containing a partial string
    input:
    df, df, df to search
    search_term, str, string to search for
    output: list of column names
    """
    col_names = []
    for item in df.columns:
        if search_term in (item):
            col_names.append(item)
    return(col_names)

def make_callender_columns(df,column,prefix):
    """
    takes a datetime column and creates multiple new columns with: hour of day, day of week, month of year.
    Input
    df, df: dataframe
    column, str: name of datetime column to work from
    prefix, str: give prefix for new column names

    Output
    df, df: new df with additional columns with numerical indicators for callender vars.
    """
    _core.message(make_callender_columns)
    df[prefix + '_hour'] = df[column].dt.hour.astype(int)
    df[prefix + '_dayofweek'] = df[column].dt.dayofweek.astype(int)
    df[prefix + '_month'] = df[column].dt.month.astype(int)
    df[prefix + '_week'] = df[column].dt.week.astype(int)
    df[prefix + '_dayofweek_name'] = df[column].dt.weekday_name.astype(str)
    df[prefix + '_year'] = df[column].dt.year.astype(int)
    df[prefix + '_date'] = df[column].dt.date.astype(object)
    df[prefix + '_flag_wkend'] = (df[prefix + '_dayofweek'] > 5).astype(int)
    return(df)


def create_datetime_from_time(df,time_col,date_col,new_col,auto_correct=True):
    """
    Function creates datetime column from separate date and time columns.
    Input:
    df, df,
    time_col, str, name of column to take time
    date_col, str, name of column to take date
    new_col, str, name of new column
    auto_correct, bool, set to false if do not want to check and correct if time has rolled over midnight.
    Output: df with additional columns
    """
    import pandas as pd
    import numpy as np
    import warnings
    _core.message('Create datetime column from: ' + str(time_col) +' & '+ str(date_col) )

    # get df without nans
    df_dropna = df[[time_col,date_col]].dropna()
    # create new column
    f = lambda i: pd.to_datetime(str(i[date_col]) + ' ' + str(i[time_col]))
    new_datetimes = df_dropna.apply(f,axis=1) # get new datetimes
    df.loc[new_datetimes.index,new_col] = new_datetimes

    # create warning and correction for any times that have rolled over the 24 hour mark; and therefore need 1 day adding (assumption that LOS !> 24hours!!)
    if auto_correct == True:
        datetime_values = df[(df[new_col] - df.arrive_datetime) < pd.Timedelta(0)][new_col] + pd.Timedelta('1 days')
        if datetime_values.shape[0] >= 1:
            warnings.warn(str(datetime_values.shape[0]) + ' patients detected who have -ve wait times. They have probably rolled over midnight, so we add + 1day to the new datetime column created. This assumes < 24hr stays only.\n\n\n')
            df.loc[datetime_values.index,new_col] = datetime_values.values
    return(df)
