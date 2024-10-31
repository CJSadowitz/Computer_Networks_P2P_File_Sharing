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
    connect.grid(row=5, column=0, ipady=10)


def connectGridDeactivate():
    connect.grid_forget()
    labelServer.grid_forget()
    IP_entry.grid_forget()
    labelPort.grid_forget()
    PORT_entry.grid_forget()

def authenGridActivate():
    labelUser.grid(row=1, column=0, ipady=10)
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




# Create the main window
window = tk.Tk()
window.title("File Sharing Cloud Server")
window.geometry("300x250")

# Label for instructions
labelServer = tk.Label(window, text="Enter address of the file server:")
labelServer.grid(row=1, column=0, ipady=10)

# Entry field for the file name
IP_entry = tk.Entry(window)
IP_entry.grid(row=2, column=0, ipady=10)

# Label for instructions
labelPort = tk.Label(window, text="Enter port of the file server:")
labelPort.grid(row=3, column=0, ipady=10)

# Entry field for the file name
PORT_entry = tk.Entry(window)
PORT_entry.grid(row=4, column = 0, ipady = 10)

# Button to trigger file upload
connect = tk.Button(window, text="Connect", command=connect)
connect.grid(row = 5, column =0, ipady =10)




# Label for user credentials
labelUser = tk.Label(window, text="Enter your username for authentication:")
labelUser.grid(row=1, column=0, ipady=10)
hideWidget(labelUser)

'''
# Entry field for the file name
IP_entry = tk.Entry(window)
IP_entry.grid(row=2, column=0, ipady=10)

# Label for instructions
labelPort = tk.Label(window, text="Enter port of the file server:")
labelPort.grid(row=3, column=0, ipady=10)

# Entry field for the file name
PORT_entry = tk.Entry(window)
PORT_entry.grid(row=4, column = 0, ipady = 10)

# Button to trigger file upload
connect = tk.Button(window, text="Connect", command=connect)
connect.grid(row = 5, column =0, ipady =10)
'''
# Run the application
window.mainloop()



while True:  ### multiple communications
    data = client.recv(SIZE).decode(FORMAT)
    cmd, msg = data.split("@")
    if cmd == "OK":
        print(f"{msg}")
    elif cmd == "DISCONNECTED":
        print(f"{msg}")
        break
