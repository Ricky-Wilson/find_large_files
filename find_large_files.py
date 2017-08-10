
'''Find large files on a linux system.

:Example:
excludes = ['/proc', '/sys', '/dev', '/swapfile']
find_large_files('/', n_results=20, excludes=excludes)
'''

import os
import operator
from itertools import islice
import fnmatch
import re
import argparse
import scandir


def take(number, iterable):
    """Return first n items of the iterable as a list.
    
    :param number: `int` How many do you want to take.
    :param iterable: `iterable`
    :rtype: `list`
    """
    return list(islice(iterable, number))


def walk(fpath, **kwargs):
    ''' Traverse thru a directory tree.
    
    :param fpath: `int` The root file path
    :param excludes: `list` optional directories to exclude
    :rtype: `generator`
    '''
    kwargs.setdefault('excludes', [])
    excludes = kwargs.get('excludes')
    # transform glob patterns to regular expressions
    excludes = r'|'.join([fnmatch.translate(x) for x in excludes]) or r'$.'
    for root, dirs, files in scandir.walk(fpath):
        # exclude dirs
        if excludes:
            dirs[:] = [os.path.join(root, d) for d in dirs]
            dirs[:] = [d for d in dirs if not re.match(excludes, d)]
        for name in files:
            yield os.path.join(root, name)


def getsize(fpath):
    ''' Return the size of a file.
    Will return 0 if an OSError is raised.
    :param fpath: `str` 
    ''' 
    try:
        return os.path.getsize(fpath)
    except OSError:
        return 0


def find_large_files(fpath, n_results=10, **kwargs):
    ''' Recursively find the largest files in a directory.
    
    return n largest files in a directory tree.
    :param fpath: `str` where to start.
    :param n_results: `int` how many results to retrun.
    :param kwargs: This will be passed to walk.
    :rtype: `None` it prints the paths and sizes to the screen.
    '''
    results = {}
    for name in walk(fpath, **kwargs):
        results[name] = getsize(name)

    results = reversed(sorted(results.items(), key=operator.itemgetter(1)))
    for name, size in take(n_results, results):
        yield name, size

def main():

    parser = argparse.ArgumentParser(description='Find large files')
    parser.add_argument('path', metavar='-p', type=str, help='The path to start crawling')
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
   
    args = parser.parse_args()
    for name, size in find_large_files(args.path, n_results=args.results, excludes=args.exclude):
        print name, size
    
if __name__ == '__main__':
    main()
