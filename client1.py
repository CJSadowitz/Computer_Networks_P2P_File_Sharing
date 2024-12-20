import tkinter as tk
from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
import customtkinter
import socket
import json
import tqdm
import time
import logging
from network_log import response_time, download_time, upload_time
import os

logger = logging.getLogger(__name__)

TOKEN = ''
IP = 'localhost' #default IP
PORT = 4450 #default port
ADDR = (IP, PORT)
SIZE = 1024
FORMAT = "utf-8"

currentWorkingServerDirectory = ""


# ensures user is authenticated
def check_auth(auth):
    try:
        cmd, msg = auth.split('||')
        if cmd == 'DSC':
            messagebox.showwarning("Connection Status", f"{msg}")
            return False
    except Exception as e:
        return True

# Standard RSA encryption
def encrypt(creds, n, e):
    creds = creds.encode(FORMAT)
    creds = int.from_bytes(creds, byteorder='big')
    creds = pow(creds, int(e), int(n))
    return creds


# Parses login parameters to user
def login(username, password, conn):
    conn.send(f"LOGIN||Public Keys".encode(FORMAT))
    cmd, data = conn.recv(SIZE).decode(FORMAT).split("||")
    n, e = data.split(';')
    username = encrypt(username, n, e)
    password = encrypt(password, n, e)
    conn.send(f"{username};{password}".encode(FORMAT))



def hideWidget(widget): #helper function to easily hide a widget
    widget.grid_forget()

def connectGridActivate(): #activates all the widgets related to connecting to the file server
    labelServer.grid(row=1, column=0, ipady=10)
    IP_entry.grid(row=2, column=0, ipady=10)
    labelPort.grid(row=3, column=0, ipady=10)
    PORT_entry.grid(row=4, column=0, ipady=10)
    labelUser.grid(row=5, column=0, ipady=10)
    userName_entry.grid(row=6, column=0, ipady=10)
    labelPass.grid(row=7, column=0, ipady=10)
    PASS_entry.grid(row=8, column=0, ipady=10)
    connect.grid(row=9, column=0, ipady=10)


def connectGridDeactivate(): #used to deactivate and clear the entry fields related to connecting to a file server
    connect.grid_forget()
    labelServer.grid_forget()
    IP_entry.grid_forget()
    IP_entry.delete(0,tk.END)
    labelPort.grid_forget()
    PORT_entry.grid_forget()
    PORT_entry.delete(0, tk.END)

    labelUser.grid_forget()
    userName_entry.grid_forget()
    userName_entry.delete(0, tk.END)

    labelPass.grid_forget()
    PASS_entry.grid_forget()
    PASS_entry.delete(0, tk.END)


def directGridDeactivate(): #function used to deactive the widgets related to post-connection, hasnt been updated
    mylistFiles.grid_forget()
    scrollbar.grid_forget()


def connect(): #simple function used for the client to initially connect to the server, more to update client variables for socket connectivity
    global IP
    global PORT
    global ADDR
    global TOKEN
    IP = IP_entry.get()
    PORT = PORT_entry.get()
    username = userName_entry.get()
    password = PASS_entry.get()
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_CON:
        if IP and PORT:
            ADDR = (IP, int(PORT))
            client_CON.connect(ADDR)
            login(username, password, client_CON)
            data = client_CON.recv(SIZE).decode(FORMAT)
            cmd, msg = data.split('||')
            if cmd == 'OK':
                messagebox.showinfo("Connection Status", f"'{ADDR}' successful!")
                TOKEN = msg
                connectGridDeactivate()
                direct(".")
            else:
                messagebox.showwarning("Connection Status", "Incorrect Username or Password")
        else:
            messagebox.showwarning("Input Needed", "Please enter a valid file server address.")

def direct(directory): #used to obtain the directory information regarding the currentWorkingServerDirectory, separates it into files and folders
    global ADDR
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_DIR:
            cmd = "DIR"
            client_DIR.connect(ADDR)
            combined = cmd + "||" + directory + ";" + TOKEN

            files, init_time = response_time(client_DIR, combined.encode(FORMAT))

            if check_auth(files):
                pass
            else:
                return
            ack = 0

            files = files.decode('utf-8')
            if files[0] == '[' and files[1] == ']':
                files = files[2:]
            if files != "":
                try:
                    ack = 1
                    contents = json.loads(files)
                except Exception as e:
                    print ("Bad Format:", e)
                    print (files)
                    contents = json.loads('["cd.."]') # lets me traverse backwards
            else:
                contents = ""

            chngdirectory.grid(row=1, column=0, ipady=10)
            makekDir.grid(row=1, column=1, ipady=10)
            logout.grid(row=1, column=2, ipady=10)
            upload.grid(row=2, column=0, ipady=10)
            download.grid(row=2, column=1, ipady=10)
            delete.grid(row=2, column=2, ipady=10)

            if len(contents) <= 0:
                mylistFiles.grid(row=4, rowspan=10, padx=10)
                mylistFiles.delete(0, tk.END)
            else:
                mylistFiles.grid(row=4, rowspan=len(contents), padx=10)
                mylistFiles.delete(0, tk.END)
                for line in range(len(contents)):
                    mylistFiles.insert(END, str(contents[line]))

            folders, init_time = response_time(client_DIR, str(ack).encode(FORMAT))

            folders = folders.decode('utf-8')

            if folders == "":
                 dir_contents = ""
            else:
                dir_contents = json.loads(folders)

            if len(dir_contents) <= 0:
                mylistDIR.grid(row=4, rowspan=10, column=1)
                mylistDIR.delete(0, tk.END)
            else:
                mylistDIR.grid(row=4, rowspan=len(dir_contents), column=1)
                mylistDIR.delete(0, tk.END)

                for line in range(len(dir_contents)):
                    mylistDIR.insert(END, str(dir_contents[line]))
    except Exception as e:
        print ("Direct Error:", e) # Yay
        messagebox.showerror("Error", f"Failed to load directory: {e}")

