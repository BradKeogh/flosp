import numpy as np
import pandas as pd
import seaborn as sns
sns.set()
import matplotlib.pyplot as plt

class plotED():
    """ class containts all plotting """
    def __init__(self,data):
        self._data = data
        print(self)
        print(self._data)
        print(self._data)

    def plot1(self):
        print('plotting 1')
        print(self._data)
        return


    def atten_adm_numbers_bar(self):
        """ reporoduce atten and admission bar plot """
        yearly = self._data.dataED.groupby('arrive_year').agg({'hosp_patid':'count','adm_flag':'sum'})[1:-1]

        yearly.rename(columns={'adm_flag':'ED admissions','hosp_patid':'ED attendances'},inplace=True)

        yearly['conversion ratio'] = 100* yearly['ED admissions'] / yearly['ED attendances']

        ax = plt.subplot()

        width= 0.2

        yearly['ED attendances'].plot.bar(ax=ax,position=1,width=width,color='xkcd:blue',figsize=(6,4))
        ax2 = ax.twinx()
        yearly['ED admissions'].plot.bar(ax=ax2,position=0,width=width,color='xkcd:red')
        ax2.grid(False);

        ax.set_ylabel('attendances');
        ax2.set_ylabel('admissions');
        ax.set_xlabel('')
        ## sort legend
        #lns = lns1+lns2
        #labs = ['attendances','admissions']

        lines, labels = ax.get_legend_handles_labels()
        lines2, labels2 = ax2.get_legend_handles_labels()
        ax2.legend(lines + lines2, labels + labels2, loc='lower right',frameon=True)

        #ax.legend(lns, labs, loc=0)
        #ax.legend(labs,frameon=True);
        return
