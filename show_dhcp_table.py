#!/usr/bin/env python
'''
Simple script that logs into my linksys router and prints the DHCP table
of connected devices
'''

import re
import os
import getpass
import requests

def ascii_table(output):
    '''Print output table in a pretty ascii table

    Args:
        output: list
    '''

    max_nm = 20
    max_ip = 15

    print('+{}+{}+'.format('-' * max_nm, '-' * max_ip))
    print('| {0:18} | {1:13} |'.format('Hostname', 'IP Address'))
    print('+{}+{}+'.format('-' * max_nm, '-' * max_ip))

    for row in output:
        print('| {0:18} | {1:13} |'.format(row[0], row[1]))

    print('+{}+{}+'.format('-' * max_nm, '-' * max_ip))

def main():
    '''Log into Linksys router and display DHCP table
    '''
    url = 'http://192.168.1.1/DHCPTable.asp'
    pattern = r"^table\[\d\] = new AAA\('(.+)','(\d+\.\d+\.\d+\.\d+)',.+;"

    passwd_file = '/home/luke/API_Keys/linksys'
    if os.path.isfile(passwd_file):
        with open(passwd_file, 'r') as f:
            passwd = f.read().rstrip()
    else:
        passwd = getpass.getpass('Enter router password: ')

    response = requests.get(url, auth=('', passwd))

    matches = re.findall(pattern, response.text, re.M)

    ascii_table(matches)

if __name__ == '__main__':
    main()
