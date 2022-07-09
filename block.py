from hashlib import sha256
import json

class Block:
    def __init__(self, _id, _transactions, _prevHash, _nonce=0):
        self.id = _id
        self.transactions = _transactions
        self.prevHash = _prevHash
        self.nonce = _nonce

    def compute_hash(self):
        return sha256(json.dumps(self.__dict__, sort_keys=True)).hexdigest()