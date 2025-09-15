# CN_Assignment_1

This assignment implements a simple DNS resolver using a client-server model in Python.  
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
5. Open another terminal and run the client:
   ```bash
   python client.py
6. You should be able to see these resolutions:

Custom Header	Domain	Resolved IP
18041600	wikipedia.org	192.168.1.6
18041601	reddit.com	192.168.1.7
18041602	apple.com	192.168.1.8
18041603	twitter.com	192.168.1.9
18041604	yahoo.com	192.168.1.10
18041605	linkedin.com	192.168.1.6
