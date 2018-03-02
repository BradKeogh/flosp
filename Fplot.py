import matplotlib.pyplot as plt


def plotEDday(df):
    """ plots a number of different plots """
    df[['ED_breaches_perc']].plot(kind='line');
    df.ED_breaches_perc.rolling(10).mean().plot(kind='line',style='r')
