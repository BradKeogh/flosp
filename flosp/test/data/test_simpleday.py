from flosp.interface import Interface


class TestInterfaceED():
    """ import example data
    - check correct sizes
    - columns in df
    """
    def setup(self):
        print ("setup Interface and load data files.")
        self.hosp = Interface('./flosp/test/data/simpleday/setup.py')
        self.hosp.load_dataED('./flosp/test/data/simpleday/SimpleED.csv') # note this path makes it important which dir 
     

    def test_dataED_shape(self):
        """check size of dataframes, check all expected columns exist etc.
        Is this useful for checks module too?
        Is this all reproduced in test_io"""
        assert self.hosp.data.ED.shape == (24,41)

    def test_extract_dataED(self):
        """check returns dataframe object, with valid and invalid inputs"""
        pass





class TestInterfaceIP():
    """ import example data
    - check correct sizes
    - columns in df
    """
    def setup(self):
        print ("setup Interface and load data files.")
        self.hosp = Interface('./flosp/test/data/simpleday/setup.py')
        self.hosp.load_dataIP('./flosp/test/data/simpleday/SimpleIP.csv') # note this path makes it important which dir run from

    def test_dataIP_shape(self):
        """check size of dataframes, check all expected columns exist etc.
        Is this useful for checks module too?
        Is this all reproduced in test_io"""
        assert self.hosp.data.IP.shape == (48,35)


class TestCompleteAggregation():
    """ Import example data & aggregate.
    - check correct sizes.
    """
    def setup(self):
        print('Setup Interface class, load data files and aggreatate.')
        self.hosp = Interface('./flosp/test/data/simpleday/setup.py')
        self.hosp.load_dataIP('./flosp/test/data/simpleday/SimpleIP.csv')
        self.hosp.make_new_tables()

    def test_aggregation_shape(self):
        "check length of dataframe. NOTE: width will change in future as add new aggregations (columns) to analysis."
        assert self.hosp.data.HOURLY.shape[0] == 96

    def test_HOURLY_shape(self):
        " check sums of columns for HOURLY aggregation dataframe."
        columns = {
            'ED_arrivals':24,
            'ED_departures':24,
            'IP_admissions_total':24,
            'IP_discharges_total':24,
            'EDocc_total':48,          
            'IPocc_total':1752,
            'IP_admissions_nonelec':12,
            'IP_discharges_elec':12,
            'IPadm_minus_dis_elec_nonelec':0,
            }

        for column in columns.keys():
            assert self.hosp.data.HOURLY[column].sum() == columns[column]
