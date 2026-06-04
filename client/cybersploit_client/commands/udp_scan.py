"""Scan common UDP ports on a target host."""

import socket

COMMON_UDP_PORTS = {
    53: "DNS",
    67: "DHCP",
    69: "TFTP",
    123: "NTP",
    137: "NetBIOS",
    161: "SNMP",
    500: "ISAKMP/VPN",
    514: "Syslog",
}


class command:
    def do_command(self, args):
        target = args.strip()

        if target == "":
            print("Usage: udp_scan <target_ip_or_hostname>")
            print("Example: udp_scan e1-target.local")
            print("Scans common UDP ports like DNS, DHCP, TFTP, NTP, SNMP, VPN, and Syslog.")
            return

        print(f"Starting UDP scan on {target}")

        for port, service in COMMON_UDP_PORTS.items():
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.settimeout(2)

            try:
                sock.sendto(b"hello", (target, port))
                sock.recvfrom(1024)
                print(f"[OPEN] UDP {port} ({service}) - received response")

            except socket.timeout:
                print(f"[OPEN|FILTERED] UDP {port} ({service}) - no response")

            except ConnectionRefusedError:
                print(f"[CLOSED] UDP {port} ({service})")

            except Exception as e:
                print(f"[ERROR] UDP {port} ({service}) - {e}")

            finally:
                sock.close()