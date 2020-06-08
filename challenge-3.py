

######## CHALLENGE 3 ########


# Iniitial libraries

import pandas as pd
import datetime

import pandas_datareader.data as web
import os
import requests


# I am interested in collecting county-level data on coronavirus deaths and cases
# for the state of Maryland, where I live. I retrieve a dataframe from the New
# York Times github page, which shares data on coronavirus deaths and cases across
# the U.S., disaggregated at the national, state, and county levels
# (https://github.com/nytimes/covid-19-data).

# First, I retrieve data at the county level and create a csv file in my own
# directory.

response = requests.get('https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-counties.csv')

data = response.text

with open(r'C:\Users\Shehryar\Documents\GitHub\shnabi\python-master\us-counties.csv', 'w') as ofile:
        ofile.write(data)

path = os.getcwd()

counties = pd.read_csv(os.path.join(path, 'us-counties.csv'), encoding='latin-1')

# Then, I filter the dataframe to only include counties in Maryland, and save it
# to a new dataframe.

MD_counties = counties[counties['state'] == 'Maryland']


# Total cases and deaths by counties in Maryland

grouped_counties = MD_counties.groupby('county')

grouped_counties.sum()['cases']
grouped_counties.sum()['deaths']

grouped_counties.sum()['deaths']/grouped_counties.sum()['cases']



#
# response = requests.get('https://scorecard.prosperitynow.org/get-csv?file=csv-data-table%2F51510-48de0db2d0d9c47d9bb9406c97ec860f.csv')
#
# response.text
# data = response.text
#
# with open(r'C:\Users\Shehryar\Documents\GitHub\shnabi\python-master\dmv.csv', 'w') as ofile:
#     ofile.write(data)
#
# os.chdir(path)
# path = os.getcwd()
#
# dmv = pd.read_csv(os.path.join(path, 'dmv.csv'))
# dmv
# dmv.drop(0)
#
# dmv.drop([])
