
'''Find large files on a linux system.

:Example:
excludes = ['/proc', '/sys', '/dev', '/swapfile']
find_large_files('/', n_results=20, excludes=excludes)
'''

# Standard imports.
import os
import operator
from itertools import islice
import fnmatch
import re
import sys

# Third party imports.
import scandir

# Local project imports.
from arguments import args


def is_empty(fpath):
    try:
        return os.stat(fpath).st_size == 0
    except OSError:
        pass


def find_empty_files(root_dir='.'):
    """ Find empty files and yield there path.
    """
    empty = 0
    for dirpath, dirs, files in scandir.walk(root_dir):
        for _file in files:
            fullpath = os.path.join(dirpath, _file)
            if is_empty(fullpath):
                empty += 1
                yield empty, fullpath


def find_empty_dirs(root_dir='.'):
    """ Find empty directories and yield there path.

    """
    empty = 0
    for dirpath, dirs, files in scandir.walk(root_dir):
        if not dirs and not files:
            empty += 1
            yield empty, dirpath


def take(number, iterable):
    """Return first n items of the iterable as a list.

    :param number: `int` How many do you want to take.
    :param iterable: `iterable`
    :rtype: `list`
    """
    return list(islice(iterable, number))


def human_size(bytes, units=[' bytes', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB']):
    """ Returns a human readable string reprentation of bytes"""
    return str(bytes) + units[0] if bytes < 1024 else human_size(bytes>>10, units[1:])


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
            fullpath = os.path.join(root, name)
            if os.path.isfile(fullpath):
                yield fullpath


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
    """
    So pylint will shut up about missing doc string.
    """

    if args.find_empty_dirs:
        for index, empty in find_empty_dirs(args.path):
            print index, empty
        print("{} empty directories found in {}".format(index, args.path))
        sys.exit(0)

    if args.find_empty_files:
        for index, empty in find_empty_files(args.path):
            print index, empty
        print "{} empty files found in {}".format(index, args.path)
        sys.exit(0)

    # I create the options dict to shorten line 82.
    options = {'n_results': args.results, 'excludes':args.exclude}
    for name, size in find_large_files(args.path, **options):
        if not args.human_readable:
            print name, size
        else:
            print name, human_size(size)


if __name__ == '__main__':
    main()
