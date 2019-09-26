import hashlib
import pickle

file = open("./files/prueba.pdf", "rb")

data = file.read()

m = hashlib.sha256()

m.update(data)
print(m.digest())

digest = m.digest()

print(digest)

print(len(digest))




