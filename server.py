import socket
import threading
import tensorflow as tf
import numpy as np
import pickle


#loading trained MLP model. The following function is used to get symptoms as input and predict the result
ann = pickle.load(open('/mnt/c/Users/Pariya/Desktop/Program/finalized_model.sav', 'rb'))
def symptom_prediction(data):
    result = ann.predict_proba(data) #This function calculates the probablity of each class
    #print(result)
    if result[0][0] < result[0][1]:
        answer = "\u001b[31mThe probability of infection is " + str(result[0][1]) + " which is comparatively high."
    else:
        answer = "\u001b[32mThe probability of infection is " + str(result[0][1]) + " which is comparatively low."
    return answer


#loading trained CNN model. The following function is used to get an image as input and predict the result
model = tf.keras.models.load_model('/mnt/c/Users/Pariya/Desktop/Program/model')
def xray_prediction(filename):
    from tensorflow.keras.preprocessing import image
    test_image = image.load_img(filename, target_size = (200,200,3))
    test_image = image.img_to_array(test_image)
    test_image = np.expand_dims(test_image, axis = 0)
    result = model.predict(test_image)
    
    if result[0][0]==1:
        prediction = '\u001b[31mYou may have covid-19. Visit a doctor.'
    else :
        prediction = '\u001b[32mYour chest X-ray seems normal.'
    return prediction


#this is just a function that will convert user's answers on survey to the format accepted by MLP algorithm
def convertion(my_list):
    if my_list[1] == 2:
        my_list[1] = 0
    if my_list[4] == 2:
        my_list[4] = 0
    if my_list[4] == 3:
        my_list[4] = -1
    return my_list

#A dictionary to store registered user's information 
users = {}

#A text file to to store registered user's information
f = open("dict.txt","w")


#A function handle client's requests
def handle_client(conn, addr):
    print(f"[New Connection] {addr} connected.")
    

    while True:
        data = conn.recv(1024).decode()
        if not data:
            break

        #Get requests from client as tokens like (command, required input)
        tokens = data.split()
        cmd = tokens[0]

        if cmd == "REGISTER":
            username = tokens[1]
            password = tokens[2]
            
            #registration
            if username in users:
                conn.send(str.encode("DUPLICATED")) #Usernames should be unique
            else:
                #Save the user information to a database
                users[username] = password
                conn.send(str.encode("REGISTERED"))

        elif cmd == "LOGIN":
            username = tokens[1]
            password = tokens[2]
            
            #authentication
            #Comparing the hash of the password sent from the client with the stored hash in the database
            if username in users and users[username] == password:
                conn.send(str.encode("AUTHENTICATED"))
            else:
                conn.send(str.encode("UNAUTHORIZED"))
            
        elif cmd == "CALCULATE":
            #Split the tokens by ,
            numbers = tokens[1].split(",")
            
            #convert string to integers and save them in a new list
            input_data = []
            for number in numbers:
                input_data.append(int(number))
                
            result = symptom_prediction([convertion(input_data)])
            conn.send(str.encode(result))

        elif cmd == "LOAD":
            #get the filename/address as token
            filename = tokens[1]
            
            #prediction of infection based on the loaded image
            result = xray_prediction(filename)
            conn.send(str.encode(result))

    #add users' info to the file and close it
    f.write(str(users))
    f.close()
    
    print(f"[Connection Closed] {addr} disconnected.")

#set address and port number
host = '127.0.0.1'
port = 3500

server = socket.socket()
server.bind((host, port))

#server can listen to maximum 10 clients
server.listen(10)
print(f"[Listening] Server is listening on {host}:{port}")

while True:
    conn, addr = server.accept()
    thread = threading.Thread(target=handle_client, args=(conn, addr))
    thread.start()

server.close()
