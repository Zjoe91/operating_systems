import socket
import threading
import signal
import sys
import os

process_id = os.getpid()
print(f"Process ID: {process_id}")

#server configuration
HOST = '127.0.0.1'
PORT = 56297

backup_file = 'shopping_list_backup.txt'
shopping_list = []
active_clients = []

def handle_client(connection, address):
    print(f"Connected by {address}")
    active_clients.append(connection)
    try:
        while True:
            data = connection.recv(1024)
            if not data:
                break
            command, *args = data.decode().split(':')
            if command == 'ADD':
                shopping_list.append(':'.join(args))
                connection.sendall(b"Item added successfully.")
            elif command == 'GET':
                response = str(shopping_list).encode()
                connection.sendall(response)
            elif command == 'EXIT':  
                print(f"Client {address} requested to close the connection.")
                break  
            else:
                connection.sendall(b"Invalid command.")
    except Exception as e:
        if not sigint_handler:    
             print(f"Error handling client {address}: {e}")
        else:
            pass
    
    finally:
        connection.close()
        print(f"Connection with {address} closed.")

def backup_shopping_list():
    print("Backing up shopping list...")
    with open(backup_file, 'w') as file:
        for item in shopping_list:
            file.write(f"{item}\n")
        print("Backup completed.")

def sigint_handler(sig, frame): # Gracefully shutdown the server and close all active connections
    signame = signal.Signals(sig).name
    print(f"Signal received: {signame}: Graceful shutdown initiated, all active conections will be closed")
    for connection in active_clients:
        connection.close()

    sys.exit(0) # i am using sys.exit(0) instead of sys.exit(1) to exit the program gracefully

def sigterm_handler(sig, frame): # sigterm handler for your own testing on a linux or mac system
    signame = signal.Signals(sig).name
    print(f"Signal received: {signame}, performing cleanup and backup")
    backup_shopping_list()
    
def sigbreak_handler(sig, frame): # i used to SIGBREAK as it does the same thing as SIGTERM on windows for my testing
    signame = signal.Signals(sig).name
    print(f"Signal received: {signame}, performing cleanup and backup")
    backup_shopping_list()
    
def start_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen(5)
        s.settimeout(1)
        print(f"Server listening on {HOST}:{PORT}")

        while True:
            try:
                connection, address = s.accept()
                client_thread = threading.Thread(target=handle_client, args=(connection, address))
                client_thread.start()
            except socket.timeout:
                continue  
            except Exception as e:
                print(f"Error accepting connection: {e}")

if __name__ == "__main__":
    
    #registering signal handlers
    signal.signal(signal.SIGINT, sigint_handler)
    signal.signal(signal.SIGTERM, sigterm_handler)
    signal.signal(signal.SIGBREAK, sigbreak_handler)

    start_server()
