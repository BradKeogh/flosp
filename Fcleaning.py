

def checkmissing(x):
    """
    input: df, for checking
    output: info about missing values
    """
    return df.isnull().sum()
