import socket
import ssl
import threading
import os

HOST = '0.0.0.0'  # Listen on all interfaces
PORT = 7632

class Server:
    def __init__(self):
        self.context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        self.context.load_cert_chain('server.crt', 'server.key')
        
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((HOST, PORT))
        self.sock.listen()
        print(f"Server running on {HOST}:{PORT} (Waiting for client...)")

        self.conn, self.addr = self.sock.accept()
        self.secure_conn = self.context.wrap_socket(self.conn, server_side=True)
        print(f"Connected to {self.addr}")

        threading.Thread(target=self.receive).start()
        self.send()

    def receive(self):
        while True:
            try:
                data = self.secure_conn.recv(1024).decode()
                if not data:
                    break
                print(f"Client: {data}")
            except:
                break
        print("Client disconnected.")
        os._exit(0)

    def send(self):
        while True:
            try:
                msg = input()
                self.secure_conn.send(msg.encode())
            except:
                break
        os._exit(0)

if __name__ == "__main__":
    Server()