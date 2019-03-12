''' Get python packages

'''

import sys, getopt
import os
import numpy as np
import pandas as pd
from itertools import combinations_with_replacement
from netCDF4 import Dataset
from datetime import datetime
import calendar
import pathlib

'''Set your local working directory that has the netcdf files
'''
path='D:\\CCAP\\LOCA\\netcdf'
os.chdir(path)

'''
Netcdf files were downloaded for both RCP 4.5 and RCP 8.5
For this analysis, only RCP 8.5 is used

Totally 9 models are analyslized. The netcdf comes with totally 18 columns.
Every alternate column starting from column index 1 is RCP 8.5
Strating at Column 0, alternate columns are RCP 4.5

'''

'''to get only RCP 8.5 associated columns
'''
rcp85_seq = list(range(1,19,2))

#df_size = list(range(0,(precip.shape[1] -1))
''' 
lat and lon location indices for each subgrid within a single grid

'''
lat_lon = list(combinations_with_replacement([0,1], 2)) 

tp = tp = tuple(reversed(ls[1])) 

lat_lon.append(tp)

#Emty pandas dataframe
grid = pd.DataFrame()

#Empty pandas dataframe
gridAll = pd.DataFrame()

# define the path
currentDirectory = pathlib.Path('.')

# Call all netcdf files only
currentPattern = "*.nc"

for currentFile in currentDirectory.glob(currentPattern):

#file_name = 'Extraxtion_pr_grid1.nc'

	file_name = os.path.basename(currentFile)

	gridname = os.path.splitext(file_name)[0]

	nc = Dataset(currentFile, 'r', format = 'NETCDF3_CLASSIC')

	nc.variables.keys()

	nc.variables['pr'].dimensions 

	lat = nc.variables['lat'][:]
	
	lon = nc.variables['lon'][:]
	
	precip = nc.variables['pr'][:]

'''Each grid has 4 subgrids. The data for each subgrid can be extracted using lat/lon location of that subgrid.

'''

	 for i in range(0,len(lat_lon)):
        df = pd.DataFrame(precip[0:precip.shape[0], 0:precip.shape[1], lat_lon[i][0], lat_lon[i][1]])
        subgrid = df.transpose()
        subgrid = subgrid.loc[:, subgrid.columns.isin(rcp85_seq)]
        subgrid.columns = ['Model1', 'Model2', 'Model3', 'Model4', 'Model5', 'Model6', 'Model7', 'Model8', 'Model9']
        subgrid['date']= pd.date_range(start='1950-01-01', end='2100-01-01', closed='left')
        subgrid['latlon'] = np.repeat(str(lat_lon[i]),precip.shape[1])
        subgrid['SubgridName'] = np.repeat('SubGrid' + '' + str(i), precip.shape[1])
        subgrid['gridName'] = np.repeat(gridname, precip.shape[1])
        grid = grid.append(subgrid, ignore_index = False)

'''

repeat same for each netcdf file and append to a new pandas dataframe

'''

	gridAll = gridAll.append(grid, ignore_index = False)

#Make new working copy of the pandas dataframe
gridWorking = gridAll.copy()

gridWorking = gridWorking[gridWorking.columns[0:10]]

loca = gridWorking.groupby('date').mean()

loca.reset_index(inplace= True)

#write to csv

loca.to_csv('loca.csv', sep=',', encoding='utf-8', index =False)