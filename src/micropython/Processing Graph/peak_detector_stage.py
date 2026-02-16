from sensor_processing_stage import SensorProcessingStage
from processing_utils import decode_sensor_data, SensorData, ParseType, StageProcessingError
import struct
import math

class PeakDetectorStage(SensorProcessingStage):
    """
    Detects peaks and troughs in a single-channel signal.

    Produces output only when a peak or trough is finalized.
    Output SensorData contains:
        [original bytes] + [int8 peak_sign] + [prominence encoded as parse_type]
    """

    RISE, FLAT, FALL = 1, 0, -1

    def __init__(self, parse_type: ParseType, eps: float = 0.0, max_open: int = 16):
        super().__init__(1)
        self.parse_type = parse_type
        self.eps = eps

        self.last_data = None
        self.last_dx = math.nan
        self.last_dir = self.FLAT

        self.last_valley = math.nan
        self.have_valley = False
        self.last_peak = math.nan
        self.have_peak = False

        self.pstack = []  # peaks
        self.tstack = []  # troughs
        self.max_open = max(max_open, 2)

    def deriv_dir(self, dx: float):
        if dx > self.eps:
            return self.RISE
        elif dx < -self.eps:
            return self.FALL
        return self.FLAT

    def encode_prominence(self, v: float):
        t = self.parse_type
        if t == ParseType.INT8:
            s = int(max(-128, min(127, round(v))))
            return struct.pack("<b", s)
        elif t == ParseType.UINT8:
            s = int(max(0, min(255, round(v))))
            return struct.pack("<B", s)
        elif t == ParseType.INT16:
            s = int(max(-32768, min(32767, round(v))))
            return struct.pack("<h", s)
        elif t == ParseType.UINT16:
            s = int(max(0, min(65535, round(v))))
            return struct.pack("<H", s)
        elif t == ParseType.INT32:
            s = int(max(-2147483648, min(2147483647, round(v))))
            return struct.pack("<i", s)
        elif t == ParseType.UINT32:
            s = int(max(0, min(4294967295, round(v))))
            return struct.pack("<I", s)
        elif t == ParseType.FLOAT:
            return struct.pack("<f", v)
        elif t == ParseType.DOUBLE:
            return struct.pack("<d", v)
        else:
            return struct.pack("<f", v)

    def process(self, inputs):
        if not inputs or inputs[0] is None:
            raise StageProcessingError("Input missing")

        in_sd = inputs[0]
        curr = decode_sensor_data(in_sd, self.parse_type)

        if self.last_data is None:
            self.last_data = in_sd
            self.last_dx = math.nan
            self.last_dir = self.FLAT
            return None

        prev = decode_sensor_data(self.last_data, self.parse_type)
        dx = curr - prev
        dir_now = self.deriv_dir(dx)
        prev_dir = self.last_dir

        self.last_data = in_sd
        self.last_dx = dx
        self.last_dir = dir_now

        output = None

        # check for trough (FALL->RISE)
        if prev_dir == self.FALL and dir_now == self.RISE:
            left_base = self.last_peak if self.have_peak else prev
            prominence = left_base - curr
            output = SensorData(
                data=in_sd.data + struct.pack("<b", -1) + self.encode_prominence(prominence),
                timestamp=in_sd.timestamp
            )
            self.tstack.append(curr)
            self.have_valley = True
            self.last_valley = prev
            self.have_peak = False

        # check for peak (RISE->FALL)
        elif prev_dir == self.RISE and dir_now == self.FALL:
            left_base = self.last_valley if self.have_valley else prev
            prominence = curr - left_base
            output = SensorData(
                data=in_sd.data + struct.pack("<b", 1) + self.encode_prominence(prominence),
                timestamp=in_sd.timestamp
            )
            self.pstack.append(curr)
            self.have_peak = True
            self.last_peak = prev
            self.have_valley = False

        return output
