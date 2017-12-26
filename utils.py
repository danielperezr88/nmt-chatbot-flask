from os import getpid, path
import unicodedata
import collections
import functools
import inspect
import pickle
import re


def generate_url(host, protocol='http', port=80, directory=''):

    if isinstance(directory, list):
        directory = '/'.join(directory)

    return "%s://%s:%d/%s" % (protocol, host, port, directory)


def save_pid():
    """Save pid into a file: filename.pid."""
    pidfilename = inspect.getfile(inspect.currentframe()) + ".pid"
    f = open(pidfilename, 'w')
    f.write(str(getpid()))
    f.close()


# This variable configures Memorize decorator, allowing to set the place to store cache files globally.
# Set it to False to store cache files next to files for which function calls are cached.
USE_CURRENT_DIR = True


class Memorize(object):
    '''
    A function decorated with @memorize caches its return
    value every time it is called. If the function is called
    later with the same arguments, the cached value is
    returned (the function is not reevaluated). The cache is
    stored as a .cache file in the current directory for reuse
    in future executions. If the Python file containing the
    decorated function has been updated since the last run,
    the current cache is deleted and a new cache is created
    (in case the behavior of the function has changed).
    '''
    def __init__(self, func):
        self.func = func
        function_file = inspect.getfile(func)
        self.parent_filepath = path.abspath(function_file)
        self.parent_filename = path.basename(function_file)
        self.__name__ = self.func.__name__
        self.cache = None  # lazily initialize cache to account for changed global dir setting (USE_CURRENT_DIR)

    def check_cache(self):
        if self.cache is None:
            if self.cache_exists():
                self.read_cache()  # Sets self.timestamp and self.cache
                if not self.is_safe_cache():
                    self.cache = {}
            else:
                self.cache = {}

    def __call__(self, *args):
        self.check_cache()
        if not isinstance(args, collections.Hashable):
            return self.func(*args)
        if args in self.cache:
            return self.cache[args]
        else:
            value = self.func(*args)
            self.cache[args] = value
            self.save_cache()
            return value

    def get_cache_filename(self):
        """
        Sets self.cache_filename to an os-compliant
        version of "file_function.cache"
        """
        filename = _slugify(self.parent_filename.replace('.py', ''))
        funcname = _slugify(self.__name__)
        folder = path.curdir if USE_CURRENT_DIR else path.dirname(self.parent_filepath)
        return path.join(folder, filename + '_' + funcname + '.cache')

    def get_last_update(self):
        """
        Returns the time that the parent file was last
        updated.
        """
        last_update = path.getmtime(self.parent_filepath)
        return last_update

    def is_safe_cache(self):
        """
        Returns True if the file containing the memoized
        function has not been updated since the cache was
        last saved.
        """
        if self.get_last_update() > self.timestamp:
            return False
        return True

    def read_cache(self):
        """
        Read a pickled dictionary into self.timestamp and
        self.cache. See self.save_cache.
        """
        with open(self.get_cache_filename(), 'rb') as f:
            data = pickle.loads(f.read())
            self.timestamp = data['timestamp']
            self.cache = data['cache']

    def save_cache(self):
        """
        Pickle the file's timestamp and the function's cache
        in a dictionary object.
        """
        with open(self.get_cache_filename(), 'wb+') as f:
            out = dict()
            out['timestamp'] = self.get_last_update()
            out['cache'] = self.cache
            f.write(pickle.dumps(out))

    def cache_exists(self):
        '''
        Returns True if a matching cache exists in the current directory.
        '''
        if path.isfile(self.get_cache_filename()):
            return True
        return False

    def __repr__(self):
        """ Return the function's docstring. """
        return self.func.__doc__

    def __get__(self, obj, objtype):
        """ Support instance methods. """
        return functools.partial(self.__call__, obj)


def _slugify(value):
    """
    Normalizes string, converts to lowercase, removes
    non-alpha characters, and converts spaces to
    hyphens. From
    http://stackoverflow.com/questions/295135/turn-a-string-into-a-valid-filename-in-python
    """
    value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore')
    value = re.sub(r'[^\w\s-]', '', value.decode('utf-8', 'ignore'))
    value = value.strip().lower()
    value = re.sub(r'[-\s]+', '-', value)
    return value
