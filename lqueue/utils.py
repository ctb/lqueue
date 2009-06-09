def synchronized(lock):
    """ Synchronization decorator.

    From http://code.activestate.com/recipes/465057/
    """
    def wrap(f):
        def newFunction(*args, **kw):
            lock.acquire()
            try:
                return f(*args, **kw)
            finally:
                lock.release()
        return newFunction
    return wrap

