class flosp_class:
    """
    class which all methods work through
    """
    def __init__(self):
        #self#.name = 'Bill'
        print('created_flosp')
        self._data = data()
        pass
    
    def load_data(self):
        load_data_class()
        pass

    def process_data(self):
        pass

    def plot(self):
        pass


class load_data_class:
    """
    loading data class
    """
    def __init__(self,other):
        print('load_data')
        pass

class data:
    """
    class where all data is stored
    """
    def __init__(self):
        self.list_of_data = []
        self.dfA = 'dfA'
        pass