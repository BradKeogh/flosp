# NOTE: I think this is more integration testing!!

# BUGS found:
# in test_initialise - not using the file path given by user at beginning.

class TestInterfaceInitialisationCorrectPath:
    """ test initialisation of Interface Class. This is more like an integration test
    - check correct classes
    - sizes 
    - columns in dataframe have been made correctly: age_group, arr_month, dep_month etc.
    """
    def setup(self):
        print ("setup             class:TestStuff")
        from flosp.interface import Interface
        self.hosp = Interface()
 
    def teardown(self):
        print ("teardown          class:TestStuff")

    def test_initialise(self):
        """ Check that Interface is initialised and has data and metadata properties. 
        Check that these are parts of classes. """
        from flosp.interface import Interface
        from flosp.data import Data,MetaData
        # hosp = Interface(setup_file_path='./example/blarg/setjup.py') # how on earth is this passing? File path does not exist.
        assert(isinstance(self.hosp,Interface))
        assert(isinstance(self.hosp.data,Data))
        assert(isinstance(self.hosp.metadata,MetaData))

class TestInterfaceInitialisationNoPickles:
    """ delete files in processed directory or example, and then run initialisation. 
    assert no data is loaded after intialisation.
    Should do the same test with pickles after all data has been processed too? """
    pass

class TestInterfaceInitialisationInvalidPath():

    def setup(self):
        print ("setup             class:TestStuff")
        from flosp.interface import Interface
        self.hosp = Interface('./dfasdf/dasf/setup.py')
    
    def teardown(self):
        print ("teardown          class:TestStuff")

    def test_init_wrong_path(self):
        """ Check that Interface is initialised and has data and metadata properties. 
        Check that these are parts of classes. """
        from flosp.interface import Interface
        from flosp.data import Data,MetaData
        # hosp = Interface(setup_file_path='./example/blarg/setjup.py') # how on earth is this passing? File path does not exist.
        assert(isinstance(self.hosp,Interface))
        assert(isinstance(self.hosp.data,Data))
        assert(isinstance(self.hosp.metadata,MetaData))

class TestInterfaceLoadED():
    """ import example data
    - check correct sizes
    - columns in df
    """
    def setup(self):
        print ("setup             class:TestStuff")
        from flosp.interface import Interface
        self.hosp = Interface()
        self.hosp.load_dataED('./example/example_data_ED.csv')
     

    def test_load_dataED(self):
        """check size of dataframes, check all expected columns exist etc.
        Is this useful for checks module too?
        Is this all reproduced in test_io"""
        pass

    def test_extract_dataED(self):
        """check returns dataframe object, with valid and invalid inputs"""
        pass

class TestInterfaceLoadIP():
    "as above but with IP example data and method"
    pass

