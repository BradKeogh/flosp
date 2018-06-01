# flosp
Project to explore automation of patient FLow in hOSPitals work in a scalable manner.

# Aims
- provide means to import and clean ED and inpatient hospital data quickly
- provide standard plotting/analysis outputs

# Objectives
- create module to import/clean/impose standard format/save ED data
- create similar for inpatient data
- create module for standard ED plotting/analysis
- create module for standard IP plotting/analysis




# install
#### to install dependencies....
conda env create
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

# running
#### running the script


# dev
#### to-do

- Gen: multiple instances of set_save_path method...look to make generic function.
- Gen: create test harness
- plotting.plotED: is a mess. Needs refactoring. Many repeated functions that could be made generic.
- ioED: fix data type catagory on age_group column
