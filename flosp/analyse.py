import pandas as pd
import numpy as np
import warnings

from flosp import basic_tools
from flosp import _core
from flosp import _expected_file_structures
from flosp import _plotting

class data():
    """ class to store all data and meta """

    def __init__(self,name,save_path,valid_years):
        self.name = name
        self.save_path = _core.path_add_child_structure(save_path, self.name)
        self.valid_years = valid_years



class analyse():
    """ Class to manage hospital data importing.
    Input:
    name, str, name for class (will be used in filename saving.)
    save_path, str, e.g. './../../3_Data/' (must use parent folder).
    valid_years, list, a list of the years (ints) for which there are complete records.
    """
    #from flosp.ED import ED
    def __init__(self,name,save_path,valid_years):
        self.data = data(name,save_path,valid_years)
        self.ED = ED(self.data)
        self.IP = IP(self.data)
        self.load_processed_data()

    def set_valid_years(self, valid_years):
        """ Set list of valid years to complete any analysis over. """
        self.data.valid_years = valid_years
        return

    def set_save_path(self,save_path):
        """sets path for saving any data files to. Use the parent folder, all data will be automatically placed within a 'procesed/name/' folder.'
        Input,str, e.g. './../../3_Data/'
        """
        self.data.save_path = _core.path_add_child_structure(save_path, self.data.name)
        return

    def load_processed_data(self):
        """
        finds and imports data that has been cleaned with .name attribute of the class you are calling from.
        """
        _core.message('attemping to import processed dataframes.')

        possible_pkls = _expected_file_structures.possible_pkls_list # get list of possible pkl files

        for i in possible_pkls:
            search_filename = self.data.name + i #add the class instance name to file structure.
            exists = _core.search_for_pkl(self.data.save_path,search_filename) # find if file exists

            if exists == True:
                full_path = self.data.save_path + search_filename
                attribute_name = i[:-4]
                setattr(self.data, attribute_name , pd.read_pickle(full_path) ) #remove .pkl
        return

    def create_status_hourly(self):
        """create df of hourly hospital status from spell and ED data"""
        #### create date range for new df
        start = max(self.data.ED['arrive_datetime'].min(),self.data.IPspell['adm_datetime'].min()).round('D')
        end = max(self.data.ED['arrive_datetime'].max(),self.data.IPspell['adm_datetime'].max()).round('D')
        print('start date:', start)
        print('end date:', end)

        #### Get IP occ
        occIP = basic_tools.timeseries.create_timeseries_from_events(self.data.IPspell,'adm_datetime','dis_datetime',col_to_split='admission_type',start=start,end=end,freq='H')
        print(occIP.columns)
        # rename cols
        for i in occIP.columns:
            print(i)
            #i = str(i)
            occIP.rename(columns={i:'IPocc_' + str(i)},inplace=True)

        # make agg cols
        occIP['IPocc_total'] = occIP.sum(axis=1)
        occIP['IPocc_elec_nonelec'] = occIP[['IPocc_NonElective','IPocc_Elective']].sum(axis=1)

        #### Get ED occ
        #total + those who will be admitted
        occED = basic_tools.timeseries.create_timeseries_from_events(self.data.ED,'arrive_datetime','depart_datetime',col_to_split='adm_flag',start=start,end=end,freq='H')

        occED['EDocc_total'] = occED.sum(axis=1) # make agg col
        occED.rename(columns={0:'EDocc_nonadmit',1:'EDocc_admit'},inplace=True) # rename cols

        # those currently awaiting admission
        occED2 = basic_tools.timeseries.create_timeseries_from_events(self.data.ED,'first_adm_request_datetime','depart_datetime',start=start,end=end,freq='H')
        occED2.rename(columns={'count_all':'EDocc_awaitingadm'},inplace=True) #rename cols

        occED = occED.merge(occED2,right_index=True,left_index=True)

        # those who will breach
        occED3 = basic_tools.timeseries.create_timeseries_from_events(self.data.ED,'arrive_datetime','depart_datetime',col_to_split='breach_flag',start=start,end=end,freq='H')
        occED3.rename(columns={0:'EDocc_nonbreach',1:'EDocc_breach'},inplace=True)

        occED = occED.merge(occED3,right_index=True,left_index=True)

        ####merge all occupnacy
        mast = occED.merge(occIP,left_index=True,right_index=True)

        #### get IP arrivals/dis
        #arrivals
        query_list = ['admission_type == "Non-Elective"','admission_type == "Day Case"','admission_type == "Elective"']
        label_list = ['_nonelec','_daycase','_elective']

        adm_counts = get_adm_counts_dfs(self.data.IPspell,'adm',query_list,label_list,'IPadm')

        mast = mast.merge(pd.DataFrame(adm_counts),left_index=True,right_index=True,how='outer')

        #discharges
        query_list = ['admission_type == "Non-Elective"','admission_type == "Day Case"','admission_type == "Elective"']
        label_list = ['_nonelec','_daycase','_elective']

        dis_counts = get_adm_counts_dfs(self.data.IPspell,'dis',query_list,label_list,'IPdis')
        mast = mast.merge(pd.DataFrame(dis_counts),left_index=True,right_index=True,how='outer')

        mast['IPadm_elec_nonelec'] = mast.IPadm_elective + mast.IPadm_nonelec
        mast['IPdis_elec_nonelec'] = mast.IPdis_elective + mast.IPdis_nonelec

        #### get ED arrivals/dis
        #arrivals
        query_list = ['breach_flag == 1','adm_flag == 1']
        label_list = ['_breach','_adm']

        att_counts = get_adm_counts_dfs(self.data.ED,'arrive',query_list,label_list,'EDarrive')
        mast = mast.merge(pd.DataFrame(att_counts),left_index=True,right_index=True,how='outer')

        #departures
        query_list = ['breach_flag == 1','adm_flag == 1']
        label_list = ['_breach','_adm']

        dep_counts = get_adm_counts_dfs(self.data.ED,'depart',query_list,label_list,'EDdepart')

        mast = mast.merge(pd.DataFrame(dep_counts),left_index=True,right_index=True,how='outer')

        mast.fillna(0,inplace=True)

        #### possibly need to add something to make index continous here.
        #new_index = pd.date_range(start=start,end=end,freq='H')
        #hh.data.hourly.reindex(new_index)

        #### create datetime columns information
        mast['datetime'] = mast.index
        mast = basic_tools.make_callender_columns(mast,'datetime','dt')

        #### save new hourly df out
        self.data.HOURLY = mast

        _core.savePKL(self.data.HOURLY,self.data.save_path,self.data.name + 'HOURLY.pkl')

        return

    def create_status_daily(self):
        """creates a df with daily status of the hopsital """
        #### make daily summary from hourly status
        occH = self.data.HOURLY.copy() # copy requiered as oterhwise edits go back to .data.HOURLY!
        # make copies of cols for max/mean groupings
        occH['IPocc_total2'] = occH['IPocc_total']
        occH['IPocc_elec_nonelec2'] = occH['IPocc_elec_nonelec']
        #define aggregations for each col
        aggs={'EDarrive':'sum',
              'IPadm_elec_nonelec':'sum',
              'IPdis_elec_nonelec':'sum',
              'IPocc_total':'mean',
              'IPocc_total2':'max',
              'IPocc_elec_nonelec':'mean',
              'IPocc_elec_nonelec2':'max'
             }
        #group cols
        occD = occH.groupby(['dt_year','dt_month','dt_day']).agg(aggs).reset_index()

        occD['IPadm_minus_dis_elec_nonelec'] = occD.IPadm_elec_nonelec - occD.IPdis_elec_nonelec

        occD.rename(columns={'IPocc_total2':'IPocc_total_MAX',
        'IPocc_total':'IPocc_total_MEAN',
                             'IPocc_elec_nonelec':'IPocc_elec_nonelec_MEAN',
                            'IPocc_elec_nonelec2':'IPocc_elec_nonelec_MAX'},inplace=True)

        daily_IP1 = occD.copy()

        #### make pre12hours discharge summaries
        daily_IP2 = self.data.IPspell.query('dis_hour <= 12 & admission_type != "Day Case"').groupby(['dis_year','dis_month','dis_day']).count()['hosp_patid'].reset_index()

        daily_IP2.rename(columns={'hosp_patid':'IPdis_pre12_elec_nonelec','dis_year':'dt_year','dis_month':'dt_month','dis_day':'dt_day'},inplace=True)

        #### make ED daily counts
        aggs={'hosp_patid':'count','breach_flag':'sum','adm_flag':'sum'}
        daily_ed = self.data.ED.groupby(['arrive_year','arrive_month','arrive_day']).agg(aggs).reset_index()

        daily_ed.rename(columns={'arrive_year':'dt_year',
        'arrive_month':'dt_month',
        'arrive_day':'dt_day',
        'hosp_patid':'ED_attendances',
        'breach_flag':'ED_breaches',
        'adm_flag':'ED_admissions'},inplace=True)

        #### merge the three df created
        mast = daily_IP1.merge(daily_IP2,on=['dt_year','dt_month','dt_day'])
        mast = daily_ed.merge(mast,on=['dt_year','dt_month','dt_day'])

        #### amke timeseries index
        mast['dt'] = mast.apply(lambda x : pd.datetime(int(x.dt_year),int(x.dt_month),int(x.dt_day)) ,axis=1)

        mast.set_index('dt',inplace=True)

        #### save data out
        self.data.DAILY = mast
        _core.savePKL(self.data.DAILY,self.data.save_path,self.data.name + 'DAILY.pkl')
        return

