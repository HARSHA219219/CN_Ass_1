from scapy.all import rdpcap, DNS, DNSQR
import socket
from datetime import datetime
import csv

PCAP_FILE = "7.pcap"  # Replace with your PCAP file
SERVER_IP = "127.0.0.1"
SERVER_PORT = 53535

def generate_header(pkt_time, seq_id: int) -> str:
    """Generate custom header HHMMSSID using packet timestamp and sequence ID."""
    dt = datetime.fromtimestamp(float(pkt_time))    
    header = dt.strftime("%H%M%S") + f"{seq_id:02d}"    # HHMMSS + 2-digit seq
    return header

results = []
seen_domains = set()  # Track unique external domains

# Read PCAP and filter DNS query packets
packets = rdpcap(PCAP_FILE)
dns_queries = [pkt for pkt in packets if DNS in pkt and pkt[DNS].qr == 0]

seq_id = 0  # custom counter starting from 0

for pkt in dns_queries:
    domain = pkt[DNSQR].qname.decode().rstrip(".")
    
    # Skip local network services
    if domain.endswith(".local"):
        continue

    # Skip duplicates
    if domain in seen_domains:
        continue
    seen_domains.add(domain)
    
    # Generate custom header from packet timestamp
    pkt_time = pkt.time  # Timestamp from PCAP
    custom_header = generate_header(pkt_time, seq_id)
    
    # Send to server
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((SERVER_IP, SERVER_PORT))
    message = f"{custom_header}|{domain}"
    client_socket.send(message.encode())
    
    # Receive resolved IP
    response = client_socket.recv(1024).decode()
    header, domain_name, resolved_ip = response.split("|")
    results.append((custom_header, domain_name, resolved_ip))
    client_socket.close()
    
    seq_id += 1  # increment only for valid domains

# Print report
print("\n--- DNS Resolution Report (Unique External Domains) ---")
print("Custom Header | Domain | Resolved IP")
for r in results:
    print(f"{r[0]} | {r[1]} | {r[2]}")

# Save report to CSV
with open("dns_report.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["Custom Header", "Domain", "Resolved IP"])
    writer.writerows(results)

print("\nReport saved as dns_report.csv")
