import pandas as pd
import numpy as np
import warnings

from flosp import basic_tools
from flosp import _core
from flosp import _expected_file_structures

class ioIP:
    """ ioIP is a tool for easy importing and cleaning of ED data. It can also enforce specific formatting which will allow the use of analyse class for standard analysis.
    """
    def __init__(self,name,save_path,stay='fce'):
        self.name = name
        self._stay = stay
        self.set_save_path(save_path)

    def set_save_path(self,save_path):
        """sets path for saving any data files to. Use the parent folder, all data will be automatically placed within a 'procesed/classname/' folder.
         Input,str, e.g. './../../3_Data/' """
        save_path = _core.path_backslash_check(save_path) #ensure that path has / at end
        self.save_path = save_path + 'processed/' + self.name + '/' #make save_path an attribute
        return

    def load_csv(self,path_to,nrows=None):
        _core.message('importing ED csv data to RAW dataframe')
        df = pd.read_csv(path_to, low_memory=False,nrows=nrows)
        self._dataRAW = df
        return



    def small_sample(self, size = 1000):
        """
        Take a sample of df. Used so that can run development quickly. DO NOT USE IN FINAL DATA IMPORT!!!
        takes head an tail of df.
        Input: size, int, size of sample to be returned.
        """
        size_half = int(size/2)
        df = pd.concat([self._dataRAW.head(size_half), self._dataRAW.tail(size_half)])
        self._dataRAW = df
        warnings.warn('Using small_sample removes rows of good data. DO NOT USE IN FINAL DATA IMPORT!!')
        return

    def autoclean(self):
        """
        Attempts to clean and force data structure. Using order:
        - map data columns to new values
        - ensure columns are of expected formats, if not attempt conversions
        - convert all datetimes
        - clean column names (in case has additional columns?)
        """
        #! implement method as series of other method calls...use jupyter notebook as guide for order.
        self.make_callender_columns()
        self.make_wait_columns()
        self.make_breach_columns()
        self.make_age_group_column()
        return

    def map_columns(self, col_mapping, tidy_up_cols = False):
        """
        map columns to standard names using user-defined dictionary
        """
        if tidy_up_cols == True:
            _core.message('tidying column headers')
            self._dataRAW = basic_tools.tidy_column_heads(self._dataRAW)

        _core.message('mapping column names')
        self._dataRAW.rename(columns = col_mapping,inplace=True)
        self._dataRAW = self._dataRAW[list(col_mapping.values())]
        #! insert exception here for checking that i'm not just deleting a load of columns
        return

    def convert_cols_datetime(self,dt_format, col_names = None):
        """
        convert selected columns to datetime format.
        Input:
        dt_format, str, format of datetime columns, e.g. "%d/%m/%Y %H:%M"
        col_list, list, list of columns to ensure are datetime format.
        """
        warnings.warn("Datetime conversion can be problemtic. Make sure you have used the correct datetime string format for each column. You can call this method multiple times with different 'datetime formats' & 'list of columns' to convert if neccessary.")

        self._dataRAW = basic_tools.convert_cols_datetime(self._dataRAW,dt_format, col_names)
        return

    def make_callender_columns(self):
        """
        create additional arrival and depart columns with: arrive_hour,depart_dayofweek etc.
        """
        self._dataRAW = basic_tools.make_callender_columns(self._dataRAW,'adm_datetime','adm')
        self._dataRAW = basic_tools.make_callender_columns(self._dataRAW,'dis_datetime','dis')
        return



    def make_age_group_column(self, bins = None, labels= None):
        """ add additional column called age_group.
        input:
        bins, lst of int, bin edges e.g. [-1, 18, 65,200]
        labels, lst of str, labels for groups e.g. ["0-17", "18-64", "65+"]
        """
        df = self._dataRAW

        ### use standard bins/labels if none provided
        if (bins == None) & (labels == None):
            bins = [-1, 18, 65,200]
            labels = ["0-17", "18-64", "65+"]

        df['age_group'] = pd.cut(df.age, bins=bins, right=False, labels=labels)

        self._dataRAW = df
        return


    def create_datetime_from_time(self,time_col,date_col,new_col,auto_correct=True):
        """
        produce a new column in datetime format from two columns in date and time column.
        """
        if date_col not in self._dataRAW.columns:
            warnings.warn('date column passed does not exist. Defaulting to use "arrive_datetime". NOTE: this will generate arrive_date column.')
            self._dataRAW['arrive_date'] = self._dataRAW['arrive_datetime'].dt.date
            date_col = 'arrive_date'

        self._dataRAW = basic_tools.create_datetime_from_time(self._dataRAW,time_col,date_col,new_col)
        return



    def get_EDraw(self):
        """ retrieve raw ED data, returns df """
        # possible selection wiht keyword?
        return self._dataRAW

    def replace_EDraw(self, x):
        """ replace EDraw data with new df (input) """
        self._dataRAW = x
        return

    def saveRAWasCLEAN(self,path=None):
        """ save raw df as .pkl file in the path specified.
        Use once happy that data is all clean.
        Can specify path, but best to leave blank to allow standard naming.
        """
        if path == None:
            path = self.save_path # if no path given apply standard path naming.
        _core.savePKL(self._dataRAW, path, self.name + 'IP' + self._stay)

        if hasattr(self,'_dataRAWspell') == True:
            _core.savePKL(self._dataRAWspell, path, self.name + 'IP' + 'spell')
        return

    def saveRAWasRAW(self,path=None):
        """ save raw df as .pkl file.
        Can specify path, but best to leave blank to allow standard naming
        Use once happy that data is all clean.
        """
        if path == None:
            path = self.save_path + 'RAW/' # if no path given apply standard path naming.
        _core.savePKL(self._dataRAW, path, self.name + 'IP' + self._stay)

        if hasattr(self,'_dataRAWspell') == True:
            _core.savePKL(self._dataRAWspell, path, self.name + 'IP' + 'spell')
        return

    def loadPKLasRAW(self, path = None ,filename = None):
        """
        load any pkl file as raw data for prcessing again.
        input:
        path, str, folder to pkl
        filename, str, string of pkl file.
        """
        if path == None:
            path = self.save_path # if no path given apply standard path naming.
        if filename == None:
            filename = self.name + 'IP' + self._stay

        self._dataRAW = _core.loadPKL(path ,filename)

        return

    def create_spell_df(self):
        """ create spell records from fce or ward level record: i.e. each line is a seperate fce or ward stay. in new spell level df, i.e. each line is a patient spell/hospital stay.
        """
        _core.message('Creating spell dataframe...could take 10minutes or more depending on size of data set.')
        self._dataRAWspell = _core.create_spell_from_multimove(self._dataRAW)
        return
