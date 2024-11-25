import logging
import time
import os
from matplotlib import pyplot as plt

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
	logger.info("DOWN: " + str(round(time_1 - init_time, 6)) + ' ' + str(file_size))
	return file_part

def upload_time(conn, encoded_data, init_time):
	conn.send(encoded_data)
	time_1 = time.time()
	logger.info("UPLD: " + str(time_1 - init_time))

#######################################################################################################################################
### DATA ANALYSIS ###
#######################################################################################################################################

# Number of packets received over time from the server?
def received_packets(file):
	pass

# Upload packet times
def sent_packets(file):
	pass

# Response times since the start of the clients connection
def response_times(file):
	# Plot response time to time since connected to server
	start_time = None
	response_times = []
	occurance_times = []
	with open(file, "r") as f:
		for line in f:
			all_info = line.split(' ')
			log_info = all_info[0].split(':')
			try:
				log_info[1]
			except Exception as e:
				print (log_info)
			if log_info[1] == '__main__':
				start_time = float(all_info[1])
			if log_info[2] == "RESP":
				response_times.append(float(all_info[1]))
				occurance_times.append(float(all_info[2]) - start_time)

	plt.scatter(occurance_times, response_times)
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

	print (len(logs))

	directory = "separated_logs"
	try:
		os.mkdir(directory)
	except Exception as e:
		print (e)

	write_logs(logs, directory)

def write_logs(logs_list, directory):
	i = 0
	for log in logs_list:
		with open(directory + "/log_" + str(i) + ".txt", "w") as f:
			for line in log:
				f.write(line)
			i += 1


if __name__ == "__main__":
	file = "response_times.log"
	split_log(file)

	response_times("separated_logs/log_0.txt")
	response_times("separated_logs/log_1.txt")
	response_times("separated_logs/log_2.txt")
