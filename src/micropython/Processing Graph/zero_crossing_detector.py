from sensor_processing_stage import SensorProcessingStage
from processing_utils import SensorData, decode_sensor_data
import struct

class ZeroCrossingDetectorStage(SensorProcessingStage):
    """
    Detects zero crossings in a single-channel input.
    Emits an event only when the signal crosses zero.
    Output = -1 for falling, +1 for rising
    """

    def __init__(self, parse_type):
        super().__init__(1)
        self.parse_type = parse_type
        self.is_initialized = False
        self.last_scalar = 0.0

    def process(self, inputs):
        if not inputs or inputs[0] is None:
            return None

        in_sd = inputs[0]
        cur = decode_sensor_data(in_sd, self.parse_type)

        #init
        if not self.is_initialized:
            self.last_scalar = cur
            self.is_initialized = True
            return None

        # Check zero crossing
        crossing = 0
        if self.last_scalar < 0 and cur > 0:
            crossing = 1  # rising through zero
        elif self.last_scalar > 0 and cur < 0:
            crossing = -1  # falling through zero

        self.last_scalar = cur

        if crossing == 0:
            return None  # no crossing

        out_data = struct.pack("<b", crossing)
        output = SensorData(data=out_data, timestamp=in_sd.timestamp)
        return output
