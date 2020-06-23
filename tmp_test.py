import hashlib
from datetime import date, timedelta

from Crypto.PublicKey import ECC

x = date.today()

y = date.today() - timedelta(days=14)

print(str(y))
print(hashlib.sha256('1234'.encode('utf-8')).hexdigest())

# key = b'Sixteen byte key'
# cipher = AES.new(key, AES.MODE_EAX)
# nonce = cipher.nonce
# ciphertext, tag = cipher.encrypt_and_digest('sdsfs'.encode('utf-8'))
# plaintext = cipher.decrypt(ciphertext)
# print(plaintext)

key = ECC.generate(curve='P-256')
print(key)
f = open('myprivatekey.pem', 'wt')
f.write(key.export_key(format='PEM'))
f.close()
f = open('myprivatekey.pem', 'rt')
key = ECC.import_key(f.read())
print(key)
