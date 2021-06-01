import socket 
from constants import *

def verify_user_client(s):
    while True:
        username = input('Enter your username (Enter -1 to exit): ')
        if username == '-1':
            s.send(EXIT)
            return False 
        password = input('Enter your password: ')
        # print(f'({username}, {password})')
    
        s.send(username.encode())
        s.send(password.encode())
        
        
        datachunk = s.recv(CHUNK_SIZE)
        if datachunk == OK:
            print('Access granted')
            return True
        else:
            print("Username not found, please re-input")



with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    
    # Connecting to the server
    s.connect((HOST, PORT))
    
    
    # Username verification
    if not verify_user_client(s):
        print('Closing')
        s.close()
    else:
        print("Say something... (Enter -1 to disconnect)")
        while True:
                msg = input()
                
                if msg == '-1':
                    s.send(DISCONNECT)
                    break 
                
                s.send(msg.encode())
        s.close()
        


    # data = ''
    # while True:
    #     print(datachunk)
    #     if not datachunk:
    #             break 
    #     data += datachunk.decode()
    #     print(data)

