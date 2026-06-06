# ENGR 1 - Malware Defense Final Project

### by Leo, Natalie, Kimberly

> ⚠️ **For educational use only.** This project is a toy malware framework
> built for the ACM Cyber E1 course. Do not deploy outside of designated lab VMs.

## Overview
 
This project is a client/payload malware framework. The **client** is a
command-and-control (C2) CLI run by the attacker on `e1-attack`. The
**payload** (`server.py`) is a TCP listener deployed on the victim (`e1-target`)
that receives and executes commands sent from the client.

## Project Structure

```
project-skeleton/
├── client/                        # Run this on e1-attack
│   ├── app.py                     # CLI entry point
│   └── cybersploit_client/
│       ├── commands/              # One file per CLI command — add yours here!
│       ├── actions/               # Optional: reusable attack logic
│       └── util/                  # Optional: shared helpers
└── payload/
    └── server.py                  # Deployed on e1-target, listens on :5050
```

## Implemented Features
 
| Category | Feature | Command |
|---|---|---|
| Exploitation | Shellshock (CVE-2014-6271) | `shellshock <target>` |
| Exploitation | Ghostcat (CVE-2020-1938) | `exploit <target>` |
| Enumeration | UDP port scan | `port_scan <target>` |
| Privilege Escalation | Writable crontab folder | *(via privesc)* |
| Privilege Escalation | Writable /etc/passwd | *(via privesc)* |
| Persistence | Alias hijacking | `alias_hijack <target>` |
| Persistence | Systemd service | `persistence <target>` |
| C2 | Ransomware (file encryption) | `ransomware <target> <dir>` |
| C2 | Decrypt files | `decrypt <target> <dir>` |
| C2 | Remote camera capture | `camera_capture <target>` |
| Kill Switch | GitHub-triggered self-destruct | *(automatic)* |

---

