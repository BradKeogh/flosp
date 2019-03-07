import pandas as pd
from flosp.data import Data
from flosp.data import MetaData
from flosp import core
from flosp.plotting import HistoricalPlotting,  WeeklyPlotting, PeriodPlotting

class Interface:
    """ Class which contains all actions (methods) available to user.
    """


    def __init__(self,setup_file_path = './setup.py'):
        """
        Decision made to enforce user specification of setup_file_path to avoid confusion incase working on mulitple sites (unpractical to have in same dir).
        """
        print('flosp started.')
        #### make data classes
        self.data = Data()
        self.metadata = MetaData(setup_file_path)
        #### import already processed data
        self.load_processed_data()
        return

    def load_processed_data(self):
        """
        # used in new implementation
        Finds pickle files that has been cleaned and saved in the 'processed' folder.
        If exist assigns to data class attribute.       
        """
        # core.message('attemping to import processed dataframes.')
        print('Loading processed data from pickles.')

        for filename in self.metadata.POSSIBLE_PICKLES_LIST:
            search_filepath = self.metadata.RESULTS_SAVE_PATH + 'processed/'
            exists = core.search_for_pkl(search_filepath, filename) # find if file exists

            if exists == True:
                full_path = search_filepath + filename
                attribute_name = filename[:-4]
                setattr(self.data, attribute_name , pd.read_pickle(full_path) ) #remove .pkl
        return
    
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
        """Create all aggregate tables possible i.e. hourly and daily tables """
        # aggregation module:
        from flosp.aggregation import Aggregate
        Aggregate(self.data,self.metadata)
        # create_hourly_table()
        # create_daily_table()
        pass

    def extract_data(self, name):
        """ extract a dataframe for user manipulation.
        returns dataframe. """
        assert hasattr(self.data,name) == True, "That data name does not exist." #check data attribute asked for exists
        df = getattr(self.data,name) # extract df
        return(df)

    def plot_historical(self, EDyears, IPyears, required_plot_no='all'):
        """ Plot all graphs and tables possible with current analysis.
        Input
        -----
        EDyears, list of int, contains each year that will be included in ED plots.
        IPyears, list of int, contains each year that will be included in IP plots.
        
        Ouput
        -----
        All plots saved to dir with corresponding tables in csv format.
        All figures saved in self.data. .

        """ 
        HistoricalPlotting(self.data, self.metadata, EDyears, IPyears, required_plot_no)
        return

    def plot_period(self, dt_start, dt_end, required_plot_no='all'):
        """ 
        Plot all graphs and tables possible with current analysis.
        Input
        -----
        start, datetime, start window for period of plotting.
        end, datetime, end of window for period of plotting. ]
        
        Output
        ------


        """ 
        PeriodPlotting(self.data, self.metadata, dt_start, dt_end, required_plot_no)
        return

    def plot_week(self, dt_weekstart, required_plot_no='all'):
        """ 
        Plot all graphs and tables possible with current analysis.
        Input
        -----
        start_week, datetime, start of window for plots.
        
        Output
        ------

        """ 
        WeeklyPlotting(self.data, self.metadata, dt_weekstart, required_plot_no)
        return

    def get_plot_list(self):
        """
        When called returns dataframe with full list of plots and their information.
        """
        return self.metadata.PLOT_LIST
