#!/bin/bash

mkdir -p ./data/shape

wget -O ./data/CPH-T-5.xls https://www.census.gov/population/www/cen2010/cph-t/CPH-T-5.xls 
wget -O ./data/QCLCD201505.zip http://www.ncdc.noaa.gov/orders/qclcd/QCLCD201505.zip 
unzip -o ./data/QCLCD201505.zip -d ./data

wget -O ./data/shape/cb_2015_us_cbsa_500k.zip http://www2.census.gov/geo/tiger/GENZ2015/shp/cb_2015_us_cbsa_500k.zip
unzip -o ./data/shape/cb_2015_us_cbsa_500k.zip -d ./data/shape
