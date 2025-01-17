from typing import *
from subprocess import *
import json
import os, sys
import argparse


def send_req_company(webpage : str) -> CompletedProcess:
    """
        Runs API call for company info search on harmonic

        PARAMS
            webpage : str = Company website URL

        RETURNS
            CompletedProcess object from result of API call
        
    """
    cmd_str = f'''
        curl -X POST \
        https://api.harmonic.ai/companies?website_domain={webpage} \
        -H accept:application/json \
        -H apikey:{os.environ['HARMONIC_API_KEY']}
    '''.strip().split()

    return run(cmd_str, capture_output=True, text=True)


def send_req_person(linkedin : str) -> CompletedProcess:
    """
        Runs API call for person info search on harmonic

        PARAMS
            linkedin : str = LinkedIn URL

        RETURNS
            CompletedProcess object from result of API call
        
    """
    cmd_str = f'''
        curl -X POST \
        https://api.harmonic.ai/persons?linkedin_url={linkedin} \
        -H accept:application/json \
        -H apikey:{os.environ['HARMONIC_API_KEY']}
    '''.strip().split()

    return run(cmd_str, capture_output=True, text=True)


def search_companies(search : str) -> CompletedProcess:
    """
        Runs API call to search for companies given keywords string 'search'

        PARAMS
            search : str = str of keywords separated by commas
                eg. "artificial intelligence, machine learning"
        
        RETURNS
            CompletedProcess object from result of API call
    """
    cmd_str = 'curl -X POST'.split()
    endpt = 'https://api.harmonic.ai/search/companies_by_keywords?page=0&size=50'
    cmd_str.append(endpt)
    cmd_str.append('-H')
    cmd_str.append('contains_all_of_keywords:' + search)
    cmd_str.extend(f'''
        -H accept:application/json \
        -H apikey:{os.environ['HARMONIC_API_KEY']}
    '''.strip().split())
    # print(cmd_str)
    # return
    return run(cmd_str, capture_output=True, text=True)


def read_data(file_name : str) -> Dict:
    """ Returns python dictionary from json dump file """
    with open(file_name, 'r') as f:
        text = f.read().strip()
    return json.loads(text)


def main():
    parser = argparse.ArgumentParser(description='Query harmonic API for one of several searches')
    parser.add_argument('type', type=str, default='company')
    parser.add_argument('query', type=str)
    parser.add_argument('-o', '--output_filename')
    args = parser.parse_args()

    match args.type:
        case 'person':
            out = send_req_person(args.query)
        case 'company':
            out = send_req_company(args.query)
        case 'keywords':
            out = search_companies(args.query)
    
    print('STDERR:\n', out.stderr)
    with open(args.output_filename, 'w') as f:
        f.write(out.stdout)
    
    run(f'jq . {args.output_filename} | sponge {args.output_filename}')
    
    print('Wrote output to', args.output_filename)


if __name__ == '__main__':
    main()