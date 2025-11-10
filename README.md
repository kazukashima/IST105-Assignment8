# IST105 - Assignment 8: Network Automation Web Application

### Author
Kazutora Hattori  
Student No: CT1011013  

### Overview
This Django web app simulates DHCPv4/DHCPv6 IP assignment using Python and MongoDB on AWS.  
It accepts user input for MAC address and DHCP version, generates an IP address, and stores it in MongoDB.

### Features
- DHCPv4 and DHCPv6 simulation
- MAC address validation
- Bitwise operations for EUI-64 and even/odd check
- Lease time tracking
- MongoDB integration (separate EC2 instance)
- View stored leases via web

### EC2 Architecture
- **WebServer-EC2** (Amazon Linux): runs Django app on port 8000  
- **MongoDB-EC2** (Ubuntu): hosts MongoDB on port 27017  

### How to Run
1. SSH into the WebServer-EC2.
2. Activate virtual environment:
   ```bash
   source venv/bin/activate
