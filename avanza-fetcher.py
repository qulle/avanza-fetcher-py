# Author: Qulle 2020-11-02
# Github: github.com/qulle/avanza-fetcher-py
# Editor: vscode
# Run: python avanza-fetcher.py urls.json
# Run: python avanza-fetcher.py urls.json > output.txt

import json # Json parser
import re   # Regex
import sys  # Command-line-arguments
import time # Thread sleep
import requests # HTTP Get requests, install via: pip install requests
from requests.exceptions import HTTPError
from json.decoder        import JSONDecodeError

class Config:
    LAST_GROUP = 3 # Regex capture group
    SLEEP_TIME = 1 # Delay between http requests, seconds

# Don't touch if you don't know what you are doing, you have been warned // Qulle
class Regex:
    CHANGE_PROCENT = '(changePercent)(.*?)>([\+|-]?\d+,\d+\s+%)'
    CHANGE_SEK     = '(change)(.*?)>([\+|-]?\d+,\d+\s+SEK)'
    BUY            = '(buyPrice)(.*?)>(\d+,?\d+|-)'
    SELL           = '(sellPrice)(.*?)>(\d+,?\d+|-)'
    LATEST         = '(data-e2e="quoteLastPrice")(.*?)>(\d+,?\d+|-)'
    HIGHEST        = '(highestPrice)(.*?)>(\d+,?\d+|-)'
    LOWEST         = '(lowestPrice)(.*?)>(\d+,?\d+|-)'
    AMOUNT         = '(totalVolumeTraded)(.*?)>([\d|\s]+)'

def http_request(url):
    res = ''
    try:
        res = requests.get(url).text
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
    except Exception as err:
        print(f'Request error: {url} - Timeout?')

    return res 

def regex_search(HTMLBuffer, regex):
    res = re.search(regex, HTMLBuffer)
    return res[Config.LAST_GROUP] if res else '***'

def get_data_from_file(filename):
    try:
        with open(filename, 'r') as f:
            return f.read()
    except FileNotFoundError:
        print(f'The file "{filename}" was not found')
    except Exception as err:
        print('Unknown file error')

def parse_json(data):
    res = ''
    try:
        res = json.loads(data)
    except JSONDecodeError as decode_err:
        print('Error decoding the json-file. Check the syntax')
    except Exception as err:
        print('Unknown JSON error')

    return res

def print_table_head(group):
    print(f'\n{group}')
    print('-' * 129)
    print(
        'Name', 
        'Today %'  .rjust(27),
        'Today SEK'.rjust(16),
        'Buy'      .rjust(10),
        'Sell'     .rjust(11),
        'Latest'   .rjust(13),
        'Highest'  .rjust(14),
        'Lowest'   .rjust(13),
        'Amount'   .rjust(13)
    )

def print_table_row(stock, HTMLBuffer):
    print(
        stock['name'],
        regex_search(HTMLBuffer, Regex.CHANGE_PROCENT).rjust(31 - len(stock['name'])),
        regex_search(HTMLBuffer, Regex.CHANGE_SEK).rjust(16),
        regex_search(HTMLBuffer, Regex.BUY)       .rjust(10),
        regex_search(HTMLBuffer, Regex.SELL)      .rjust(11),
        regex_search(HTMLBuffer, Regex.LATEST)    .rjust(13),
        regex_search(HTMLBuffer, Regex.HIGHEST)   .rjust(14),
        regex_search(HTMLBuffer, Regex.LOWEST)    .rjust(13),
        regex_search(HTMLBuffer, Regex.AMOUNT)    .rjust(13)
    )

def main(filename):
    raw_file = get_data_from_file(filename)

    if raw_file:
        json_object = parse_json(raw_file)

    if raw_file and json_object:
        for group in json_object:
            print_table_head(group)

            for stock in json_object[group]:
                print_table_row(stock, http_request(stock['url']))
                time.sleep(Config.SLEEP_TIME) # Wait so the server does not block too many requests
            
        print('\n')

if __name__ == '__main__':
    dependencies = 'requests'
    if len(sys.argv) > 1:
        if not dependencies in sys.modules:
            print(f'The script depends on \'{dependencies}\' package, install using $ pip install {dependencies}')
        else:
            main(sys.argv[1])
    else:
        print(f'Run using: python {sys.argv[0]} json-file')