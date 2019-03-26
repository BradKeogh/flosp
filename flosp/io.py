import pandas as pd
from flosp import basic_tools
from flosp import core

class IO:
    """ Class to take csv data and produce cleaned DataFrame 
    - load csv:
            - enforce data type conversion here with pd import
            - ensure columns needed exist but allow other columns too
    - make callender columns required for arrive and depart
    - make wait time columns
    - make breach columns
    - make age group columns
    - save data to pkl files

    - checks for:
        - all columns present
        - datatypes okay
        - datetime format okay (multiple columns and rows of file - to check format hasnt changed)
        - erroneus data columns (i.e. datetimes do not exist yet or 1970, missing values in crucial columns)


    Further considerations:
    - how to deal with CDU in ED
    - how to deal with GP in ED

    """
    def __init__(self, path_to_file, patient_record_type, data , metadata):
        print('IO class called.')
        #### make data attributes available
        self.path_to_file = path_to_file
        self.patient_record_type = patient_record_type
        self.RawName = 'Raw' + patient_record_type
        self.data = data
        self.metadata = metadata
        setattr(self.metadata, 'PRType', getattr(self.metadata, patient_record_type)) # attribute set for access to patient_record_type
        # metadata within methods. e.g. self.metadata.ED. becomes self.metadata.PRType 
        # NOTE: FEELS LIKE A BODGE.

        #### load csv and call methods to prcoess data
        self.load_csv()
        self.parse_datetimes()
        
        self.make_callender_columns()
        self.make_age_group_column()
        # some conversions only for ED
        if patient_record_type == 'ED':            
            self.make_wait_columns_ED()
            self.make_breach_columns()
        # some converions only for IP
        if patient_record_type == 'IP':
            self.make_simple_adm_method_column()
        

        #### save clean data
        setattr(self.data, patient_record_type, self.RawData) #in class
        # as pickle file
        self.save_clean_to_pickle()
        
        return print('Import completed.')

    def load_csv(self):
        """ loads a csv and assigns to an attribute

        - enforce data types upon loading here in future 
        """
        # _core.message('importing ED csv data to RAW dataframe')
        df = pd.read_csv(
                self.path_to_file,
                low_memory=True,
                dtype=self.metadata.PRType.dataRAW_expected_col_dtypes
                )

        setattr(self.data, self.RawName, df)
        # setattr(self, self.RawNam , df) # set data to attribute for easy access
        self.RawData = df
        return


    def parse_datetimes(self):
        """ Takes list of columns and parses each one as datetime with datetime specified in setup.py file.
        Assigns new dataframe to .data.* attribute. 
        input: list of columns
        """
        cols_to_parse = self.metadata.PRType.dataRAW_expected_datetime_cols
        # df = getattr(self.data, self.RawName)
        df = self.RawData
        for column in cols_to_parse:
                print(column)
                df[column] = pd.to_datetime(df[column], format = self.metadata.PRType.DATETIME_FORMAT) # change format to input from metadata

        self.RawData = df
        # setattr(self.data, self.RawName, df)
        return

    def make_callender_columns(self):
        """
        create additional arrival and depart columns with: arrive_hour,depart_dayofweek etc.
        """
        # df = getattr(self.data, self.RawName)
        first_prefix = get_prefix_to_column(self.metadata.PRType.dataRAW_first_datetime_col)
        last_prefix = get_prefix_to_column(self.metadata.PRType.dataRAW_second_datetime_col)
        self.RawData = basic_tools.make_callender_columns(self.RawData, self.metadata.PRType.dataRAW_first_datetime_col,first_prefix)
        self.RawData = basic_tools.make_callender_columns(self.RawData, self.metadata.PRType.dataRAW_second_datetime_col,last_prefix)
        # setattr(self.data, self.RawName, df)
        return

    def make_wait_columns_ED(self):
        """
        create additional columns with waiting times in minutes. Requires standard column names to generate.
        """
        # df = getattr(self.data, self.RawName)
        self.RawData = core.make_wait_columns_ED(self.RawData)
        # setattr(self.data, self.RawName, df)
        return

    def make_breach_columns(self):
        """
        make new columns of breach flag and breach datetime. Requires: waiting_time column in minutes.
        """
        df = self.RawData
        df['BREACH_FLAG'] = (df['waiting_time'] > 4*60).astype(int)
        df['breach_datetime'] = df['ARRIVAL_DTTM'] + pd.Timedelta(4,unit='h')
        self.RawData = df
        # setattr(self.data, self.RawName, df)
        return

    def make_age_group_column(self, bins = None, labels= None):
        """ add additional column called age_group.
        input:
        bins, lst of int, bin edges e.g. [-1, 18, 65,200]
        labels, lst of str, labels for groups e.g. ["0-17", "18-64", "65+"]
        """
        # df = getattr(self.data, self.RawName)
        df = self.RawData
        ### use standard bins/labels if none provided
        if (bins == None) & (labels == None):
            bins = [-1, 18, 65,200]
            labels = ["0-17", "18-64", "65+"]

        df['age_group'] = pd.cut(df.AGE_AT_ARRIVAL, bins=bins, right=False, labels=labels)

        self.RawData = df
        # setattr(self.data, self.RawName, df)
        return

    def make_simple_adm_method_column(self):
        """ Makes new column with 4 catagories of admission method. Based on the Admission method column.
        """
        df = self.RawData

        df['ADM_METHOD_simple'] = 'other'

        query = df.query("ADM_METHOD in ['21','2A']")
        df.loc[query.index,'ADM_METHOD_simple'] = 'ED'

        query = df.query("ADM_METHOD in ['31','32']")
        df.loc[query.index,'ADM_METHOD_simple'] = 'Maternity'

        query = df.query("ADM_METHOD in ['22']")
        df.loc[query.index,'ADM_METHOD_simple'] = 'GP'
        
        self.RawData = df

        return

    def save_clean_to_pickle(self):
        """ save raw df as .pkl file in the results directory specified in setup.py.
        """
        core.path_backslash_check(self.metadata.RESULTS_SAVE_PATH)
        core.save_pickle(self.RawData, self.metadata.RESULTS_SAVE_PATH + 'processed/', self.patient_record_type)
        return

def get_prefix_to_column(string):
    """takes string of column name, returns first characters before underscore """
    first_chars = string.split('_')[0]
    return(first_chars)