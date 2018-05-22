#### script provides class defintions for hospital data project.
# seperate scripts provided in F* files for now which are imported seperately.
import pandas as pd
from expected_file_structures import *

class hosp(object):
    """ Class to manage hospital data importing.
    Input: name, string, for all file prefixs.
    """
    def __init__(self,name):
        print('-'*40)
        print('Created hosp class instance: ', name)
        print('-'*40)
        # make dict for passing down class heirarcy
        meta_info = {
        '_name': name,
        '_pathCLEAN': './../../3_Data/processed/',
        '_pathOUTPUT': './../../6_Outputs/',
        '_dataRAW_expected_dtypes':dataRAW_expected_dtypes,
        '_dataRAW_expected_cols':dataRAW_expected_cols,
        '_dataframes_list':dataframes_list
        }

        # import expected file structure data
        # dataRAW_expected_dtypes #dict of cols:dtypes
        # list(dataRAW_expected_dtypes.keys()) #list columns of above
        # dataframes_list # list of possible dataframes


        self._unpack_meta(meta_info)

        #### instantiate class heirarcy
        self.ioED = ioED(meta_info)
        self.ioIP = ioIP(meta_info)
        self.pat = pat(meta_info)
        self.day = day(meta_info)
        self.week = week(meta_info)
        #self.mon = mon(meta_info)


    def _unpack_meta(self, meta_info):
        """ place each meta item as attribute of class """
        for key, value in meta_info.items():
            setattr(self, key, value)

    def _loadPKL(self, path_to,attribute_name):
        """ find clean pkl file and load
        input
        path_to: str, location of pkl
        attribute_name: str, name to store under
        """
        x = pd.read_pickle(path_to) # read pkl to df
        setattr(self, attribute_name, x) # save to attribute

    def _searchFILE(self, path, filenames):
        """
        looks for filelist matching (filename), in folder (path), if not print not found. Retunr list of founds.
        Input
        path: str, path to folder
        filenames: list of str, filenames to find
        """
        from os.path import exists
        avail_files = []
        for i in filenames:
            if exists(path + i):
                print('Found: ',i)
                avail_files.append(path+i)
            else:
                print('Missing: ', i)

        return avail_files

    def _loadCLEAN(self,select_period = None):
        ## look for filelist, if present load, if not print not found. Retunr list of founds.

        #generate possible filelist
        poss_files = []
        for j in self._dataframes_list:
            f1 = self._name + j[7:] + '.pkl'
            if select_period == None:
                poss_files.append(f1) # if no period selected will choose load all files into class that called
            elif select_period in f1:
                poss_files.append(f1) # if select_period specified will only add files to poss_files if contains the string. Used for .pat .day .week .mon loading.



        files = self._searchFILE(self._pathCLEAN,poss_files)
        #call load on list that is retuned
        for i in files:
            # get attribute name 'ED' or 'IP' from filename
            attrib_name = i.split('/')[-1].split('.')[0][len(self._name):-len(self._period)]
            attrib_name = '_'+ attrib_name
            # load data and assign to attribute
            self._loadPKL(i,attrib_name)

    def _loadRAW(self, select_period=None):
        ## look for filelist, if present load, if not print not found. Retunr list of founds.

        #generate possible filelist
        poss_files = []
        for j in self._dataframes_list:
            f1 = self._name + j[7:] + '.pkl'
            if select_period == None:
                poss_files.append(f1) # if no period selected will choose load all files into class that called
            elif select_period in f1:
                poss_files.append(f1) # if select_period specified will only add files to poss_files if contains the string. Used for .pat .day .week .mon loading.

        self._pathRAW = self._pathCLEAN + 'RAW/'
        files = self._searchFILE(self._pathRAW,poss_files)
        #call load on list that is retuned
        for i in files:
            # get attribute name 'ED' or 'IP' from filename
            attrib_name = i.split('/')[-1].split('.')[0][len(self._name):-len(self._period)]
            attrib_name = '_'+ attrib_name
            # load data and assign to attribute
            self._loadPKL(i,attrib_name)

    def _searchATTRIBUTE(self):
        attribute_list = []
        for i in self._dataframes_list:
            if hasattr(self, i):
                attribute_list.append(i)
        return attribute_list

    def _savePKL(self, path, attribute_list):
        """
        save dfs as pkls given list of attributes and path
        """
        for i in attribute_list:
            df = getattr(self,i)
            dt_period = i[7:] # get EDpat, IPday part of name
            fullfilepath = path + self._name + dt_period + '.pkl'
            df.to_pickle(fullfilepath)
            print(self._name + dt_period + '.pkl')

    def get_pathCLEAN(self):
        return self._pathCLEAN

    def status(self):
        """
        Method to print details about class instance.
        """
        print(40*'-')
        print('Name of data: ' + self._name)
        print()
        print('Datas currently loaded:')
        for i in self._dataframes_list:
            present = check_presence_df(self,i)
            if present == True:
                print(i)
        return



    def __str__(self):
        return 'info about class instance'

