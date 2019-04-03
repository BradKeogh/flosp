import pandas as pd

possible_pkls_list = ['ED.pkl','IP.pkl','IPSPELL.pkl','HOURLY.pkl','DAILY.pkl']

# Info about plots: plot number, plot name, ED or IP, DAILY, data required?, [historical, Period, week] 
cols = ['plot_number','plot_name','plot_type','data_required']
data = [
    [1, 'ED attendance and admission numbers by year','hist',['ED']],
    [2, 'ED attendance and admission numbers by year and age group','hist',['ED']],
    [3, 'Variation by admission or not','period',['ED']],
    [4, 'Variation by admission or not','period',['ED']],
    [5, 'Waiting time for admitted/non-admitted patients by year','hist',['ED']],
    [6, 'Waiting time distributions','period',['ED']],
    [7, 'Waiting times by hour of day','period',['ED']],
    [8, 'Waiting times by month of year', 'period',['ED']],
    [9, 'ED arrival and departure by hour of day','period',['ED']],
    [10, 'ED arrival and departure by hour of day (admitted)','period',['ED']],
    [11, 'Types of admission by year', 'hist',['IP']],
    [12, 'Admission by age group by year', 'hist', ['IP']],
    [13, 'Patient volume by type (table)', 'hist', ['IP']], # NOTE: S7 IP
    [14, 'Emergency patient admission route', 'hist', ['IP']],
    [15, 'Variation in ED attendance numbers by day of week', 'period', ['ED']],
    [16, 'Variation in Inpatient admission numbers by day of week (excluding day cases)', 'period', ['IP']],
    [17, 'Peak ED occupancy by day of week','period',['ED']],
    [18, 'Peak ED occupancy by month of year', 'period', ['ED']],
    [19, 'Average ED occupancy by month', 'hist', ['ED']],
    [20, 'Average inpatient occupancy by month', 'hist',['IP']],
    [21, 'Max inpatient occupancy by day of week','period',['IP']],
    [22, 'Max inpatient occupancy by month of year', 'period',['IP']],
    [23, 'ED occupancy','weekly',['ED']], # potential issue with this if there is no IP data - as aggregation to hourly may not have happened
    [24, 'Inpatient occupancy', 'weekly',['IP']],
    #NOTE: add tables for aggreagated explantion of admission rates/numbers etc. different weeks also.
]

plot_information_table = pd.DataFrame(data=data,columns = cols)

