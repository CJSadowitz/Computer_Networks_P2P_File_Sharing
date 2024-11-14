#!/usr/bin/env python3
# -*- coding: utf-8 -*-


# Author : Ayesha S. Dina

import os
import socket
import threading
import json

IP = "192.168.1.56"
PORT = 53849
ADDR = (IP, PORT)
SIZE = 1024
FORMAT = "utf-8"
SERVER_PATH = "server"


### to handle the clients
def handle_client(conn, addr):
    data = conn.recv(SIZE).decode(FORMAT)
    if data == "LOGOUT":
        conn.close()

    elif data == "DIR":
        directory_path = "."  # Current directory
        chngDir = conn.recv(SIZE).decode(FORMAT)
        if chngDir != ".":
            directory_path = chngDir
        try:
            contents = os.listdir(directory_path)
            filedata = []
            folderdata = []
            folderdata.append("cd..")
            cwd = os.getcwd()
            if directory_path != ".":
                for line in contents:
                    if os.path.isfile(cwd + "/" + directory_path + "/" + line):
                        filedata.append(line)
                    else:
                        folderdata.append(line)
            else:
                for line in contents:
                    if os.path.isfile(line):
                        filedata.append(line)
                    else:
                        folderdata.append(line)

            filedata = json.dumps(filedata)
            conn.sendall(filedata.encode("utf-8"))

            folderdata = json.dumps(folderdata)
            conn.sendall(folderdata.encode("utf-8"))

            conn.close()
        except Exception as E:
            conn.send(f"Invalid directory".encode(FORMAT))
            conn.close()

    elif data == "DOWNLOAD":
        filename = conn.recv(SIZE).decode(FORMAT)

        filesize = os.path.getsize(filename)
        conn.send(f"{filesize}".encode(FORMAT))
        with open(filename, "rb") as f:
            while True:
                # read the bytes from the file
                bytes_read = f.read(SIZE)
                if not bytes_read:
                    # file transmitting is done
                    break
                # we use sendall to assure transimission in
                # busy networks
                conn.sendall(bytes_read)
        conn.close()
    else:
        send_data = "Unknown command\n"
        conn.send(send_data.encode(FORMAT))
        conn.close()


'''
def authenticate(client_socket):
    # Prompt for username
    client_socket.send("Username: ".encode())
    username = client_socket.recv(1024).decode().strip()

    # Prompt for password
    #client_socket.send("Password: ".encode())
    password = client_socket.recv(1024).decode().strip()
    print(username)
    if username != "user":
        client_socket.close()
        print("ksgh")

    # Verify credentials
    if username in user_credentials and user_credentials[username] == password:
        client_socket.send("Login successful!".encode())
        return True
    else:
        client_socket.send("Invalid credentials. Connection closed.".encode())
        return False
    '''


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

