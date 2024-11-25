import os
import socket
import threading
import json
import time

IP = "127.0.0.1" #default IP for the server
PORT = 53849 #default port for the server
ADDR = (IP,PORT)
SIZE = 1024
FORMAT = "utf-8"

def handle_client (conn, addr):
    # server receives initial data from the client in the format COMMAND||DATA
        received =  conn.recv(SIZE).decode(FORMAT)
        cmd = received.split("||")[0]
        data = received.split("||")[1]
        print (received)
        if cmd == "LOGOUT":
            conn.close()
        elif cmd == "DIR": #client wants directory information
            directory_path = ""  # Current directory
            if data == '.' or data == '': # Fixed Logic
                directory_path = ""
            else:
                directory_path = data
            try:
                cwd = os.getcwd()
                contents = os.listdir(cwd + directory_path) #obtaining all the items within the currently selected directory
                filedata = []
                folderdata = []
                folderdata.append("cd..") #required entry to traverse upwards
                if directory_path != "." or directory_path != "":
                    for line in contents:
                        if os.path.isfile(cwd + directory_path + "/" + line):
                            filedata.append(line)
                        else:
                            folderdata.append(line)
                else: #client is in the root directory, this might be able to be merged with the other one now
                    for line in contents:
                        if os.path.isfile(line):
                            filedata.append(line)
                        else:
                            folderdata.append(line)
                filedata = json.dumps(filedata)
                conn.sendall(filedata.encode("utf-8")) #sends all the filenames as a json

                ack = conn.recv(4096)

                folderdata = json.dumps(folderdata)
                conn.sendall(folderdata.encode("utf-8")) #sends all the folders as a json
                conn.close()
            except Exception as e: #used for catching invalid directories, should be minimal when this can execute
                print (e)
                conn.send(cwd.encode(FORMAT))
                conn.send(f"Invalid directory".encode(FORMAT))
                conn.close()

        elif cmd == "DOWNLOAD": #client wants to download a file from the server
            entire_path = os.getcwd() + data #obtaining the absolute path of the file to be downloaded
            filesize = -1 #flag value in case the file does not exist
            try:
                filesize = os.path.getsize(entire_path) #obtains filesize
            except Exception as e: #catches invalid files or missing ones
                conn.send(f"-1".encode(FORMAT))
            conn.send(f"{filesize}".encode(FORMAT)) #sends the filesize to the client to prepare for the download of that length

            with open(entire_path, "rb") as f: #sends the file in chunks to the client
                while True:
                    bytes_read = f.read(SIZE)
                    if not bytes_read:
                        break
                    conn.sendall(bytes_read)
            conn.close()

        elif cmd =="MKDIR": #client wants to add a new subdirectory on their currently selected directory
            #creates a new directory if the directory name is not already in use
            cwd = os.getcwd()

            conn.send('1'.encode(FORMAT)) # Send ACK for init CMD
            proposed_name = conn.recv(SIZE).decode(FORMAT) # Make sure that an ACK is sent before this

            big_path = cwd + data
            contents = os.listdir(big_path)
            if proposed_name not in contents:
                os.mkdir(big_path + '/' + proposed_name)
                conn.send('1'.encode(FORMAT))
            else:
                conn.send('0'.encode(FORMAT))

        elif cmd =="FILE": #helper command to return whether or not the inputed item is a file or a directory
            client_path = data
            cwd = os.getcwd()
            test = os.path.isfile(cwd+client_path)
            conn.send(f"{test}".encode(FORMAT))

        elif cmd =="DEL": #client wants to delete a selected item, returns information if errors occur
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
                    os.rmdir(entire_path)
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
        print(f"New connection on {addr}")
        thread = threading.Thread(target = handle_client, args = (conn, addr)) ## assigning a thread for each client
        thread.start()

if __name__ == "__main__":
    try:
        os.chdir("projectTesting")
        print ("Changed Directory to 'projectTesting'")
    except Exception as e:
        print ("Made Directory 'projectTesting'", e)
        os.mkdir("projectTesting")
        os.chdir("projectTesting")
    main()

