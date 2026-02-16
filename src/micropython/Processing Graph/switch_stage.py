from sensor_processing_stage import SensorProcessingStage
from processing_utils import SensorData, decode_sensor_data
import struct

class SwitchStage(SensorProcessingStage):
    """
    Switch stage with low/high thresholds.
    Emits a new sample only when the state changes.
    """

    def __init__(self, parse_type, low_threshold: float, high_threshold: float):
        super().__init__(1)
        self.parse_type = parse_type
        self.low_threshold = low_threshold
        self.high_threshold = high_threshold
        self.current_state = 0

    def process(self, inputs):
        if not inputs or inputs[0] is None:
            return None

        in_sd = inputs[0]
        cur = decode_sensor_data(in_sd, self.parse_type)

        new_state = self.current_state
        if cur < self.low_threshold:
            new_state = 0
        elif cur > self.high_threshold:
            new_state = 1

        if new_state == self.current_state:
            return None  # no state change

        self.current_state = new_state

        out_data = in_sd.data + struct.pack("<B", self.current_state)
        output = SensorData(data=out_data, timestamp=in_sd.timestamp)
        return output
