import xmlrpclib, os, time

WAIT = 0.1
_conn = None

def get_connection():
    global _conn
    if _conn is None:
        _conn = xmlrpclib.ServerProxy('http://localhost:8080/')
    return _conn

def request_ok(wait=True, pid=None):
    get_connection()
    if pid is None:
        pid = os.getpid()

    while not _conn.request_ok(pid):
        if not wait:
            return False

        time.sleep(WAIT)
        
    return True

def release(pid=None):
    get_connection()
    if pid is None:
        pid = os.getpid()

    _conn.release(pid)
