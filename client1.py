import tkinter as tk
from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
import os
import time
import socket
import json
import tqdm
import re


IP = 'localhost'
PORT = 4450
ADDR = (IP, PORT)
SIZE = 1024
FORMAT = "utf-8"
SERVER_DATA_PATH = "server_data"

currentWorkingServerDirectory = ""

def format_bytes(size):
    #convert to optimal byte representation
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size < 1024:
            return f"{size:.2f} {unit}"
        size /= 1024
    return f"{size:.2f} TB"  # Fallback if the size is enormous


def hideWidget(widget):
    widget.grid_forget()

def connectGridActivate():
    labelServer.grid(row=1, column=0, ipady=10)
    IP_entry.grid(row=2, column=0, ipady=10)
    labelPort.grid(row=3, column=0, ipady=10)
    PORT_entry.grid(row=4, column=0, ipady=10)
    labelUser.grid(row=5, column=0, ipady=10)
    userName_entry.grid(row=6, column=0, ipady=10)
    labelPass.grid(row=7, column=0, ipady=10)
    PASS_entry.grid(row=8, column=0, ipady=10)
    connect.grid(row=9, column=0, ipady=10)


def connectGridDeactivate():
    connect.grid_forget()
    labelServer.grid_forget()
    IP_entry.grid_forget()
    #IP_entry.delete(0,tk.END)
    labelPort.grid_forget()
    PORT_entry.grid_forget()
   #PORT_entry.delete(0, tk.END)

    labelUser.grid_forget()
    userName_entry.grid_forget()
    userName_entry.delete(0, tk.END)

    labelPass.grid_forget()
    PASS_entry.grid_forget()
    PASS_entry.delete(0, tk.END)


def directGridDeactivate():
    mylistFiles.grid_forget()
    scrollbar.grid_forget()


def connect():
    IP = IP_entry.get()
    PORT = PORT_entry.get()
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_CON:
        if IP and PORT:
            ADDR = (IP, int(PORT))
            client_CON.connect(ADDR)
            messagebox.showinfo("Connection Status", f"'{ADDR}' successful!")
            connectGridDeactivate()

        else:
            messagebox.showwarning("Input Needed", "Please enter a valid file server address.")


    direct(".") #default directory
def direct(directory):
    IP = IP_entry.get()
    PORT = PORT_entry.get()
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_DIR:
            cmd = "DIR"
            ADDR = (IP, int(PORT))
            client_DIR.connect(ADDR)
            client_DIR.send(cmd.encode(FORMAT))
            client_DIR.send(directory.encode(FORMAT))
            files = client_DIR.recv(4096)
            contents = json.loads(files.decode('utf-8'))
            chngdirectory.grid(row=1, column=0, ipady=10)
            logout.grid(row=1, column=1, ipady=10)

            upload.grid(row=2, column=0, ipady=10)
            download.grid(row=2, column=1, ipady=10)
            delete.grid(row=2, column=2, ipady=10)
            if len(contents) <=0:
                mylistFiles.grid(row=4, rowspan=10)
                mylistFiles.delete(0, tk.END)
            else:
                mylistFiles.grid(row=4, rowspan=len(contents))
                mylistFiles.delete(0, tk.END)
                for line in range(len(contents)):
                    mylistFiles.insert(END, str(contents[line]))

            folders = client_DIR.recv(4096)
            contents = json.loads(folders.decode('utf-8'))

            if len(contents) <= 0:
                mylistDIR.grid(row=4, rowspan=10, column=1)
                mylistDIR.delete(0, tk.END)

            else:
                mylistDIR.grid(row=4, rowspan=len(contents), column=1)
                mylistDIR.delete(0, tk.END)

                for line in range(len(contents)):
                    mylistDIR.insert(END, str(contents[line]))

    except Exception as e:
        messagebox.showerror("Error", f"Failed to load directory: {e}")


def logout():
    quit()

def chngdirectory():
    directory = mylistDIR.selection_get()
    global currentWorkingServerDirectory
    try:
        if directory == "cd..":
            if currentWorkingServerDirectory == "":
                raise Exception("Cannot traverse up from the root directory")
            else:
                lastSlash = currentWorkingServerDirectory.rindex("/")
                currentWorkingServerDirectory = currentWorkingServerDirectory[0:lastSlash]
        else:
            currentWorkingServerDirectory += "/" + directory

        if currentWorkingServerDirectory:
            direct(currentWorkingServerDirectory)

        else:
            direct(".")
    except Exception as e:
        messagebox.showerror("Error", f"Directory traversal error: {e}")


def upload():
    filename = filedialog.askopenfilename(initialdir="/", title = "Select a file to upload", filetypes = (("Text files", "*.txt*"),("Audio files", "*.mp3*"), ("Audio files", "*.flac*"), ("Video files", "*.mp4*")))
