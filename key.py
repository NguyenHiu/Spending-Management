from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

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

    key = RSA.importKey(open('public.pem').read())
    cipher = PKCS1_OAEP.new(key)
    ciphertext = cipher.encrypt(message)
    return ciphertext

def decrypt_message(ciphertext):
    key = RSA.importKey(open('private.pem').read())
    cipher = PKCS1_OAEP.new(key)
    return cipher.decrypt(ciphertext)

# generate_key()
message = b'You can attack now!'
cipher = encrypt_message(message)
msg = decrypt_message(cipher)
print(msg)