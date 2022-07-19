# Spending-Management

## About The Project
Spending management is very important to our lives, it helps us to always be ready for anything that will happen. For example, if your car breaks down, you need a lot of money to fix it, but it's okay because managing your monthly expenses will help you save some money.

**Purpose:** The application runs on a __**BLOCKCHAIN**__ database, we are studying blockchain, so this project helps us to understand more broadly about bitcoin/blockchain mechanism. App uses __Socket__ to send or receive messages, it's optional.

We use _tkinter library_ to create a basic UI.

**Important:** The project was taken as an exercise to understand the blockchain mechanism. So there is still something we haven't done, such as: 
- The network can't contain 2 users with the same name.
- Nodes/Users can only work when run.exe is open...
- ...

The program will be crashed if something wrong happens. But these problems don't directly relate to _the blockchain machanism_, so take it easy. 

## About us:

|            Name               | Profile 
|-------------------------------|----------------------------
|Nguyen Hoang Lam | [@Hoanglam1134](https://github.com/Hoanglam1134)            
|Nguyen Trong Hieu | [@NguyenHiu](https://github.com/NguyenHiu)    

## Installation
```console
git clone https://github.com/NguyenHiu/Spending-Management
pip install -r requirements.txt
```
## Release Folder 
There are 2 files in _the release folder_, 
1. **run.exe** creates a Hub which every node joins to the network must be connected with, Hub will provide _Ip, Port, Public Key, and Private Key_ for the node. So we need to run _run.exe_ first.
2. **user.exe** creates a new user, represents a user which joins the network and contains a node object.

## Demo
First, click START to open the Hub.

![image](https://user-images.githubusercontent.com/87634727/179823093-af321272-dafa-47b1-bb9e-75ff918f231a.png)
