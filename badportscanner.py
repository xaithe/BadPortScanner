import sys
import socket
from datetime import datetime

# Define target
if len(sys.argv) == 2:
    # Resolve hostname
    target = socket.gethostbyname(sys.argv[1])
else:
    print("Invalid amount of arguments")
    print("Usage: python3 scanner.py <ip>")

# Add a nice banner
print("-" * 50)
print("Scanning " + target)
print("Time started: " + str(datetime.now()))

try:
    for port in range(50,85):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socket.setdefaulttimeout(1)
        result = s.connect_ex((target,port))
        if result == 0:
            print("Port {} is open".format(port))
        s.close()
        
except KeyboardInterrupt:
    print("\nExiting.")
    sys.exit()

except socket.gaierror:
    print("Hostname could not be resolved")
    sys.exit()

except socket.error:
    print("Could not connect to host.")
    sys.exit()

        