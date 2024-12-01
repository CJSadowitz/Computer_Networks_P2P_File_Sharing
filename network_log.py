import logging
import time
import os
from matplotlib import pyplot as plt
SIZE = 1024
FORMAT = "utf-8"

logger = logging.getLogger(__name__)

def response_time(conn, encoded_cmd):
	conn.send(encoded_cmd)
	time_0 = time.time()
	ack = conn.recv(4096)
	time_1 = time.time()
	logger.info("RESP:" + ' ' + str(round(time_1 - time_0, 6)) + ' ' + str(time_0))
	return ack, time_0

# should have an ack after each recieved packet iff there is an ack then this function is just response time
def download_time(conn, init_time, file_size):
	file_part = conn.recv(4096)
	time_1 = time.time()
	logger.info("DOWN: " + str(round(time_1 - init_time, 6)) + ' ' + str(time.time())  + ' ' + str(file_size))
	return file_part, time_1

def upload_time(conn, encoded_data, init_time):
	conn.send(encoded_data)
	time_1 = time.time()
	logger.info("UPLD: " + str(time_1 - init_time))

#######################################################################################################################################
### DATA ANALYSIS ###
#######################################################################################################################################

# Number of packets received over time from the server?
# Differentiate Download Times and Files Transfer Rates
# Does Techincally Work just averages ALL File Transfer Rates and times
def received_packets(file):
	start_time = None
	packet_times = []
	packet_size = None
	occurance_time = []
	with open(file, "r") as f:
		for line in f:
			all_info = line.split(' ')
			log_info = all_info[0].split(':')
			if log_info[1] == "__main__":
				start_time = float(all_info[1])
			if log_info[2] == "DOWN":
				packet_size = float(all_info[3])
				# occurance_time.append(float(all_info[2]) - start_time)
				occurance_time.append(float(all_info[2]))
				packet_times.append(float(all_info[1]))

	plt.scatter(occurance_time, packet_times)
	try:
		average_time = sum(packet_times) / len(packet_times)
	except Exception as e:
		print (e)
	print ("DOWNLOAD")
	try:
		print ("AVG Response Time", average_time, "NUM", len(packet_times), "LEN", packet_size)
	except Exception as e:
		print (e)
	try:
		print ("AVG Bps", round(packet_size / sum(packet_times), 2))
		print ("AVG MBps", round((packet_size / sum(packet_times)) / (1 * 10**6), 2))
	except Exception as e:
		print (e)
	plt.xlabel("Time since client connected (s)")
	plt.ylabel("Response Time (s)")
	plt.title(str(file))
	plt.show()

# Upload packet times
def sent_packets(file):
	pass

# Response times since the start of the clients connection
def response_times(file):
	# Plot response time to time since connected to server
	start_time = None
	length = None
	response_times = []
	occurance_times = []
	with open(file, "r") as f:
		for line in f:
			all_info = line.split(' ')
			log_info = all_info[0].split(':')
			if log_info[1] == "__main__":
				start_time = float(all_info[1])
			if log_info[2] == "RESP":
				response_times.append(float(all_info[1]))
				# occurance_times.append(float(all_info[2]) - start_time)
				occurance_times.append(float(all_info[2]))

	plt.scatter(occurance_times, response_times)
	plt.xlabel("Time since client connected (s)")
	plt.ylabel("Response Time (s)")

	try:
		average_time = sum(response_times) / len(response_times)
		print ("RESPONSE: AVG", average_time)
	except Exception as e:
		print (e)

	plt.title(str(file))
	plt.show()

# All times are in one file, we split for individual analysis
def split_log(file):
	logs = []
	temp_log = []
	with open(file, "r") as f:
		lines = f.readlines()
		# This data V is not read: temp sol to bad code
		lines.append(lines[0])

		length = len(lines)

	for i, line in enumerate(lines):
		all_info = line.split(' ')
		log_info = all_info[0].split(':')

		if (log_info[1] == "__main__" and i != 0) or (i == length - 1):
			if len(temp_log) != 0:
				new_log = temp_log[:]
				logs.append(new_log)
				temp_log = []

		temp_log.append(line)

	directory = "separated_logs"
	try:
		os.mkdir(directory)
	except Exception as e:
		pass

	write_logs(logs, directory)

def write_logs(logs_list, directory):
	i = 0
	for log in logs_list:
		path = os.path.join(directory, "log_" + str(i) + ".txt")
		with open(path, "w") as f:
			for line in log:
				f.write(line)
			i += 1


if __name__ == "__main__":
	file = "response_times.log"
	split_log(file)
	directory = "separated_logs"

	for file in os.listdir("separated_logs"):
		path = os.path.join(directory, str(file))
		filename = os.fsdecode(path)
		response_times(filename)
		received_packets(filename)
	# response_times("separated_logs/log_0.txt")
	# received_packets("separated_logs/log_0.txt")
