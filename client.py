import socket 
from constants import *


def send(conn, msg):
# * Sends msg to conn using HEADER approach
    message = msg.encode()
    msg_len = len(message)
    send_len = str(msg_len).encode()
    send_len += b' ' * (HEADER - len(send_len))
    conn.send(send_len)
    conn.send(message)


def receive(conn):
# * Receives msg from conn using HEADER approach
    msg_len = conn.recv(HEADER).decode()
    msg_len = int(msg_len)
    msg = conn.recv(msg_len).decode()
    return msg


def verify_user_client(s):
# * Verification on client side
# * returns True if user is logged in, False if otherwise
    while True:
        username = input('Enter your username (Enter -1 to exit): ')
        if username == '-1':
            send(s, EXIT)
            return False 
        password = input('Enter your password: ')

        # * Sending data
        send(s, username)
        send(s, password)

        # * Receiving ACK
        datachunk = receive(s)
        if datachunk == OK:
            print('Access granted')
            return True
        else:
            print("Username or password is incorret, please re-input")


def chat(conn):
# * Currently just sends messages to server where they are printed
# * Sees if it's this user's turn to talk, sends message if it is, else receives message
# * Returns if message is -1

    # * Check if my turn to speak 
    my_turn = receive(conn)
    my_turn = True if my_turn == 'True' else False 


    while True:
        if my_turn:
            msg = input('>> ')
            if msg == '-1':
                send(conn, DISCONNECT)
                break             
            send(conn, msg)
            my_turn = False 
        
        
        else:
            msg = receive(conn)
            print(msg) 
            my_turn = True


def get_online_users(conn):
# * Gets all the users that are currently active

    num_online = int(receive(conn))
    print(f'Number of online users: {num_online}')
    
    # * Printing all the online users
    users = []
    for _ in range(num_online):
        user = receive(conn)
        users.append(user)
        
    return users


def menu(conn):
# * Shows the menu of the client side
# * Returns None when you enter -1
# * Prints online users if you enter R using print_online_users
    while True:
        print('Enter R to show the online active users')
        print('Enter !wait to wait to be connected')
        print('Enter -1 to exit')

        choice = input('>>')
        if choice == '-1':
            send(conn, DISCONNECT)
            return

        elif choice == 'R':
            send(conn, SHOW_CLIENTS)
            users = get_online_users(conn)
            print_online_users(users)

        elif choice == '!wait':
            send(conn, WAIT)
            print('Waiting on this side')
            ack = wait_for_confirm(conn)
            if ack == OK:
                print('Can now talk')
                chat(conn)
                if ack == OK:
                    return
    
    
        elif choice in users:
            send(conn, choice)
            chat(conn)
            ack = receive(conn)
            if ack == OK:
                return 

        else:
            print(f'Invalid choice, please re-enter')
        



def wait_for_confirm(conn):
# * Helper function
# * Used for client that is waiting to be connected
    msg = receive(conn)
    return msg 


def print_online_users(users: list) -> None:
# * Helper function that prints all the usersnames taken
    for user in users: 
        print(user)

if __name__ == '__main__':
    
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as conn:
        conn.connect((HOST, PORT))
        try:
            # * Verify the user
            if not verify_user_client(conn):
                print('Closing....')
                conn.close()

            # * Show the user list
            menu(conn)


            print('Closing...')
            conn.close()
        
        except KeyboardInterrupt:
            print('\nOkay bye')
            conn.close()
            exit()