def logout(): #outdated function for resetting the connection
    quit()

def chngdirectory(): #used for updating the currentWorkingServerDirectory and then obtaining the information regarding it
    directory = "" # Check here if the 'directory' that I am changing to is a file or a directory
    try:
        directory = mylistDIR.selection_get()
    except Exception as e:
        messagebox.showwarning("No directory Selected", "No directory selected to navigate to")
        print (e)
        return
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
        print ("Change Directory error", e)
        messagebox.showerror("Error", f"Directory traversal error: {e}")


def upload(): #used for uploading files to the server, not currently functional
    filename = filedialog.askopenfilename(initialdir="/", title="Select a file to upload", filetypes=(
    ("Text files", "*.txt*"), ("Audio files", "*.mp3*"), ("Audio files", "*.flac*"), ("Video files", "*.mp4*"), ("Video files", "*.mov")))
    file_size = os.path.getsize(filename)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_upload:
        # Connect to the server
        client_upload.connect(ADDR)
        # Initiate upload
        encoded_message = f"UPLOAD||File Upload;{TOKEN}".encode(FORMAT)
        response, init_time = response_time(client_upload, encoded_message)
        cmd, data = response.decode(FORMAT).split('||')

        if cmd == 'OK':
            # Verify file does not already exist
            encoded_message = os.path.basename(filename).encode(FORMAT)
            response, init_time = response_time(client_upload, encoded_message)
            cmd, data = response.decode(FORMAT).split('||')

            if cmd == 'OK':
                pass
            elif cmd == 'EXISTS':
                answer = messagebox.askquestion("File Exists", "File exists would you like to overwrite it.")
                if answer == 'yes':
                    pass
                else:
                    client_upload.send(f'FAIL||Don\'t Overwrite'.encode(FORMAT))
                    return
            # Verify file is not too large

            encoded_message = f"OK||{str(os.path.getsize(filename))}".encode(FORMAT)
            response, init_time = response_time(client_upload, encoded_message)
            cmd, data = response.decode(FORMAT).split("||")

            if cmd == 'OK':
                # Send File
                # with open(filename, 'rb') as f:
                #    while chunk := f.read(1024):
                #        client_upload.sendall(chunk)
                upload_time(client_upload, filename, init_time)
                messagebox.showinfo("Upload successful", f"Upload of {os.path.basename(filename)} complete")
                direct('.')
            else:
                messagebox.showwarning("Upload Failed", f"{data}")
        else:
            messagebox.showwarning("Upload Failed", f"{data}")

def download(updateinterval=1): #used for downloading a selected file from the server
    global ADDR
    global currentWorkingServerDirectory
    filename = ""
    big_path = ""
    try: #error-check to ensure the selected item is actually a file, during debugging it would sometimes allow for a directory to be selected
        filename = mylistFiles.selection_get()
        command = "FILE"
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_error:
            client_error.connect(ADDR)
            big_path = currentWorkingServerDirectory + '/' + filename
            combined = command + "||" + big_path + ";" + TOKEN
            client_error.send(combined.encode(FORMAT))

            test = client_error.recv(SIZE).decode(FORMAT)
            if test == 'False':
                messagebox.showwarning("No File Selected", "No file selected to download")
                client_error.close()
                return
    except Exception:
        messagebox.showwarning("No File Selected", "No file selected to download")
        return

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_Download: #initiates the download with the server
        client_Download.connect(ADDR)
        cmd = "DOWNLOAD"
        combined = cmd + "||" + big_path + ";" + TOKEN

        try:
            filesize, init_time = response_time(client_Download, combined.encode(FORMAT))
            filesize = int(filesize)

            if filesize and filesize != -1:
                with open(filename, "wb") as file:
                    last_time = init_time
                    while True:
                        bytes_read, prev_time = download_time(client_Download, last_time, filesize)
                        last_time = prev_time
                        if not bytes_read:
                            break
                        file.write(bytes_read)

                messagebox.showinfo("Download successful", f"Download of {filename} complete")

            elif filesize == -1:
                messagebox.showerror("Error", f"File not found")
        except Exception as E:
            messagebox.showerror("Error", f"Failed to download file: {E}")

