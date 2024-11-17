#!/usr/bin/env python3
# -*- coding: utf-8 -*-



import os
import socket
import threading
import json
import time

IP = "192.168.1.56"
PORT = 53849
ADDR = (IP,PORT)
SIZE = 1024
FORMAT = "utf-8"
SERVER_PATH = "server"

os.chdir("projectTesting")



### to handle the clients
def handle_client (conn,addr):

        received =  conn.recv(SIZE).decode(FORMAT)
        cmd = received.split("||")[0]
        data = received.split("||")[1]
        if cmd == "LOGOUT":
            conn.close()

        elif cmd == "DIR":
            directory_path = "."  # Current directory

            time.sleep(0.1)

            if data != "." or data != "":
                directory_path = data
            else:
                directory_path = ""
            try:
                cwd = os.getcwd()
                contents = os.listdir(cwd + directory_path)
                filedata = []
                folderdata = []
                folderdata.append("cd..")
                if directory_path != ".":
                    for line in contents:
                        if os.path.isfile(cwd + directory_path + "/" + line):
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

        elif cmd == "DOWNLOAD":
            entire_path = os.getcwd() + data
            filesize = -1
            try:
                filesize = os.path.getsize(entire_path)
            except Exception as e:
                conn.send(f"-1".encode(FORMAT))
            conn.send(f"{filesize}".encode(FORMAT))


            with open(entire_path, "rb") as f:
                while True:
                    bytes_read = f.read(SIZE)
                    if not bytes_read:
                        break
                    conn.sendall(bytes_read)
            conn.close()

        elif cmd =="MKDIR":
            cwd = os.getcwd()
            proposed_name = conn.recv(SIZE).decode(FORMAT)
            big_path = cwd + data
            contents = os.listdir(big_path)
            if proposed_name not in contents:
                os.mkdir(big_path + '/' +proposed_name)
                conn.send('1'.encode(FORMAT))
            else:
                conn.send('0'.encode(FORMAT))

        elif cmd =="FILE":
            client_path = data
            cwd = os.getcwd()
            time.sleep(0.1)
            test = os.path.isfile(cwd+client_path)
            conn.send(f"{test}".encode(FORMAT))

        elif cmd =="DEL":
            client_path = data
            cwd = os.getcwd()
            entire_path = cwd + client_path

            test = os.path.isfile(entire_path)
            if test: #deleting file
                try:
                    os.remove(entire_path)
                    conn.send("deleted".encode(FORMAT))
                except PermissionError:
                    conn.send("open".encode(FORMAT))
                except FileNotFoundError:
                    conn.send("NotFound".encode(FORMAT))
            else: #deleting directory
                try:
                    os.remove(entire_path)
                    conn.send("deleted".encode(FORMAT))
                except FileNotFoundError:
                    conn.send("NotFound".encode(FORMAT))
                except OSError:
                    conn.send("NotEmpty".encode(FORMAT))
        else:
            send_data = "Unknown command\n"
            conn.send(send_data.encode(FORMAT))
        conn.close()





def main():
    print("Starting the server")
    server = socket.socket(socket.AF_INET,socket.SOCK_STREAM) ## used IPV4 and TCP connection
    server.bind(ADDR) # bind the address
    server.listen() ## start listening
    print(f"server is listening on {IP}: {PORT}")


    while True:
        conn, addr = server.accept() ### accept a connection from a client
        thread = threading.Thread(target = handle_client, args = (conn, addr)) ## assigning a thread for each client
        thread.start()


if __name__ == "__main__":
    main()

