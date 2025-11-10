from django.shortcuts import render
from pymongo import MongoClient
from datetime import datetime
import random
import re

MONGO_HOST = "172.31.85.238"
MONGO_PORT = 27017
DB_NAME = "dhcpdb"
COLLECTION_NAME = "leases"

assigned_ipv4 = {}
assigned_ipv6 = {}

def generate_ipv4():
    return f"192.168.1.{random.randint(2, 254)}"

def generate_ipv6(mac):
    parts = mac.split(":")
    eui64 = parts[0:3] + ["ff", "fe"] + parts[3:]
    first_byte = int(eui64[0], 16) ^ 0x02
    eui64[0] = f"{first_byte:02x}"
    ipv6_suffix = ":".join(["".join(eui64[i:i+2]) for i in range(0, len(eui64), 2)])
    return f"2001:db8::{ipv6_suffix}"

def validate_mac(mac):
    pattern = r"^([0-9A-Fa-f]{2}:){5}[0-9A-Fa-f]{2}$"
    return re.match(pattern, mac)

def home(request):
    assigned_ip = None
    lease_time = "3600 seconds"

    if request.method == "POST":
        mac = request.POST.get("mac_address")
        dhcp_version = request.POST.get("dhcp_version")

        if not validate_mac(mac):
            return render(request, "network/home.html", {"error": "Invalid MAC address format!"})

        if dhcp_version == "DHCPv4":
            if mac in assigned_ipv4:
                assigned_ip = assigned_ipv4[mac]
            else:
                assigned_ip = generate_ipv4()
                assigned_ipv4[mac] = assigned_ip
        elif dhcp_version == "DHCPv6":
            if mac in assigned_ipv6:
                assigned_ip = assigned_ipv6[mac]
            else:
                assigned_ip = generate_ipv6(mac)
                assigned_ipv6[mac] = assigned_ip

        try:
            client = MongoClient(MONGO_HOST, MONGO_PORT)
            db = client[DB_NAME]
            collection = db[COLLECTION_NAME]
            record = {
                "mac_address": mac,
                "dhcp_version": dhcp_version,
                "assigned_ip": assigned_ip,
                "lease_time": lease_time,
                "timestamp": datetime.utcnow().isoformat(),
            }
            collection.insert_one(record)
        except Exception as e:
            return render(request, "network/home.html", {"error": f"MongoDB connection failed: {e}"})

        return render(request, "network/home.html", {
            "mac": mac,
            "dhcp_version": dhcp_version,
            "assigned_ip": assigned_ip,
            "lease_time": lease_time,
        })

    return render(request, "network/home.html")

