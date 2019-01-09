#### Base class

class Data:
    """
    class where all data is stored
    """
    def __init__(self):
        pass


#### Default data structures expected

class MetaData:
    """Import and store metadata for other modules to access."""


    def __init__(self,setup_file_path):
        self.SETUP_FILE_PATH = setup_file_path
        self.ED = LoadExpectedStructures('flosp.expected_structures.ED')
        # self.IP = LoadExpectedStructures('flosp.expected_structures.IP')
        self.load_metadata_from_setup_file()
        # self.load_expected_structures()
        #! auto-generate the new strings for file paths.

    def load_metadata_from_setup_file(self):
        """Take data from setup file and assign to current instance."""

        from example.setup import HOSPITAL_NAME, RESULTS_SAVE_PATH, ED_DATETIME_FORMAT

        self.HOSPITAL_NAME = HOSPITAL_NAME
        self.RESULTS_SAVE_PATH = RESULTS_SAVE_PATH
        setattr(self.ED, 'DATETIME_FORMAT', ED_DATETIME_FORMAT)
        # setattr(self.IP, 'DATETIME_FORMAT', IP_DATETIME_FORMAT)
        print('Imported setup.py sucessfully.')

    def load_expected_structures(self):
        """Load expected file structure requirements for use when importing files. 
        #!Expect to refactor with its own class to import similar things for ED and IP seperately.
        """
        import importlib
        ExpStructure = importlib.import_module('flosp.expected_structures.ED')



class LoadExpectedStructures:
    """ Class to load data from expected_structures folder.
    These are then used in data importing
    """


    def __init__(self,file_location):
        # from flosp.expected_structures.ED import dataRAW_expected_dtypes, dataRAW_expected_cols, dataRAW_expected_datetime_cols
        #! setattr(self.ED,dataRAW_expected_dtypes)
        import importlib
        ExpStructure = importlib.import_module(file_location)
        self.dataRAW_expected_col_dtypes = ExpStructure.dataRAW_expected_col_dtypes
        # self.dataRAW_expected_cols = ExpStructure.dataRAW_expected_cols
        self.dataRAW_expected_datetime_cols = ExpStructure.dataRAW_expected_datetime_cols
        print(ExpStructure)
        return