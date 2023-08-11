import hashlib

m = hashlib.sha256()
m.update('Life is too short'.encode('utf-8'))
print(m.hexdigest())