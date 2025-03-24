import socket
import ssl
import threading
import os

SERVER_IP = input("Enter server IP (e.g., 192.168.1.100 or public IP): ")
PORT = 7632

class Client:
    def __init__(self):
        self.context = ssl.create_default_context()
        self.context.check_hostname = False  # Disable for self-signed certs
        self.context.verify_mode = ssl.CERT_NONE  # Skip verification (testing only!)
        
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.secure_sock = self.context.wrap_socket(self.sock, server_hostname=SERVER_IP)
        self.secure_sock.connect((SERVER_IP, PORT))
        print(f"Connected to {SERVER_IP}:{PORT}")

        threading.Thread(target=self.receive).start()
        self.send()

    def receive(self):
        while True:
            try:
                data = self.secure_sock.recv(1024).decode()
                if not data:
                    break
                print(f"Server: {data}")
            except:
                break
        print("Server disconnected.")
        os._exit(0)

    def send(self):
        while True:
            try:
                msg = input()
                self.secure_sock.send(msg.encode())
            except:
                break
        os._exit(0)

if __name__ == "__main__":
    Client()