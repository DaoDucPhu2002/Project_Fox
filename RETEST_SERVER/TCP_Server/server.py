import socket
import threading


# Cac thong so co ban cua server
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MSG = "!DISCONNECT"
TIMEOUT_TIME = 3600

clients = []

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)


def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")
    connected = True
    while connected:
        try:
            msg = conn.recv(1024).decode(FORMAT)
            if msg:
                print(f"[{addr}] {msg}")
                # Handle the message
                if msg == DISCONNECT_MSG:
                    connected = False
                    clients.remove(conn)
                message = msg
                conn.send(message.encode(FORMAT))
                print("send message done")
        except socket.timeout:
            print(f"[TIMEOUT]: {addr} connection timed out")
            connected = False
        except socket.error as e:
            print(f"[ERROR]: {e}")
            connected = False
        except Exception as e:
            print(f"[ERROR]: {e}")
            connected = False
    conn.close()


def start():
    server.listen()
    print(f"[LISTENING]: Server is listening on {SERVER}")
    while True:

        conn, addr = server.accept()
        conn.settimeout(TIMEOUT_TIME)
        print(f"[ACTIVE CONNECTIONS] {threading.active_count()}")
        clients.append(conn)
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()


print("[STARTING]: Server is starting...")
start()
