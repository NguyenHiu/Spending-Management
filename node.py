from hashlib import sha256
from block import Block
import json
import time

class Node:
    def __init__(self, _name, _priKey, _pubKey):
        '''Sau khi tao thi se goi co-che-dong-thuan de copy chain cua node khac !'''
        self.name = _name
        self.priKey = _priKey
        self.pubKey = _pubKey
        # consensus

    # def consensus(self)