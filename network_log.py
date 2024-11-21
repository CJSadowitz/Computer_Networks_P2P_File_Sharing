import logging
import time

logger = logging.getLogger(__name__)

def response_time(conn, encoded_cmd):
	conn.send(encoded_cmd)
	time_0 = time.time()
	ack = conn.recv(4096)
	time_1 = time.time()
	logger.info(str(encoded_cmd.decode('utf-8')[:4]) + ' ' + str(time_1 - time_0))
	return ack, time_0


def download_time(conn, init_time):
	file_part = conn.recv(4096)
	time_1 = time.time()
	logger.info("DOWNLOAD: " + str(time_1 - init_time))
	return file_part

def upload_time(conn, encoded_data, init_time):
	conn.send(encoded_data)
	time_1 = time.time()
	logger.info("UPLOAD: " + str(time_1 - init_time))

# Should be a way to combine the last two functions
# There may be a way to combine all three...