class ioED(hosp):
    """ Tools for io of ED data.
    Workflow:
    1) import hosp csv with: load_hosp_csv
    2) use tools/manually transform df to standard columns types (use checks method).
    3) create daily and with:
    4) save as RAW to stage changes at any time: saveRAWasRAW
    5) once cleaned: saveRAWasCLEAN (files will then autoload in other parts of hospital class)
    """
    def __init__(self, meta_info):
        self._unpack_meta(meta_info)
        self._location = 'ED'
        pass

    def loadCLEAN(self):
        self._loadCLEAN()

    def loadRAW(self):
        self._loadRAW()

    def saveRAWasRAW(self):
        """ save all raw files in memory as .pkl in the processed folder specified """
        self._dataR_EDpat = self._dataRAW #move patinet lvl data to this attribute for saving
        print('-'*40)
        print('Saving RAW as pkls in RAW folder...')
        raw_df_list = self._searchATTRIBUTE()
        if len(raw_df_list) == 0:
            print('No RAW files to save.')
        else:
            path = self._pathCLEAN + 'RAW/'
            self._savePKL(path,raw_df_list)

        print('Save complete.')
        return

    def saveRAWasCLEAN(self):
        """ save all raw files in memory as .pkl in the processed folder specified. Do once happy that data is all clean. """
        self._dataR_EDpat = self._dataRAW #move patinet lvl data to this attribute for saving
        print('-'*40)
        print('Saving RAW as pkls in CLEAN folder...')
        raw_df_list = self._searchATTRIBUTE()
        raw_df_list.remove('_dataRAW')
        if len(raw_df_list) == 0:
            print('No RAW files to save.')
        else:
            path = self._pathCLEAN
            self._savePKL(path,raw_df_list)

        print('Save complete.')
        return





######################################################
#### seperate functions ####
######################################################





def check_presence_df(x,df_name):
    """
    check if dataframe present
    """
    if hasattr(x, df_name):
        present = True
    else:
        present = False
    return present









def create_dailyED(x):
    """
    create new df at daily level from patient level.

    input: df, x
    output: df, dailyED
    """
    ##### First need to calculate waiting times (split over days for calc of how mnay ED waiting minutes there were)
    ##### possible that should move this upstream at later stage so available to pat level df.
    df = x

    def minutes_in_ED_today(x):
        if x.arrive_datetime.date() == x.depart_datetime.date():
            y = x.waiting_time
        else:
            y = (24*60) - (x.arrive_datetime.hour*60 + x.arrive_datetime.minute)
        return(y)

    print(df.columns)

    df['minutes_today'] = df.apply(minutes_in_ED_today,axis=1)

    def minutes_in_ED_tomo(x):
        if x.arrive_datetime.date() != x.depart_datetime.date():
            y = x.depart_datetime.minute + x.depart_datetime.hour*60
        else:
            y = 0
        return(y)

    df['minutes_tomo'] = df.apply(minutes_in_ED_tomo,axis=1)

    # check total waiting times match up
    if df[['minutes_tomo','minutes_today']].sum().sum() != df['waiting_time'].sum():
        print('WARNING: problem with aggregating minutes over days.')
        print(df[['minutes_tomo','minutes_today']].sum().sum())
        print(df['waiting_time'].sum())

    # calc: arrive numbers, median age

    df_gb = df[['arrive_datetime','age','minutes_today']]

    agg_dic = {'arrive_datetime':'count'
                ,'age':'median'
              ,'minutes_today':'sum'
              }

    daily1 = df_gb.groupby(by=[df_gb['arrive_datetime'].dt.date]).agg(agg_dic)

    #calc: discharges + admissions
    df_gb = df[['depart_datetime','age','adm_flag','minutes_tomo']]

    agg_dic = {'depart_datetime':'count'
               ,'adm_flag':'sum'
               ,'minutes_tomo':'sum'
                }

    daily2 = df_gb.groupby(by=[df_gb['depart_datetime'].dt.date]).agg(agg_dic)
    #daily2.head()

    #calc: breaches counts - this should be lifted updwards!
    df['breach_datetime'] = df.arrive_datetime + pd.Timedelta('4 hour')

    df_gb = df[['breach_datetime','breach_flag']]

    agg_dic = {'breach_flag':'sum'
                }

    daily3 = df_gb.groupby(by=[df_gb['breach_datetime'].dt.date]).agg(agg_dic)
    #daily3.head(5)

    #cal total number of minutes waiting each day?

    # merge each of daily dfs created

    daily1.shape

    daily2.shape

    daily = pd.merge(daily1,daily2,left_index=True, right_index=True,how='outer')
    daily.shape

    daily3.shape

    daily = pd.merge(daily,daily3,left_index=True,right_index=True,how='outer')
    daily.shape


    # make total minutes used in ED column
    daily['minutes_used'] = daily.minutes_today + daily.minutes_tomo
    daily.shape
    daily.drop(['minutes_today','minutes_tomo'],axis=1,inplace=True)
    daily.shape

    # rename columns sensibly
    #daily.columns
    daily.rename(columns={'arrive_datetime':'arrivals','depart_datetime':'discharges','age':'age_median',
                         'adm_flag':'admissions','breach_flag':'breaches'},inplace=True)
    daily.head()
    daily['mean_patient_minutes'] = daily.minutes_used/daily.arrivals

    #### !! print wanring if we are missing dates, check that in reshape daily df was correct size
    # check for missing dates
    daily.shape
    daily.reindex().shape
    daily.isnull().sum()

    # create other vars of interest from daily
    daily['conversion_ratio'] = daily.admissions/daily.arrivals
    daily['breaches_perc'] = daily.breaches/daily.arrivals

    # create cols of dow,month,year
    daily['date'] = daily.index

    daily['year'] = daily.date.apply(lambda x: x.year)

    daily['month'] = daily.date.apply(lambda x: x.month)

    #### workaround for dayofweek as date col is a
    daily['dayofweek'] = pd.to_datetime(daily.date.values).dayofweek

    daily['weekday_name'] = pd.to_datetime(daily.date.values).weekday_name

    daily['date'] = pd.to_datetime(daily.index)

    #### add prefix ED_ to columns
    prefix_cols(daily,'ED_')

    return daily

def prefix_cols(x,prefix):
    """ adds string prefix to all col names inplace"""
    for i in x.columns:
        x.rename(columns={i:prefix + i},inplace=True)
