#!/usr/bin/env python3
'''Upwork project inspired this. It just grabs the Contact Us page from
    a site and returns the url
'''

import requests
import re

def contact_us(url):
    '''Function scrapes url for Contact Us information and returns address
    or source from that Page
    
    Args:
        url (string): url to look at for Contact Us page
    Returns:
        tuple with url of contact us page, and email/physical 
    '''
    response = requests.get(url)

    pattern = r'<a href="(.+)">Contact Us</a>'

    match = re.search(pattern, response.text, re.MULTILINE|re.UNICODE)

    if match:
        return match.group(1)

    return False
    

def main():

    urls = ['http://www.tune.com', 'http://www.google.com']

    for url in urls:
        print('{} - {}'.format(url, contact_us(url)))


if __name__ == '__main__':
    main()
