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


    # Return the list of found open ports


    # Returns a fake list
    # Remove once implemented
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
    print(f"{'port':<10} {'service':<10}")
    print(f"{'----':<10} {'-------':<10}")

    for port in open_ports:
        try:  
            service = socket.getservbyport(port, "tcp")
        except:
            # If the port doesn't have a standard name, use 'unknown'
            service = "unknown"
        
        # 4. Print the row with aligned columns
        print(f"{port:<10} {service:<10}")

    # This will allow the python file to run even if you haven't put any code in this function yet
    pass

class port_scan(Command): # Call the class anything you'd like
    """
    Scanning to find open ports
    """

    def do_command(self, lines: str):
        lines = lines.split(" ")
        port1 = int(lines[1])
        port2 = int(lines[2])
        port_range = (port1, port2)
        open_ports = scan_ip(lines[0], port_range)
        pretty_print_scan(open_ports)

if __name__ == "__main__":
    import sys

    target = sys.argv[1]
    port1 = int(sys.argv[2])
    port2 = int(sys.argv[3])

    port_range = (port1, port2)

    open_ports = scan_ip(target, port_range)
    pretty_print_scan(open_ports)

command = port_scan

    