def download(updateinterval=1):
    IP = IP_entry.get()
    PORT = PORT_entry.get()
    ADDR = (IP,int(PORT))
    global currentWorkingServerDirectory
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_Download:
        client_Download.connect(ADDR)
        filename = mylistFiles.selection_get()
        cmd = "DOWNLOAD"
        client_Download.send(cmd.encode(FORMAT))
        progress_label.grid(row=3, column=0, columnspan=2, padx=10, pady=5, sticky="we")
        try:
            client_Download.send(filename.encode(FORMAT))
            time.sleep(0.1)
            if currentWorkingServerDirectory == "." or currentWorkingServerDirectory == "":
                client_Download.send(".".encode(FORMAT))
            else:
                client_Download.send(currentWorkingServerDirectory.encode(FORMAT))

            filesize = client_Download.recv(SIZE).decode(FORMAT)
            filesize = int(filesize)
            ack = "1"
            client_Download.send(ack.encode(FORMAT))

            start_time = time.time()
            downloaded_size = 0

            last_update_time = start_time
            last_downloaded_size = 0
            if filesize:
                #progress = tqdm.tqdm(range(filesize), f"Downloading {filename}", unit="B", unit_scale=True, unit_divisor=1024) #for testing purposes only
                with open(filename, "wb") as file:
                    while True:
                        bytes_read = client_Download.recv(SIZE)
                        if not bytes_read:
                            break
                        file.write(bytes_read)
                        time.sleep(0.1)

                        #downloaded_size += len(bytes_read)
                    '''
                        current_time = time.time()
                        if current_time - last_update_time >= updateinterval:
                            percent_complete = (downloaded_size / filesize) * 100
                            elapsed_time = current_time - start_time
                            speed = (downloaded_size - last_downloaded_size) / (current_time - last_update_time) if current_time - last_update_time > 0 else 0
                            remaining_time = (filesize - downloaded_size) / speed if speed > 0 else 0

                            progress_label.config(text=(
                                f"Progress: {format_bytes(downloaded_size)}/{format_bytes(filesize)} "
                                f"({percent_complete:.2f}%) | "
                                f"Speed: {format_bytes(speed)}/s | "
                                f"Elapsed: {elapsed_time:.2f}s | "
                                f"ETA: {remaining_time:.2f}s"
                            ))
                            progress_label.update()  # Force the GUI to update the label

                            last_update_time = current_time
                            last_downloaded_size = downloaded_size

                        progress_label.config(text="Download successful")
                        progress.update(len(bytes_read)) #for testing purposes only
                        '''
        except Exception as E:
            messagebox.showerror("Error", f"Failed to download file: {E}")
            #progress_label.config(text="Download unsuccessful")

    #progress_label.update()
    
    #currently need to implement a way to keep track of the current directory from the client's side so we can try to identify where a file is based on the current 
    #directory and download that instance of it and not one from a different folder
    

    
    #Additional notes: need to change the default directory on the server side so the client cannot delete the server code :)
    

def delete():
    print("Buhbai")


window = tk.Tk()
window.title("File Sharing Cloud Server")
window.geometry("500x500")

labelServer = tk.Label(window, text="Enter address of the file server:")
labelServer.grid(row=1, column=0, ipady=10)

IP_entry = tk.Entry(window)
IP_entry.grid(row=2, column=0, ipady=10)

labelPort = tk.Label(window, text="Enter port of the file server:")
labelPort.grid(row=3, column=0, ipady=10)

PORT_entry = tk.Entry(window)
PORT_entry.grid(row=4, column = 0, ipady = 10)







labelUser = tk.Label(window, text="Enter your username for authentication:")
labelUser.grid(row=5, column=0, ipady=10)


userName_entry = tk.Entry(window)
userName_entry.grid(row=6, column=0, ipady=10)


labelPass = tk.Label(window, text="Enter your password for the server:")
labelPass.grid(row=7, column=0, ipady=10)

PASS_entry = tk.Entry(window, show="*")
PASS_entry.grid(row=8, column = 0, ipady = 10)

connect = tk.Button(window, text="Connect", command=connect)
connect.grid(row = 9, column =0, ipady =10)



scrollbar = tk.Scrollbar(window, orient="vertical")
#scrollbar.grid(rowspan=10)
#hideWidget(scrollbar)

mylistFiles = Listbox(window, yscrollcommand=scrollbar.set)
mylistFiles.grid()
hideWidget(mylistFiles)

mylistDIR = Listbox(window, yscrollcommand=scrollbar.set)
mylistDIR.grid()
hideWidget(mylistDIR)

scrollbar.config(command=mylistFiles.yview)

chngdirectory = tk.Button(window, text="Change Directory", command=chngdirectory)
chngdirectory.grid(row = 1, column = 0, ipady = 10)
hideWidget(chngdirectory)


upload = tk.Button(window, text="Upload file", command=upload)
upload.grid(row = 2, column = 0, ipady = 10)
hideWidget(upload)

download = tk.Button(window, text="Download file", command=download)
download.grid(row = 2, column = 1, ipady = 10)
hideWidget(download)

delete = tk.Button(window, text="Delete file", command=delete)
delete.grid(row = 2, column = 2, ipady = 10)
hideWidget(delete)

progress_label = tk.Label(window, text="Progress: ")
progress_label.grid(row=3, column=0, columnspan=2, padx=10, pady=5, sticky="we")
hideWidget(progress_label)

logout = tk.Button(window, text ="Disconnect", command = logout)
logout.grid(row=1, column=1, ipady=10)
hideWidget(logout)


window.mainloop()
