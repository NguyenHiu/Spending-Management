from calendar import c
from textwrap import fill
from node import Node
import key
import time
import socket

import tkinter as tk
from tkinter import Toplevel, ttk
from PIL import Image, ImageTk


class User:
    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry('450x250')
        self.root.title('Spending Management')

        self.create_Join_Frame(self.root)
        self.create_Feature_Frame(self.root)
        self.create_GetBalance_Frame(self.root)
        self.root.join_frame.pack()

    
    def run(self):
        self.root.mainloop()

        
    def create_Join_Frame(self, root):
        # Join Frame
        root.join_frame = tk.Frame(root)
        root.join_frame.title = tk.Label(root.join_frame, text="Spending Managament", font="Bold 20")
        root.join_frame.name_label = tk.Label(root.join_frame, text="Input your name:")
        root.join_frame.name_input = tk.Entry(root.join_frame)
        root.join_frame.join_btn = tk.Button(root.join_frame, text="Join", command=self.join)
        root.join_frame.warning = tk.Label(root.join_frame, text="", foreground='red')
        # grid
        root.join_frame.title.grid(column=0, row=0, columnspan=2)
        root.join_frame.name_label.grid(column=0, row=1)
        root.join_frame.name_input.grid(column=1, row=1)
        root.join_frame.join_btn.grid(column=0, row=2, columnspan=2)
        root.join_frame.warning.grid(column=0, row=3, columnspan=2)


    def create_Feature_Frame(self, root):
        # Features Frame
        root.feature_frame = tk.Frame(root)
        root.feature_frame.title = tk.Label(root.feature_frame, text="Features", font="20")
        root.feature_frame.get_balance = tk.Button(root.feature_frame, text="Get balance", command=self.FeatureFrame2GetBalanceFrame)
        root.feature_frame.create_transaction = tk.Button(root.feature_frame, text="Create transaction", command=self.FeatureFrame2CreateTransactionFrame)
        root.feature_frame.title.grid(row=0)
        root.feature_frame.get_balance.grid(row=1)
        root.feature_frame.create_transaction.grid(row=2)

    
    def create_CreateTransaction_Frame(self, root):
        # Create Transaction Frame
        root.create_transaction_frame = tk.Frame(root)
        root.create_transaction_frame.title = tk.Label(root.create_transaction_frame, text="Create transaction", font="20")
        root.create_transaction_frame.name_label = tk.Label(root.create_transaction_frame, text="Receiver's name: ")
        root.create_transaction_frame.name_input = tk.Entry(root.create_transaction_frame, )
        root.create_transaction_frame.amount_label = tk.Label(root.create_transaction_frame, text="Amount: ")
        root.create_transaction_frame.amount_input = tk.Entry(root.create_transaction_frame, )
        root.create_transaction_frame.note_label = tk.Label(root.create_transaction_frame, text="Note: ")
        root.create_transaction_frame.note_input = tk.Entry(root.create_transaction_frame, )
        root.create_transaction_frame.warning = tk.Label(root.create_transaction_frame, text="", foreground='red')
        root.create_transaction_frame.create_btn = tk.Button(root.create_transaction_frame, text="Create", command=self.create_transaction)
        # grid
        root.create_transaction_frame.title.grid(column=1, row=1, columnspan=2)
        root.create_transaction_frame.name_label.grid(column=1, row=2)
        root.create_transaction_frame.name_input.grid(column=2, row=2)
        root.create_transaction_frame.amount_label.grid(column=1, row=3)
        root.create_transaction_frame.amount_input.grid(column=2, row=3)
        root.create_transaction_frame.note_label.grid(column=1, row=4)
        root.create_transaction_frame.note_input.grid(column=2, row=4)
        root.create_transaction_frame.create_btn.grid(column=1, row=5, columnspan=2)
        root.create_transaction_frame.warning.grid(column=1, row=6, columnspan=2)


    def create_GetBalance_Frame(self, root):
        # Get Balance
        root.get_balance = tk.Frame(root)
        root.get_balance.balance = tk.Label(root.get_balance, text="")
        # grid
        root.get_balance.balance.grid(row=0)
        

    def FeatureFrame2CreateTransactionFrame(self):
        self.root.create_transaction_newWin = Toplevel(self.root)
        self.create_CreateTransaction_Frame(self.root.create_transaction_newWin)
        self.root.create_transaction_newWin.create_transaction_frame.pack()


    def FeatureFrame2GetBalanceFrame(self):
        self.root.get_balance.balance.configure(text=str(self.node.getBalanceOf(self.node.pubKey)), foreground='green')
        self.root.get_balance.pack()

    
    def join(self):
        _name = self.root.join_frame.name_input.get()
        if not _name:
            self.root.join_frame.warning.configure(text="Please input your name !", foreground='red')
        else:
            self.root.join_frame.warning.configure(text="")

            requestJoin = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            requestJoin.connect(("127.0.0.1", 60001))
            requestJoin.sendall(bytes("join|"+_name, 'utf-8'))
            MSG = ""
            MSG = requestJoin.recv(4096).decode("utf8")
            requestJoin.close()

            self.ip, self.port, self.sk, self.pk, self.ip_cn, self.port_cn = MSG.split("|")
            self.node = Node(_name, self.sk, self.pk, (self.ip, int(self.port)), (self.ip_cn, int(self.port_cn)), 3)

            self.root.join_frame.forget()
            self.root.feature_frame.pack()

    
    def create_transaction(self):
        recv_name = self.root.create_transaction_newWin.create_transaction_frame.name_input.get()
        amount = self.root.create_transaction_newWin.create_transaction_frame.amount_input.get()
        note = self.root.create_transaction_newWin.create_transaction_frame.note_input.get()

        if (not recv_name) or (not amount) or (not note):
            self.root.create_transaction_newWin.create_transaction_frame.warning.configure(text="Please fill-in something :'( ", foreground='red')
        else:
            msg = "pk" +  "|" + recv_name
            requestPK = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            requestPK.connect(("127.0.0.1", 60001))
            requestPK.sendall(bytes(msg, 'utf-8'))
            _pk = requestPK.recv(4096).decode('utf-8')
            requestPK.close()

            if _pk == "~|":
                self.root.create_transaction_newWin.create_transaction_frame.warning.configure(text="Receiver's name does not exist !", foreground='red')
            else:
                self.node.create_transaction(_pk, int(amount), note)
                self.root.create_transaction_newWin.create_transaction_frame.warning.configure(text="Create Successfully !", foreground='green')


user = User()
user.run()