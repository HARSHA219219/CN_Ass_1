import socket
import json
from datetime import datetime

# Load rules.json dynamically (must be in the same folder)
with open("rules.json", "r") as f:
    rules_data = json.load(f)

# Extract IP pool (hardcoded 15 IPs)
IP_POOL = [
    "192.168.1.1", "192.168.1.2", "192.168.1.3", "192.168.1.4", "192.168.1.5",
    "192.168.1.6", "192.168.1.7", "192.168.1.8", "192.168.1.9", "192.168.1.10",
    "192.168.1.11", "192.168.1.12", "192.168.1.13", "192.168.1.14", "192.168.1.15"
]

time_rules = rules_data["timestamp_rules"]["time_based_routing"]

def resolve_ip(header_value):
    hh = int(header_value[:2])      # Hour from HHMMSSID
    ssid = int(header_value[6:8])   # Query sequence ID

    # Determine which time slot
    if 4 <= hh <= 11:
        rule = time_rules["morning"]
    elif 12 <= hh <= 19:
        rule = time_rules["afternoon"]
    else:  # 20-23 or 0-3
        rule = time_rules["night"]

    pool_start = rule["ip_pool_start"]

    index = pool_start + (ssid % 5)  # 5 IPs per time slot
    return IP_POOL[index]

# Server socket
HOST = "0.0.0.0"
PORT = 53535

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(5)
print(f"Server listening on {HOST}:{PORT}...")

while True:
    conn, addr = server_socket.accept()
    try:
        data = conn.recv(4096).decode()
        header, domain = data.split("|")
        resolved_ip = resolve_ip(header)
        response = f"{header}|{domain}|{resolved_ip}"
        conn.send(response.encode())
    except Exception as e:
        print("Error:", e)
    finally:
        conn.close()
