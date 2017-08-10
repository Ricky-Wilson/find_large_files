# find_large_files
A Command-Line tool  to locate large files on a linux system

```
Help on module find_large_files:

NAME
    find_large_files - Find large files on a linux system.

FILE
    /home/ricky/Projects/Python/find_larg_files/find_large_files.py

DESCRIPTION
    :Example:
    excludes = ['/proc', '/sys', '/dev', '/swapfile']
    find_large_files('/', n_results=20, excludes=excludes)

FUNCTIONS
    find_large_files(fpath, n_results=10, **kwargs)
        Recursively find the largest files in a directory.
        
        return n largest files in a directory tree.
        :param fpath: `str` where to start.
        :param n_results: `int` how many results to retrun.
        :param kwargs: This will be passed to walk.
        :rtype: `None` it prints the paths and sizes to the screen.
    
    getsize(fpath)
        Return the size of a file.
        Will return 0 if an OSError is raised.
        :param fpath: `str`
    
    main()
    
    take(number, iterable)
        Return first n items of the iterable as a list.
        
        :param number: `int` How many do you want to take.
        :param iterable: `iterable`
        :rtype: `list`
    
    walk(fpath, **kwargs)
        Traverse thru a directory tree.
        
        :param fpath: `int` The root file path
        :param excludes: `list` optional directories to exclude
        :rtype: `generator`
 ```
