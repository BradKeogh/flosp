import pandas as pd
#from flosp.plotting import *

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

def make_wait_columns_ED(df):
    """ creates wait columns for dataframe
    """
    df['waiting_time'] = (df['DEPARTURE_DTTM'] - df['ARRIVAL_DTTM']) / pd.Timedelta('1 minute')

    df['arr_triage_wait'] = (df.TRIAGE_ASSESSMENT_DTTM - df.ARRIVAL_DTTM) / pd.Timedelta('1 minute')
    df['arr_dr_wait'] = (df.FIRSTDOC_FOR_TREATMENT_DTTM - df.ARRIVAL_DTTM) / pd.Timedelta('1 minute')
    df['arr_adm_req_wait'] = (df.ADM_REQUEST_DTTM - df.ARRIVAL_DTTM) / pd.Timedelta('1 minute')

    df['adm_req_dep_wait'] = (df.DEPARTURE_DTTM - df.ADM_REQUEST_DTTM) / pd.Timedelta('1 minute')

    df['dr_adm_req_wait'] = (df.ADM_REQUEST_DTTM - df.FIRSTDOC_FOR_TREATMENT_DTTM) / pd.Timedelta('1 minute')

    df['dr_dep_wait'] = (df.DEPARTURE_DTTM - df.FIRSTDOC_FOR_TREATMENT_DTTM) / pd.Timedelta('1 minute')

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

def create_dir(path):
    """ check if directory path exisits. and if not create it. """
    import os
    #check that folder strucutre exisits - if not create
    if os.path.isdir(path) != True:
        os.makedirs(path)
    return

def save_pickle(df, path, filename):
    """
    Save df to pkl in a directory of your choice. Will generate path if not already there.
    Inputs:
    df, df, df to save
    path, str, path to save to
    filename, str, name of file
    """
    create_dir(path)

    #add / to filename if not present
    path, filename = path_filename_checks(path,filename)

    #save as pkl
    fullfilepath = path + filename
    df.to_pickle(fullfilepath)
    message('saved file: ' + fullfilepath)
    return

def loadPKL(path,filename):
    """ load pkl file from directory of your choice.
    input
    path, str, location of pkl
    attribute_name: str, name to store under
    """
    path, filename = path_filename_checks(path,filename)

    fullfilepath = path + filename
    df = pd.read_pickle(fullfilepath) # read pkl to df
    message('loaded file: ' + fullfilepath)
    return(df)


def path_filename_checks(path,filename):
    """ ensure that filename and path are in particular format."""
    path = path_backslash_check(path)

    if filename[-4:] != '.pkl':
        filename = filename + '.pkl'
    return(path,filename)

def path_backslash_check(path):
    """ensure that path name has a / at end """
    if path[-1:] !='/':
        path = path + '/'
    return(path)

def path_add_child_structure(path,to_add):
    """ add child structure, defined only here, to the end of the path. Has call for path_backslash_check inbuilt, on both ends of child_path. """
    path = path_backslash_check(path)
    path = path + 'processed/' + to_add
    path = path_backslash_check(path)
    return(path)


def search_for_pkl(path, filename):
    """
    search for file at path. return true if file exists, eles return false.
    """
    from os.path import exists
    if exists(path + filename):
        print('Found: ' + path + filename)
        exists = True
    else:
        print('Missing: ' + path + filename)
        exists = False
    return(exists)

def create_spell_from_multimove(df,col_move_no='move_no' ):
    """ take df with fce or ward level records, i.e. each line is a seperate fce or ward stay, and produce a spell level df, i.e. each line is a patient spell/hospital stay.
    Input: df, df, @ fce or ward level; col_move_no, str, name of column to group stay on. """
    df2 = df.sort_values(['hosp_patid','adm_datetime',col_move_no]).reset_index(drop=True).copy()

    df2['move_name_dis'] = df2[col_move_no]

    aggs = {col_move_no:len,'move_name':'first','move_name_dis':'last'}

    df_gb = df2.groupby(['hosp_patid','adm_datetime']).agg(aggs)

    df_gb.reset_index(inplace=True)

    ##### list columns to add after the groupby
    addit_cols  = ['hosp_patid','adm_datetime','admission_method','admission_type','spel_los','gender','site','age_group','age','move_no',
                   'adm_year','adm_month','adm_dayofweek','adm_dayofweek_name','adm_flag_wkend','adm_hour', 'adm_day','adm_week','adm_date','adm_flag_wkend',
                   'dis_hour', 'dis_dayofweek','dis_month', 'dis_week', 'dis_dayofweek_name', 'dis_year','dis_datetime',
                   'dis_destination', 'dis_method', 'dis_day','dis_date', 'dis_flag_wkend']

    df_addit = df[addit_cols].groupby(['hosp_patid','adm_datetime']).first()

    df_addit = df[addit_cols].query('move_no == 1')

    df_addit.reset_index(inplace=True)

    df_addit.drop(col_move_no,axis=1,inplace=True)

    dfspel = df_gb.merge(df_addit,on=['hosp_patid','adm_datetime'])

    dfspel.rename(columns={col_move_no:'move_total','move_name':'adm_loc','move_name_dis':'dis_loc'},inplace=True)

    dfspel.drop('index',axis=1,inplace=True)
    return(dfspel)

def make_admtype_from_adm_method_column(df):
    """
    Takes IP pandas df in FLOSP format and creates column ADM_TYPE with entries Elective/Non-Elective/Day Case.
    ADM_METHOD column must be in string format.
    """
    
    elec_query = "ADM_METHOD in ['11','12','13']"
    nonelec_query = "ADM_METHOD in ['21','22','23','24','25','2A','2B','2C','2D','28','81']"

    df['ADM_TYPE'] = '' # make empty column 
    # fill columns with 
    df.loc[df.query(elec_query).index, 'ADM_TYPE'] = 'Elective'
    df.loc[df.query(nonelec_query).index, 'ADM_TYPE'] = 'Non-Elective'
    df.loc[df.query("SPELL_LOS < 1").index, 'ADM_TYPE'] = 'Day Case' # this is basic, actually should be something like if ADM_DTTM =! DIS_DTTM
    
    return df


