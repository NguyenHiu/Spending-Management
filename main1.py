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
# addr = IP.generate()
# DICT.add(pk, addr)
addr = ("127.0.0.2", 60001)
B = Node("User-2", sk, pk, addr, ("127.0.0.1", 60001))
B.printConnections()
B.create_transaction("user-2", 100, "note")
time.sleep(30)

# B.blockchain.output()

