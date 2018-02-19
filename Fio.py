import pandas as pd

def EDimport(path, cols_select = None):
    """
    Function imports ED data and extracts columns of interest into generic dataframe structure. Function already has specified columns of interest, but these can be over-ridden and added to using additional_cols argument.

    Inputs
    path (string): path to ED csv file
    cols_select (dict): dictionary of columns to use {'name of col in input df':'new column name'}

    Ouput
    Pandas dataframe of ED patient level data.
    """

    print('-'*40)
    print(EDimport)
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
    portsmouth_cols = {
    'pas_id':'dept_patid',
    'nhs_number':'hosp_patid',
    'age':'age',
    'gender':'gender',
    'department':'site',
    'date_of_attendance':'arrival_date',
    'time_of_attendance':'arrival_time',
    'mode_of_arrival':'arrival_mode',
    'triage_time':'first_triage_time',
    'dr1_seen':'first_dr_time',
    'referred_to__first_referral':'first_adm_request_time',
    'referred_to_at_point_of_discharge':'adm_referral_loc',
    'departure_method':'departure_method',
    'left_dept_time':'leaving_time',
    'departure_method':'departure_method'
    }

    if cols_select == None:
        print('Only usual columns will be added.')
        cols_select = portsmouth_cols
    else:
        print('User defined columns list to be used.')
    # rename columns to standard format
    df.rename(columns = cols_select,inplace=True)
    df = df[list(cols_select.values())]
    return(df)









###other varaibles to include










    #
