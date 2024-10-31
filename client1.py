import tkinter as tk
from tkinter import messagebox
import os
import time
import socket

IP = 'localhost'
PORT = 4450
ADDR = (IP, PORT)
SIZE = 1024
FORMAT = "utf-8"
SERVER_DATA_PATH = "server_data"

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

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
    labelPort.grid_forget()
    PORT_entry.grid_forget()

    labelUser.grid_forget()
    userName_entry.grid_forget()
    labelPass.grid_forget()
    PASS_entry.grid_forget()


def connect():
    IP = IP_entry.get()
    PORT = PORT_entry.get()

    if IP and PORT:
        ADDR = (IP, int(PORT))
        client.connect(ADDR)
        messagebox.showinfo("Connection Status", f"'{ADDR}' successful!")
        connectGridDeactivate()
        authenGridActivate()

    else:
        messagebox.showwarning("Input Needed", "Please enter a valid file server address.")




window = tk.Tk()
window.title("File Sharing Cloud Server")
window.geometry("275x500")

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


window.mainloop()



while True:  ### multiple communications
    data = client.recv(SIZE).decode(FORMAT)
    cmd, msg = data.split("@")
    if cmd == "OK":
        print(f"{msg}")
    elif cmd == "DISCONNECTED":
        print(f"{msg}")
        break
