import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import seaborn as sns


sns.set() # set for nice looking plots
daysofweek = ['Mon','Tue','Wed','Thur','Fri','Sat','Sun']

class HistoricalPlotting:
    """ Class produces all historical plots automatically. """
    def __init__(self, data, metadata, EDyears, IPyears, required_plot_no):
        
        pass


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
        plot_info, pat_filtered, title = self.get_period_plot_info(plot_number, 'ED')

        #### additional cleaning for waiting times
        exclude_index = pat_filtered.query('arr_triage_wait < 0 or arr_dr_wait < 0 or arr_adm_req_wait < 0 or waiting_time < 0'
                          +'or arr_triage_wait > 24*60 or arr_dr_wait > 24*60 or arr_adm_req_wait > 24*60'
                          'or waiting_time > 24*60' + 'or adm_req_dep_wait < 0 or dr_adm_req_wait <0 or dr_dep_wait < 0'
                          ).index

        pat2 = pat_filtered.loc[~pat_filtered.index.isin(exclude_index)]

        wait_col2 = ['arr_dr_wait','dr_adm_req_wait','adm_req_dep_wait','dr_dep_wait']

        #### plot
        fig, ax = plt.subplots()
        table = pat2.groupby('ADMISSION_FLAG')[wait_col2[0],wait_col2[3]].median()
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
        plot_info, pat_filtered, title = self.get_period_plot_info(plot_number, 'ED')

        #### additional cleaning for waiting times
        exclude_index = pat_filtered.query('arr_triage_wait < 0 or arr_dr_wait < 0 or arr_adm_req_wait < 0 or waiting_time < 0'
                          +'or arr_triage_wait > 24*60 or arr_dr_wait > 24*60 or arr_adm_req_wait > 24*60'
                          'or waiting_time > 24*60' + 'or adm_req_dep_wait < 0 or dr_adm_req_wait <0 or dr_dep_wait < 0'
                          ).index

        pat2 = pat_filtered.loc[~pat_filtered.index.isin(exclude_index)]

        wait_col2 = ['arr_dr_wait','dr_adm_req_wait','adm_req_dep_wait','dr_dep_wait']

        #### plot
        fig, ax = plt.subplots()
        table = pat2.groupby('ADMISSION_FLAG')[wait_col2].median()
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
        plot_info, pat_filtered, title = self.get_period_plot_info(plot_number, 'ED')

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
        ax.set_ylim([0,500]); # consider supressing auto scale?
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
        plot_info, pat_filtered, title = self.get_period_plot_info(plot_number, 'ED')

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
        ax[0].legend(frameon=True)

        tableB = pat2[pat2.ADMISSION_FLAG == 1].groupby('ARRIVAL_hour')[wait_col2[0],wait_col2[3]].median()
        tableB.plot.bar(stacked=True,ax=ax[1])
        ax[1].set_title('Admitted patients')
        ax[1].legend(frameon=True)

        ax[0].set_ylabel('Median patient waiting time (mins)');

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
        plot_info, pat_filtered, title = self.get_period_plot_info(plot_number, 'ED')

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
        ax[0].legend(frameon=True)

        tableB = pat2[pat2.ADMISSION_FLAG == 1].groupby('ARRIVAL_month')[wait_col2[0],wait_col2[3]].median()
        tableB.plot.bar(stacked=True,ax=ax[1])
        ax[1].set_title('Admitted patients')
        ax[1].legend(frameon=True)

        ax[0].set_ylabel('Median patient waiting time (mins)');

        fig.suptitle(title)

        #### save data
        setattr(self.data.plots, 'table' + str(plot_number) + 'A', tableA)
        setattr(self.data.plots, 'table' + str(plot_number) + 'B', tableB)
        setattr(self.data.plots, 'fig' + str(plot_number), fig)

        return





    def plot9(self):
        #### plot data
        plot_number = 9
        plot_info, pat_filtered, title = self.get_period_plot_info(plot_number, 'ED')

        #### ED hourly arrival discharge curves
        # make table for plot
        arr = pat_filtered[['ARRIVAL_hour','PSEUDONYMISED_PATIENT_ID']].groupby(['ARRIVAL_hour']).count()#.plot(ax=ax)
        dep = pat_filtered[['DEPARTURE_hour','PSEUDONYMISED_PATIENT_ID']].groupby(['DEPARTURE_hour']).count()#.plot(ax=ax)
        arr.rename(columns={'PSEUDONYMISED_PATIENT_ID':'Arrivals'},inplace=True)
        dep.rename(columns={'PSEUDONYMISED_PATIENT_ID':'Departures'},inplace=True)
        table = arr.merge(dep, left_index=True, right_index=True)

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
        plot_info, pat_filtered, title = self.get_period_plot_info(plot_number, 'ED')
        # get only admitted patients
        pat_filtered = pat_filtered[pat_filtered['ADMISSION_FLAG'] == 1]

        #### ED hourly arrival discharge curves
        # make table for plot
        arr = pat_filtered[['ARRIVAL_hour','PSEUDONYMISED_PATIENT_ID']].groupby(['ARRIVAL_hour']).count()#.plot(ax=ax)
        dep = pat_filtered[['DEPARTURE_hour','PSEUDONYMISED_PATIENT_ID']].groupby(['DEPARTURE_hour']).count()#.plot(ax=ax)
        arr.rename(columns={'PSEUDONYMISED_PATIENT_ID':'Arrivals'},inplace=True)
        dep.rename(columns={'PSEUDONYMISED_PATIENT_ID':'Departures'},inplace=True)
        table = arr.merge(dep, left_index=True, right_index=True)

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
        table = daily_filtered[['IP_admissions_excludingdaycases','date_dayofweek']]
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
        table = daily_filtered[['ED_occ_total_MAX','date_dayofweek']]
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
        table = daily_filtered[['ED_occ_total_MAX','date_month']]
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
        table = daily_filtered[['IPocc_excludingdaycases_MAX','date_dayofweek']]
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
        table = daily_filtered[['IPocc_excludingdaycases_MAX','date_month']]
        table.boxplot(by='date_month',ax=ax);
        # ax.set_xticklabels(daysofweek);
        ax.set_xlabel('');
        ax.set_ylabel('numbers of patients');
        fig.suptitle('');
        ax.set_title(title);

        setattr(self.data.plots, 'table' + str(plot_number), table)
        setattr(self.data.plots, 'fig' + str(plot_number), fig)
        return

    def get_period_plot_info(self, plot_number, data_name):
        """ Provided plot number retrieve plot info and filtered dataframe for patient level data. """
        #### plot data
        plot_info = self.metadata.PLOT_LIST.query('plot_number == plot_number')
        #### ED hourly arrival discharge curves
        # filter for period selected
        pat = getattr(self.data, data_name)
        # pat = self.data.ED
        mask = (pat['ARRIVAL_DTTM'] > self.dt_start) & (pat['DEPARTURE_DTTM'] < self.dt_end)
        pat_filtered = pat[mask]
        
        title = plot_info.query('plot_number == ' + str(plot_number))['plot_name'].values[0]

        return(plot_info, pat_filtered, title)
    



class WeeklyPlotting:
    """ Class produces weekly plots for week commencing when the user has input. """
    def __init__(self, data, metadata, dt_weekstart, required_plot_no):

        pass


