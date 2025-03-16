import socket
import signal
import sys
import os
from dotenv import load_dotenv

load_dotenv()

SERVER_IP = os.getenv("SERVER_IP")
SERVER_PORT = int(os.getenv("SERVER_PORT"))

def signal_handler(sig, frame):
    print("[INFO] Closing the server...")
    sys.exit(0)

def start_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.bind((SERVER_IP, SERVER_PORT))
        server.listen(5)
        print(f"[INFO] Server is listening on {SERVER_IP}:{SERVER_PORT}...")

        while True:
            try:
                client_socket, addr = server.accept()
                with client_socket:
                    message = client_socket.recv(1024).decode()
                    print(f"[INFO] Received message: {message}")
            except Exception as e:
                print("["
                "] Connection error:", e)

if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)  
    start_server()
