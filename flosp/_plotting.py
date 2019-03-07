import numpy as np
import pandas as pd
import seaborn as sns
sns.set()
import matplotlib.pyplot as plt

from flosp import _core

class fig_tables():
    """ class to store all plot table data """
    def __init__(self):
        pass

class fig_plot():
    """ class to store all plot table data """
    def __init__(self):
        pass


class plotED():
    """ class containts all plotting """
    def __init__(self,data):
        self._data = data
        self._fig_tables = fig_tables()
        self._fig_plot = fig_plot()
        print(self)
        print(self._data)
        print(self._data)

    def _filter_years(self,df,filter_on = 'arrive_year'):
        """ takes data frame and returns df with only valid years in arrive_date. input: filter_on, str, column name """

        df = df.query(filter_on+ " in " + str(self._data.valid_years))
        return(df)

    def _filter_clean_timings(self,df):
        """ takes df and returns records only with clean timings, i.e. makes sure none of the times between atten->triage->dr->adm->leave dept are negative.
        """
        # selection query
        exclude_index = df.query('arr_triage_wait < 0 or arr_dr_wait < 0 or arr_adm_req_wait < 0 or waiting_time < 0'
                          +'or arr_triage_wait > 24*60 or arr_dr_wait > 24*60 or arr_adm_req_wait > 24*60'
                          'or waiting_time > 24*60' + 'or adm_req_dep_wait < 0 or dr_adm_req_wait <0 or dr_dep_wait < 0'
                          ).index

        # select only clean records
        df_clean = df.loc[~df.index.isin(exclude_index)]


        return(df_clean)

    def _autosave_fig_tables(self,fig_name):
        """ save all figs and tables currently generated """
        path = self._data.save_path + 'ED/'
        #### ensure path exists
        _core.create_dir(path)
        fullpath = path + 'table_plots.xlsx'

        #### save table -
        writer  = pd.ExcelWriter(fullpath)
        # loop through each table that exists
        mylist = dir(self._fig_tables)
        mylist = [x for x in mylist if not x.startswith('__')]
        for i in mylist:
            df = getattr(self._fig_tables,i)
            df.to_excel(writer,sheet_name = i)

        # save all tables to file
        writer.save()

        ####save figure
        fullpath = path + fig_name + '.png'
        ax = getattr(self._fig_plot, fig_name)
        ax.get_figure().savefig(fullpath,dpi=600)
        return

    def additional_tables(self):
        """ make additional standard tables from ED df """
        #### make path for saving
        path = self._data.save_path + 'ED/'
        #### ensure path exists
        _core.create_dir(path)
        fullpath = path + 'additional_tables.xlsx'

        #### open excel writer
        writer  = pd.ExcelWriter(fullpath)
        df = self._data.dataED
        df = self._filter_years(df)

        ##### table 1
        yearly = df.groupby('arrive_year').agg({'hosp_patid':'count','adm_flag':'sum'})

        yearly.rename(columns={'adm_flag':'ED admissions','hosp_patid':'ED attendances'},inplace=True)

        yearly['conversion ratio'] = 100* yearly['ED admissions'] / yearly['ED attendances']

        yearly.round(1)
        yearly.to_excel(writer,sheet_name = 'year_counts')

        ##### table 2
        yearly_pct_change = (yearly[['ED attendances','ED admissions']].pct_change()*100).round(1)
        yearly_pct_change.to_excel(writer,sheet_name = 'yearly_pct_change')

        ##### table 3
        last = df.arrive_year.max()
        first = df.arrive_year.min()
        total_pct_change = (yearly.loc[[first,last]].pct_change()*100).round(1)

        total_pct_change.to_excel(writer,sheet_name = 'total_pct_change')

        ##### table 4

        ##### table 5
        temp = df.groupby(['arrive_year','adm_flag']).sum()['BREACH_FLAG'].unstack()
        temp['perc_breach_adm'] = 100*temp[1]/(temp[0] + temp[1])
        temp.columns.name=None
        temp.rename(columns={0:'no. of breach (non-adm)',1:'no. of breach (adm)', 'perc_breach_adm':'% of breach from adm'},inplace=True)
        temp.round(0)

        temp.to_excel(writer,sheet_name = 'breach_per_adm-nonadm')

        ##### table 6

        # get clean timings
        df = self._data.dataED
        df = self._filter_clean_timings(df)

        #function for generating table
        def year_timings(df, year):
            "for sinlge year specified make df of: descriptive stats on wait times, timings for each admisison route."
            #filter for year
            df[df.arrive_year == year]
            ### describe timings
            wait_cols = ['arr_triage_wait','arr_dr_wait','dr_adm_req_wait','adm_req_dep_wait','dr_dep_wait']
            describe = df[wait_cols].describe()

            # make groupby function
            agg_f = {'adm_req_dep_wait':['median','count']}


            # perform aggregation
            ref_loc_timings = df.groupby(['adm_referral_loc']).agg(agg_f)['adm_req_dep_wait'].sort_values(ascending=False,by='median').round(0)

            ref_loc_timings.rename(columns={'median':'average time','count':'no. of patients'},inplace=True)

            return(describe,ref_loc_timings)


        df1,df2 = year_timings(df,first)
        name = str(first) + '_timing_descriptive_stats'
        df1.to_excel(writer,sheet_name = name)
        name = str(first) + '_timing_adm_routes_median'
        df2.to_excel(writer,sheet_name = name)

        df1,df2 = year_timings(df,last)
        name = str(last) + '_timing_descriptive_stats'
        df1.to_excel(writer,sheet_name = name)
        name = str(last) + '_timing_adm_routes_median'
        df2.to_excel(writer,sheet_name = name)

        #### save all tables
        writer.save()
        return

    def bar_att_adm_no(self):
        """ reporoduce atten and admission no.s bar plot """
        #### get data
        df = self._data.dataED
        fig_name  = 'fig1'
        #### call the production of yearly table counts
        df = self._filter_years(df)

        #### make table
        yearly = df.groupby('arrive_year').agg({'hosp_patid':'count','adm_flag':'sum'})

        yearly.rename(columns={'adm_flag':'ED admissions','hosp_patid':'ED attendances'},inplace=True)

        yearly['conversion ratio'] = 100* yearly['ED admissions'] / yearly['ED attendances']

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

        #### save table to excel
        self._fig_tables.fig1 = yearly
        self._fig_plot.fig1 = ax2
        self._autosave_fig_tables(fig_name)
        return

    def bar_age_split(self):
        """ bar chart with age split over different years """
        df_att = self._data.dataED
        df_att = self._filter_years(df_att)

        def plot1(df,fig_name):
            "make bar plot & save"

            ax = plt.subplot()
            df2 = df.groupby(['arrive_year','age_group']).count()['hosp_patid'].unstack()
            df2.plot(kind='bar',ax=ax);
            ax.set_ylabel('ED attendances (yearly)');
            ax.set_xlabel('year');
            ax.legend(title = 'age group',frameon=True,loc='lower right');

            # save fig
            setattr(self._fig_tables,fig_name,df2)
            setattr(self._fig_plot,fig_name,ax)
            self._autosave_fig_tables(fig_name)
            return

        # plot for atendances
        plot1(df_att,'fig2a')

        #plot for admissions
        df_adm = df_att[df_att.adm_flag == 1]
        plot1(df_adm,'fig2b')


        return
