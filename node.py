from transaction import Transaction
from blockchain import Blockchain
from threading import Thread
from hashlib import sha256
from block import Block
import random as rd
import socket
import time
import json
import key

REQUESTBLOCKCHAIN = 'blockchain'
BROADCASTBLOCK = 'bblock'
REQUESTADDR = 'addr'
BUFFER_SIZE = 4096
SEPARATOR = '|'

class Node:
    def __init__(self, _name, _priKey, _pubKey, _addr, _connectedBlock=("0", 0), _max=5):
        self.name = _name
        self.priKey = _priKey
        self.pubKey = _pubKey
        self.max = _max # the maximum number of connections
        self.addr = _addr

        self.receiver = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.receiver.bind(self.addr)
        self.receiver.listen(1) # 1 or 2 or 3 or ?
        self.sender = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


        self.connections = []
        self.getConnection(_connectedBlock)

        # print("Done Get-Connection")

        self.blockchain = Blockchain()
        self.requestBlockchain() # copy blockchain from connected nodes
        # self.blockchain.output()

        # print("Done Request-Blockchain")

        self.accept_signal = True
        self.recv_signal = True
        # self.send_signal = True
        
        self.Thread_accept = Thread(target=self.accept, daemon=True)
        self.Thread_accept.start()

        # time.sleep(30)


    def requestBlockchain(self):
        if self.connections == []:
            return

        # find the longest chain of connected nodes
        maxChain = str(self.blockchain.length())
        for addr in self.connections:
            self.sender.connect(addr)
            self.sender.sendall(bytes(REQUESTBLOCKCHAIN, "utf8"))
            _chain = self.sender.recv(BUFFER_SIZE).decode("utf8")
            # print("<<<<<<< Receive blockchain >>>>>\n" + _chain)
            self.sender.close()
            self.sender = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            if int(_chain[0]) > int(maxChain[0]):
                maxChain = _chain

        if maxChain == str(self.blockchain.length()):
            return
        
        maxChain = maxChain.split(SEPARATOR)
        self.blockchain.convertJson2Chain(json.loads(maxChain[1]))

    def getConnection(self, addr): 
        if (addr == ("0", 0)) or (addr == self.addr):
            return

        msg = REQUESTADDR + SEPARATOR + self.addr[0] + SEPARATOR + str(self.addr[1])

        for i in range(0, rd.randint(1, self.max)):
            if addr not in self.connections:
                self.connections.append(addr)

            self.sender.connect(addr)
            self.sender.sendall(bytes(msg, "utf8")) # request new addr
            _addr = self.splitMsg1(self.sender.recv(BUFFER_SIZE).decode("utf8"))
            self.sender.close()
            self.sender = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            if _addr != self.addr:
                addr = _addr

        # print('* Get Connections: ')
        # self.printConnections()
            
    
    def getSize(self):
        return len(self.connections)


    def accept(self):
        while self.accept_signal:
            self.client, _ = self.receiver.accept()

            self.Thread_recv = Thread(target=self.recvMsg, daemon=True)
            self.Thread_recv.start()
            # self.Thread_recv.join()


    def recvMsg(self):
        while self.recv_signal:
            try:
                cmd = self.client.recv(BUFFER_SIZE).decode("utf8")
                # print("    > cmd: " + cmd)
            except socket.error:
                continue

            if cmd == "":
                continue
            
            elif cmd[0:4] == REQUESTADDR:
                _in4 = cmd.split(SEPARATOR)
                # print(_in4)
                msg = self.randomAddr()
                self.client.sendall(bytes(msg, "utf8"))
                if (_in4[1], int(_in4[2])) not in self.connections:
                    self.connections.append((_in4[1], int(_in4[2])))
                self.client.close() 
                cmd = ""
                return

            elif (len(cmd) >= 6) and (cmd[0:6] == BROADCASTBLOCK):
                _in4 = cmd.split(SEPARATOR)
                # print(cmd)
                # print(_in4)

                # newBlock = Block()
                block = json.loads(_in4[1])
                # print('--------------')
                # print(block)
                # print('--------------')
                newBlock = Block.convertJson2Block(block)
                # print('newBlock\'s previous hash: ', end="")
                # print(newBlock.prevHash)
                if self.blockchain.is_valid_proof(newBlock) and self.blockchain.verifyBlock(newBlock):
                    self.blockchain.add_block(newBlock)
                    # print("    > Blockchain after add: ")
                    # self.blockchain.output()
                    self.sendBroadcast(cmd)
                cmd = ""
                return

            elif (len(cmd) >= 10) and (cmd[0:10] == REQUESTBLOCKCHAIN):
                # print(json.dumps(self.blockchain.convertChain2Json()))
                msg = str(self.blockchain.length()) + SEPARATOR + json.dumps(self.blockchain.convertChain2Json())
                # print('>>>>>> send blockchain <<<<<<<<')
                self.client.sendall(bytes(msg, "utf8"))
                self.client.close()
                cmd = ""
                return

            else:
                # print('(X) outto!')
                return


    def verifyBlock(self, block):
        return self.blockchain.verifyBlock(block)


    def randomAddr(self):
        if self.getSize() == 0:
            return self.addr[0]+SEPARATOR+str(self.addr[1])
        rand = rd.randint(0, self.getSize()-1)
        # print(self.connections[rand])
        return self.connections[rand][0]+SEPARATOR+str(self.connections[rand][1])


    def splitMsg1(self, msg):
        ip, _port = msg.split(SEPARATOR)
        return (ip, int(_port))


    def printConnections(self):
        print("- List of connections:")
        for addr in self.connections:
            print("   + ", end="")
            print(addr)


    def sendBroadcast(self, msg):
        # signature = key.sign(msg, self.priKey)
        for addr in self.connections:
            msg_temp = msg
            # print("    > cmd will be broadcasted: " + msg_temp)
            self.sender.connect(addr)
            self.sender.sendall(bytes(msg_temp, "utf8"))
            self.sender.close()
            self.sender = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        msg = ""

    
    def verifyTransaction(self, transaction):
        # Check if the transaction comes from right node.
        if not key.verify(json.dumps(transaction.toJson()), transaction.signature, transaction.sender):
            # the transaction is not valid
            return False

        # Check if amount <= balance of sender
        # if self.getBalanceOf(self.sender) < transaction.amount:
        #     return False

        # Check if receiver is valid
        # chua nghi ra

        return True


    def getBalanceOf(self, SO):
        return self.blockchain.getBalanceOf(SO)


    def create_transaction(self, receiver, amount, note):
        transaction = Transaction(receiver, self.pubKey, self.priKey, amount, note, time.time())

        # special case: after creating a transaction, blockchain will take it and generate a block, then broadcast, 
        #               but we still have the same verification function as bitcoin (even though not even any value)
        if not self.verifyTransaction(transaction):
            return False

        self.blockchain.add_transaction(transaction)
        self.blockchain.mine()
        msg = BROADCASTBLOCK + SEPARATOR + json.dumps(self.blockchain.last_block().convertBlock2Json())
        self.sendBroadcast(msg)
        msg = ""
        # -------------------------------

        return transaction

    
    def _deposit(self, amount):
        transaction = Transaction(self.pubKey, self.pubKey, self.priKey, amount, "Deposit", time.time())
        self.blockchain.add_transaction(transaction)
        self.blockchain.mine()
        self.sendBroadcast(BROADCASTBLOCK + SEPARATOR + json.dumps(self.blockchain.last_block.__dict__))