def delete(): #used for deleting a selected item (file or directory from the server), sends information if the command cannot be properly executed
    selected = [mylistFiles.selection_get()]
    global ADDR
    global currentWorkingServerDirectory
    for option in selected:
        if option:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_DEL:
                client_DEL.connect(ADDR)
                entire_path = currentWorkingServerDirectory + '/' + option
                combined = "DEL" + "||" + entire_path + ";" + TOKEN

                result = response_time(client_DEL, combined.encode(FORMAT))

                if result == "deleted":  # success
                    messagebox.showinfo("Item deleted", f"The item {option} has been deleted")
                elif result == "open":  # selected item is open, raise a warning to try again later
                    messagebox.showwarning("Item Open", f"Selected item is currently open, try deleting later")
                elif result == "NotFound":  # selected item is not found
                    messagebox.showerror("Item Not Found", f"The selected item was not found on the server")
                elif result == "NotEmpty": #selected directory is not empty
                    messagebox.showwarning("Items in Directory", f"Items present within the directory selected")
    direct(currentWorkingServerDirectory)


def makeDirectory(): #used for creating new directories on the server, has checks on the client side to prevent certain characters from being passed to the server
    dialog = customtkinter.CTkInputDialog(text="Name the new directory", title="Make a new subdirectory")
    newFolder = dialog.get_input()
    forbidden_char = ['/', '\\', ':', '*', '<', '>', '\"', '|', '?']
    if newFolder:
        if any(char in newFolder for char in forbidden_char):
            messagebox.showwarning("Forbidden Character", f"Directories cannot include /, \\, :, *, <, >, \", |, or ?")
        else:
            cmd = "MKDIR"
            global ADDR
            global currentWorkingServerDirectory
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_mkDir:
                client_mkDir.connect(ADDR)
                combined = cmd + "||" + currentWorkingServerDirectory + ";" + TOKEN

                cmd_ack = response_time(client_mkDir, combined.encode(FORMAT))
                ack, init_time = response_time(client_mkDir, newFolder.encode(FORMAT))

                if ack.decode(FORMAT) != '1':
                    messagebox.showwarning("Folder Conflict", f"Folder name in use")
            direct(currentWorkingServerDirectory)
    else:
        messagebox.showwarning("No Input", f"No input detected")

if __name__ == "__main__":

    logging.basicConfig(filename='response_times.log', level=logging.INFO)
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
    PORT_entry.grid(row=4, column=0, ipady=10)

    labelUser = tk.Label(window, text="Enter your username for authentication:")
    labelUser.grid(row=5, column=0, ipady=10)

    userName_entry = tk.Entry(window)
    userName_entry.grid(row=6, column=0, ipady=10)

    labelPass = tk.Label(window, text="Enter your password for the server:")
    labelPass.grid(row=7, column=0, ipady=10)

    PASS_entry = tk.Entry(window, show="*")
    PASS_entry.grid(row=8, column=0, ipady=10)

    connect = tk.Button(window, text="Connect", command=connect)
    connect.grid(row=9, column=0, ipady=10)

    scrollbar = tk.Scrollbar(window, orient="vertical")
    # scrollbar.grid(rowspan=10) #tbh idk what this even did
    # hideWidget(scrollbar)

    mylistFiles = Listbox(window, yscrollcommand=scrollbar.set, selectmode=tk.SINGLE)
    mylistFiles.grid()
    hideWidget(mylistFiles)

    mylistDIR = Listbox(window, yscrollcommand=scrollbar.set, selectmode=tk.SINGLE)
    mylistDIR.grid()
    hideWidget(mylistDIR)

    scrollbar.config(command=mylistFiles.yview)

    chngdirectory = tk.Button(window, text="Change Directory", command=chngdirectory)
    chngdirectory.grid(row=1, column=0, ipady=10)
    hideWidget(chngdirectory)

    upload = tk.Button(window, text="Upload file", command=upload)
    upload.grid(row=2, column=0, ipady=10)
    hideWidget(upload)

    download = tk.Button(window, text="Download file", command=download)
    download.grid(row=2, column=1, ipady=10)
    hideWidget(download)

    delete = tk.Button(window, text="Delete", command=delete)
    delete.grid(row=2, column=2, ipady=10)
    hideWidget(delete)

    makekDir = tk.Button(window, text="New Directory", command=makeDirectory)
    makekDir.grid(row=1, column=1, ipady=10)
    hideWidget(makekDir)

    logout = tk.Button(window, text="Disconnect", command=logout)
    logout.grid(row=1, column=2, ipady=10)
    hideWidget(logout)

    logger.info("Client_Connected: " + str(time.time()))

    window.mainloop()