class ED():
    """
    doc here
    """
    def __init__(self,data):
        self._data = data
        self.plot = _plotting.plotED(data)

    def filter():
        """ """
        return

    def auto_plot():
        """ calls and attempts all the known plots. Messages if there is an error creating any of them. """

        return

class IP():
    """ doc here """
    def __init__(self,data):
        self._data = data
        pass

def count_numbers_byhour(df,prefix,new_col='counts'):
    """ makes counts of numbers of events by hour using groupby.
    inputs:
    df, df to make counts on
    prefix, str, prefix of column names for year, month, day, hour.
    new_col, str, new col name

    output: df with counts in single column and datetime index to hour.

    """
    adm_counts = df.groupby([prefix+'_year',prefix+'_month',prefix+'_day',prefix+'_hour']).count()['hosp_patid'].reset_index()

    adm_counts.rename(columns={'hosp_patid':new_col},inplace=True)

    adm_counts = adm_counts.astype('int') # inc as error occuring because sometimes float

    def make_datetime(x):
        y = pd.datetime(x[prefix+'_year'],x[prefix+'_month'],x[prefix+'_day'],x[prefix+'_hour'])
        return(y)

    adm_counts['datetime'] = adm_counts.apply(make_datetime,axis=1)

    adm_counts.set_index('datetime',inplace=True)

    return(adm_counts)

def get_adm_counts_dfs(df,prefix,query_list,label_list,new_col):
    """
    Function creates a df with counts of patients arriving each hour
    """
    counts = count_numbers_byhour(df,prefix,new_col)

    for i in np.arange(len(label_list)):

        #### create new counts df of sub groups
        counts2 = count_numbers_byhour(df.query(query_list[i]),prefix,new_col+label_list[i])
        # merge to large one
        counts = counts.merge(pd.DataFrame(counts2[new_col+label_list[i]]),left_index=True,right_index=True,how='outer')

    counts.drop([i for i in counts.columns if (i.startswith(prefix))],inplace=True,axis=1) # get only count columns
    return(counts)
