# Author : Ayesha S. Dina

import os
import threading
import socket
import hashlib

# IP = "192.168.1.101" #"localhost"
IP = "localhost"
PORT = 4450
ADDR = (IP, PORT)
SIZE = 1024  ## byte .. buffer size
FORMAT = "utf-8"
SERVER_DATA_PATH = "server_data"
hashing = hashlib.sha256()
creds = {'jordan': ['salt', '7a37b85c8918eac19a9089c0fa5a2ab4dce3f90528dcdeec108b23ddf3607b99']}

print('jp')
def get_salt(username):
    if username in creds:
        return creds[username][0]
    else:
        return None


def check_creds(username, password):
    salt = get_salt(username)
    hashing.update(password.encode('utf-8') + salt.encode('utf-8'))
    hashed = hashing.hexdigest()
    if creds[username][1] == hashed:
        return True
    else:
        return False


def handle_login(username, password, conn):
    if check_creds(username, password):
        conn.send("OK@Welcome to the server".encode(FORMAT))
    else:
        conn.send("DISCONNECTED@Incorrect Password".encode(FORMAT))


def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")
    conn.send("LOGIN@Please Enter Username and Password".encode(FORMAT))
    data = conn.recv(SIZE).decode(FORMAT)
    data = data.split("@")
    username, password = data[1].split(":")
    handle_login(username, password, conn)

    while True:
        data = conn.recv(SIZE).decode(FORMAT)
        data = data.split("@")
        cmd = data[0]

        send_data = "OK@"

        if cmd == "LOGOUT":
            break

        elif cmd == "TASK":
            send_data += "LOGOUT from the server.\n"

            conn.send(send_data.encode(FORMAT))

    print(f"{addr} disconnected")
    conn.close()


def main():
    print("Starting the server")
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  ## used IPV4 and TCP connection
    server.bind(ADDR)  # bind the address
    server.listen()  ## start listening
    print(f"server is listening on {IP}: {PORT}")
    while True:
        conn, addr = server.accept()  ### accept a connection from a client
        thread = threading.Thread(target=handle_client, args=(conn, addr))  ## assigning a thread for each client
        thread.start()


if __name__ == "__main__":
    main()
