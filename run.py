from turtle import color
from blockchain import *
from node import *
import key
import socket
import random as rd

import tkinter as tk
from tkinter import Toplevel, ttk
from PIL import Image, ImageTk


DEFAULT_IP = "127.0.0."
DEFAULT_PORT = 60001
REQUESTJOIN = 'join'
REQUESTPK = 'pk'

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