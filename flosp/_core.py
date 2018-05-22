import pandas as pd

def message(text, size = 'l',footer=False):
    """ make output from message call """
    if size == 'l':
        print('-'*40)
        print(text)
    elif size == 'm':
        print('-'*20)
        print(text)
    elif size == 's':
        print(text)
    if footer == True:
        print('-'*20)
    return

def make_wait_columns(df):
    """ creates wait columns for dataframe
    """
    df['waiting_time'] = (df['depart_datetime'] - df['arrive_datetime']) / pd.Timedelta('1 minute')

    df['arr_triage_wait'] = (df.first_triage_datetime - df.arrive_datetime) / pd.Timedelta('1 minute')
    df['arr_dr_wait'] = (df.first_dr_datetime - df.arrive_datetime) / pd.Timedelta('1 minute')
    df['arr_adm_req_wait'] = (df.first_adm_request_datetime - df.arrive_datetime) / pd.Timedelta('1 minute')

    df['adm_req_dep_wait'] = (df.depart_datetime - df.first_adm_request_datetime) / pd.Timedelta('1 minute')

    df['dr_adm_req_wait'] = (df.first_adm_request_datetime - df.first_dr_datetime) / pd.Timedelta('1 minute')

    df['dr_dep_wait'] = (df.depart_datetime - df.first_dr_datetime) / pd.Timedelta('1 minute')

    return(df)

def check_column_dtypes(df,exp_dtype_dict = None ,col_to_check = None):
    """
    Check columns match expected datatype.
    Input:
    df,df, dataframe to check
    exp_dict, dict, columns (index) and list of aceptable dtype (values).
    col_to_check, lst of str, column names that we wish to check. If None, will check all cols.
    """
    df_dtypes = exp_dtype_dict

    if col_to_check == None:
        for j in df.columns:
            if not df[j].dtypes in df_dtypes[j]:
                print('Col ', j.ljust(25), ' is:',df[j].dtypes,'. Expected any of: ', df_dtypes[j])
    else:
        for j in col_to_check:
            if df[j].dtypes != df_dtypes[j]:
                print('Col ', j.ljust(25), ' is:',df[j].dtypes,'. Expected any of: ', df_dtypes[j])
    return
