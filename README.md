# hospital-flow

Project to explore automation of hospital flow work in a scalable manner.

#### to install dependencies....
conda env create\
activate hospital-flow

#### installing python
If are new to python then the easiest way to get up and running is to download
the anaconda distribution of python:
https://www.anaconda.com/download/

#### creating a python environment
Creating an environment should be the easiest way to ensure that you can run
our code sucessfully. To do this:
- navigate to your directory which should contain the downloaded files (.csv, .yml, .ipynb)
- open command prompt (terminal in mac)
- type: 'conda env create'
- type: 'activate hospital-flow' ('source activate hospital-flow' in mac)

#### running the script



#### to-do
- resolve pink copy warning in create arrival_datetime columns
- bug: ioED.loadRAW and loadCLEAN
- question that required_cols in expected file strucutre are all required in the end! remove: arrival_date, arrival_time,
- make check column dtypes only operate on pat, day, week cols as appropriate..(need seperate name dictionary for day data etc.)

ED day: ED_arrivals', 'ED_age_median', 'ED_discharges', 'ED_admissions',
       'ED_breaches', 'ED_minutes_used', 'ED_mean_patient_minutes',
       'ED_conversion_ratio', 'ED_breaches_perc', 'ED_date', 'ED_year',
       'ED_month', 'ED_dayofweek', 'ED_weekday_name'


- _loadRAW/_loadCLEAN : make option so that ioED will only load ED files. Use select_loc = None as option?
