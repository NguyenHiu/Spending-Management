from tkinter import Toplevel, ttk
from node import Node
import tkinter as tk
import socket
import time


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
        root.feature_frame.list_connections = tk.Button(root.feature_frame, text="List Connections", command=self.FeatureFrame2ListConnection)
        root.feature_frame.blockchain_detail = tk.Button(root.feature_frame, text="Blockchain Detail", command=self.FeatureFrame2BlockchainDetail)
        root.feature_frame.history = tk.Button(root.feature_frame, text="History", command=self.FreatureFrame2History)
        root.feature_frame.information = tk.Button(root.feature_frame, text="Information", command=self.FeatureFrame2Information)
        root.feature_frame.name = tk.Label(root.feature_frame, text="")

        root.feature_frame.title.grid(row=0)
        root.feature_frame.get_balance.grid(row=1)
        root.feature_frame.create_transaction.grid(row=2)
        root.feature_frame.list_connections.grid(row=3)
        root.feature_frame.blockchain_detail.grid(row=4)
        root.feature_frame.history.grid(row=5)
        root.feature_frame.information.grid(row=6)
        root.feature_frame.name.grid(row=7)


    def create_ListConnection_Frame(self, root):
        root.ListConnectionTable = tk.Frame(root)
        root.ListConnectionTable.list = ttk.Treeview(root.ListConnectionTable)
        root.ListConnectionTable.list['column'] = ("IP", "Port")

        root.ListConnectionTable.list.column("#0", anchor="w", width=30, stretch='NO')
        root.ListConnectionTable.list.column("IP", anchor="center", width=120, stretch='NO')
        root.ListConnectionTable.list.column("Port", anchor="center", width=200, stretch='NO')

        root.ListConnectionTable.list.heading("IP", text="IP", anchor="center")
        root.ListConnectionTable.list.heading("Port", text="Port", anchor="center")
        
        _list = self.node.GetConnections()
        for connection in _list:
            root.ListConnectionTable.list.insert('', tk.END, values=connection)

        root.ListConnectionTable.list.grid(row=0, column=0, sticky='nsew')

        scrollbar = ttk.Scrollbar(root.ListConnectionTable, orient=tk.VERTICAL, command=root.ListConnectionTable.list.yview)
        root.ListConnectionTable.list.configure(yscroll=scrollbar.set)
        scrollbar.grid(row=0, column=1, sticky='ns')

    
    def create_BlockchainDetail_Frame(self, root):
        root.BlockchainDetailTable = tk.Frame(root)
        root.BlockchainDetailTable.list = ttk.Treeview(root.BlockchainDetailTable)
        root.BlockchainDetailTable.list['column'] = ("BlockID", "TransactionID", "Sender", "Receiver", "Amount", "Note")

        root.BlockchainDetailTable.list.column("#0", anchor="center", width=30, stretch='NO')
        root.BlockchainDetailTable.list.column("BlockID", anchor="center", width=120, stretch='NO')
        root.BlockchainDetailTable.list.column("TransactionID", anchor="center", width=120, stretch='NO')
        root.BlockchainDetailTable.list.column("Sender", anchor="center", width=200, stretch='NO')
        root.BlockchainDetailTable.list.column("Receiver", anchor="center", width=200, stretch='NO')
        root.BlockchainDetailTable.list.column("Amount", anchor="center", width=200, stretch='NO')
        root.BlockchainDetailTable.list.column("Note", anchor="w", width=200, stretch='NO')
        
        root.BlockchainDetailTable.list.heading("BlockID", text="Block ID", anchor="center")
        root.BlockchainDetailTable.list.heading("TransactionID", text="Transaction ID", anchor="center")
        root.BlockchainDetailTable.list.heading("Sender", text="Sender", anchor="center")
        root.BlockchainDetailTable.list.heading("Receiver", text="Receiver", anchor="center")
        root.BlockchainDetailTable.list.heading("Amount", text="Amount", anchor="center")
        root.BlockchainDetailTable.list.heading("Note", text="Note", anchor="w")

        chain_infor = self.node.GetBlockchainInfor()
        # Get name via public key
        for block in chain_infor:
            for transaction in block:
                transaction[0] = self.requestNAMEviaPK(transaction[0])
                transaction[1] = self.requestNAMEviaPK(transaction[1])

        block_id = 0
        transaction_id = 1
        for block in chain_infor:
            for transaction in block:
                root.BlockchainDetailTable.list.insert('', tk.END, values=(block_id, transaction_id, transaction[0], transaction[1], transaction[2], transaction[3]))
                transaction_id += 1
            
            block_id += 1
            transaction_id = 1

        root.BlockchainDetailTable.list.grid(row=0, column=0, sticky='nsew')

        scrollbar = ttk.Scrollbar(root.BlockchainDetailTable, orient=tk.VERTICAL, command=root.BlockchainDetailTable.list.yview)
        root.BlockchainDetailTable.list.configure(yscroll=scrollbar.set)
        scrollbar.grid(row=0, column=1, sticky='ns')


    def create_YourInformation_Frame(self, root):
        root.YourInformation_Frame = tk.Frame(root)
        root.YourInformation_Frame.title = tk.Label(root.YourInformation_Frame, text="Your information", font="Bold 20")
        root.YourInformation_Frame._name = tk.Label(root.YourInformation_Frame, text="Name: ")
        root.YourInformation_Frame.name = tk.Label(root.YourInformation_Frame, text=self.root.name)
        root.YourInformation_Frame._PublicKey = tk.Label(root.YourInformation_Frame, text="Public Key: ")
        root.YourInformation_Frame.PublicKey = tk.Button(root.YourInformation_Frame, text="press to show", command=self.InformationFrame2PublicKeyFrame)
        root.YourInformation_Frame._PrivateKey = tk.Label(root.YourInformation_Frame, text="Private Key: ")
        root.YourInformation_Frame.PrivateKey = tk.Button(root.YourInformation_Frame, text="press to show", command=self.InformationFrame2PrivateKeyFrame)
        root.YourInformation_Frame._IP = tk.Label(root.YourInformation_Frame, text="IP: ")
        root.YourInformation_Frame.IP = tk.Label(root.YourInformation_Frame, text=self.node.addr[0])
        root.YourInformation_Frame._PORT = tk.Label(root.YourInformation_Frame, text="PORT: ")
        root.YourInformation_Frame.PORT = tk.Label(root.YourInformation_Frame, text=self.node.addr[1])

        root.YourInformation_Frame.title.grid(column=0, row=0, columnspan=2)
        root.YourInformation_Frame._name.grid(column=0, row=1)
        root.YourInformation_Frame.name.grid(column=1, row=1)
        root.YourInformation_Frame._PublicKey.grid(column=0, row=2)
        root.YourInformation_Frame.PublicKey.grid(column=1, row=2)
        root.YourInformation_Frame._PrivateKey.grid(column=0, row=3)
        root.YourInformation_Frame.PrivateKey.grid(column=1, row=3)
        root.YourInformation_Frame._IP.grid(column=0, row=4)
        root.YourInformation_Frame.IP.grid(column=1, row=4)
        root.YourInformation_Frame._PORT.grid(column=0, row=5)
        root.YourInformation_Frame.PORT.grid(column=1, row=5)

    
    def create_PublicKey_Frame(self, root):
        root.PublicKey_Frame = tk.Frame(root)
        root.PublicKey_Frame.pk = tk.Label(root.PublicKey_Frame, text=self.node.pubKey)
        root.PublicKey_Frame.pk.pack()

    
    def create_PrivateKey_Frame(self, root):
        root.PrivateKey_Frame = tk.Frame(root)
        root.PrivateKey_Frame.pk = tk.Label(root.PrivateKey_Frame, text=self.node.priKey)
        root.PrivateKey_Frame.pk.pack()

    def InformationFrame2PublicKeyFrame(self):
        self.root.publicKey_newWin = Toplevel(self.root)
        self.create_PublicKey_Frame(self.root.publicKey_newWin)
        self.root.publicKey_newWin.PublicKey_Frame.pack()

    def InformationFrame2PrivateKeyFrame(self):
        self.root.privateKey_newWin = Toplevel(self.root)
        self.create_PrivateKey_Frame(self.root.privateKey_newWin)
        self.root.privateKey_newWin.PrivateKey_Frame.pack()
    

    def create_History_Frame(self, root):
        root.HistoryTable = tk.Frame(root)
        root.HistoryTable.list = ttk.Treeview(root.HistoryTable)
        root.HistoryTable.list['column'] = ("Type", "From", "Amount", "Note", "Time")

        root.HistoryTable.list.column("#0", anchor="center", width=30, stretch='NO')
        root.HistoryTable.list.column("Type", anchor="center", width=120, stretch='NO')
        root.HistoryTable.list.column("From", anchor="center", width=120, stretch='NO')
        root.HistoryTable.list.column("Amount", anchor="center", width=200, stretch='NO')
        root.HistoryTable.list.column("Note", anchor="center", width=200, stretch='NO')
        root.HistoryTable.list.column("Time", anchor="w", width=200, stretch='NO')
        
        root.HistoryTable.list.heading("Type", text="Type", anchor="center")
        root.HistoryTable.list.heading("From", text="From", anchor="center")
        root.HistoryTable.list.heading("Amount", text="Amount", anchor="center")
        root.HistoryTable.list.heading("Note", text="Note", anchor="center")
        root.HistoryTable.list.heading("Time", text="Time", anchor="w")

        transactionsInfor = self.node.GetTransactionOf(self.node.pubKey)
        infor = []
        # Get name via public key
        for transaction in transactionsInfor:
            if transaction[0] == self.node.pubKey:
               infor.append(["Send", self.requestNAMEviaPK(transaction[1]), transaction[2], transaction[3], time.ctime(transaction[4])]) 
            else:
               infor.append(["Receive", self.requestNAMEviaPK(transaction[0]), transaction[2], transaction[3], time.ctime(transaction[4])]) 
                
        for transaction in infor:
            root.HistoryTable.list.insert('', tk.END, values=(transaction[0], transaction[1], transaction[2], transaction[3], transaction[4]))

        root.HistoryTable.list.grid(row=0, column=0, sticky='nsew')

        scrollbar = ttk.Scrollbar(root.HistoryTable, orient=tk.VERTICAL, command=root.HistoryTable.list.yview)
        root.HistoryTable.list.configure(yscroll=scrollbar.set)
        scrollbar.grid(row=0, column=1, sticky='ns')

    
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


    def FeatureFrame2ListConnection(self):
        self.root.list_connection_newWin = Toplevel(self.root)
        self.create_ListConnection_Frame(self.root.list_connection_newWin)
        self.root.list_connection_newWin.ListConnectionTable.pack()


    def FeatureFrame2Information(self):
        self.root.information_newWin = Toplevel(self.root)
        self.create_YourInformation_Frame(self.root.information_newWin)
        self.root.information_newWin.YourInformation_Frame.pack()


    def FeatureFrame2BlockchainDetail(self):
        self.root.blockchain_detail_newWin = Toplevel(self.root)
        self.create_BlockchainDetail_Frame(self.root.blockchain_detail_newWin)
        self.root.blockchain_detail_newWin.BlockchainDetailTable.pack()


    def FreatureFrame2History(self):
        self.root.history_newWin = Toplevel(self.root)
        self.create_History_Frame(self.root.history_newWin)
        self.root.history_newWin.HistoryTable.pack()

    
    def join(self):
        self.root.name = self.root.join_frame.name_input.get()
        if not self.root.name:
            self.root.join_frame.warning.configure(text="Please input your name !", foreground='red')
        else:
            self.root.join_frame.warning.configure(text="")

            requestJoin = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            requestJoin.connect(("127.0.0.1", 60001))
            requestJoin.sendall(bytes("join|"+self.root.name, 'utf-8'))
            MSG = ""
            MSG = requestJoin.recv(4096).decode("utf8")
            requestJoin.close()

            self.ip, self.port, self.sk, self.pk, self.ip_cn, self.port_cn = MSG.split("|")
            self.node = Node(self.root.name, self.sk, self.pk, (self.ip, int(self.port)), (self.ip_cn, int(self.port_cn)), 3)

            self.root.join_frame.forget()

            _name = "Your name: " + self.root.name
            self.root.feature_frame.name.configure(text=_name, font="Bold")
            self.root.feature_frame.pack()

    
    def requestPKviaNAME(self, name):
        msg = "pk" +  "|" + name
        requestPK = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        requestPK.connect(("127.0.0.1", 60001))
        requestPK.sendall(bytes(msg, 'utf-8'))
        _pk = requestPK.recv(4096).decode('utf-8')
        requestPK.close()

        if _pk == "~|":
            return False
        return _pk


    def requestNAMEviaPK(self, pk):
        msg = "name" +  "|" + pk
        requestNAME = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        requestNAME.connect(("127.0.0.1", 60001))
        requestNAME.sendall(bytes(msg, 'utf-8'))
        _NAME = requestNAME.recv(4096).decode('utf-8')
        requestNAME.close()

        if _NAME == "~|":
            return False
        return _NAME


    def create_transaction(self):
        recv_name = self.root.create_transaction_newWin.create_transaction_frame.name_input.get()
        amount = self.root.create_transaction_newWin.create_transaction_frame.amount_input.get()
        note = self.root.create_transaction_newWin.create_transaction_frame.note_input.get()

        if (not recv_name) or (not amount) or (not note):
            self.root.create_transaction_newWin.create_transaction_frame.warning.configure(text="Please fill-in something :'( ", foreground='red')
        else:
            _pk = self.requestPKviaNAME(recv_name)

            if _pk == False:
                self.root.create_transaction_newWin.create_transaction_frame.warning.configure(text="Receiver's name does not exist !", foreground='red')
            else:
                _success = self.node.create_transaction(_pk, int(amount), note)
                if not _success:
                    self.root.create_transaction_newWin.create_transaction_frame.warning.configure(text="Check your balance sir !", foreground='purple')
                else:
                    self.root.create_transaction_newWin.create_transaction_frame.warning.configure(text="Create Successfully !", foreground='green')


# List Connection Done
# Show blockchain Done
# History Done

user = User()
user.run()