from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA256

def generate_key():
    key = RSA.generate(1024)
    pubkey = key.publickey()
    key = key.exportKey('PEM').decode('utf-8')
    pubkey = pubkey.exportKey('PEM').decode('utf-8')
    return str(key), str(pubkey)

def encrypt_message(message, pk):
    if type(message) != bytes:
        message = bytes(message, 'utf-8')
    pk = RSA.importKey(pk)
    cipher = PKCS1_OAEP.new(pk)
    return cipher.encrypt(message)

def decrypt_message(ciphertext, sk):
    sk = RSA.importKey(sk)
    cipher = PKCS1_OAEP.new(sk)
    return cipher.decrypt(ciphertext)

def sign(message, sk):
    if type(message) != bytes:
        message = bytes(message, 'utf-8')
    sk = RSA.importKey(sk)
    signer = PKCS1_v1_5.new(sk)
    digest = SHA256.new()
    digest.update(message)
    return signer.sign(digest).hex()

def verify(message, signature, pk) -> bool:
    if type(message) != bytes:  
        message = bytes(message, 'utf-8')
    pk = RSA.importKey(pk)
    if type(signature) != bytes:
        signature = bytes.fromhex(signature)
    signer = PKCS1_v1_5.new(pk)
    digest = SHA256.new()
    digest.update(message)
    return signer.verify(digest, signature)

# https://stackoverflow.com/questions/51228645/how-can-i-encrypt-with-a-rsa-private-key-in-python
# https://pycryptodome.readthedocs.io/en/latest/src/cipher/oaep.html
# https://viblo.asia/p/ecdsa-he-mat-dua-tren-duong-cong-elliptic-va-ung-dung-trong-blockchain-XL6lA4oDZek
# https://cryptobook.nakov.com/asymmetric-key-ciphers/rsa-encrypt-decrypt-examples