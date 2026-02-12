from abc import ABC, abstractmethod

class SensorProcessingStage(ABC):
    """Base class for all processing stages."""

    def __init__(self, in_ports: int):
        self.in_ports = in_ports

    @abstractmethod
    def process(self, inputs):
        pass

    def get_in_ports(self):
        return self.in_ports