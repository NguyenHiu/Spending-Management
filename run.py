from blockchain import *
from node import *

class Run:
    def __init__(self) -> None:
        self.listNodes = []
        self.listServices = []

    def addNode(self, name, priK, pubK):
        node = Node(name, priK, pubK)
        self.listNodes.append(node)
    
    def spendMoney(self, stt, amount):
        self.listNodes[stt]

run = Run()
run.addNode('user1', 'private', 'public')
