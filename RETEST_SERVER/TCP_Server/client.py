import socket
import threading
from time import sleep

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
    client.close()
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(ADDR)
    client.settimeout(TIMEOUT_TIME)
    thread = threading.Thread(target=handle_rev, args=(client,))
    thread.start()


def handle_rev(client):
    while True:
        msg = client.recv(20).decode(FORMAT)
        try:
            if msg:
                print(f"[SERVER]: {msg}")
        except socket.timeout:
            print(f"[TIMEOUT]: Connection timed out")
            break
        except socket.error as e:
            print(f"[ERROR]: {e}")
            break
        except Exception as e:
            print(f"[ERROR]: {e}")
            break


def send(msg):
    try:
        message = msg.encode(FORMAT)
        message += b' ' * (20 - len(message))
        client.send(message)
    except socket.timeout:
        print(f"[TIMEOUT]: Connection timed out")
    except socket.error as e:
        print(f"[ERROR]: {e}")
    except Exception as e:
        print(f"[ERROR]: {e}")


thread = threading.Thread(target=handle_rev, args=(client,))
thread.start()

while True:
    # send("Hi.I am client 01!")
    # send string
    msg = input("Enter message: ")
    send("[CLIENT 1]: " + msg)
    # sleep(5)

send(DISCONNECT_MSG)
connected = False
thread.join()
