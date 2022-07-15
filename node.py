from hashlib import sha256
from block import Block
from transaction import Transaction
from blockchain import Blockchain
import json
import time
import socket
from threading import Thread
import random as rd

REQUESTADDR = 'addr'
REQUESTBLOCK = 'block'
REQUESTBLOCKCHAIN = 'blockchain'

BUFFER_SIZE = 4096

class Node:
    def __init__(self, _name, _priKey, _addr, _connectedBlock=("0", 0), _max=5):
        '''
        Sau khi tao thi se goi co-che-dong-thuan de copy chain cua node khac !
        '''
        self.receiver = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.receiver.bind(self.addr)
        self.receiver.listen(1) # 1 or 2 or 3 or ?
        self.sender = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.name = _name
        self.priKey = _priKey
        self.addr = _addr

        self.connections = []
        self.getConnection(_connectedBlock)

        self.blockchain = Blockchain()
        self.requestBlockchain() # copy blockchain from connected nodes

        self.max = _max # the maximum number of connections
        self.accept_signal = True
        self.recv_signal = True
        # self.send_signal = True
        
        self.Thread_accept = Thread(target=self.accept, daemon=True)
        self.Thread_accept.start()

        # consensus

    def requestBlockchain(self):
        if self.connections == []:
            return

        # find the longest chain of connected nodes
        maxChain = "0"
        for addr in self.connections:
            self.sender.connect(addr)
            self.sender.sendall(bytes(REQUESTBLOCKCHAIN, "utf8"))
            _chain = self.sender.recv(BUFFER_SIZE).decode("utf8")
            if int(_chain[0]) > int(maxChain[0]):
                maxChain = _chain

        self.blockchain.convertJson2Chain(maxChain[1:-1])

    def getConnection(self, addr): 
        if addr == ("0", 0):
            return

        msg = REQUESTADDR + "," + self.addr[0] + "," + str(self.addr[1])
        check = False

        self.sender.connect(addr)
        self.connections.append(addr)
        
        for i in range(0, rd.randint(1, self.max)):
            self.sender.sendall(bytes(msg, "utf8")) # request new addr
            addr = self.splitMsg1(self.sender.recv(BUFFER_SIZE).decode("utf8"))

            self.sender.close()
            self.sender = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            if addr in self.connections:
                check = True
                continue      
            
            check = False

            self.sender.connect(addr)
            self.connections.append(addr) 

        if not check:
            self.sender.close()
            self.sender = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    
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
                print("cmd: " + cmd)
            except:
                continue
            if cmd[0:4] == REQUESTADDR:
                _in4 = cmd.split(",")
                print(_in4)
                msg = self.randomAddr()
                self.client.sendall(bytes(msg, "utf8"))
                if (_in4[1], int(_in4[2])) not in self.connections:
                    self.connections.append((_in4[1], int(_in4[2])))
                self.client.close() 
                return
            elif (len(cmd) > 5) and (cmd[0:5] == REQUESTBLOCK):
                _in4 = cmd.split(",", 1)
                print(_in4)
                # block = Block(_in4[1])
                # if self.verifyBlock(block):
                    # add block
                    # broadcast block
            elif (len(cmd) > 9) and (cmd[0:9] == REQUESTBLOCKCHAIN):
                return
            else:
                print('outto!')
                return


    def verifyBlock(self, block):
        # if block in self.blocks[]
        # return False
        return True


    def randomAddr(self):
        if self.getSize() == 0:
            return self.ip+","+str(self.port)
        rand = rd.randint(0, self.getSize()-1)
        print(self.connections[rand])
        return self.connections[rand][0]+","+str(self.connections[rand][1])


    def splitMsg1(self, msg):
        ip, _port = msg.split(",")
        return (ip, int(_port))


    def printConnections(self):
        print("- List of connections:")
        for addr in self.connections:
            print("   + ", end="")
            print(addr)


    def sendBroadcast(self, msg):
        for addr in self.connections:
            self.sender.connect(addr)
            self.sender.sendall(bytes(msg, "utf8"))
            # self.socket.close()

    # def consensus(self)
    def create_transaction(self, receiver, amount, note):
        '''
        Create a transaction
        '''
        # create a transaction
        transaction = Transaction(receiver, sha256(self.priKey), amount, note, time.time())
        return transaction