#### Base class

class Data:
    """
    class where all data is stored
    """
    def __init__(self):
        pass


#### Default data structures expected

class MetaData:
    """import and stores metadata for processing
    """
    def __init__(self,setup_file_path):
        self.setup_file_path = setup_file_path
        self.load_metadata_from_setup_file()
        # load data about expected file types

    def load_metadata_from_setup_file(self):
        from example.setup import HOSPITAL_NAME, RESULTS_SAVE_PATH, ED_DATETIME_FORMAT
        self.HOSPITAL_NAME = HOSPITAL_NAME
        self.RESULTS_SAVE_PATH = RESULTS_SAVE_PATH
        self.ED_DATETIME_FORMAT = ED_DATETIME_FORMAT
        print('Imported setup sucessfully.')

    def load_expected_structures(self):
        """Load expected file structures for imported files. 
        Expect to refactor with its own class to import similar things for ED and IP seperately.
        """ 
        from _expected_file_structures import dataRAW_expected_dtypes, dataRAW_expected_cols
        self.EDdataRAW_expected_dtypes = dataRAW_expected_dtypes
        self.EDdataRAW_expected_cols = dataRAW_expected_cols