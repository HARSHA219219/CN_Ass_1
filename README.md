# DNS Resolver using PCAP, Client-Server Model

This project implements a simple DNS resolver using a client-server model in Python.  
The client parses DNS query packets from a `.pcap` file, and the server responds with resolved IPs from a custom IP pool.

1. Download the sample packet capture file `7.pcap` from the following link:  
   [Download 7.pcap](https://drive.google.com/drive/folders/1_LhhdsAA7miN91GcRTKOPZOWroQQNGWV)

2. Clone the repository:
   ```bash
   git clone https://github.com/HARSHA219219/CN_Ass_1.git

3. Install the required library:
   ```bash
   pip install scapy
4. Open a terminal and start the server:
   ```bash
    python server.py
