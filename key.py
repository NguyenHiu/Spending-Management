from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA256

def generate_key():
    key = RSA.generate(1024)
        # f = open("private.pem", "wb")
        # f.write(key.exportKey('PEM'))
        # f.close()

    pubkey = key.publickey()
        # f = open("public.pem", "wb")
        # f.write(pubkey.exportKey('OpenSSH'))
        # f.close()

    # Hieu
    key = key.exportKey('PEM').decode('utf-8')
    pubkey = pubkey.exportKey('PEM').decode('utf-8')
    #
    return str(key), str(pubkey)

def encrypt_message(message, pk):
    # Hieu
    if type(message) != bytes:
        message = bytes(message, 'utf-8')
    pk = RSA.importKey(pk)
    #
        # key = RSA.importKey(open('private.pem').read())
    cipher = PKCS1_OAEP.new(pk)
    return cipher.encrypt(message)

def decrypt_message(ciphertext, sk):
    # Hieu
    sk = RSA.importKey(sk)
    #
        # key = RSA.importKey(open('public.pem').read())
    cipher = PKCS1_OAEP.new(sk)
    return cipher.decrypt(ciphertext)

def sign(message, sk):
    # Hieu
    if type(message) != bytes:
        message = bytes(message, 'utf-8')
    sk = RSA.importKey(sk)
    #
    signer = PKCS1_v1_5.new(sk)
    digest = SHA256.new()
    digest.update(message)
    return signer.sign(digest).hex()
    # return str(signer.sign(digest))

def verify(message, signature, pk) -> bool:
    # Hieu
    if type(message) != bytes:  
        message = bytes(message, 'utf-8')
    pk = RSA.importKey(pk)
    if type(signature) != bytes:
        signature = bytes.fromhex(signature)
    #
    signer = PKCS1_v1_5.new(pk)
    digest = SHA256.new()
    digest.update(message)
    return signer.verify(digest, signature)

# generate_key()
# message = b'You can attack now!'
# priv_key = RSA.importKey(open('private.pem').read())
# pub_key = RSA.importKey(open('public.pem').read())

# signature = sign(message, priv_key)
# check = verify(message, signature, pub_key)

# print(check)