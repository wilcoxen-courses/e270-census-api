#! /bin/python3
#  Spring 2020 (PJW)

import requests
import pandas as pd

pd.set_option('display.max_rows',None)

#
#  Demonstrate the Census Surname endpoint
#

api = 'https://api.census.gov/data/2010/surname'

get_what = 'COUNT,RANK'

#%%

payload = { 'get':get_what, 'NAME':'SMITH' }
response = requests.get(api,payload)

print( '\n' )
print( 'url:', response.url )
print( 'status:', response.status_code )
print( response.text )

#%%

payload = { 'get':get_what, 'NAME':'ZUCKERBERG' }
response = requests.get(api,payload)

print( '\n' )
print( 'url:', response.url )
print( 'status:', response.status_code )
print( response.text )

#%%

#
#  Demonstrate the Census ACS5 endpoint
#
#     B01001_001E -- total
#     B01001_002E -- male
#     B01001_026E -- female
#

api = 'https://api.census.gov/data/2018/acs/acs5'

var_list = ['B01001_001E','B01001_002E','B01001_026E']

variables = 'NAME,'+','.join(var_list)

for_clause = 'county:*'
in_clause = 'state:36'

payload = { 'get':variables, 'for':for_clause, 'in':in_clause }

response = requests.get(api,payload)

print( '\n' )
print( 'url:', response.url )
print( 'status:', response.status_code )
print( response.text )

#%%

rows = response.json() 

colnames = rows[0]
datarows = rows[1:]

popframe = pd.DataFrame(columns=colnames,data=datarows)
popframe.set_index('NAME',inplace=True)
popframe[var_list] = popframe[var_list].astype(int)

popframe['check'] = popframe['B01001_002E'] + popframe['B01001_026E']
popframe['error'] = popframe['B01001_001E'] - popframe['check']

popframe['ratio'] = round(popframe['B01001_002E']/popframe['B01001_026E'],2)

print(popframe)
