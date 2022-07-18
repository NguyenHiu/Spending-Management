from transaction import Transaction
from hashlib import sha256
from block import *
import json

class Blockchain:
    def __init__(self, _difficulty=1):
        self.unconfirm_transactions = []
        self.chain = []
        self.difficulty = _difficulty
        self.first_block()


    def first_block(self):
        fBlock = Block(0, [], 0, "0")
        self.chain.append(fBlock)


    def convertJson2Chain(self, msg):
        self.difficulty = msg["difficulty"]
        un_trans = msg["unconfirm_transactions"]

        self.unconfirm_transactions = []
        for trans in un_trans:
            self.unconfirm_transactions.append(Transaction.Json2Transaction(trans))

        _chain = msg["chain"]
        self.chain = []
        for block in _chain:
            self.chain.append(Block.convertJson2Block(block))


    def convertChain2Json(self):
        str = {
            "unconfirm_transactions": [],
            "chain": [],
            "difficulty": self.difficulty
        }
        for trans in self.unconfirm_transactions:
            str["unconfirm_transactions"].append(trans.toJson_())

        for block in self.chain:
            str["chain"].append(block.convertBlock2Json())

        return str


    def last_block(self):
        return self.chain[-1]


    def length(self):
        return len(self.chain)


    def is_valid_proof(self, block):
        return block.compute_hash().startswith('0' * self.difficulty)


    def add_block(self, block):
        self.chain.append(block)
    

    def add_transaction(self, transaction):
        self.unconfirm_transactions.append(transaction)


    def proof_of_work(self, block):
        block.nonce = 0

        computed_hash = block.compute_hash()
        while not computed_hash.startswith('0' * self.difficulty):
            block.nonce += 1
            computed_hash = block.compute_hash()

        return computed_hash
    

    def getBalanceOf(self, SO):
        balance = 0
        for so in self.chain:
            for trans in so.transactions:
                if trans.receiver == SO:
                    balance += trans.amount
                if trans.sender == SO:
                    balance -= trans.amount
        return balance


    def verifyBlock(self, block):
        last_hash = self.last_block().compute_hash()
        if block.prevHash == last_hash:
            return True
        return False


    def mine(self):
        if not self.unconfirm_transactions:
            return False

        last_block = self.last_block()

        new_block = Block(last_block.id + 1, 
                          self.unconfirm_transactions, last_block.compute_hash(), 0)
    
        hash_val = self.proof_of_work(new_block)
        self.add_block(new_block)#, hash_val)
        self.unconfirm_transactions = []
        return new_block.id


    def output(self):
        print("---Begin Blockchain---")
        print("       * Unconfirm_Transaction: ")
        for trans in self.unconfirm_transactions:
            print("            " + json.dumps(trans.toJson()))

        print("       * Chain: ")
        for block in self.chain:
            print("            " + json.dumps(block.convertBlock2Json()))

        print("       * Difficulty: " + str(self.difficulty))
        print("---End Blockchain---")