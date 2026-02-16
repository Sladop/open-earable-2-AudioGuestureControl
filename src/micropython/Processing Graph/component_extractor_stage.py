from sensor_processing_stage import SensorProcessingStage
from processing_utils import SensorData, ParseType, parseTypeSizes


class ComponentExtractorStage(SensorProcessingStage):
    """
    Extracts a single component from a sensor data input at a given offset.
    """

    def __init__(self, offset: int, parse_type: ParseType):
        super().__init__(1)
        self.offset = offset
        self.parse_type = parse_type

    def process(self, inputs):
        sample = inputs[0]

        elem_size = parseTypeSizes[self.parse_type]

        extracted = sample.data[self.offset:self.offset + elem_size]

        return SensorData(
            data=extracted,
            timestamp=sample.timestamp
        )
