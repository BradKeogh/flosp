import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import seaborn as sns


sns.set() # set for nice looking plots
daysofweek = ['Mon','Tue','Wed','Thur','Fri','Sat','Sun']

class HistoricalPlotting:
    """ Class produces all historical plots automatically. """
    def __init__(self, data, metadata, EDyears, IPyears, required_plot_no):
        #### save arguments as attributes 
        self.data = data
        self.metadata = metadata
        self.EDyears = EDyears
        self.IPyears = IPyears

        #### get only period plots in list
        plot_list = self.metadata.PLOT_LIST
        plot_list_historical = plot_list.query('plot_type == "hist"')
        
        #### call all plot methods unless required_plot_no
        if required_plot_no == 'all':
            for plot_no in plot_list_historical.plot_number.values: #### NOTE: must rerplace this with list from general - once creater (filter for Period only plots)
                exec('self.' + 'plot' + str(plot_no) +'()')
        else:
            exec('self.' + 'plot' + str(required_plot_no) + '()')
        
        #### save tables and figures in this initialisatation

        return
    
    def plot1(self):
        """ Create table and plot for figure 1. """
        plot_number = 1
        plot_info, pat_filtered, title = self.get_historical_plot_info(plot_number, 'ED')

        #### get yearly table
        yearly = pat_filtered.groupby('ARRIVAL_year').agg({'PSEUDONYMISED_PATIENT_ID':'count','ADMISSION_FLAG':'sum'})
        yearly.rename(columns={'ADMISSION_FLAG':'ED admissions','PSEUDONYMISED_PATIENT_ID':'ED attendances'},inplace=True)
        yearly['conversion ratio'] = 100* yearly['ED admissions'] / yearly['ED attendances']
        table = yearly.round(1)
        
        #### plot
        fig, ax = plt.subplots()
        width= 0.2
        yearly['ED attendances'].plot.bar(ax=ax,position=1,width=width,color='xkcd:blue',figsize=(5,4))
        ax2 = ax.twinx()
        yearly['ED admissions'].plot.bar(ax=ax2,position=0,width=width,color='xkcd:red')
        ax2.grid(False);

        ax.set_ylabel('attendances');
        ax2.set_ylabel('admissions');
        ax.set_xlabel('');
        ax.set_title(title)

        lines, labels = ax.get_legend_handles_labels()
        lines2, labels2 = ax2.get_legend_handles_labels()
        ax2.legend(lines + lines2, labels + labels2, loc='lower right',frameon=True)

        setattr(self.data.plots, 'table' + str(plot_number), table)
        setattr(self.data.plots, 'fig' + str(plot_number), fig)

        return

    def plot2(self):
        " create figure and table for plot 2."
        plot_number = 2
        plot_info, pat_filtered, title = self.get_historical_plot_info(plot_number, 'ED')

        #### get tables
        tableA = pat_filtered.groupby(['ARRIVAL_year','age_group']).count()['PSEUDONYMISED_PATIENT_ID'].unstack()
        tableB = pat_filtered[pat_filtered.ADMISSION_FLAG == 1].groupby(['ARRIVAL_year','age_group']).count()['PSEUDONYMISED_PATIENT_ID'].unstack()
        
        #### plot 
        fig, ax = plt.subplots(1,2,figsize=(14,5))

        tableA.plot(kind='bar',ax=ax[0]);
        ax[0].set_ylabel('ED attendances (yearly)');
        ax[0].set_xlabel('year');
        ax[0].legend(title = 'age group',frameon=True,loc='lower right');

        tableB.plot(kind='bar',ax=ax[1]);
        ax[1].set_ylabel('ED admissions (yearly)');
        ax[1].set_xlabel('year');
        ax[1].legend(title = 'age group',frameon=True,loc='lower right');
        fig.suptitle(title)

        #### save data
        setattr(self.data.plots, 'table' + str(plot_number) + 'A', tableA)
        setattr(self.data.plots, 'table' + str(plot_number) + 'B', tableB)
        setattr(self.data.plots, 'fig' + str(plot_number), fig)
        
        return

    def plot5(self):
        " create figure and table for plot 2."
        plot_number = 5
        plot_info, pat_filtered, title = self.get_historical_plot_info(plot_number, 'ED')
        
        #### filter further for clean wait times
        exclude_index = pat_filtered.query('arr_triage_wait < 0 or arr_dr_wait < 0 or arr_adm_req_wait < 0 or waiting_time < 0'
                          +'or arr_triage_wait > 24*60 or arr_dr_wait > 24*60 or arr_adm_req_wait > 24*60'
                          'or waiting_time > 24*60' + 'or adm_req_dep_wait < 0 or dr_adm_req_wait <0 or dr_dep_wait < 0'
                          ).index

        pat2 = pat_filtered.loc[~pat_filtered.index.isin(exclude_index)]

        wait_col2 = ['arr_dr_wait','dr_adm_req_wait','adm_req_dep_wait','dr_dep_wait']
        
        #### get tables
        tableA = pat2[pat2.ADMISSION_FLAG == 0].groupby('ARRIVAL_year')[wait_col2[0],wait_col2[3]].median()
        tableB = pat2[pat2.ADMISSION_FLAG == 1].groupby('ARRIVAL_year')[wait_col2[0],wait_col2[3]].median()
        

        #### plot figures
        fig, ax = plt.subplots(1,2, figsize=(14,5))

        tableA.plot.bar(stacked=True,ax=ax[0])
        ax[0].set_ylabel('Median time in department (mins)');
        # ax[0].set_ylim([0,250]);
        ax[0].set_xlabel('');
        ax[0].legend(['arrival -> dr','dr -> departure'],frameon=True);
        ax[0].set_title('Non-admitted patients');

        tableB.plot.bar(stacked=True,ax=ax[1])
        ax[1].set_ylabel('Median time in department (mins)');
        ax[1].set_xlabel('');
        ax[1].legend(['arrival -> dr','dr -> departure'],frameon=True,loc='center right');
        ax[1].set_title('Admitted patients');
        # ax[1].set_ylim([0,250]);

        fig.suptitle(title)
        ylim = ax[1].get_ylim() # get ylim of 2nd plot
        ax[0].set_ylim(ylim) # set first plot to have same axis size.

        #### save data
        setattr(self.data.plots, 'table' + str(plot_number) + 'A', tableA)
        setattr(self.data.plots, 'table' + str(plot_number) + 'B', tableB)
        setattr(self.data.plots, 'fig' + str(plot_number), fig)

        return


    def plot11(self):
        ""
        plot_number = 11

        plot_info, pat_filtered, title = self.get_historical_plot_info(plot_number, 'IPSPELL')
        #### filter for baby births
        pat_filtered = pat_filtered.query("ADM_METHOD not in ['82','83','2C']")

        #### get tables
        table = pat_filtered.groupby(['ADM_year','ADM_TYPE']).count()['PSEUDONYMISED_PATIENT_ID'].unstack()
        table = table.loc[self.IPyears] # get only years specified in original plot call.

        #### make plot
        fig, ax =plt.subplots(figsize=(7,5))
        table.plot(kind='bar',ax=ax)
        ax.set_ylabel('number of admissions')
        ax.legend(frameon=True,loc='center left')
        ax.set_xlabel('')
        ax.set_title(title)


        setattr(self.data.plots, 'table' + str(plot_number), table)
        setattr(self.data.plots, 'fig' + str(plot_number), fig)

        return

    def plot12(self):
        ""
        plot_number = 12

        plot_info, pat_filtered, title = self.get_historical_plot_info(plot_number, 'IPSPELL')
        #### filter for baby births
        pat_filtered = pat_filtered.query("ADM_METHOD not in ['82','83','2C']")

        #### get table
        table = pat_filtered.groupby(['ADM_year','age_group']).count().unstack()['PSEUDONYMISED_PATIENT_ID']
        table = table.loc[self.IPyears]

        #### plotting
        fig, ax =plt.subplots(figsize=(5,5))
        table.plot(kind='bar',stacked=True,ax=ax)
        ax.set_ylabel('number of admissions')
        ax.legend(frameon=True,loc='upper left',title='Age group')
        ax.set_xlabel('')
        ax.set_title(title)

        setattr(self.data.plots, 'table' + str(plot_number), table)
        setattr(self.data.plots, 'fig' + str(plot_number), fig)

        return

    def plot13(self):
        "This is actually a table. It is a merge of the tables from plot 1 and plot 11."
        plot_number = 13

        if hasattr(self.data.plots, 'table1') & hasattr(self.data.plots, 'table11'):
            table = self.data.plots.table1.merge(self.data.plots.table11, left_index=True, right_index=True)
            table = table.loc[self.IPyears]
            setattr(self.data.plots, 'table' + str(plot_number), table)
            print(table)
        else:
            print('Table 13 not produced as required both fig1 and fig 11 to be made beforehand.')
        
        return

    def plot14(self):
        ""
        plot_number = 14

        plot_info, pat_filtered, title = self.get_historical_plot_info(plot_number, 'IPSPELL')
        #### filter for baby births
        pat_filtered = pat_filtered.query("ADM_METHOD not in ['82','83','2C']")
        ####

        #### table
        table = pat_filtered.query('ADM_TYPE == "Non-Elective"').groupby(['ADM_year','ADM_METHOD_simple']).count()['PSEUDONYMISED_PATIENT_ID'].unstack()
        table = table.loc[self.IPyears]

        #### plotting
        fig, ax = plt.subplots(figsize=(5,5))
        table.plot(kind='bar',stacked=True,ax=ax)
        ax.set_ylabel('number of admissions');
        ax.legend(frameon=True,loc='lower right',title='Admission route');
        ax.set_xlabel('');
        ax.set_title(title)

        setattr(self.data.plots, 'table' + str(plot_number), table)
        setattr(self.data.plots, 'fig' + str(plot_number), fig)

        return

    def plot19(self):
        """ Create plot & table 19.
        NOTE: seems to be an issue with the values produced in plot using test data->simple_day.
        Possible issue with the aggergation module.
        """
        plot_number = 19

        plot_list = self.metadata.PLOT_LIST
        title = plot_list.query('plot_number == ' + str(plot_number))['plot_name'].values[0]
        years = self.EDyears
        occ = self.data.DAILY
        occ_filtered  = occ.query('date_year in ' + str(years))
        
        #### get tables
        table = occ_filtered.groupby(['date_month','date_year']).median()['EDocc_total_MAX'].unstack()

        #### plot figures
        fig, ax = plt.subplots(figsize=(9,5))
        table.plot(kind='bar',ax=ax)
        ax.set_xlabel('Month');
        ax.set_ylabel('Median peak daily ED occupancy');
        fig.suptitle(title);
        ax.legend(loc='lower right',frameon=True,title='Year')

        setattr(self.data.plots, 'table' + str(plot_number), table)
        setattr(self.data.plots, 'fig' + str(plot_number), fig)

        return

    def plot20(self):
        " create table and plot for 20."
        plot_number = 20

        plot_list = self.metadata.PLOT_LIST
        title = plot_list.query('plot_number == ' + str(plot_number))['plot_name'].values[0]
        years = self.IPyears
        occ = self.data.DAILY
        occ_filtered  = occ.query('date_year in ' + str(years))

        #### get table
        table = occ_filtered.groupby(['date_month','date_year']).median()['IPocc_elec_nonelec_MAX'].unstack()

        #### get figure
        fig, ax = plt.subplots(figsize=(9,5))
        
        table.plot(kind='bar',ax=ax)
        ax.set_xlabel('Month');
        ax.set_ylabel('Median IP max daily occupancy');
        fig.suptitle(title);
        ax.legend(loc='lower right',frameon=True,title='Year')

        setattr(self.data.plots, 'table' + str(plot_number), table)
        setattr(self.data.plots, 'fig' + str(plot_number), fig)

        return


    def get_historical_plot_info(self, plot_number, data_name):
        """ Provided plot number retrieve plot info and filtered dataframe for patient level data. """
        #### plot data
        plot_info = self.metadata.PLOT_LIST.query('plot_number == plot_number')
        #### ED hourly arrival discharge curves
        # filter for period selected
        pat = getattr(self.data, data_name)

        if data_name == 'ED':
            # pat = self.data.ED
            years = self.EDyears
            pat_filtered = pat.query('ARRIVAL_year in ' + str(years) +' and DEPARTURE_year in ' + str(years))
            # this filter will miss those patients crossing midnight on Jan 1st.

        elif data_name =='IP':
            years = self.IPyears
            pat_filtered = pat.query('ADM_year in ' + str(years) +' or DIS_year in ' + str(years))
        
        elif data_name == 'IPSPELL':
            years = self.IPyears
            pat_filtered = pat.query('ADM_year in ' + str(years) +' or DIS_year in ' + str(years))
        
        title = plot_info.query('plot_number == ' + str(plot_number))['plot_name'].values[0]

        return(plot_info, pat_filtered, title)




