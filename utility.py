'''
    Su dung mo hinh small-world: Beta ~0.6 (chon bua)


    Khi khoi tao 1 Unility thi se mo socket 
'''

import socket
import random
from threading import Thread
from block import Block
import json
import time


class Utility:
    def __init__(self, _ip, _port):
        self.ip = _ip
        self.port = _port
        self.associations = []
        self.wait = False
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.waitBlock()
        

    def waitBlock(self, lastBlock=0):

        if self.wait:     

            # print('a')
            self.IP = (self.ip, self.port) # Day chi la tuong trung, chac phai tim hieu lai :< quen het r
            self.socket.bind(self.IP)
            self.socket.listen(1)
            Thread(target=self.accept_connect, daemon=True).start()

            time.sleep(30)

        else:
            self.send(msg='abc')
                    

    def accept_connect(self):
        self.connect, addr = self.socket.accept()
        
        while True:
            try:
                cmd = self.connect.recv(64)
            except:
                continue
            # ....
            # set up here
            print(cmd)

            self.connect.close()
            # ....  

    def getAssociation(self, block):
        print("do something xD")

    def sendBroadcast(self, block):
        # self.socket.close()
        if self.associations != []:
            for i in self.associations:
                self.socket.connect((i[0], i[1]))
                self.socket.sendall(block)
                self.socket.close()

        self.wait = True

    def send(self, msg):
        # self.socket.close()
        self.socket.connect(('127.0.1.1', 60001))
        self.socket.sendall(bytes(msg,encoding='utf8'))
        self.socket.close()


# a = Utility('127.0.1.2', 60002)