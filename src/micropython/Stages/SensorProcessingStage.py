class Node:
    def __init__(self, name: str, in_port_count: int = 1):
        self.name = name
        self.in_port_count = in_port_count

    def process(self, inputs):
        """
        inputs: Liste von Input-Daten für diese Node
        Muss in Unterklassen implementiert werden.
        """
        raise NotImplementedError("process()nicht implementiert!")

    def get_in_ports(self):
        return self.in_port_count
