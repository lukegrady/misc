#!/usr/bin/env python
'''
Based on something I saw on Upwork, need to get zip codes for addresses

So this turned into me learning about google maps geocode api
'''

import requests
import googlemaps

def zip_from_address(address):
    '''Look up zip code for address using google maps api
    Args:
        address as string
    Returns:
        zip as string
    '''
    keyfile = '/home/luke/API_Keys/googlemaps'
    with open(keyfile, 'r') as f:
        api_key = f.read().rstrip()
    gmaps = googlemaps.Client(key=api_key)
    geocode_result = gmaps.geocode(address)

    #FORMATTED_ADDRESS
    formatted_address = geocode_result[0]['formatted_address']

    #ADDRESS_COMPONENTS
    street_number = geocode_result[0]['address_components'][0]['long_name']
    route = geocode_result[0]['address_components'][1]['long_name']
    city = geocode_result[0]['address_components'][2]['long_name']
    county = geocode_result[0]['address_components'][3]['long_name']
    state = geocode_result[0]['address_components'][4]['long_name']
    country = geocode_result[0]['address_components'][5]['long_name']
    postal_code = geocode_result[0]['address_components'][6]['long_name']
    postal_code_suffix = geocode_result[0]['address_components'][7]['long_name']

    geometries = {'lat':geocode_result[0]['geometry']['location']['lat'],
                  'lng':geocode_result[0]['geometry']['location']['lng'],
                  'type':geocode_result[0]['geometry']['location_type']}

    address_components = {'street_number':street_number, 'route':route,
                          'city':city, 'county':county, 'state':state,
                          'country':country, 'postal_code':postal_code,
                          'postal_code_suffix':postal_code_suffix}

    return address_components['postal_code']

def without_api(address):
    '''Look up zip without API
    Args:
        address (as much of it as you have)
    Returns:
        zip code
    '''
    url = 'https://maps.googleapis.com/maps/api/geocode/json'
    keyfile = '/home/luke/API_Keys/googlemaps'

    with open(keyfile, 'r') as f:
        appid = f.read().rstrip()

    payload = {'address':'+'.join(address.split()), 'key':appid}

    response = requests.get(url, payload)
    result = response.json()

    postal_code = result['results'][0]['address_components'][6]['long_name']

    return postal_code

def main():
    '''Main function
    Args: none
    Returns: nothing
    '''
    address_list = ['516 galbewood cir']

    for address in address_list:
        postal_code = zip_from_address(address)
        print(postal_code)
        without_api(address)

if __name__ == '__main__':
    main()
