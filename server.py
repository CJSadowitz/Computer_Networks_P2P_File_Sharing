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
    while True:
        data = conn.recv(SIZE).decode(FORMAT)

        send_data = "OK@"

        if data == "LOGOUT":
            break

        elif data == "TASK":
            send_data += "Yarg be a task.\n"

            conn.send(send_data.encode(FORMAT))
        elif data == "DIR":

            directory_path = "."  # Current directory
            contents = os.listdir(directory_path)
            data = json.dumps(contents)  # Convert list to JSON string
            conn.sendall(data.encode("utf-8"))
        else:
            send_data += "Unknown command\n"
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

