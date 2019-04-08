import numpy as np
import pandas as pd

from flosp.interface import Interface
from flosp import aggregation
from flosp.aggregation import get_max_min_datetimes, get_occ_hour_athour


class TestAgg():
    """ 
    Testing of aggregation functions for simple day example data.
    """

    def setup(self):
        print ("Get some data.")
        self.hosp = Interface('./flosp/test/data/simpleday/setup.py')
        self.hosp.load_dataED('./flosp/test/data/simpleday/SimpleED.csv') # note this path makes it important which dir 
        self.hosp.make_new_tables()

    def test_hourly_IPocc_total(self):
        """
        Test occupancy calcs, flosp vs. manual check with function from this test file.
        This is really testing that the flosp aggregation of occupancy calcs is correct, rather than the calculation of occupancy itself.
        """
        #### get list of datetimes to test

        hours_list = get_datetimes_list(self.hosp.data.IPSPELL, 'ADM_DTTM')

        df_flosp = self.hosp.data.HOURLY

        for datetime_hour in hours_list:
            occ_value = get_occ_hour_athour(self.hosp.data.IPSPELL, 'ADM_DTTM', 'DIS_DTTM', datetime_hour)
            assert occ_value == df_flosp.loc[datetime_hour].IPocc_total

        return


    def test_hourly_IPocc_nonelec(self):
        """
        Test occupancy calcs, flosp vs. manual check with function from this test file.
        """
        #### get list of datetimes to 
        
        df = self.hosp.data.IPSPELL

        dff = df.query('ADM_TYPE in ["Non-Elective"]')

        hours_list = get_datetimes_list(dff, 'ADM_DTTM')

        df_flosp = self.hosp.data.HOURLY

        for datetime_hour in hours_list:
            occ_value = get_occ_hour_athour(dff, 'ADM_DTTM', 'DIS_DTTM', datetime_hour)
            assert occ_value == df_flosp.loc[datetime_hour].IPocc_nonelec

        return

    def test_hourly_EDocc_total(self):
        """
        Test occupancy calcs, flosp vs. manual check with function from this test file.
        """
        #### get list of datetimes to 
        
        df = self.hosp.data.ED

        dff = df

        # dff = df.query('ADM_TYPE in ["Non-Elective"]')

        hours_list = get_datetimes_list(dff, 'ARRIVAL_DTTM')

        df_flosp = self.hosp.data.HOURLY

        for datetime_hour in hours_list:
            # occ_value = get_occ_hour_inwindow(dff, 'ARRIVAL_DTTM', 'DEPARTURE_DTTM', datetime_hour)
            occ_value = get_occ_hour_athour(dff, 'ARRIVAL_DTTM', 'DEPARTURE_DTTM', datetime_hour)
            assert occ_value == df_flosp.loc[datetime_hour].EDocc_total

        return
        
    def test_(self):
        """check returns dataframe object, with valid and invalid inputs"""
        pass


def get_datetimes_list(df,col_name):
    """
    Produce a list of possible datetime hours for test sample.
    NOTE: need to extend hours_list sample.
    """
    min_val, max_val = get_max_min_datetimes(df,col_name)
    min_val = min_val.replace(second=0,minute=0)
    max_val = max_val.replace(second=0,minute=0)
    
    hours_list = []
    
    ### some recent hours
    for i in np.arange(2,12,2):
        hours_list.append(min_val + pd.Timedelta(i,'h') )
    
    ### some hours from start of period
    
    
    ### some other hours
    
    return(hours_list)