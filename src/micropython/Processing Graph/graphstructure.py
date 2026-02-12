class Node:
    def __init__(self, name, stage):
        self.name = name
        self.stage = stage
        self.inputs = []
        self.outputs = []
        self.output = None
        self.has_output = False
