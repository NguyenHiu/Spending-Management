'''
    Tui test thu :v
'''

from node import Node
import key
import time

# class IPgenerator:
#     def __init__(self):
#         # 127.0.0.x
#         self.x = 1

    
#     def generate(self):
#         addr = ("127.0.0." + str(self.x), 60001)
#         self.x += 1
#         return addr

# class IPdictionary:
#     def __init__(self):
#         self.dict = {}

    
#     def add(self, pk, addr):
#         self.dict[pk] =  addr

# IP = IPgenerator()
# DICT = IPdictionary()


sk, pk = key.generate_key()
# print(type(sk))
# print(type(pk))
addr = ("127.0.0.1", 60001)
A = Node("User-1", sk, pk, addr)
A.printConnections()
time.sleep(30)

# A.blockchain.output()
