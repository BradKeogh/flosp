import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import seaborn as sns


sns.set() # set for nice looking plots


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

    def plot9(self):
        #### plot data
        plot_number = 9
        plot_info = self.metadata.PLOT_LIST.query('plot_number == plot_number')
        #### ED hourly arrival discharge curves
        # filter for period selected
        pat = self.data.ED
        mask = (pat['ARRIVAL_DTTM'] > self.dt_start) & (pat['DEPARTURE_DTTM'] < self.dt_end)
        pat_filtered = pat[mask]

        # make table for plot
        arr = pat_filtered[['ARRIVAL_hour','PSEUDONYMISED_PATIENT_ID']].groupby(['ARRIVAL_hour']).count()#.plot(ax=ax)
        dep = pat_filtered[['DEPARTURE_hour','PSEUDONYMISED_PATIENT_ID']].groupby(['DEPARTURE_hour']).count()#.plot(ax=ax)
        arr.rename(columns={'PSEUDONYMISED_PATIENT_ID':'Arrivals'},inplace=True)
        dep.rename(columns={'PSEUDONYMISED_PATIENT_ID':'Departures'},inplace=True)
        table = arr.merge(dep, left_index=True, right_index=True)

        # plot
        fig, ax = plt.subplots()
        plt.suptitle(plot_info['plot_name'].values[0])
        table.plot(ax=ax)
        ax.set_xticks(np.arange(0,25,2));

        #### save figure and table data
        setattr(self.data.plots, 'table' + str(plot_number), table)
        setattr(self.data.plots, 'fig' + str(plot_number), fig)
        return
    



class WeeklyPlotting:
    """ Class produces weekly plots for week commencing when the user has input. """
    def __init__(self, data, metadata, dt_weekstart, required_plot_no):

        pass
