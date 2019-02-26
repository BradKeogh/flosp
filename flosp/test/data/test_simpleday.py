class TestInterfaceED():
    """ import example data
    - check correct sizes
    - columns in df
    """
    def setup(self):
        print ("setup             class:TestStuff")
        from flosp.interface import Interface
        self.hosp = Interface('./flosp/test/data/simpleday/setup.py')
        self.hosp.load_dataED('./flosp/test/data/simpleday/SimpleED.csv') # note this path makes it important which dir pytest is run
     

    def test_dataED_shape(self):
        """check size of dataframes, check all expected columns exist etc.
        Is this useful for checks module too?
        Is this all reproduced in test_io"""
        assert self.hosp.data.ED.shape() == (24,10)

    def test_extract_dataED(self):
        """check returns dataframe object, with valid and invalid inputs"""
        pass
