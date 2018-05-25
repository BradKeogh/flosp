import pandas as pd
import numpy as np
import warnings

from flosp import basic_tools
from flosp import _core
from flosp import _expected_file_structures

class ioED:
    """
    ioED is a tool for easy importing and cleaning of ED data. It can also enforce specific formatting which will allow the use of analyse class for standard analysis.

    Workflow:
    1) load_csv: import ED csv:
    2) small_sample: optional to reduce dataset for quick movement through workflow.
    3) autoclean: uses methods that are all available to user but attempts them sequentially.
        - errors wil prompt you to adress issues manually.
    2) use tools/manually transform df to standard columns types (use checks method).
    3) create daily and with:
    4) save as RAW to stage changes at any time: saveRAWasRAW
    5) once cleaned: saveRAWasCLEAN (files will then autoload in other parts of hospital class)
    """
    #from flosp.tools_basic import basic1
    #print(basic1())
    #as _core

    def __init__(self,name,save_path):
        self.name = name
        self.set_save_path(save_path)

    def set_save_path(self,save_path):
        "sets path for saving any data files to. Input,str, e.g. './../../3_Data/' "
        save_path = _core.path_backslash_check(save_path) #ensure that path has / at end
        self.save_path = save_path + self.name + '/' #make save_path an attribute
        return

    def call_test(self):
        x = basic_tools.test_fun()
        print(x)
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
        self._dataRAW = basic_tools.make_callender_columns(self._dataRAW,'arrive_datetime','arrive')
        self._dataRAW = basic_tools.make_callender_columns(self._dataRAW,'depart_datetime','depart')
        return

    def make_wait_columns(self):
        """
        create additional columns with waiting times in minutes. Requires standard column names to generate.
        """
        self._dataRAW = _core.make_wait_columns(self._dataRAW)
        return

    def make_breach_columns(self):
        """
        make new columns of breach flag and breach datetime. Requires: waiting_time column in minutes.
        """
        import pandas as pd
        self._dataRAW['breach_flag'] = (self._dataRAW['waiting_time'] > 4*60).astype(int)
        self._dataRAW['breach_datetime'] = self._dataRAW['arrive_datetime'] + pd.Timedelta(4,unit='h')
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

    def run_tests(self):
        """
        Tests to see if raw data is in standard format.
        """
        # check all columns are in RAW df
        _core.message('Finding missing columns...','m')
        for i in _expected_file_structures.dataRAW_expected_cols:
            if i not in self._dataRAW.columns:
                #print missing column & mesaage comment
                print(i,'try using: ',_expected_file_structures.dataRAW_expected_cols[i])

        # check all column datatypes
        _core.message('Finding columns with wrong datatypes...','m')
        _core.check_column_dtypes(self._dataRAW,exp_dtype_dict = _expected_file_structures.dataRAW_expected_dtypes ,col_to_check = None)
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
        _core.savePKL(self._dataRAW, path, self.name + 'ED')
        return

    def saveRAWasRAW(self,path=None):
        """ save raw df as .pkl file.
        Can specify path, but best to leave blank to allow standard naming
        Use once happy that data is all clean.
        """
        if path == None:
            path = self.save_path + 'RAW/' # if no path given apply standard path naming.
        _core.savePKL(self._dataRAW, path, self.name + 'ED')
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
            filename = self.name + 'ED'

        self._dataRAW = _core.loadPKL(path ,filename)
        return
