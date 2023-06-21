# -*- coding: utf-8 -*-
"""
Created on Tue Jan 19 14:03:04 2016

@author: Administrator"""

import pandas as pd
import requests
import json
import time
import io
import plotly.express as px
import os
from googlesearch import search # get zpid
pwd = os.getcwd()
# show all columns
pd.set_option('display.max_columns', None)

def get_zpid(street=None, city=None, state=None, zip_code=None, full_address=None):
  # get search query string
  if full_address == None:
    try:
      query = '{0}, {1}, {2} {3} zillow home details'.format(street, city, state, str(zip_code))
    except:
      return 'Please enter a query string or address details'
  else:
    query = full_address + ' zillow home details'

  # get google search results
  search_results = search(query, tld='com', lang='en', num=3, start=0, stop=1, pause=0)
  search_results_list = [u for u in search_results]
  url = search_results_list[0] # extract first returned result
  
  # return zpid
  try:
    return [x for x in url.split('/') if 'zpid' in x][0].split('_')[0]
  except:
    return None

def get_property_detail(rapid_api_key, zpid):
  # get property details from API
  url = "https://zillow-com1.p.rapidapi.com/property"

  querystring = {"zpid":zpid} # zpid

  headers = {
    "X-RapidAPI-Host": "zillow-com1.p.rapidapi.com",
    "X-RapidAPI-Key": rapid_api_key
  }

  # request data
  return requests.request("GET", url, headers=headers, params=querystring)

# read in api key file
df_api_keys = pd.read_csv(pwd + '/api_keys.csv')

# get keys
rapid_api_key = df_api_keys.loc[df_api_keys['API'] =='rapid']['KEY'].iloc[0]

# property address
property_address = "11622 Pure Pebble Dr, RIVERVIEW, FL 33569" # https://www.zillow.com/homedetails/11622-Pure-Pebble-Dr-Riverview-FL-33569/66718658_zpid/

# search query
query = property_address + ' zillow home details'
print('Searching for query: ', query)

# google search results
search_results = search(query, tld='com', lang='en', num=3, start=0, stop=3, pause=0)
search_results_list = [u for u in search_results] # get all results
print (search_results_list)

# get the first search result
url = search_results_list[0] # extract first returned result
print (url)

# extract the zpid
zpid = [x for x in url.split('/') if 'zpid' in x][0].split('_')[0]
print('Zpid of the property is:', zpid )

# get property details from API
url = "https://zillow-com1.p.rapidapi.com/property"

querystring = {"zpid":zpid} # zpid

headers = {
	"X-RapidAPI-Host": "zillow-com1.p.rapidapi.com",
	"X-RapidAPI-Key": rapid_api_key # your key here
    }

# request data
response = requests.request("GET", url, headers=headers, params=querystring)
# show success
response.status_code

#print raw output
print (response.json())

# transform data to pandas dataframe
df_property_detail = pd.json_normalize(data=response.json())
print('Num of rows:', len(df_property_detail))
print('Num of cols:', len(df_property_detail.columns))
df_property_detail.head()

# retrieve property detail elements
bedrooms = df_property_detail['bedrooms'].iloc[0]
bathrooms = df_property_detail['bathrooms'].iloc[0]
year_built = df_property_detail['yearBuilt'].iloc[0]
property_type = df_property_detail['homeType'].iloc[0]
living_area = df_property_detail['resoFacts.livingArea'].iloc[0]
lot_size = df_property_detail['resoFacts.lotSize'].iloc[0]
lot_dimensions = df_property_detail['resoFacts.lotSizeDimensions'].iloc[0]
zoning = df_property_detail['resoFacts.zoning'].iloc[0]
zestimate = df_property_detail['zestimate'].iloc[0]
rent_zestimate = df_property_detail['rentZestimate'].iloc[0]

print('Property Details for: ', property_address)
print('  Bedrooms: {}'.format( bedrooms))
print('  Bathrooms: {}'.format( bathrooms))
print('  Year Built: {}'.format( year_built))
print('  Living Area: {}'.format( living_area))
print('  Lot Size: {}'.format( lot_size))
print('  Lot Dimensions: {}'.format( lot_dimensions))
print('  Zoning: {}'.format( zoning))
print('  Property Type: {}'.format( property_type))
print('  Zestimate: ${:,.0f}'.format( zestimate))
print('  Rent Zestimate: ${:,.0f}'.format( rent_zestimate))

# save to csv
df_property_detail.to_csv(pwd + '/output.csv', index=False)