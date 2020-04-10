import sys
import argparse
import socket
from datetime import datetime
from queue import Queue
import threading

# Sort out command line args
parser = argparse.ArgumentParser()
parser.add_argument("host", help="The IP address or hostname of the scan target")
parser.add_argument("mode", help="1: 1023 standardized ports, 2: All 65535 ports, 3: Common ports, 4: User selected ports")
args = parser.parse_args()

target = args.host
mode = int(args.mode)
queue = Queue()

# Attempt connection to specified port, returning True/False depending on result
def scan(port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
   # socket.setdefaulttimeout(1)
    try:
        result = s.connect_ex((target,port))
        if result == 0:
            return True
        else:
            return False
    except socket.gaierror:
        print("Hostname could not be resolved")
        sys.exit()

    except socket.error:
        print("Could not connect to host.")
        sys.exit()

# Set ports for scanning based on user input
def ports(mode):
    if mode == 1:
        for port in range(1, 1024):
            queue.put(port)
    elif mode == 2:
        for port in range(1,65535):
            queue.put(port)
    elif mode == 3:
        common = [20, 21, 22, 23, 25, 53, 80, 110, 139, 143, 443, 445]
        for port in common:
            queue.put(port)
    elif mode == 4:
        ports = input("Enter ports, space seperated:")
        ports = ports.split()
        ports = list(map(int, ports))
        for port in ports:
            queue.put(port)


# Get port from the queue and run a scan
def worker():
    while not queue.empty():
        port = queue.get()
        if scan(port):
            print("Port {} is open".format(port))

# Handle threaded component of the script
def scanner(numberOfThreads, mode):
    ports(mode)
    threads = []
    try:
        for t in range(numberOfThreads):
            thread = threading.Thread(target=worker)
            threads.append(thread)

        for thread in threads:
            thread.start()

        for thread in threads:
            thread.join()

    except KeyboardInterrupt:
        print("\nExiting.")
        sys.exit()

# Add a nice banner
print("-" * 50)
print("Scanning " + target)
starttime = datetime.now()
print("Time started: {}".format(str(starttime)))

scanner(100, mode)

finishtime = datetime.now()
duration = finishtime - starttime
print("Completed in {} seconds".format(str(duration.total_seconds())))