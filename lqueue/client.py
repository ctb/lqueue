import xmlrpclib

s = xmlrpclib.ServerProxy('http://localhost:8080/')
print s.foo(5, 6)
