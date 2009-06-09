import sys
import time

import SocketServer
import BaseHTTPServer
from SimpleXMLRPCServer import SimpleXMLRPCRequestHandler, SimpleXMLRPCServer

class ThreadingXMLRPCServer(SocketServer.ThreadingMixIn,
                            SimpleXMLRPCServer):
    pass

def create_server(port):
    server = ThreadingXMLRPCServer(('localhost', port),
                                   SimpleXMLRPCRequestHandler)

#    server.register_function(foo, 'foo')
    return server

###
    

