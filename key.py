from Crypto.PublicKey import RSA
key = RSA.generate(1024)
f = open("private.pem", "wb")
f.write(key.exportKey('PEM'))
f.close()

pubkey = key.publickey()
f = open("public.pem", "wb")
f.write(pubkey.exportKey('OpenSSH'))
f.close()

# Crypto.Cipher.PKCS1_OAEP nghien cuu them cho nay
encMessage = pubkey.encrypt("Hello World", 32)
print(encMessage)
decMessage = key.decrypt(encMessage)
print(decMessage)