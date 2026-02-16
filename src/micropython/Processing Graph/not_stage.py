from sensor_processing_stage import SensorProcessingStage
from processing_utils import decode_sensor_data, SensorData, ParseType, StageProcessingError
import copy
import struct


class NotStage(SensorProcessingStage):
    """
    Logical NOT of a single input.

    - Input 0 = value to invert
    - Output = 1 if input == 0, else 0
    """

    def __init__(self):
        super().__init__(1)

    def process(self, inputs):
        if not inputs or inputs[0] is None:
            raise StageProcessingError("Input is None")

        in_val = decode_sensor_data(inputs[0], ParseType.UINT8)


        out_val = 1 if in_val == 0 else 0


        output = copy.deepcopy(inputs[0])

        output.data = struct.pack("<B", out_val)
        output.size = 1

        return output
