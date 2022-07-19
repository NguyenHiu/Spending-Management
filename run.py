from threading import Thread
import tkinter as tk
import random as rd
import socket
import key

BANKER_SK = "-----BEGIN RSA PRIVATE KEY-----\nMIICWwIBAAKBgQDWpzX7Dwm2yzHY7Toi25UtTiRcEERXwlTMbw4i0RvoO+qf7JAF\nre53MLw7s7i3T5dFTUyI7yA/+jrSwkJ4RAqoJsvJj9JoPeO2kuE6xWF3ksmYY99V\n5oRDq1CqbG3nTqAAb2hSz8FXaLUQtjvA+qYYS/wxxbf0/FqatbphPhzx1wIDAQAB\nAoGAIBxrit85CMtk7Zqvc799lYV3Ev6r+qTropmKd9LoZdlww/PTp8XZQqNbxWKh\nY2rYqllh9aowHOIGIrlE0FD9dtv4/cMghO47GWZLjO1lqQDIc69BNh4f8RMO1J3x\nZiE3fmvod23N0dlJGyjo0zfDDddyS0gXILRebHK8bzj05MECQQDd5TyTU54MrzXI\nnpTtIuHZwP7fTWe7yXq/d8glxzoDz3ChtyHuPAIguLg04Yvg3fKAY6+mVaUGlP32\n5GYx1Q25AkEA96UEXcfMAB04lKd1q3k4s3W8GPdQDR4H0xiALg2o8Q1cA2gzHpb+\nZ45Z6je8jaiqy7JXBzGehHgyExoHcNxEDwJAXlzD++sNRVulRaGat5Wj8hROzut9\n96/g0VfA97/XfhNTVJIqjcNbLEshmutnrsL0A4FhCx1Uxo3JypqqkvqFkQJAJsIT\n4d2QRwBLx7BB0VmCj0vA6aNjSvpFPTubbBnFNBzkJsBbJ9F39Zso5WhdwUoBmSnL\nRxvz9EWfiK/NNFO07wJAEzm/WbjRTh1fyIbGDlK19C7hi4EWJEdl3+9Z3e4MnGGD\nxTKN5ZUFmJjDhTcKn468cSHUHUIcJoOvpVIlj1V8ww==\n-----END RSA PRIVATE KEY-----"
BANKER_PK = "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAAAgQDWpzX7Dwm2yzHY7Toi25UtTiRcEERXwlTMbw4i0RvoO+qf7JAFre53MLw7s7i3T5dFTUyI7yA/+jrSwkJ4RAqoJsvJj9JoPeO2kuE6xWF3ksmYY99V5oRDq1CqbG3nTqAAb2hSz8FXaLUQtjvA+qYYS/wxxbf0/FqatbphPhzx1w=="
DEFAULT_IP = "127.0.0."
REQUESTJOIN = 'join'
REQUESTNAME = 'name'
DEFAULT_PORT = 60001
BUFFER_SIZE = 4096
REQUESTPK = 'pk'
SEPARATOR = '|'

class Run:
    # 127.0.0.x
    def __init__(self):
        # UI - tkinter
        self.root = tk.Tk()
        self.root.geometry('450x250')
        self.root.title('Hub')

        self.root.title = tk.Label(text="Spending Management", font='30')
        self.root.start_btn = tk.Button(self.root, text="START",
                                                   command=self.start,
                                                   compound=tk.TOP)
        self.root.close_btn = tk.Button(self.root, text="CLOSE",
                                                   command=self.close,
                                                   compound=tk.TOP)
        self.root._status = tk.Label(text="Status:", font='Bold 15')
        self.root.status = tk.Label(text="Closed", fg='red', font='15')

        self.root.title.grid(column=0, row=0, columnspan=2)
        self.root._status.grid(column=0, row=1)
        self.root.status.grid(column=1, row=1)
        self.root.start_btn.grid(column=0, row=2)
        self.root.close_btn.grid(column=1, row=2)

    def start(self):
        if self.root.start_btn["text"] == "START":
            self.root.status.configure(text="Opening...", fg='green', font='15')

            self.x = 2
            self.banker = False
            self.pkDictionary = {}
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.bind(("127.0.0.1", 60001))
            self.socket.listen(1)
            Thread(target=self.accept_connect, daemon=True).start()


    def close(self):
        self.root.status.configure(text="Closed", fg='red', font='15')
        self.root.destroy()


    def run(self):
        self.root.mainloop()

    
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
                # print('cmd: ' + cmd)
            except socket.error:
                continue

            if cmd == "":
                # return
                continue
            
            elif cmd[0:4] == REQUESTJOIN:
                _, name = cmd.split(SEPARATOR)

                # print('name: ' + name)

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

                # print('msg: ' + msg)

                self.client.sendall(bytes(msg, 'utf-8'))
                self.client.close()

                return

            elif cmd[0:4] == REQUESTNAME:
                _, pk = cmd.split(SEPARATOR)

                msg = "~|"
                for _name, _pk in self.pkDictionary.items():
                    if _pk == pk:
                        msg = _name

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
run.run()