# intro to pytest from here http://pythontesting.net/framework/pytest/pytest-introduction/

from unnecessary_math import multiply

print('Test start.')

def test_number_3_4():
    assert(multiply(3,4)== 12)

def test_strings_a_3():
    assert(multiply('a',3)== 'aaa')