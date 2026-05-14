from client.cybersploit_client.commands import send_data

from ..commands import Command # Required
import socket
def scan_ip(target: str, port_range: tuple[int, int]) -> list[int]:

    # Create a list to store open ports

    port_list = []

    # Iterate over the range of ports
        # For each port:
        # - Create a sockhoet
        # - Attempt to connect to the ip and port

    for i in range(port_range[0], port_range[1] + 1):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        results = s.connect_ex((target, i))

        if (results == 0):
            port_list.append(i)
            
        s.close()
   
    return port_list


def pretty_print_scan(open_ports: list[int]) -> None:
    """Takes in a list of ports (like from the output of scan_ip), and outputs a user-friendly table to read"""
    # DO NOT call the scan ip function in here - only use the list of ports provided in the function argument

    
    # Now, let's use python formatting to make a nice little table, kinda like nmap!
    # Up to you for the details, but your table should contain the port that is open,
    # and the name of the service that is running on it. It should look "nice", i.e. columns
    # should be lined up vertically when printed out, and include a table header
    # Python format strings may come in handy for this!
    # For the service on the port, you might find the getservbyport function helpful.
    # print(f"{'port':<10} {'service':<10}")
    # print(f"{'----':<10} {'-------':<10}")
    print(f"{'port':<10} {'service':<10}")
    print(f"{'----':<10} {'-------':<10}")

    for port in open_ports:
        try:
            service = socket.getservbyport(port, "tcp")
        except:
            service = "unknown"

        print(f"{port:<10} {service:<10}")
        

def pretty_print_service_scan(target: str, open_ports: list[int]) -> None:
    print(f"{'port':<10} {'service':<15} {'version':<40}")
    print(f"{'----':<10} {'-------':<15} {'-------':<40}")

    for port in open_ports:
        try:
            service = socket.getservbyport(port, "tcp")
        except:
            service = "unknown"

        version = scan_service(target, port)
        print(f"{port:<10} {service:<15} {version:<40}")


class port_scan(Command): # Call the class anything you'd like
    """
    Scanning to find open ports
    """

    def do_command(self, lines: str):
        line = lines.split(" ")
        port1 = int(line[1])
        port2 = int(line[2])
        port_range = (port1, port2)
        open_ports = scan_ip(line[0], port_range)
        pretty_print_scan(open_ports)
        for port in open_ports:
            trigger_string = f"{line[0]} {port} whoami" 
            send_data(trigger_string)


command = port_scan

