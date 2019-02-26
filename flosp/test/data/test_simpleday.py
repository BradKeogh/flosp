class TestInterfaceED():
    """ import example data
    - check correct sizes
    - columns in df
    """
    def setup(self):
        print ("setup Interface and load data files.")
        from flosp.interface import Interface
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
        from flosp.interface import Interface
        self.hosp = Interface('./flosp/test/data/simpleday/setup.py')
        self.hosp.load_dataIP('./flosp/test/data/simpleday/SimpleIP.csv') # note this path makes it important which dir

    def test_dataIP_shape(self):
        """check size of dataframes, check all expected columns exist etc.
        Is this useful for checks module too?
        Is this all reproduced in test_io"""
        assert self.hosp.data.IP.shape == (48,35)