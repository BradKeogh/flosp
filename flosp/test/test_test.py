from nose import with_setup
from flosp import Interface
from flosp.data import Data

def test_instantiation():
    inst = Interface('./setup.py')
    #assert isinstance(inst,Interface)
    #assert hasattr(inst,data,metadata)

def test_loaddata():

    inst = Interface('./setup.py')
    inst.load_data()
    assert isinstance(inst,Interface)
    assert isinstance(inst.data,Data)


def setup_func():
    "set up test fixtures"
    import numpy as np
    X = np.random.randint(20)
    print(X)

def teardown_func():
    "tear down test fixtures"

@with_setup(setup_func, teardown_func)
def test():
    "test ..."
    # idont understand why this is failing. i htought that the setup_func would make the variables names X and np?
    #print(X)
    #assert type(np.random.randint(20)) == np.int



### running new example - setUp used for instantiation class which is avail to other tests but must create lots 
# of new classes each time call method?, https://docs.python.org/3/library/unittest.html#basic-example 
import unittest

class WidgetTestCase(unittest.TestCase):
    def setUp(self):
        self.inst = Interface('./setup.py')

    def test_Instantiation(self):
        self.assertIsInstance(self.inst,Interface)
        # self.assertEqual(self.widget.size(), (50,50),
                        #  'incorrect default size')

    def test_LoadData(self):
        self.inst.load_data()

    # def test_widget_resize(self):
    #     self.widget.resize(100,150)
    #     self.assertEqual(self.widget.size(), (100,150),
    #                      'wrong size after resize')

# def test_subtract():
#     assert subtract(5,3) == 2

# def test_subtract2():
#     assert subtract(3,5) == -2

# def test_subtract_return_int():
#     assert type(subtract(3,5)) == int

# def my_function_test():
#     "test to see if input as float causes error"
#     assert type(subtract(33.0,5)) == int


# def Brad_name_check_test():
#     instance = Brad()
#     assert instance.name == 'Brad'