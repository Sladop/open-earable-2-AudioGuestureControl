import struct
from sensor_processing_stage import SensorProcessingStage
from processing_utils import decode_sensor_data, SensorData, ParseType


class BiQuadFilterStage(SensorProcessingStage):
    """
    Applies a biquad filter to a single sensor input and outputs float.

    Can be constructed with:
    - with a filter object
    - directly from coefficients
    """

    def __init__(self, input_type: ParseType, filter_obj):
        super().__init__(1)
        self.parse_type = input_type
        self.filter = filter_obj

    @staticmethod
    def from_coefficients(input_type: ParseType, stages: int, coefficients, filter_class):
        """
        Create BiQuadFilter from coefficients.
        """
        filter_obj = filter_class(stages)
        filter_obj.set_coefficients(coefficients, stages)
        return BiQuadFilterStage(input_type, filter_obj)

    def process(self, inputs):
        sample = inputs[0]

        x = float(decode_sensor_data(sample, self.parse_type))

        buf = [x]
        self.filter.apply(buf, 1)
        y = buf[0]

        return SensorData(
            data=struct.pack("<f", y),
            timestamp=sample.timestamp
        )