class PeriodPlotting:
    """ Class produces all plots for a period of time defined by user. """
    def __init__(self, data, metadata, dt_start, dt_end, required_plot_no):
        #### initialise all data
        self.data = data
        self.metadata = metadata
        self.dt_start = dt_start
        self.dt_end = dt_end

        #### get only period plots in list
        plot_list = self.metadata.PLOT_LIST
        plot_list_period = plot_list.query('plot_type == "period"')
        
        #### call all plot methods unless required_plot_no
        if required_plot_no == 'all':
            for plot_no in plot_list_period.plot_number.values: #### NOTE: must rerplace this with list from general - once creater (filter for Period only plots)
                exec('self.' + 'plot' + str(plot_no) +'()')
        else:
            exec('self.' + 'plot' + str(required_plot_no) + '()')
        return

    def plot3(self):
        " Create table and plot figure 3."
        #### get info and data
        plot_number = 3
        plot_info, pat_filtered, title = self.get_period_plot_info(plot_number)

        #### additional cleaning for waiting times
        exclude_index = pat_filtered.query('arr_triage_wait < 0 or arr_dr_wait < 0 or arr_adm_req_wait < 0 or waiting_time < 0'
                          +'or arr_triage_wait > 24*60 or arr_dr_wait > 24*60 or arr_adm_req_wait > 24*60'
                          'or waiting_time > 24*60' + 'or adm_req_dep_wait < 0 or dr_adm_req_wait <0 or dr_dep_wait < 0'
                          ).index

        pat2 = pat_filtered.loc[~pat_filtered.index.isin(exclude_index)]

        wait_col2 = ['arr_dr_wait','dr_dep_wait','dr_adm_req_wait','adm_req_dep_wait']

        #### plot
        fig, ax = plt.subplots()
        table = pat2.groupby('ADMISSION_FLAG')[wait_col2].median()
        table.loc[1,'dr_dep_wait'] = table.loc[1]['dr_adm_req_wait'] + table.loc[1]['adm_req_dep_wait'] # this required to get same admission times as plot4. Caused by erroneous admission_flag data.
        table = table[['arr_dr_wait','dr_dep_wait']]
        table.plot.bar(stacked=True,ax=ax,figsize=(4,4))
        ax.set_xticklabels(['non-admission','admission']);
        ax.set_ylabel('Median time in department (mins)');
        ax.set_xlabel('');
        ax.legend(['arrival -> dr','dr -> departure'],frameon=True);
        ax.set_title(title)

        #### save figure and table data
        setattr(self.data.plots, 'table' + str(plot_number), table)
        setattr(self.data.plots, 'fig' + str(plot_number), fig)

        return

    def plot4(self):
        " Create table and plot figure 4."
        #NOTE: i think should expect an error if ED data for non-admitted patients have datetimes in REQ_ADMISSION_DTTM and ADM_DTTM.
        #### get info and data.
        plot_number = 4
        plot_info, pat_filtered, title = self.get_period_plot_info(plot_number)

        #### additional cleaning for waiting times
        exclude_index = pat_filtered.query('arr_triage_wait < 0 or arr_dr_wait < 0 or arr_adm_req_wait < 0 or waiting_time < 0'
                          +'or arr_triage_wait > 24*60 or arr_dr_wait > 24*60 or arr_adm_req_wait > 24*60'
                          'or waiting_time > 24*60' + 'or adm_req_dep_wait < 0 or dr_adm_req_wait <0 or dr_dep_wait < 0'
                          ).index

        pat2 = pat_filtered.loc[~pat_filtered.index.isin(exclude_index)]

        wait_col2 = ['arr_dr_wait','dr_dep_wait','dr_adm_req_wait','adm_req_dep_wait']

        #### plot
        fig, ax = plt.subplots()

        table = pat2.groupby('ADMISSION_FLAG')[wait_col2].median()
        table.loc[0,'dr_adm_req_wait'] = np.nan 
        table.loc[0,'adm_req_dep_wait'] = np.nan
        table.loc[1,'dr_dep_wait'] = np.nan

        table.plot.bar(stacked=True,ax=ax,figsize=(4,4))
        ax.legend(['arrival -> dr','dr -> departure','dr -> adm req','adm req -> departure'],loc='upper left',frameon=True);
        ax.set_xticklabels(['non-admission','admission']);
        ax.set_ylabel('Median time in department (mins)');
        ax.set_xlabel('');
        ax.set_title(title)
        # ax.set_yticks(np.arange(0,225,50));

        #### save figure and table data
        setattr(self.data.plots, 'table' + str(plot_number), table)
        setattr(self.data.plots, 'fig' + str(plot_number), fig)

        return

    def plot6(self):
        " Create table and plot figure 6."
        #### filter data
        plot_number = 6
        plot_info, pat_filtered, title = self.get_period_plot_info(plot_number)

        #### clean wait times
        exclude_index = pat_filtered.query('arr_triage_wait < 0 or arr_dr_wait < 0 or arr_adm_req_wait < 0 or waiting_time < 0'
                          +'or arr_triage_wait > 24*60 or arr_dr_wait > 24*60 or arr_adm_req_wait > 24*60'
                          'or waiting_time > 24*60' + 'or adm_req_dep_wait < 0 or dr_adm_req_wait <0 or dr_dep_wait < 0'
                          ).index

        pat2 = pat_filtered.loc[~pat_filtered.index.isin(exclude_index)]
        temp = pat2[['arr_dr_wait','dr_dep_wait','ADMISSION_FLAG']].pivot(columns='ADMISSION_FLAG')

        t1 = temp['arr_dr_wait'][0]
        t2 = temp['dr_dep_wait'][0]
        t3 = temp['arr_dr_wait'][1]
        t4 = temp['dr_dep_wait'][1]

        table = pd.DataFrame(data = dict(t1=t1,t2=t2,t3=t3,t4=t4))
        fig, ax = plt.subplots()
        table.plot.box(ax=ax,figsize=(5,4))
        ax.set_ylim([0,600]); # consider supressing auto scale?
        ax.set_xticklabels(['arr -> dr\n (non-admission)','dr -> departure\n (non-admission)',
                            'arr -> dr\n (admission)','dr -> departure\n (admission)']);
        ax.set_ylabel('wait time (mins)');
        ax.set_title(title);

        #### save figure and table data
        setattr(self.data.plots, 'table' + str(plot_number), table)
        setattr(self.data.plots, 'fig' + str(plot_number), fig)

        return

    def plot7(self):
        "Create table and plot 7."
        #### get data
        plot_number = 7
        plot_info, pat_filtered, title = self.get_period_plot_info(plot_number)

        #### filter for clean wait times
        exclude_index = pat_filtered.query('arr_triage_wait < 0 or arr_dr_wait < 0 or arr_adm_req_wait < 0 or waiting_time < 0'
                          +'or arr_triage_wait > 24*60 or arr_dr_wait > 24*60 or arr_adm_req_wait > 24*60'
                          'or waiting_time > 24*60' + 'or adm_req_dep_wait < 0 or dr_adm_req_wait <0 or dr_dep_wait < 0'
                          ).index

        pat2 = pat_filtered.loc[~pat_filtered.index.isin(exclude_index)]

        wait_col2 = ['arr_dr_wait','dr_adm_req_wait','adm_req_dep_wait','dr_dep_wait']

        #### plot
        fig, ax = plt.subplots(1,2, figsize=(14,5))
        tableA = pat2[pat2.ADMISSION_FLAG == 0].groupby('ARRIVAL_hour')[wait_col2[0],wait_col2[3]].median()
        tableA.plot.bar(stacked=True,ax=ax[0])
        ax[0].set_title('Non-admitted patients')
        ax[0].legend(['arrival -> dr','dr -> departure'], frameon=True)
        

        tableB = pat2[pat2.ADMISSION_FLAG == 1].groupby('ARRIVAL_hour')[wait_col2[0],wait_col2[3]].median()
        tableB.plot.bar(stacked=True,ax=ax[1])
        ax[1].set_title('Admitted patients')
        ax[1].get_legend().remove()
        
        ax[0].set_ylabel('Median patient waiting time (mins)');
        ylim = ax[1].get_ylim() # get ylim of 2nd plot
        ax[0].set_ylim(ylim) # set first plot to have same axis size.



        fig.suptitle(title)

        #### save data
        setattr(self.data.plots, 'table' + str(plot_number) + 'A', tableA)
        setattr(self.data.plots, 'table' + str(plot_number) + 'B', tableB)
        setattr(self.data.plots, 'fig' + str(plot_number), fig)

        return

    def plot8(self):
        "Create table and plot 8."
        #### get data
        plot_number = 8
        plot_info, pat_filtered, title = self.get_period_plot_info(plot_number)

        #### filter for clean wait times
        exclude_index = pat_filtered.query('arr_triage_wait < 0 or arr_dr_wait < 0 or arr_adm_req_wait < 0 or waiting_time < 0'
                          +'or arr_triage_wait > 24*60 or arr_dr_wait > 24*60 or arr_adm_req_wait > 24*60'
                          'or waiting_time > 24*60' + 'or adm_req_dep_wait < 0 or dr_adm_req_wait <0 or dr_dep_wait < 0'
                          ).index

        pat2 = pat_filtered.loc[~pat_filtered.index.isin(exclude_index)]

        wait_col2 = ['arr_dr_wait','dr_adm_req_wait','adm_req_dep_wait','dr_dep_wait']

        #### plot
        fig, ax = plt.subplots(1,2, figsize=(14,5))
        tableA = pat2[pat2.ADMISSION_FLAG == 0].groupby('ARRIVAL_month')[wait_col2[0],wait_col2[3]].median()
        tableA.plot.bar(stacked=True,ax=ax[0])
        ax[0].set_title('Non-admitted patients')
        ax[0].legend(['arrival -> dr','dr -> departure'], frameon=True)

        tableB = pat2[pat2.ADMISSION_FLAG == 1].groupby('ARRIVAL_month')[wait_col2[0],wait_col2[3]].median()
        tableB.plot.bar(stacked=True,ax=ax[1])
        ax[1].set_title('Admitted patients')
        ax[1].get_legend().remove()

        ax[0].set_ylabel('Median patient waiting time (mins)');
        ylim = ax[1].get_ylim() # get ylim of 2nd plot
        ax[0].set_ylim(ylim) # set first plot to have same axis size.

        fig.suptitle(title)

        #### save data
        setattr(self.data.plots, 'table' + str(plot_number) + 'A', tableA)
        setattr(self.data.plots, 'table' + str(plot_number) + 'B', tableB)
        setattr(self.data.plots, 'fig' + str(plot_number), fig)

        return





    def plot9(self):
        #### plot data
        plot_number = 9
        plot_info, pat_filtered, title = self.get_period_plot_info(plot_number)

        #### ED hourly arrival discharge curves
        # make table for plot
        arr = pat_filtered[['ARRIVAL_hour','PSEUDONYMISED_PATIENT_ID']].groupby(['ARRIVAL_hour']).count()#.plot(ax=ax)
        dep = pat_filtered[['DEPARTURE_hour','PSEUDONYMISED_PATIENT_ID']].groupby(['DEPARTURE_hour']).count()#.plot(ax=ax)
        arr.rename(columns={'PSEUDONYMISED_PATIENT_ID':'Arrivals'},inplace=True)
        dep.rename(columns={'PSEUDONYMISED_PATIENT_ID':'Departures'},inplace=True)
        table = arr.merge(dep, left_index=True, right_index=True)

        # make mean attendance values
        no_days = len(pat_filtered.ARRIVAL_date.unique())
        table = table/no_days

        # plot
        fig, ax = plt.subplots()
        plt.suptitle(title)
        table.plot(ax=ax)
        ax.set_xticks(np.arange(0,25,2));

        #### save figure and table data
        setattr(self.data.plots, 'table' + str(plot_number), table)
        setattr(self.data.plots, 'fig' + str(plot_number), fig)
        return

    def plot10(self):
        #### plot data
        plot_number = 10
        plot_info, pat_filtered, title = self.get_period_plot_info(plot_number)
        # get only admitted patients
        pat_filtered = pat_filtered[pat_filtered['ADMISSION_FLAG'] == 1]

        #### ED hourly arrival discharge curves
        # make table for plot
        arr = pat_filtered[['ARRIVAL_hour','PSEUDONYMISED_PATIENT_ID']].groupby(['ARRIVAL_hour']).count()#.plot(ax=ax)
        dep = pat_filtered[['DEPARTURE_hour','PSEUDONYMISED_PATIENT_ID']].groupby(['DEPARTURE_hour']).count()#.plot(ax=ax)
        arr.rename(columns={'PSEUDONYMISED_PATIENT_ID':'Arrivals'},inplace=True)
        dep.rename(columns={'PSEUDONYMISED_PATIENT_ID':'Departures'},inplace=True)
        table = arr.merge(dep, left_index=True, right_index=True)

        
        # make mean attendance values
        no_days = len(pat_filtered.ARRIVAL_date.unique())
        table = table/no_days

        # plot
        fig, ax = plt.subplots()
        plt.suptitle(title)
        table.plot(ax=ax)
        ax.set_xticks(np.arange(0,25,2));

        #### save figure and table data
        setattr(self.data.plots, 'table' + str(plot_number), table)
        setattr(self.data.plots, 'fig' + str(plot_number), fig)
        return

    def plot15(self):
        #### plot data
        plot_number = 15
        daily = self.data.DAILY
        mask = (daily.index >= self.dt_start) & (daily.index <= self.dt_end)
        daily_filtered = daily[mask]        
        title = self.metadata.PLOT_LIST.query('plot_number == ' + str(plot_number))['plot_name'].values[0]

        
        fig,ax = plt.subplots()
        table = daily_filtered[['ED_arrivals','date_dayofweek']]
        table.boxplot(by='date_dayofweek',ax=ax);
        ax.set_xticklabels(daysofweek);
        ax.set_xlabel('');
        ax.set_ylabel('numbers of patients');
        fig.suptitle('');
        ax.set_title(title);

        #### save figure and table data
        setattr(self.data.plots, 'table' + str(plot_number), table)
        setattr(self.data.plots, 'fig' + str(plot_number), fig)

        return

    def plot16(self):

        #### plot data 
        plot_number = 16
        daily = self.data.DAILY
        mask = (daily.index >= self.dt_start) & (daily.index <= self.dt_end)
        daily_filtered = daily[mask]        
        title = self.metadata.PLOT_LIST.query('plot_number == ' + str(plot_number))['plot_name'].values[0]

        #### plot
        fig,ax = plt.subplots()
        table = daily_filtered[['IP_admissions_elec_nonelec','date_dayofweek']]
        table.boxplot(by='date_dayofweek',ax=ax);
        ax.set_xticklabels(daysofweek);
        ax.set_xlabel('');
        ax.set_ylabel('numbers of patients');
        fig.suptitle('');
        ax.set_title(title);

        #### save figure and table data
        setattr(self.data.plots, 'table' + str(plot_number), table)
        setattr(self.data.plots, 'fig' + str(plot_number), fig)


        return

    def plot17(self):

        plot_number = 17
        daily = self.data.DAILY
        mask = (daily.index >= self.dt_start) & (daily.index <= self.dt_end)
        daily_filtered = daily[mask]        
        title = self.metadata.PLOT_LIST.query('plot_number == ' + str(plot_number))['plot_name'].values[0]

        #### plot
        fig,ax = plt.subplots()
        table = daily_filtered[['EDocc_total_MAX','date_dayofweek']]
        table.boxplot(by='date_dayofweek',ax=ax);
        ax.set_xticklabels(daysofweek);
        ax.set_xlabel('');
        ax.set_ylabel('numbers of patients');
        fig.suptitle('');
        ax.set_title(title);

        setattr(self.data.plots, 'table' + str(plot_number), table)
        setattr(self.data.plots, 'fig' + str(plot_number), fig)

        return

    def plot18(self):

        plot_number = 18
        daily = self.data.DAILY
        mask = (daily.index >= self.dt_start) & (daily.index <= self.dt_end)
        daily_filtered = daily[mask]        
        title = self.metadata.PLOT_LIST.query('plot_number == ' + str(plot_number))['plot_name'].values[0]

        #### plot
        fig,ax = plt.subplots()
        table = daily_filtered[['EDocc_total_MAX','date_month']]
        table.boxplot(by='date_month',ax=ax);
        # ax.set_xticklabels(daysofweek);
        ax.set_xlabel('');
        ax.set_ylabel('numbers of patients');
        fig.suptitle('');
        ax.set_title(title);

        setattr(self.data.plots, 'table' + str(plot_number), table)
        setattr(self.data.plots, 'fig' + str(plot_number), fig)
        return


    def plot21(self):

        plot_number = 21
        daily = self.data.DAILY
        mask = (daily.index >= self.dt_start) & (daily.index <= self.dt_end)
        daily_filtered = daily[mask]        
        title = self.metadata.PLOT_LIST.query('plot_number == ' + str(plot_number))['plot_name'].values[0]

        #### plot
        fig,ax = plt.subplots()
        table = daily_filtered[['IPocc_elec_nonelec_MAX','date_dayofweek']]
        table.boxplot(by='date_dayofweek',ax=ax);
        ax.set_xticklabels(daysofweek);
        ax.set_xlabel('');
        ax.set_ylabel('numbers of patients');
        fig.suptitle('');
        ax.set_title(title);

        setattr(self.data.plots, 'table' + str(plot_number), table)
        setattr(self.data.plots, 'fig' + str(plot_number), fig)

        return

    def plot22(self):

        plot_number = 22
        daily = self.data.DAILY
        mask = (daily.index >= self.dt_start) & (daily.index <= self.dt_end)
        daily_filtered = daily[mask]        
        title = self.metadata.PLOT_LIST.query('plot_number == ' + str(plot_number))['plot_name'].values[0]

        #### plot
        fig,ax = plt.subplots()
        table = daily_filtered[['IPocc_elec_nonelec_MAX','date_month']]
        table.boxplot(by='date_month',ax=ax);
        # ax.set_xticklabels(daysofweek);
        ax.set_xlabel('');
        ax.set_ylabel('numbers of patients');
        fig.suptitle('');
        ax.set_title(title);

        setattr(self.data.plots, 'table' + str(plot_number), table)
        setattr(self.data.plots, 'fig' + str(plot_number), fig)
        return

    def get_period_plot_info(self, plot_number):
        """ Provided plot number retrieve plot info and filtered dataframe for patient level data.
        Only gets 'ED' (patient) data at present. """
        #### plot data
        plot_info = self.metadata.PLOT_LIST.query('plot_number == plot_number')
        #### ED hourly arrival discharge curves
        # filter for period selected
        pat = getattr(self.data, 'ED')
        # pat = self.data.ED
        mask = (pat['ARRIVAL_DTTM'] > self.dt_start) & (pat['DEPARTURE_DTTM'] < self.dt_end) # NOTE: mask will miss the overnight patients at beginning and end days of period. At present all plots are expected to be for a year/significnat period and so small difference in plots expected.
        pat_filtered = pat[mask]
        
        title = plot_info.query('plot_number == ' + str(plot_number))['plot_name'].values[0]

        return(plot_info, pat_filtered, title)
    



