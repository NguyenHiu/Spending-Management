'''
    Khi khoi tao 1 Unility thi se mo socket 
'''

from threading import Thread
from block import Block
import random as rd
import socket
# import json
# import time

requestMsg = 'please'

class Postman:
    def __init__(self, _ip, _port, _firstRelation, _max = 5):
        self.max = _max # the maximum number of connections
        self.ip = _ip
        self.port = _port
        # self.wait = True
        self.connections = []
        Thread(target=self.accept_connect, daemon=True).start()
        self.getConnection(_postman=_firstRelation)
        # self.waitBlock()
        

    def getConnection(self, connection): # connection = [(socket, addr), (socket, addr), ...]
        newConnection = connection
        for i in range(0, rd.randint(1, self.max)):
            _, newConnection = connection.getConnectionAt(rd.randint(0, connection.getSize()))

            if newConnection == connection:
                i -= 1
                continue
            
            self.requestConnection(connection)
            newConnection = connection
            self.connections.append(connection)


    def requestConnection(self, socket):
        socket.sendall(bytes(requestMsg,encoding='utf8'))
    
    def getSize(self):
        return len(self.connections)


    def getConnectionAt(self, index):
        return self.relations[index][0], self.relations[index][1] # return (connect, addr)


    # def waitBlock(self, lastBlock=0):
    #     # self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    #     if self.wait:     
    #         # self.IP = (self.ip, self.port) # Day chi la tuong trung, chac phai tim hieu lai :< quen het r
    #         # self.socket.bind(self.IP)
    #         # self.socket.listen(1)
    #         Thread(target=self.accept_connect, daemon=True).start()
    #         # time.sleep(30)
    #     else:
    #         self.sendBroadcast(lastBlock)
                    

    def accept_connect(self):
        # self.connect, addr = self.socket.accept()
        # if addr not in self.relations:
        #     self.connect.close()
        #     print('not neighbor !')
        #     return

        while True:
            for i in self.connections:
                try:
                    cmd = i[0].recv(64)
                except:
                    continue
                # ....
                # set up here
                print(cmd)

                # self.connect.close()
                # ....  


    def sendBroadcast(self, msg):
        # self.socket.close()
        # self.wait = False
        if self.connections != []:
            for i in self.connections:
                # self.socket.connect((i[0], i[1]))
                i[0].sendall(msg)
                # self.socket.close()

        # self.wait = True

    
    def killTheNode(self):
        for i in self.connections:
            i[0].close()

    # def send(self, msg):
    #     # self.socket.close()
    #     self.socket.connect(('127.0.1.1', 60001))
    #     self.socket.sendall(bytes(msg,encoding='utf8'))
    #     self.socket.close()


# a = Utility('127.0.1.2', 60002)