from flosp.data import Data
from flosp.data import MetaData

class Interface:
    """ Class which contains all actions (methods) available to user.
    """


    def __init__(self,setup_file_path = './setup.py'):
        print('flosp started.')
        self.data = Data()
        self.metadata = MetaData(setup_file_path)
        #! Look for pkl files that already exist under folder naming convention and import.
    
    def load_dataED(self,path_to_file):
        """ Load csv data for ED
        patient record type, str, 'ED', 'IP' 
        """
        from flosp.io import IO
        IO(path_to_file, 'ED', self.data, self.metadata)
    
    def load_dataIP(self,path_to_file):
        """ Load csv data for ED
        patient record type, str, 'ED', 'IP' 
        """
        from flosp.io import IO
        IO(path_to_file, 'IP', self.data, self.metadata)

    def run_checks(self):
        """An output of current status of flosp analysis, including:
        - Prints current status of data 
        - Gives summary of errors
        """
        pass

    def make_new_tables(self):
        """Create all aggregate tables possible i.e. houlry and daily tables """
        pass

    def extract_data(self):
        """ extract dataframe for user manipulation """
        pass

    def plot(self):
        """ Plot all graphs and tables possible with current analysis """ 
        pass

