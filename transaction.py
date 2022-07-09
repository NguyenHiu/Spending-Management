# from hashlib import sha256
import json

class Transaction: 
    def __init__(self, _recipient, _signature, _amount, _note):
        self.recipient = _recipient
        self.signature = _signature
        self.amount = _amount
        self.note = _note

    def toJson(self):
        return json.dumps(self.__dict__)

# a = Transaction('0x1', '0x2', '5', 'testing')
# print(a.toJson())

