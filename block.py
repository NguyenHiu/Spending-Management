from hashlib import sha256
import json

from transaction import Transaction

class Block:
    def __init__(self, _id=0, _transactions=[], _prevHash=0, _nonce=0):
        self.id = _id
        self.transactions = _transactions
        self.prevHash = _prevHash
        self.nonce = _nonce


    def compute_hash(self):
        return sha256(json.dumps(self.convertBlock2Json()).encode()).hexdigest()


    def convertJson2Block(self, msg):
        self.id = msg["id"]
        _transactions = msg["transactions"]
        for trans in _transactions:
            self.transactions.append(Transaction.Json2Transaction(trans))

        self.prevHash = msg["prevHash"]
        self.nonce = msg["nonce"]
    

    def convertJson2Block(msg):
        _block = Block()
        _block.id = msg["id"]
        _transactions = msg["transactions"]
        for trans in _transactions:
            _block.transactions.append(Transaction.Json2Transaction(trans))
            
        _block.prevHash = msg["prevHash"]
        _block.nonce = msg["nonce"]
        return _block

    
    def convertBlock2Json(self):
        js = {
            "id": self.id,
            "transactions": [],
            "prevHash": self.prevHash,
            "nonce": self.nonce
        }
        for trans in self.transactions:
            js["transactions"].append(trans.toJson_())
        return js