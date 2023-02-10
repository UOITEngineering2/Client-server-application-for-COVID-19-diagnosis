import socket
import hashlib
import getpass

#The main menu of the application
def main_menu():
    print("\n1. Register \n2. Login \n3. Exit")
    choice = int(input("Enter your choice: "))
    return choice

#registration
def register(s):
    username = input("Enter username: ")
    
    #using getpass to mask the password
    password = getpass.getpass(prompt="Enter password: ")
    
    #using hashlib to securely hash passwords
    password_hash = hashlib.sha256(password.encode()).hexdigest()
    s.send(str.encode(f"REGISTER {username} {password_hash}"))
    data = s.recv(1024).decode()
    
    if data == "REGISTERED":
        print("\nRegistered successfully")
    else:
        print("\nRegistration failed")

#authentication
def login(s):
    username = input("Enter username: ")
    
    #using getpass to mask the password and hashlib for hashing the password
    password = getpass.getpass(prompt="Enter password: ")
    password_hash = hashlib.sha256(password.encode()).hexdigest()
    s.send(str.encode(f"LOGIN {username} {password_hash}"))
    data = s.recv(1024).decode()
    if data == "AUTHENTICATED":
        print("\nLogged in successfully")
        return True
    else:
        print("\nLogin failed")
        return False

#The second menu. User can choose to diagnose covid-19 based on symptoms or X-ray image
def diagnosis(s):
    print("\n\u001b[37mYou can choose how to enter your data for the prediction of Covid-19 infection:")
    print("1. Complete a survey based on your symptoms. \n2. Load chest X-ray image. \n3. Logout")
    choice = int(input("Enter your choice: "))
    
    #The first option is to complete the survey
    if choice == 1:
        #There are 5 questions that the user should answer
        q1 = input("\nEnter your fever(In fahrenheit): ")
        q2 = input("\nDo you have body pain?\n1. Yes\n2. No \n")
        q3 = input("\nEnter your age: ")
        q4 = input("\nDo you have runny nose problem?\n1. Yes\n2. No \n")
        q5 = input("\nDo you have diff breath problem?\n1. Yes\n2. Yes but it's moderate \n3.No \n")
        s.send(str.encode("CALCULATE {},{},{},{},{}".format(q1, q2, q3, q4, q5)))
        answer = s.recv(1024).decode()
        print(answer)
        
    #The second option is to load an X-ray image
    elif choice == 2:
        filename = input("Enter filename: ")
        s.send(str.encode(f"LOAD {filename}"))
        data = s.recv(1024).decode()
        print(data)
        
    #Going back to the main menu or logout
    elif choice == 3:
        return main_menu()


#set address and port number
host = '127.0.0.1'
port = 3500

client = socket.socket()
client.connect((host, port))

#while loop which indicates the connection between server and client
while True:
    choice = main_menu()
    if choice == 1:
        register(client)
    elif choice == 2:
        authenticated = login(client)
        while authenticated:
            choice = diagnosis(client)
            if choice == 3:
                authenticated = False
                break
    elif choice == 3:
        authenticated = False
        break

s.close()
