# Computer Networks P2P File Sharing Project
## Installation
Install the repo `git clone https://github.com/CJSadowitz/Computer_Networks_P2P_File_Sharing.git` </br>
Create a python virtual environment `python3 -m venv venv` </br>
Activate python `source venv/bin/activate` or `source venv/scripts/activate`</br>
Download dependices `pip install -r requirements.txt`

## Running
### Server
If you are planning to run the server across wifi network, you must change the IP on the top line of server.py </br>
You can find you IP with `ipconfig` (windows) `hostname -I` (linux) </br>
To run server: `python3 server.py` </br>
### Client
The port is always `53849` unless changed by you </br>
To run client: `python3 client1.py` </br>
Assuming Local: Change IP to correct IP address as need </br>
IP: `127.0.0.1` </br>
PORT: `9999` </br>
USERNAME: `colin` or `jordan` </br>
PASSOWRD: `freedom` or `password` </br>

## Client Operation
### Change Directory
The directories box is on the right </br>
All of the files will be in the left box </br>
To navigate select a directory and click change directory </br>
To navigate out select `cd` and click change directory </br>
### New Directory
This will create a new directory within the directory the user is currently in </br>
Simply type in the name, the directory will automatically populate on the right </br>
### Upload File
This will open up the file explorer where you can select the desired file to upload </br>
In my testing this always dumped the file on the highest level of the directories </br>
### Download File
Simply navigate to a directory to where a file exists </br>
Select the file in the left box select the download option </br>
This will download the file into the directory that the client.py exists </br>
### Delete
Simply select the directory or file and select the delete option </br>
If the directory has other files or directories within it, it cannot be deleted </br>
### Disconnect
Simply select disconnect </br>

## Network Analysis
After running a client connection and doing any sort of operation an analysis can be conducted </br>
To run: `python3 network_log.py` </br>
This uses the file: `response_times.log` </br>
All of the on the user's hardware (within this directory) connections are log inside of this file </br>
All of the connections are split and put into a directory called 'separated_logs' </br>
The network analysis code runs on these individual files and creates a plot for response times, upload times, and download times </br>
There is extra information outputted into the console </br>
