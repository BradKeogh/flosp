import pandas as pd

class IO:
    """ Class to take csv data and produce cleaned DataFrame 
    - load csv: 
            - enforce data type conversion here with pd import
            - ensure columns needed exist but allow other columns too
    - checks for:
            - all columns present
            - datatypes okay
            - datetime format okay (multiple columns and rows of file - to check format hasnt changed)
            - erroneus data columns (i.e. datetimes do not exist yet or 1970, missing values in crucial columns)
    - convert datetimes of each column required


    - make callender columns required for arrive and depart
    - make wait time columns
    - make breach columns
    - make age group columns

    - save data to pkl files

    Further considerations:
    - how to deal with CDU in ED
    - how to deal with GP in ED

    """
    def __init__(self,path_to_file,data,metadata):
        print('IO class called.')
        self.path_to_file = path_to_file
        self.data = data
        self.metadata = metadata

        self.load_csv(path_to_file,'RawED')
        self.parse_datetimes('RawED')
        return print('IO class instantiated.')

    def load_csv(self,path_to,data_name):
        """ loads a csv and assigns to an attribute

        - enforce data types upon loading here in future 
        """
        # _core.message('importing ED csv data to RAW dataframe')
        df = pd.read_csv(
                self.path_to_file,
                low_memory=True,
                dtype=self.metadata.ED.dataRAW_expected_col_dtypes
                )

        setattr(self.data, data_name, df)
        return


    def parse_datetimes(self, data_name):
        """ Takes list of columns and parses each one as datetime with datetime specified in setup.py file.
        Assigns new dataframe to .data.* attribute. 
        input: list of columns
        """
        cols_to_parse = self.metadata.ED.dataRAW_expected_datetime_cols
        df = getattr(self.data, data_name)
        for column in cols_to_parse:
                print(column)
                df[column] = pd.to_datetime(df[column], format = self.metadata.ED.DATETIME_FORMAT) # change format to input from metadata

        setattr(self.data, data_name, df)
        return

    