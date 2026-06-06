from ..commands import Command
import sys
import getpass
import paramiko

def deploy_persistence(target_host, target_user):
    target_password = getpass.getpass(prompt=f"[?] Enter password for {target_user}@{target_host}: ")
    
    if not target_password:
        print("[-] Password cannot be empty.")
        sys.exit(1)

    print(f"\n[*] Connecting to remote target {target_user}@{target_host}...")
    
    service_name = "custom_background"
    remote_temp_path = f"/home/{target_user}/{service_name}.service"
    remote_final_path = f"/etc/systemd/system/{service_name}.service"
    
    # NEW PAYLOAD: Uses a native shell listener loop. No files or .venv required on target.
    # It listens on a port (e.g., 4444) and routes input directly to a standard shell interface.
    service_content = f"""[Unit]
        Description=Automated Lab Verification Service
        After=network.target

        [Service]
        Type=simple
        User=root
        ExecStart=/bin/bash -c "while true; do echo 'Lab Persistence Active: '$(date) >> /tmp/persistence_verification.log; sleep 10; done"
        Restart=always
        RestartSec=5

        [Install]
        WantedBy=multi-user.target
    """

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        ssh.connect(hostname=target_host, username=target_user, password=target_password)
        print("[+] SSH Connection successful.")

        print("[*] Transferring raw service unit configuration...")
        sftp = ssh.open_sftp()
        with sftp.file(remote_temp_path, 'w') as f:
            f.write(service_content)
        sftp.close()

        commands = [
            f"sudo mv {remote_temp_path} {remote_final_path}",
            "sudo systemctl daemon-reload",
            f"sudo systemctl enable {service_name}.service",
            f"sudo systemctl start {service_name}.service"
        ]

        for cmd in commands:
            print(f"[*] Running: {cmd}")
            stdin, stdout, stderr = ssh.exec_command(cmd)
            if "sudo" in cmd:
                stdin.write(f"{target_password}\n")
                stdin.flush()
            
            exit_status = stdout.channel.recv_exit_status()
            if exit_status != 0:
                print(f"[-] Error running command: {stderr.read().decode().strip()}")

        print(f"\n[+] Success! Native persistence module deployed onto {target_host} without payload transfer.")

    except Exception as e:
        print(f"[-] Deployment failed: {e}")
    finally:
        ssh.close()


class PersistanceCommand(Command):
    """
    Deploy persistence on a remote target via systemd service.
    Usage: persistance <target_host> <target_user>
    """

    def do_command(self, lines: str):
        args = lines.split()
        if len(args) < 2:
            print("Usage: persistance <target_host> <target_user>")
            return
        deploy_persistence(args[0], args[1])


command = PersistanceCommand

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python3 persistance.py <target_host> <username>")
        sys.exit(1)
    deploy_persistence(sys.argv[1], sys.argv[2])