import numpy as np
import pandas as pd
import seaborn as sns
sns.set()
import matplotlib.pyplot as plt

from flosp import _core

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

    def _filter_years(self,df,filter_on = 'arrive_year'):
        """ takes data frame and returns df with only valid years in arrive_date. input: filter_on, str, column name """

        df = df.query(filter_on+ " in " + str(self._data.valid_years))
        return(df)

    def _autosave_fig_tables(self,df,ax,fig_name):
        """ save all figs and tables currently generated """
        path = self._data.save_path + 'ED/'
        #### ensure path exists
        _core.create_dir(path)
        fullpath = path + 'table_plots.xlsx'

        #### save table
        writer  = pd.ExcelWriter(fullpath)
        df.to_excel(writer,sheet_name = fig_name)
        writer.save()

        ####save figure
        fullpath = path + fig_name + '.png'
        ax.get_figure().savefig(fullpath,dpi=600)
        return

    def tab_yearly_counts(self):
        return



    def bar_att_adm_no(self):
        """ reporoduce atten and admission bar plot """
        #### get data
        df = self._data.dataED
        fig_name  = 'fig1'
        #### call the production of yearly table counts
        df = self._filter_years(df)

        #### make table
        yearly = df.groupby('arrive_year').agg({'hosp_patid':'count','adm_flag':'sum'})

        yearly.rename(columns={'adm_flag':'ED admissions','hosp_patid':'ED attendances'},inplace=True)

        yearly['conversion ratio'] = 100* yearly['ED admissions'] / yearly['ED attendances']
        #### save table to self.data


        #### plot table
        ax = plt.subplot()

        width= 0.2

        yearly['ED attendances'].plot.bar(ax=ax,position=1,width=width,color='xkcd:blue',figsize=(6,4))
        ax2 = ax.twinx()
        yearly['ED admissions'].plot.bar(ax=ax2,position=0,width=width,color='xkcd:red')
        ax2.grid(False);

        ax.set_ylabel('attendances');
        ax2.set_ylabel('admissions');
        ax.set_xlabel('')

        lines, labels = ax.get_legend_handles_labels()
        lines2, labels2 = ax2.get_legend_handles_labels()
        ax2.legend(lines + lines2, labels + labels2, loc='lower right',frameon=True)
        #### save fig out now


        #### save table to excel
        #! make function to save - test this function
        self._autosave_fig_tables(yearly,ax2,fig_name)


        return
