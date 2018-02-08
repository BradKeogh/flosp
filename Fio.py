import pandas as pd
pd.read_csv
def EDimport():
    """
    function imports ED data for assignment
    """
    df = pd.read_csv('./../../3_Data/Patient Journey ED Data 22.01.2014 to 31.10.2015.csv',
    low_memory=False)

    return(df)
