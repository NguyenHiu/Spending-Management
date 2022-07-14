from hashlib import sha256
from block import *
import json
import time

class Blockchain:
    def __init__(self, _difficulty=1):
        self.unconfirm_transactions = []
        self.chain = []
        self.first_block()
        self.difficulty = _difficulty

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

    def add_block(self, block, hash_val):
        block.hash = hash_val
        self.chain.append(block)
    
    def add_transaction(self, transaction):
        jsonTrans = json.dumps(transaction.__dict__)
        self.unconfirm_transactions.append(jsonTrans)

    def proof_of_work(self, block):
        """
        Function that tries different values of nonce to get a hash
        that satisfies our difficulty criteria.
        """
        block.nonce = 0

        computed_hash = block.compute_hash()
        while not computed_hash.startswith('0' * self.difficulty):
            block.nonce += 1
            computed_hash = block.compute_hash()

        return computed_hash
    
    def mine(self):
        if not self.unconfirm_transactions:
            return False

        last_block = self.last_block()

        new_block = Block(last_block.id + 1, 
        self.unconfirm_transactions, last_block.hash, 0)
    
        hash_val = self.proof_of_work(new_block)
        self.add_block(new_block, hash_val)
        self.unconfirm_transactions = []
        return new_block.id
