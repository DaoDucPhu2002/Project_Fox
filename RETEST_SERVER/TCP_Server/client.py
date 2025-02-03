import socket
import threading
from time import sleep
import json
import os

PORT = 5050
FORMAT = 'utf-8'
DISCONNECT_MSG = "!DISCONNECT"
SERVER = "192.168.1.29"
ADDR = (SERVER, PORT)
TIMEOUT_TIME = 3600
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)
client.settimeout(TIMEOUT_TIME)
connected = True


def reconnect():
    global client
    print("[RECONNECTING]: Attempting to reconnect...")
    client.close()
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        client.connect(ADDR)
        client.settimeout(TIMEOUT_TIME)
        thread = threading.Thread(target=handle_rev, args=(client,))
        thread.start()

    except socket.error as e:
        print(f"[RECONNECT ERROR]: {e}")
        print("Retrying in 5 seconds...")
        sleep(5)


def handle_rev(client):
    while True:
        try:
            msg = client.recv(20).decode(FORMAT)
            if msg:
                print(f"[SERVER]: {msg}")
        except socket.timeout:
            print("[TIMEOUT]: No data received within the timeout period")
            reconnect()
            break
        except socket.error as e:
            print(f"[ERROR]: {e}")
            reconnect()
            break
        except Exception as e:
            print(f"[ERROR]: {e}")
            reconnect()
            break


def send(msg):
    try:
        message = msg.encode(FORMAT)
        # message += b' ' * (20 - len(message))
        client.send(message)
    except socket.timeout:
        print(f"[TIMEOUT]: Connection timed out")
    except socket.error as e:
        print(f"[ERROR]: {e}")
        reconnect()
    except Exception as e:
        print(f"[ERROR]: {e}")
        reconnect()


def send_json_data():
    JSON_FILE = os.path.join(os.path.dirname(__file__), 'open_count.json')
    with open(JSON_FILE, 'r') as f:
        data = json.load(f)
        send(json.dumps(data))


thread = threading.Thread(target=handle_rev, args=(client,))
thread.start()

while True:
    # msg = input("Enter message: ")
    # msg = 'Hello'
    # send("[CLIENT 1]: " + msg)
    send_json_data()
    sleep(2)
    # read json file and send to server


send(DISCONNECT_MSG)
connected = False
thread.join()
client.close()
