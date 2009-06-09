from lqueue import client

###

conn = client.get_connection()

conn.zero()
conn.set_flush(0)
conn.set_queuesize(1)

###

assert client.request_ok(False)
# n => 1
assert client.request_ok(False)

assert client.request_ok(False, 1) == 0

client.release()
# n => 0

try:
    assert client.request_ok(False, 1)
finally:
    client.release(1)
# n = 0

###

conn.set_queuesize(2)

try:
    assert client.request_ok(False)
    assert client.request_ok(False, 1)
finally:
    client.release()
    client.release(1)

###

conn.set_queuesize(2)

try:
    assert client.request_ok(False)
    assert client.request_ok(False, 1)
    assert client.request_ok(False, 2) == 0
    client.release(1)
    assert client.request_ok(False, 2)
finally:
    client.release()
    client.release(1)
    client.release(2)    
