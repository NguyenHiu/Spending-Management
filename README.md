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

## Banker
Because of the blockchain database, so we need a input source. 
The Hub will take the first user as the **Banker** who can create money, that's mean this user can send the amount of money larger than he has. 

## Demo
First, click START to open the Hub.

![image](https://user-images.githubusercontent.com/87634727/179823161-842c67fd-76f4-403a-9f87-6b876f5803a0.png)

Then, create user, input your name and click join to request.

![image](https://user-images.githubusercontent.com/87634727/179823501-cad018df-67f0-4d17-b227-eddfee8d1c08.png)

Then, you can try some features from Feature Screen.

![image](https://user-images.githubusercontent.com/87634727/179823657-56956f68-cfa7-4524-9b2f-c9a2c11922b5.png)

### Features

1. Get Balance: calculates transactions in blockchain to know how much money you have, using the same mechanism as bitcoin. 
```console
Balance = (money in) - (money out)
```
2. Create Transaction: allows you send/receive money from other. **Note:** Don't pass the note (must write something - It's just a bug XD).

![image](https://user-images.githubusercontent.com/87634727/179824808-6a955099-c96d-44ca-88f5-4526b6b7a47d.png)

3. List Connections: shows list of user connected with (IP - PORT).

![image](https://user-images.githubusercontent.com/87634727/179825498-7d0d967f-7a00-4f8d-a966-e053dbbe109f.png)

4. Blockchain Detail: shows detail of the local blockchain, because we are studying blockchain xD.

![image](https://user-images.githubusercontent.com/87634727/179825544-3c9056d7-1b80-42db-b452-0ca040e9f65f.png)

5. History: shows transaction which you sent or received.

![image](https://user-images.githubusercontent.com/87634727/179825626-030c64ba-e878-44a1-8130-193adb4ec93d.png)

6. Information: shows your information. 

![image](https://user-images.githubusercontent.com/87634727/179825665-c0f556b0-5b13-44fa-bf0e-e648d881a479.png)
