from hashlib import sha256
from block import *
import json
import time

from transaction import Transaction

class Blockchain:
    def __init__(self, _difficulty=1):
        self.unconfirm_transactions = []
        self.chain = []
        self.difficulty = _difficulty
        self.first_block()


    def first_block(self):
        fBlock = Block(0, [], 0, "0")
        # fBlock.hash = fBlock.compute_hash()
        # print('in blockchain: ', end="")
        # print(fBlock.hash)
        self.chain.append(fBlock)
        # self.output()


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


    def is_valid_proof(self, block):#, proof):
        return block.compute_hash().startswith('0' * self.difficulty)
        # return (proof.startswith('0' * self.difficult) and proof == block.compute_hash())


    def add_block(self, block):#, hash_val):
        # block.hash = hash_val
        self.chain.append(block)
    

    def add_transaction(self, transaction):
        # jsonTrans = json.dumps(transaction.__dict__)
        # self.unconfirm_transactions.append(jsonTrans)
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
        # print('<><><><><><> publickey: ' + SO)
        for so in self.chain:
            for trans in so.transactions:
                if trans.receiver == SO:
                    balance += trans.amount
                    print(trans.amount)
                if trans.sender == SO:
                    balance -= trans.amount
                    print(trans.amount)
        # print(">>>>>> Balance: " + str(balance))
        return balance


    def verifyBlock(self, block):
        last_hash = self.last_block().compute_hash()
        # print('lash_hash: ', end="")
        # print(last_hash)
        # verify transactions of the block ?  --> Dunno ...
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
