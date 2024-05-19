import socket

#client configuration
HOST = '127.0.0.1'  
PORT = 56297        

def main():
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.connect((HOST, PORT))
            except socket.error as e:
                print(f"Error connecting to server(Server Unavailable): {e}")
                return
            
            while True:
                print("\nMenu:")
                print("1. Add item to shopping list")
                print("2. Retrieve shopping list")
                print("3. Exit")
                choice = input("Enter your choice: ")

                if choice == '1':
                    item = input("Enter the item to add: ")
                    command = f"ADD:{item}"
                elif choice == '2':
                    command = "GET"
                elif choice == '3':
                    command = "EXIT"
                    print("Exiting client...")
                    s.sendall(command.encode())
                    break
                else:
                    print("Invalid choice, please try again!")
                    continue
                
                try:
                    s.sendall(command.encode())
                    response = s.recv(1024).decode()
                    print("Server response:", response)
                except socket.error as e:
                    print(f"Error communicating with server(Server Unavailable): {e}")
                    break
    except Exception as e:
        print(f"An unexpected error occurred while exiting(Server Unavailable): {e}")

if __name__ == "__main__":
    main()
