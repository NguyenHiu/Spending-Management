from inspect import signature
from turtle import pu
from blockchain import *
from node import *
import enum

class Run:
    def __init__(self) -> None:
        self.listNodes = []
        self.listServices = []

    def addNode(self, name, priK, pubK):
        node = Node(name, priK, pubK)
        self.listNodes.append(node)
    
    def addServices(self, name, priK, pubK):
        node = Node(name, priK, pubK)
        self.listServices.append(node)    

    def spendMoney(self, stt, amount, receiver, note):
        trans = self.listNodes[stt].create_transaction(receiver, amount, note)
        block_chain.add_transaction(trans)
        

    def show(self, stt: int):
        res_table = {}

        for i in block_chain.chain:
            if i.id == 0:
                continue
            for tx in i.transactions:
                res = json.loads(tx)
                name = res['recipient']
                idx = Service[name].value - 1
                
                if res['signature'] not in res_table.keys():
                    res_table[res['signature']] = [0, 0, 0, 0, 0, 0]

                # res_table[res['signature']][idx] = res['amount']
                res_table[res['signature']][idx] += res['amount']
        k=0
        for i in res_table.keys():
            print(i, ' da chi tieu:')
            for sv, _ in Service.__members__.items():
                print(sv, ':', res_table[i][k])
                k+=1
            k=0

# Gia lap moi truong
run = Run()
block_chain = Blockchain()

# enum class (not used yet)
class Service(enum.Enum):
    energy = 1
    water = 2
    internet = 3
    gas = 4
    electricity = 5
    telephone = 6

# Cac dich vu chi tieu
run.addServices('Energy', 'energy1', 'energy')
run.addServices('Water', 'water1', 'water')
run.addServices('Electricity', 'electricity1', 'electricity')
run.addServices('Gas', 'gas1', 'gas')
run.addServices('Internet', 'internet1', 'internet')
run.addServices('Telephone', 'telephone1', 'telephone')

# Tai khoan nguoi dung
run.addNode('user1', 'user1', 'user1')
# 0 la so tt cua user1, 5 la amount
run.spendMoney(0, 5, 'energy', 'tien do xang')
run.spendMoney(0, 10, 'water', 'tien nuoc')
run.spendMoney(0, 30, 'electricity', 'tien dien')
block_chain.mine()

# Kiem tra tai khoan
run.show(0)