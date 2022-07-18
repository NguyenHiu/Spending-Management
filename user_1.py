from node import Node
import key
import time
import socket

BANKER_SK = "-----BEGIN RSA PRIVATE KEY-----\nMIICWwIBAAKBgQDWpzX7Dwm2yzHY7Toi25UtTiRcEERXwlTMbw4i0RvoO+qf7JAF\nre53MLw7s7i3T5dFTUyI7yA/+jrSwkJ4RAqoJsvJj9JoPeO2kuE6xWF3ksmYY99V\n5oRDq1CqbG3nTqAAb2hSz8FXaLUQtjvA+qYYS/wxxbf0/FqatbphPhzx1wIDAQAB\nAoGAIBxrit85CMtk7Zqvc799lYV3Ev6r+qTropmKd9LoZdlww/PTp8XZQqNbxWKh\nY2rYqllh9aowHOIGIrlE0FD9dtv4/cMghO47GWZLjO1lqQDIc69BNh4f8RMO1J3x\nZiE3fmvod23N0dlJGyjo0zfDDddyS0gXILRebHK8bzj05MECQQDd5TyTU54MrzXI\nnpTtIuHZwP7fTWe7yXq/d8glxzoDz3ChtyHuPAIguLg04Yvg3fKAY6+mVaUGlP32\n5GYx1Q25AkEA96UEXcfMAB04lKd1q3k4s3W8GPdQDR4H0xiALg2o8Q1cA2gzHpb+\nZ45Z6je8jaiqy7JXBzGehHgyExoHcNxEDwJAXlzD++sNRVulRaGat5Wj8hROzut9\n96/g0VfA97/XfhNTVJIqjcNbLEshmutnrsL0A4FhCx1Uxo3JypqqkvqFkQJAJsIT\n4d2QRwBLx7BB0VmCj0vA6aNjSvpFPTubbBnFNBzkJsBbJ9F39Zso5WhdwUoBmSnL\nRxvz9EWfiK/NNFO07wJAEzm/WbjRTh1fyIbGDlK19C7hi4EWJEdl3+9Z3e4MnGGD\nxTKN5ZUFmJjDhTcKn468cSHUHUIcJoOvpVIlj1V8ww==\n-----END RSA PRIVATE KEY-----"
BANKER_PK = "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAAAgQDWpzX7Dwm2yzHY7Toi25UtTiRcEERXwlTMbw4i0RvoO+qf7JAFre53MLw7s7i3T5dFTUyI7yA/+jrSwkJ4RAqoJsvJj9JoPeO2kuE6xWF3ksmYY99V5oRDq1CqbG3nTqAAb2hSz8FXaLUQtjvA+qYYS/wxxbf0/FqatbphPhzx1w=="


name = input("Input your name: ")

requestJoin = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
requestJoin.connect(("127.0.0.1", 60001))
requestJoin.sendall(bytes("join|"+name, 'utf-8'))
MSG = ""
MSG = requestJoin.recv(4096).decode("utf8")
requestJoin.close()
ip, port, sk, pk, ip_cn, port_cn = MSG.split("|")


node = Node(name, sk, pk, (ip, int(port)), (ip_cn, int(port_cn)), 3)

cmd = ""
menu = "---------------------------------------\n"
if pk == BANKER_PK:
    menu += "[ You are the banker ! ]\n"
menu += "Choose:\n"
menu += "1. Create transaction\n"
menu += "2. List connections\n"
menu += "3. Print your blockchain\n"
menu += "4. Balance\n"
menu += "5. Stop\n"
menu += "---------------------------------------\n"


print(menu)
while True:
    cmd = input("Your answer: ")
    if cmd == "5":
        break
    elif cmd == "1":
        recv_name = input("Receiver's name: ")
        amount = int(input("Amount: "))
        note = input("Note: ")
        
        msg = "pk" +  "|" + recv_name
        requestPK = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        requestPK.connect(("127.0.0.1", 60001))
        requestPK.sendall(bytes(msg, 'utf-8'))
        _pk = requestPK.recv(4096).decode('utf-8')
        requestPK.close()

        if _pk == "~|":
            print('======================================================')
            print("     (X) Receiver's name does not exist !")
            print('======================================================')
            continue
        
        node.create_transaction(_pk, amount, note)

        print('======================================================')
        print('     (/) Create Successfully !')
        print('======================================================')
    
    elif cmd == "2":
        print('======================================================')
        node.printConnections()
        print('======================================================')
    
    elif cmd == "3":
        print('======================================================')
        node.blockchain.output()
        print('======================================================')

    elif cmd == "4":
        print('======================================================')
        print("Your balance: " + str(node.getBalanceOf(node.pubKey)))
        print('======================================================')
