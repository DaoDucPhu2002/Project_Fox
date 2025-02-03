import socket
import threading
import json
import os

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

# Đường dẫn tuyệt đối tới file host_info.txt
HOST_INFO_FILE = os.path.join(os.path.dirname(__file__), 'host_info.txt')


def save_host_info(addr, hostname):
    data = {"ip": addr[0], "hostname": hostname}
    try:
        if not os.path.getsize(HOST_INFO_FILE) > 0:
            with open(HOST_INFO_FILE, 'r') as f:
                host_info = json.load(f)
        else:
            host_info = []
    except FileNotFoundError:
        host_info = []

    host_info.append(data)

    with open(HOST_INFO_FILE, 'w') as f:
        json.dump(host_info, f, indent=4)


def remove_host_info(addr):
    try:
        with open(HOST_INFO_FILE, 'r') as f:
            host_info = json.load(f)
    except FileNotFoundError:
        host_info = []
    for host in host_info:
        if host["ip"] == addr[0]:
            host_info.remove(host)
    with open(HOST_INFO_FILE, 'w') as f:
        json.dump(host_info, f, indent=4)


def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")
    try:
        hostname = socket.gethostbyaddr(addr[0])[0]
        print(f"[HOSTNAME]: {hostname}")

    except socket.herror:
        print("[HOSTNAME]: Unable to resolve hostname")
    save_host_info(addr, hostname)
    connected = True
    while connected:
        try:
            msg = conn.recv(1024).decode(FORMAT)
            if msg:
                print(f"[{addr}] {msg}")
                print(len(msg))
                # Handle the message
                if msg == DISCONNECT_MSG:
                    connected = False
                    clients.remove(conn)
                else:
                    save_json_data(msg)
                message = msg
                conn.send(message.encode(FORMAT))
                print("send message done")
            else:
                connected = False
                clients.remove(conn)
                remove_host_info(addr)
                print(f"[DISCONNECTED] {addr} disconnected")

        except socket.timeout:
            print(f"[TIMEOUT]: {addr} connection timed out")
            connected = False
        except socket.error as e:
            print(f"[ERROR]: {e}")
            clients.remove(conn)
            remove_host_info(addr)
            print(f"[DISCONNECTED] {addr} disconnected")
            connected = False

        except Exception as e:
            print(f"[ERROR]: {e}")
            clients.remove(conn)
            remove_host_info(addr)
            print(f"[DISCONNECTED] {addr} disconnected")
            connected = False
    conn.close()


def save_json_data(data):
    JSON_FILE = os.path.join(os.path.dirname(__file__), 'data.json')
    with open(JSON_FILE, 'w') as f:
        json.dump(json.loads(data), f, indent=4)


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
