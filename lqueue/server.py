import os
import threading
import SocketServer
import BaseHTTPServer
from SimpleXMLRPCServer import SimpleXMLRPCRequestHandler, SimpleXMLRPCServer

from utils import synchronized

###

class ThreadingXMLRPCServer(SocketServer.ThreadingMixIn,
                            SimpleXMLRPCServer):
    pass

_server = None
def create_server(port):
    global _server
    assert _server is None
    _server = ThreadingXMLRPCServer(('localhost', port),
                                    SimpleXMLRPCRequestHandler)

    _server.register_function(request_ok, 'request_ok')
    _server.register_function(release, 'release')
    _server.register_function(set_queuesize, 'set_queuesize')
    _server.register_function(set_flush, 'set_flush')
    _server.register_function(zero, 'zero')
    return _server

def get_server():
    global _server
    return _server

###

###

thelock = threading.Lock()
_do_flush = True                        # adjust for testing/debugging
_queuesize = 1
active_pids = set()
waiting_pids = []

def _flush_pid_queues():
    global active_pids, waiting_pids

    if not _do_flush:
        return
    
    rm = set()
    for pid in active_pids:
        try:
            os.getpgid(pid)
        except OSError:
            # pid no longer active
            rm.add(pid)

    active_pids -= rm
    
    rm = set()
    for pid in waiting_pids:
        try:
            os.getpgid(pid)
        except OSError:
            # pid no longer active
            rm.add(pid)

    for p in rm:
        waiting_pids.remove(p)

    print 'ACTIVE', active_pids
    print 'WAITING', waiting_pids

@synchronized(thelock)
def request_ok(pid):
    global active_pids, waiting_pids

    print 'REQUEST OK:', pid, active_pids, waiting_pids, _queuesize
    
    if pid in active_pids:
        return 1

    _flush_pid_queues()

    n = len(active_pids)
    allow = _queuesize - n
    print 'ALLOW:', allow
    if allow:
        ok = False
        if len(waiting_pids) >= allow and pid in waiting_pids[:allow]:
            print 'IN'
            waiting_pids.remove(pid)
            ok = True
        elif len(waiting_pids) < allow:
            print 'SHORT'
            ok = True
        
        if ok:
            print 'OK'
            active_pids.add(pid)
            return 1

    if pid not in waiting_pids:
        waiting_pids.append(pid)

    print 'NOK'

    return 0

@synchronized(thelock)
def release(pid):
    global active_pids, waiting_pids
    if pid in active_pids:
        active_pids.remove(pid)
        if pid in waiting_pids:
            waiting_pids.remove(pid)
        return 1

    if pid in waiting_pids:
        waiting_pids.remove(pid)
    
    return 0

@synchronized(thelock)
def set_queuesize(n):
    global _queuesize

    n = int(n)
    assert n > 0
    
    _queuesize = n

    return 1

@synchronized(thelock)
def set_flush(flag):
    global _do_flush

    _do_flush = bool(flag)

    return int(_do_flush)

@synchronized(thelock)
def zero():
    global _do_flush, _queuesize, active_pids, waiting_pids
    
    _do_flush = True
    _queuesize = 1
    active_pids = set()
    waiting_pids = []

    return 1
