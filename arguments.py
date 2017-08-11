
'''
Cammand-Line parser for find_large_files.py
'''

import argparse

parser = argparse.ArgumentParser(description='Find the largest files on disc.')

parser.add_argument('path', metavar='-p', type=str, help='The path to start crawling')

parser.add_argument(
    '--human-readable', action='store_true',  help='Display filesize in human readable format',
    )

parser.add_argument(
    '--results', metavar='-n', type=int,
    help='How many results to return the default is 10.',
    default=10
    )

parser.add_argument(
    '--exclude', metavar='-e', type=list,
    help='Directoris to exclude in the search.',
    nargs='+', default=[]
    )

parser.add_argument(
    '--find-empty-dirs', action='store_true',  help='Find empty dirs',
    )


args = parser.parse_args()
