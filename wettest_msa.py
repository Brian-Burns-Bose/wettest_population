"""
Please see README.md for requirements and overview.
Make sure to run ./data.sh to download data sources.
"""

import pandas as pd
import numpy as np

#read the csv file into a DataFrame.
hourly_raw = pd.read_csv(
    './data/201505precip.txt', 
    usecols=[0,1,2,3],
    na_values={'Precipitation': [' ', '  T']}
)

#rename the Wban column to match the station data.
hourly_raw.rename(columns={'Wban': 'WBAN', 'Precipitation': 'Precip'}, inplace=True)

#get rid of rows that have null values.  This will shrink the size of our DataFrame.
hourly_trimmed = hourly_raw.dropna(axis=0, how='any')

#get rid of precip values between midight and 7am.
hourly_clean = hourly_trimmed[
    (hourly_trimmed['Hour'] >= 7) & 
    (hourly_trimmed['Hour'] <= 23)]

#sum for each WBAN
totals_df = hourly_clean.groupby('WBAN').agg({'Precip': 'sum'})

#create the station data DataFrame.  Make sure we load only the relevant columns.
stations_df = pd.read_csv('./data/201505station.txt', 
                          sep='|',
                          usecols=['WBAN', 'Latitude', 'Longitude', 'Location'])

#join the totals DataFrame.
stations_hourly = totals_df.join(stations_df.set_index('WBAN')).reset_index()

from geopandas import GeoSeries, GeoDataFrame, read_file, sjoin
from shapely.geometry import Point

#create a list of Point objects.  
#zip operates on 2 lists yielding paired values. 
#use python's list comprehension to build a list of Points.
geometry = [Point(xy) for xy in zip(stations_hourly.Longitude, stations_hourly.Latitude)]

#Convert to GeoDataFrame.
geo_df = GeoDataFrame(stations_hourly, crs={'init': 'epsg:4269'}, geometry=geometry)

#Load the shapefile as a GeoDataFrame.
shape_df = read_file('./data/shape/cb_2015_us_cbsa_500k.shp')

#The shapefile meta data contains both metropolitan (M1) and micropolitan data (M2).  
#We only care about metropolitan areas.
shape_df = shape_df.loc[shape_df['LSAD'] == 'M1']

#drop unused columns
shape_df.drop(['ALAND','AWATER','CBSAFP','CSAFP','LSAD','AFFGEOID','GEOID'], axis=1, inplace=True)

#do the spaital join.  
#This will join rows where the Point is contained 
#in the Polygon defined in shape DataFrame.
msa_df = sjoin(geo_df, shape_df, how="inner", op='within').drop('index_right',axis=1)
msa_mean_df = msa_df.groupby('NAME').agg({'Precip':'mean'})

#Load the excel file. Make sure we skip over the micropolitan entries.
pop = pd.read_excel(
    './data/CPH-T-5.xls', 
    usecols=[0,2],
    header=0,
    names=['MSA', 'Population'],
    skiprows=range(0,7),
    skip_footer=(955 - 389)
)

#join with our previous dataframe.
msa_pop = msa_mean_df.join(pop.set_index('MSA'))

#Add the wetness column.
msa_pop['Wetness'] = msa_pop.apply(lambda row: row['Precip'] * row['Population'], axis=1)

#Display the results
print(msa_pop.sort_values('Wetness', ascending=False).head(25))
