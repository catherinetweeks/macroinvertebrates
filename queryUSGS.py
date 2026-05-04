import requests
import json

def get_usgs_data(url, params):
    response = requests.get(url, params)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        return None
    
'''
results in ft^3/s
'''
def get_discharge(date):
    API_KEY = 'KCDOlfflItiUnC7gtzxgUjbMXFHgC5EofJ0PXSpR'
    url = 'https://api.waterdata.usgs.gov/ogcapi/v0/collections/continuous/items'
    params = {
        'api_key': API_KEY,
        'parameter_code' : '00060',
        'monitoring_location_id' : 'USGS-01171500',
        'datetime' : date
    }
    response = get_usgs_data(url,params=params)
    value = response['features'][0]['properties']['value']
    return value
'''
results in ft
'''
def get_gage_Height(date):
    API_KEY = 'KCDOlfflItiUnC7gtzxgUjbMXFHgC5EofJ0PXSpR'
    url = 'https://api.waterdata.usgs.gov/ogcapi/v0/collections/continuous/items'
    params = {
        'api_key': API_KEY,
        'parameter_code' : '00065',
        'monitoring_location_id' : 'USGS-01171500',
        'datetime' : date
    }
    response = get_usgs_data(url,params=params)
    value = response['features'][0]['properties']['value']
    return value