class WeeklyPlotting:
    """ Class produces weekly plots for week commencing when the user has input. """
    def __init__(self, data, metadata, dt_weekstart, required_plot_no):
        #### initialise all data
        self.data = data
        self.metadata = metadata
        self.dt_weekstart = dt_weekstart

        #### get only period plots in list
        plot_list = self.metadata.PLOT_LIST
        plot_list_period = plot_list.query('plot_type == "weekly"')
        
        #### call all plot methods unless required_plot_no
        if required_plot_no == 'all':
            for plot_no in plot_list_period.plot_number.values: #### NOTE: must rerplace this with list from general - once creater (filter for Period only plots)
                exec('self.' + 'plot' + str(plot_no) +'()')
        else:
            exec('self.' + 'plot' + str(required_plot_no) + '()')
        return
    
    def plot23(self):
        """ Creates plots and tables for a week of ED activity: plot of occupancy & of arrivals/departures """
        # data
        plot_number = 23
        days = 7
        df = self.data.HOURLY

        size = (13,7)
        #### get start and end times as datetimes
        # s = pd.datetime(start[0],start[1],start[2])
        s = self.dt_weekstart
        print(s)
        e = s + pd.Timedelta(days,unit='d')
        
        #### check and warn if start time is not a monday
        if s.weekday() != 0:
            print('Warning: date does not start on a Monday, day:' + str(s.weekday()))
            #warnings.warn('The date does not start on a monday.')
        
        #### ED occ plot
        EDocccols = ['EDocc_total','EDocc_breaching_patients','EDocc_awaiting_adm']
        # name  = '-'.join([str(x) for x in start]) + '_ED_occ' +  addname
        figA, axA = plt.subplots()
        tableA = df[s:e][EDocccols]
        tableA.plot.area(stacked=False,figsize=size,ax=axA)
        axA.set_ylim(0,50)
        axA.set_ylabel('Number of patients in ED')
        axA.legend(frameon=True)
    #     fig.savefig('./../hhft/visualisataions_for_hhft_slides(IP)/plots/' + name + '.png', dpi=300)
        
        
        #### ED adm/dis plot
        EDflowcols = ['ED_arrivals','ED_departures']
        # name  = '-'.join([str(x) for x in start]) + '_ED_flow' +  addname
        figB, axB = plt.subplots()
        tableB = df[s:e][EDflowcols].rolling(3).mean()
        tableB.plot(figsize=size,ax=axB)
        axB.set_ylim(0,25)
        axB.set_ylabel('Number of attendances and leaving ED per hour')
        axB.legend(frameon=True)
    #     fig.savefig('./../hhft/visualisataions_for_hhft_slides(IP)/plots/' + name + '.png', dpi=300)

        setattr(self.data.plots, 'table' + str(plot_number) + 'A', tableA)
        setattr(self.data.plots, 'fig' + str(plot_number) + 'A', figA)

        setattr(self.data.plots, 'table' + str(plot_number) + 'B', tableB)
        setattr(self.data.plots, 'fig' + str(plot_number) + 'B', figB)
        
        return

    def plot24(self):
        """ Creates plots and tables for a week of IP activity: plot of occupancy & of arrivals/departures. """
        # data
        plot_number = 24
        days = 7
        df = self.data.HOURLY

        size = (13,7)
        #### get start and end times as datetimes
        # s = pd.datetime(start[0],start[1],start[2])
        s = self.dt_weekstart
        print(s)
        e = s + pd.Timedelta(days,unit='d')
        
        #### check and warn if start time is not a monday
        if s.weekday() != 0:
            print('Warning: date does not start on a Monday, day:' + str(s.weekday()))
            #warnings.warn('The date does not start on a monday.')

        #### IP occ plot
        IPocccols = ['IPocc_total','IPocc_elec_nonelec','IPocc_daycases','IPocc_elec']
        # name  = '-'.join([str(x) for x in start]) + '_IP_occ' +  addname
        figA, axA = plt.subplots()
        tableA = df[s:e][IPocccols]
        tableA.plot.area(stacked=False,figsize=size,ax=axA)
        axA.set_ylim(0,550)
        axA.set_ylabel('Number of attendances and leaving ED per hour')
        axA.legend(frameon=True)
        #     fig.savefig('./../hhft/visualisataions_for_hhft_slides(IP)/plots/' + name + '.png', dpi=300)
        
        #### IP adm/dis plot
        IPcols = ['IP_admissions_total','IP_discharges_total']
        # name  = '-'.join([str(x) for x in start]) + '_IP_flow' +  addname
        figB, axB = plt.subplots()
        tableB = df[s:e][IPcols].rolling(1).mean()
        tableB.plot(figsize=size,ax=axB);
        axB.set_ylim(0,50)
        axB.set_ylabel('Number of inpatients')
        axB.legend(frameon=True)

        setattr(self.data.plots, 'table' + str(plot_number) + 'A', tableA)
        setattr(self.data.plots, 'fig' + str(plot_number) + 'A', figA)
        
        setattr(self.data.plots, 'table' + str(plot_number) + 'B', tableB)
        setattr(self.data.plots, 'fig' + str(plot_number) + 'B', figB)
        
        return


