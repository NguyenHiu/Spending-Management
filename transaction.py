# from hashlib import sha256
import json
import key

class Transaction: 
    def __init__(self, _recvPK=0, _sendPK=0, _sk=0, _amount=0, _note=0, _time=0, Null=False):
        if Null:
            return

        self.receiver = _recvPK
        self.sender = _sendPK
        self.amount = _amount
        self.note = _note
        self.time = _time
        self.signature = (key.sign(json.dumps(self.toJson()), _sk))
        # print('sig: ', end="")
        # print(self.signature)
        # print(type(self.signature))
        # if bytes.fromhex(self.signature.hex()) == self.signature:
        #     print("YESS")
        # else:
        #     print("NOOO")

    def _json_dump(self) -> dict:
        js = {
            "sender": self.sender,
            "receiver": self.receiver,
            "amount": self.amount,
            "note": self.note,
            "time": self.time
        }
        return js

    def toJson(self) -> dict: # For broadcast
        return self._json_dump()
    
    def toJson_(self) -> dict: # For copy
        return self.__dict__

    def Json2Transaction(msg):
        trans = Transaction(Null=True)
        trans.receiver = msg["receiver"]
        trans.sender = msg["sender"]
        trans.amount = msg["amount"]
        trans.note = msg["note"]
        trans.time = msg["time"]
        trans.signature = msg["signature"]
        return trans

# a = Transaction('0x1', '0x2', '5', 'testing')
# print(a.toJson())

