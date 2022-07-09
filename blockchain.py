from hashlib import sha256
from block import Block
import json
import time

class Blockchain:
    def __init__(self, _difficult=1):
        self.unconfirm_transactions = []
        self.chain = []
        self.first_block()
        self.difficult = _difficult

    def first_block(self):
        fBlock = Block(0, [], 0, "0")
        fBlock.hash = fBlock.compute_hash()
        self.chain.append(fBlock)
    
    def last_block(self):
        return self.chain[-1]

    def proof_of_work(self, block):
        block.nonce = 0

        res = block.compute_hash()
        while not res.startswith('0' * self.difficult):
            block.nonce += 1
            res = block.compute_hash()
        
        return res

    def is_valid_proof(self, block, proof):
        return (proof.startswith('0' * self.difficult) and proof == block.compute_hash())

    def add_block(self, block):
        print()

