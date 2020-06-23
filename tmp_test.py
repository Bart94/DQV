import hashlib
from datetime import date, timedelta

from Crypto.Hash import SHA256
from Crypto.PublicKey import ECC
from Crypto.Signature import DSS

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

message = b'I give my permission to order #4355'
key = ECC.import_key(open('DQV_certs/lab_sk.pem').read())
h = SHA256.new(message)
signer = DSS.new(key, 'fips-186-3')
signature = signer.sign(h)
print(signature.hex())

key = ECC.import_key(open('DQV_certs/lab_pk.pem').read())
h = SHA256.new(message)
verifier = DSS.new(key, 'fips-186-3')
try:
    verifier.verify(h, signature)
    print("The message is authentic.")
except ValueError:
    print("The message is not authentic.")
