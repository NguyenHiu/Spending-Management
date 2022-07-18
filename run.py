from blockchain import *
from node import *
import key
import socket
import random as rd

DEFAULT_IP = "127.0.0."
DEFAULT_PORT = 60001
BUFFER_SIZE = 4096
SEPARATOR = '|'
REQUESTJOIN = 'join'
REQUESTPK = 'pk'

BANKER_SK = "-----BEGIN RSA PRIVATE KEY-----\nMIICWwIBAAKBgQDWpzX7Dwm2yzHY7Toi25UtTiRcEERXwlTMbw4i0RvoO+qf7JAF\nre53MLw7s7i3T5dFTUyI7yA/+jrSwkJ4RAqoJsvJj9JoPeO2kuE6xWF3ksmYY99V\n5oRDq1CqbG3nTqAAb2hSz8FXaLUQtjvA+qYYS/wxxbf0/FqatbphPhzx1wIDAQAB\nAoGAIBxrit85CMtk7Zqvc799lYV3Ev6r+qTropmKd9LoZdlww/PTp8XZQqNbxWKh\nY2rYqllh9aowHOIGIrlE0FD9dtv4/cMghO47GWZLjO1lqQDIc69BNh4f8RMO1J3x\nZiE3fmvod23N0dlJGyjo0zfDDddyS0gXILRebHK8bzj05MECQQDd5TyTU54MrzXI\nnpTtIuHZwP7fTWe7yXq/d8glxzoDz3ChtyHuPAIguLg04Yvg3fKAY6+mVaUGlP32\n5GYx1Q25AkEA96UEXcfMAB04lKd1q3k4s3W8GPdQDR4H0xiALg2o8Q1cA2gzHpb+\nZ45Z6je8jaiqy7JXBzGehHgyExoHcNxEDwJAXlzD++sNRVulRaGat5Wj8hROzut9\n96/g0VfA97/XfhNTVJIqjcNbLEshmutnrsL0A4FhCx1Uxo3JypqqkvqFkQJAJsIT\n4d2QRwBLx7BB0VmCj0vA6aNjSvpFPTubbBnFNBzkJsBbJ9F39Zso5WhdwUoBmSnL\nRxvz9EWfiK/NNFO07wJAEzm/WbjRTh1fyIbGDlK19C7hi4EWJEdl3+9Z3e4MnGGD\nxTKN5ZUFmJjDhTcKn468cSHUHUIcJoOvpVIlj1V8ww==\n-----END RSA PRIVATE KEY-----"
BANKER_PK = "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAAAgQDWpzX7Dwm2yzHY7Toi25UtTiRcEERXwlTMbw4i0RvoO+qf7JAFre53MLw7s7i3T5dFTUyI7yA/+jrSwkJ4RAqoJsvJj9JoPeO2kuE6xWF3ksmYY99V5oRDq1CqbG3nTqAAb2hSz8FXaLUQtjvA+qYYS/wxxbf0/FqatbphPhzx1w=="

class Run:
    # 127.0.0.x
    def __init__(self):
        self.x = 2
        self.banker = False
        self.pkDictionary = {}
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind(("127.0.0.1", 60001))
        self.socket.listen(1)
        Thread(target=self.accept_connect, daemon=True).start()
        
    
    def newAddress(self):
        addr = (DEFAULT_IP+str(self.x), DEFAULT_PORT)
        self.x += 1
        return addr

    
    def newKey(self):
        sk, pk = key.generate_key()
        return sk, pk

    
    def accept_connect(self):
        while True:
            self.client, _ = self.socket.accept()

            Thread(target=self.recvMsg, daemon=True).start()

    def recvMsg(self):
        while True:
            try:
                cmd = ""
                cmd = self.client.recv(BUFFER_SIZE).decode("utf8")
                print('cmd: ' + cmd)
            except socket.error:
                continue

            if cmd == "":
                # return
                continue
            
            elif cmd[0:4] == REQUESTJOIN:
                _, name = cmd.split(SEPARATOR)

                print('name: ' + name)

                newAddr = self.newAddress()
                
                sk = ""
                pk = ""
                if not self.banker:
                    sk = BANKER_SK
                    pk = BANKER_PK
                    self.banker = True
                else:
                    sk, pk = self.newKey()

                self.pkDictionary[name] = pk

                nodeConnect = "0|0"              
                if self.x != 3:
                    nodeConnect = DEFAULT_IP + str(rd.randint(2, self.x-2)) + SEPARATOR + str(DEFAULT_PORT)

                msg = ""
                msg = newAddr[0] + SEPARATOR + str(newAddr[1]) + SEPARATOR + sk + SEPARATOR + pk + SEPARATOR + nodeConnect

                print('msg: ' + msg)

                self.client.sendall(bytes(msg, 'utf-8'))
                self.client.close()

                return

            elif cmd[0:2] == REQUESTPK:
                _, name = cmd.split(SEPARATOR)
                
                msg = "~|"
                if name in self.pkDictionary:
                    msg = self.pkDictionary[name]
                
                self.client.sendall(bytes(msg,'utf-8'))
                self.client.close()

                return

            else:
                continue
            

run = Run()
abc = ""
while abc != "STOP":
    abc = input('If u want to stop the process, please type "STOP": ')