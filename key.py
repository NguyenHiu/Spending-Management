from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA256

def generate_key():
    key = RSA.generate(1024)
    f = open("private.pem", "wb")
    f.write(key.exportKey('PEM'))
    f.close()

    pubkey = key.publickey()
    f = open("public.pem", "wb")
    f.write(pubkey.exportKey('OpenSSH'))
    f.close()

def encrypt_message(message):
    key = RSA.importKey(open('private.pem').read())
    cipher = PKCS1_OAEP.new(key)
    return cipher.encrypt(message)

def decrypt_message(ciphertext):
    key = RSA.importKey(open('public.pem').read())
    cipher = PKCS1_OAEP.new(key)
    return cipher.decrypt(ciphertext)

def sign(message, priv_key):
    signer = PKCS1_v1_5.new(priv_key)
    digest = SHA256.new()
    digest.update(message)
    return signer.sign(digest)

def verify(message, signature, pub_key) -> bool:
    signer = PKCS1_v1_5.new(pub_key)
    digest = SHA256.new()
    digest.update(message)
    return signer.verify(digest, signature)

# generate_key()
message = b'You can attack now!'
priv_key = RSA.importKey(open('private.pem').read())
pub_key = RSA.importKey(open('public.pem').read())

signature = sign(message, priv_key)
check = verify(message, signature, pub_key)

print(check)