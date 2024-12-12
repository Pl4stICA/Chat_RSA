import socket
import threading
import random
import sys


class ReceiveThread(threading.Thread):
    def __init__(self, client_socket):
        super().__init__()
        self.client_socket = client_socket

    def run(self):
        while True:
            self.receive_message()

    def receive_message(self):
        try:
            message = self.client_socket.recv(1024)
            if message:
                print(message.decode())
            else:
                print("[INFO] Server disconnected.")
                sys.exit(0)
        except Exception as e:
            print(f"[ERROR] Failed to receive message: {e}")
            sys.exit(1)

class Client:
    def __init__(self):
        self.tcp_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self, host, port, nickname):
        try:
            self.tcp_client.connect((host, port))
            self.tcp_client.send(nickname.encode())
            print(f"[INFO] Connected to server at {host}:{port} as {nickname}")
            return True
        except Exception as e:
            print(f"[ERROR] Unable to connect: {e}")
            return False

    def send_message(self):
        while True:
            message = input("Enter message: ")
            if message.lower() == 'exit':
                self.tcp_client.close()
                print("[INFO] Disconnected from server.")
                sys.exit(0)
            else:
                try:
                    self.tcp_client.send(message.encode())
                except Exception as e:
                    print(f"[ERROR] Failed to send message: {e}")
                    sys.exit(1)

def main():
    print("Welcome to the chat client!")
    host = 'localhost'
    
    nickname = input("Enter your nickname (leave empty for random): ")

    if not nickname:
        nickname = f"User_{random.randint(1, 1000)}"

    try:
        port = 5555
    except ValueError:
        print("[ERROR] Invalid port number. Using default port 5555.")
        port = 5555

  
    client = Client()
    if client.connect(host, port, nickname):
      
        receive_thread = ReceiveThread(client.tcp_client)
        receive_thread.start()

    
        client.send_message()

if __name__ == "__main__":
    main()
