

######## CHALLENGE 3 ########


# Iniitial libraries

import pandas as pd
import numpy as np
import datetime
from dateutil import parser

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


# My first graph will show the change in total cases and deaths in Maryland
# over time on a log scale.

# I begin by creating a new dataframe that is grouped by date and totals cases
# and deaths across counties in Maryland.

grouped_date = MD_counties.groupby('date')
MD_deaths_cases = grouped_date.sum()
MD_deaths_cases = MD_deaths_cases.reset_index()

# Here, I convert dates to the datetime format.

MD_deaths_cases['date'] = [parser.parse(i) for i in MD_deaths_cases['date']]

# Finally, I add variables for cases and deaths that show their log values.

MD_deaths_cases['log_cases'] = np.log(MD_deaths_cases['cases'])
MD_deaths_cases['log_deaths'] = [np.log(i + 1) if 0 in MD_deaths_cases['deaths'] else np.log(MD_deaths_cases['deaths']) for i in MD_deaths_cases['deaths']]

# Now I start plotting. I need the following libraries.

import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter
import seaborn as sns

# I set the format in which I want dates to appear on the x axis.

date_form = DateFormatter("%m-%d")

# Plot parameters:

fig, ax = plt.subplots()
plt.xlabel('Date')
cases = ax.plot(MD_deaths_cases['date'], MD_deaths_cases['log_cases'], 'b-', label='Log Cases')
plt.ylabel('Log Cases')
ax2 = ax.twinx()
deaths = ax2.plot(MD_deaths_cases['date'], MD_deaths_cases['log_deaths'], 'r-', label='Log Deaths')
plt.ylabel('Log Deaths')
ax.xaxis.set_major_formatter(date_form)
plt.title('COVID-19 Total Cases and Deaths in Maryland')
plots = cases + deaths
labs = [l.get_label() for l in plots]
plt.legend(plots, labs, loc=0)
plt.savefig(os.path.join(path, 'covid_total_MD'))
plt.show()

# We can see a flattening of the increase in total COVID-19 deaths and cases
# in Maryland over time.


# My second graph looks at new daily cases and deaths in Maryland.

fig, ax = plt.subplots()
plt.xlabel('Date')
cases = ax.plot(MD_deaths_cases['date'], MD_deaths_cases['cases'].diff(), 'b-', label='Cases')
plt.ylabel('Cases')
ax2 = ax.twinx()
deaths = ax2.plot(MD_deaths_cases['date'], MD_deaths_cases['deaths'].diff(), 'r-', label='Deaths')
plt.ylabel('Deaths')
ax.xaxis.set_major_formatter(date_form)
plt.title('Daily New COVID-19 Cases and Deaths in Maryland')
plots = cases + deaths
labs = [l.get_label() for l in plots]
plt.legend(plots, labs)
plt.savefig(os.path.join(path, 'covid_daily_new_MD'))
plt.show()

# New daily cases and deaths initially increased but have on average decreased
# over time.


# From here, I will create two scatterplots.

# First, in response to reports showing that black people are affected by COVID-19 at
# disproportionately higher rates than white people, I am interested in examining
# the relationship between black population as a share of total county population
# and COVID-19 death rate by county.

# I begin by loading county-based data from the American Community Survey (ACS).
# I downloaded this data from IPUMS and extracted it as a CSV in R (I have uploaded
# my R code for that in my GitHub repository).

counties_data = pd.read_csv(os.path.join(path, 'counties_data.csv'))

county_list = list(set(MD_counties['county']))

# Next, I replace county fips codes with county names. County fips codes
# obtained here: https://en.wikipedia.org/wiki/List_of_counties_in_Maryland

county_fips = {33: "Prince George's",
               29: 'Kent',
               5: 'Baltimore',
               41: 'Talbot',
               11: 'Caroline',
               13: 'Carroll',
               19: 'Dorchester',
               15: 'Cecil',
               0: 'Unknown',
               47: 'Worcester',
               31: 'Montgomery',
               21: 'Frederick',
               17: 'Charles',
               45: 'Wicomico',
               510: 'Baltimore city',
               27: 'Howard',
               1: 'Allegany',
               23: 'Garrett',
               3: 'Anne Arundel',
               43: 'Washington',
               35: "Queen Anne's",
               39: 'Somerset',
               25: 'Harford',
               37: "St. Mary's",
               9: 'Calvert'}

county_fips = {str(k):v for k,v in county_fips.items()}
counties_data['COUNTYFIP'] = counties_data['COUNTYFIP'].map(str)
counties_data['COUNTYFIP'] =  counties_data['COUNTYFIP'].map(county_fips)

# Now I construct a new dataframe, "select_counties", that includes death rates
# per 1000 people per county and the percentage of black people as a share of each county's
# population. I call it "select_counties" because I could not find this information
# from the IPUMS ACS data I used for all counties.

# Isolating black population per county from my county data:

county_race_groups = counties_data.groupby(['COUNTYFIP', 'RACE'])['RACE']
county_pop = county_race_groups.apply(lambda g: len(list(g))).unstack().reset_index().sum(axis = 1)
black_per_county = county_race_groups.apply(lambda g: len(list(g))).unstack()[2]

# Calculating black share of county population and adding it to select_counties.

pct_black = [(a/b)*100 for a,b in zip(black_per_county, county_pops)]
select_counties = pd.DataFrame(black_per_county).reset_index()
select_counties['pct_black'] = pct_black

# Calculating deaths per 1000 people and adding it to select_counties.

death_per_1000 = MD_counties.groupby('county').sum()['deaths']/1000
select_counties.rename(columns = {'COUNTYFIP':'county'}, inplace=True)
select_counties = select_counties.merge(death_per_1000, on='county', how='inner')

# Scatterplot:

sns.scatterplot(x='pct_black', y='deaths', data=select_counties)
plt.ylabel('Deaths per 1000 people')
plt.xlabel('Black share of population (%)')
plt.title('Deaths per 1000 people in MD counties by black share of population');
plt.savefig(os.path.join(path, 'deaths_black_county_MD'))
plt.show()

# It appears that where black people compose a higher share of the population,
# there tend to be more COVID-19 deaths per 1000 people. However, there are
# outliers that invite further investigation.


# For my second scatterplot, I add a measure of population density from
# ACS data to select_counties. This measures population
# per square mile. Since the density differed within the county depending on
# strata, I took the mean population densities for each county.

density = counties_data.groupby('COUNTYFIP')['DENSITY'].mean().reset_index()
density.rename(columns = {'COUNTYFIP':'county'}, inplace=True)
density.rename(columns = {'DENSITY':'density'}, inplace=True)
select_counties = select_counties.merge(density, on='county', how='inner')

# Scatterplot:

sns.scatterplot(x='density', y='deaths', data=select_counties)
plt.ylabel('Deaths per 1000 people')
plt.xlabel('Population density')
plt.title('Deaths per 1000 people in MD counties by population density')
plt.savefig(os.path.join(path, 'deaths_density_county_MD'))
plt.show()

# Counties with greater density see higher COVID-19 deaths per 1000 people. It is
# noteworthy that the county with the most density has lower deaths than we would
# expect.
