import sys, getopt
import os
import numpy as np
import pandas as pd
from itertools import combinations_with_replacement
from netCDF4 import Dataset
from datetime import datetime
import calendar
import pathlib

path='D:\\CCAP\\LOCA\\netcdf'
os.chdir(path)

rcp85_seq = list(range(1,19,2))

#df_size = list(range(0,(precip.shape[1] -1))

lat_lon = list(combinations_with_replacement([0,1], 2)) 

tp = tp = tuple(reversed(ls[1])) 

lat_lon.append(tp)

grid = pd.DataFrame()

gridAll = pd.DataFrame()
# define the path

currentDirectory = pathlib.Path('.')

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
SM may have done this research in that past- VR needs to check but looks like RCP85 is odd numer sequence of columns
'''

	 for i in range(0,len(lat_lon)):
        df = pd.DataFrame(precip[0:precip.shape[0], 0:precip.shape[1], lat_lon[i][0], lat_lon[i][1]])
        subgrid = df.transpose()
        subgrid = subgrid.loc[:, loca.columns.isin(rcp85_seq)]
        subgrid.columns = ['Model1', 'Model2', 'Model3', 'Model4', 'Model5', 'Model6', 'Model7', 'Model8', 'Model9']
        subgrid['date']= pd.date_range(start='1950-01-01', end='2100-01-01', closed='left')
        subgrid['latlon'] = np.repeat(str(lat_lon[i]),precip.shape[1])
        subgrid['SubgridName'] = np.repeat('SubGrid' + '' + str(i), precip.shape[1])
        subgrid['gridName'] = np.repeat(gridname, precip.shape[1])
        grid = grid.append(subgrid, ignore_index = False)

'''

repeat same for wach netcdf file and append to a new pandas dataframe

'''

	gridAll = gridAll.append(grid, ignore_index = False)

gridWorking = gridAll.copy()

gridWorking = gridWorking[gridWorking.columns[0:10]]

loca = gridWorking.groupby('date').mean()

loca.reset_index(inplace= True)

#write to csv

loca.to_csv(index = False)