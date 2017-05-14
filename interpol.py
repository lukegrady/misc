#!/usr/bin/env python3

''' Scrape interpol'''

import re
import sys
import math
import csv
import time
import requests

def get_wanted_person_detail(suffix):
    '''Scrape interpol site for wanted person details

    Args:
        list of urls for each individual wanted person on Interpol site

    Returns:
        dictionary of details for each wanted person
    '''
    url = 'https://www.interpol.int' + suffix

    response = requests.get(url)

    #Below pattern captures all details except Charges since Charges has <p>
    pattern = (r'<td class=\'col1\'>([\s\w]+):</td>\s*<td class=\'col2 '
               r'strong\'>([a-zA-Z0-9\(\)/\.,\s]+)</td>')

    #Sometimes a new character will slip into the Charges section and that
    #will cause this regex to break
    #I need to get better at these, so I'm not doing this in such a crappy
    #way, but for now, the solution is to go to the page (I write to stdout
    #that this happens and include the url. Find the special character
    #and add it below. #ghettofabulous
    charge_pattern = r'<p class="charge">([\w\s\.\(\),"-;:]+)</p>'

    matches = re.findall(pattern, response.text, re.MULTILINE|re.DOTALL)
    #This is rather annoying, but sometimes the site duplicates the charges
    #in two HTML paragrahps (<p></p>) and other times they have separate
    #charges in two paragraphs, so I'm erring on collecting duplicate
    #information rather than missing a separate charge
    charge_matches = re.findall(charge_pattern, response.text,
                                re.MULTILINE|re.DOTALL)

    details = {}
    if not matches:
        print('ERROR: Details not found on ' + url)
    else:
        for match in matches:
            details[match[0]] = match[1].strip()

    if not charge_matches:
        print('WARNING: Details of charge not found on ' + url)
    else:
        for charge_match in charge_matches:
            if 'Charges' in details:
                details['Charges'] = details['Charges'] + '\n' + charge_match
            else:
                details['Charges'] = charge_match

    return details

def get_wanted_person_urls():
    '''Scrape interpol site for wanted persons

    Interpol site displays nine (9) wanted persons per page.

    Args: None

    Returns: list of urls for individual wanted persons

    Exceptions: None
    '''
    people_per_page = 9 # Update this if site format changes

    url = 'https://www.interpol.int/notice/search/wanted/'

    response = requests.get(url)

    count_pattern = (r'<div class="bloc_pagination"><span class="orange"'
                     r'>Search result : (\d+)</span></div>')

    count_match = re.search(count_pattern, response.text, re.MULTILINE)

    if not count_match:
        print('ERROR: Could not find number of search results')
        sys.exit(0)

    person_count = int(count_match.groups()[0])

    page_count = int(math.ceil(person_count/float(people_per_page)))

    person_pattern = r'<a href="(.+)" class="details">Details</a>'

    href_matches = re.findall(person_pattern, response.text, re.MULTILINE)

    href_list = []

    if not href_matches:
        print('ERROR: Could not find any wanted persons page ' + url)
    else:
        for match in href_matches:
            href_list.append(match)

    #Loop through the rest of the (offset) pages
    for i in range(1, page_count):
        offset_url = url + '/(offset)/' + str(i*people_per_page)

        response = requests.get(offset_url)

        href_matches = re.findall(person_pattern, response.text, re.MULTILINE)

        if not href_matches:
            print('ERROR: Could not find any wanted persons page ' + offset_url)
        else:
            for match in href_matches:
                href_list.append(match)

    return href_list

def main():
    '''Main function'''
    outfile = 'wanted_persons.csv'

    url_list = get_wanted_person_urls()

    wanted_persons = []
    for url in url_list:
        time.sleep(.75) #Slow things down so we don't get flagged as bot
        wanted_persons.append(get_wanted_person_detail(url))

    with open(outfile, 'w') as csvfile:
        #Note that if Interpol adds any fields, they will need to be added
        #to this list, otherwise writer will throw an exception
        #
        #Alternatively, you can add extrasaction='ignore' to DictWriter params
        #but I prefer to throw the exception.
        fieldnames = ['Present family name', 'Forename', 'Sex', 'Date of birth',
                      'Place of birth', 'Language spoken', 'Nationality',
                      'Height', 'Weight', 'Colour of hair', 'Colour of eyes',
                      'Charges']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for person in wanted_persons:
            writer.writerow(person)

    print('Finished writing {} rows to file {}'.format(len(wanted_persons),
                                                       outfile))

if __name__ == '__main__':
    main()
