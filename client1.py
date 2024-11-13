import tkinter as tk
from tkinter import *
from tkinter import messagebox
import os
import time
import socket
import json
import tqdm

IP = 'localhost'
PORT = 4450
ADDR = (IP, PORT)
SIZE = 1024
FORMAT = "utf-8"
SERVER_DATA_PATH = "server_data"
#client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

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
    mylist.grid_forget()
    directory.grid_forget()
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
            directory.grid(row=1, column=0, ipady=10)

        else:
            messagebox.showwarning("Input Needed", "Please enter a valid file server address.")

def direct():
    IP = IP_entry.get()
    PORT = PORT_entry.get()
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_DIR:
            cmd = "DIR"
            ADDR = (IP, int(PORT))
            client_DIR.connect(ADDR)
            client_DIR.send(cmd.encode(FORMAT))

            data = client_DIR.recv(4096)
            contents = json.loads(data.decode('utf-8'))
            #messagebox.showinfo("Directory Contents", "\n".join(contents))
            hideWidget(directory)
            chngdirectory.grid(row=1, column=0, ipady=10)
            logout.grid(row=1, column=1, ipady=10)

            upload.grid(row=2, column=0, ipady=10)
            download.grid(row=2, column=1, ipady=10)
            delete.grid(row=2, column=2, ipady=10)
            mylist.grid(rowspan=len(contents))
            mylist.delete(0, tk.END)
            for line in range(len(contents)):
                mylist.insert(END, str(contents[line]))
    except Exception as e:
        messagebox.showerror("Error", f"Failed to load directory: {e}")




def logout():
    #cmd = "LOGOUT"
    #client.send(cmd.encode(FORMAT))
    #client.shutdown(socket.SHUT_RDWR)
    #client.close()
    quit()

def chngdirectory():
    print("Huwwo")
def upload():
    print("guhbye")
def download():
    IP = IP_entry.get()
    PORT = PORT_entry.get()
    ADDR = (IP,int(PORT))
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_Download:
        client_Download.connect(ADDR)
        filename = mylist.selection_get()
        cmd = "DOWNLOAD"
        client_Download.send(cmd.encode(FORMAT))
        try:
            client_Download.send(filename.encode(FORMAT))
            filesize = client_Download.recv(SIZE)

            if filesize > bytes(0):
                # progress = tqdm.tqdm(range(filesize), f"Downloading {filename}", unit="B", unit_scale=True, unit_divisor=1024)
                with open(filename, "wb") as file:
                    print("doing?")
                    while True:
                        bytes_read = client_Download.recv(SIZE)
                        if not bytes_read:
                            break
                        file.write(bytes_read)
                        # progress.update(len(bytes_read))
        except Exception as E:
            messagebox.showerror("Error", f"Failed to download file: {E}")



    '''
    server brainstorming, send the command to identify it as a download task send some form of acknowledgement to the client and then through server side expect a reply of the file-name
    from there if possible, select the file and then send it through the socket, not sure where it would download to
    '''
def delete():
    print("Buhbai")


window = tk.Tk()
window.title("File Sharing Cloud Server")
window.geometry("375x500")

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

directory = tk.Button(window, text="Load Directory", command=direct)
directory.grid(row = 1, column = 0, ipady = 10)
hideWidget(directory)

scrollbar = tk.Scrollbar(window, orient="vertical")
#scrollbar.grid(rowspan=10)
#hideWidget(scrollbar)

mylist = Listbox(window, yscrollcommand=scrollbar.set)

mylist.grid()
hideWidget(mylist)

scrollbar.config(command=mylist.yview)

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



logout = tk.Button(window, text ="Disconnect", command = logout)
logout.grid(row=1, column=1, ipady=10)
hideWidget(logout)
window.mainloop()

