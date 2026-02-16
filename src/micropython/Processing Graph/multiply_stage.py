import struct
from sensor_processing_stage import SensorProcessingStage
from processing_utils import decode_sensor_data, check_timestamp_sync, SensorData, ParseType, StageProcessingError


class MultiplyStage(SensorProcessingStage):
    """
    Multiplies all inputs together and returns the result as a SensorData object.

    Raises:
        StageProcessingError: If timestamp sync fails or inputs are invalid.
    """

    def __init__(self, in_ports: int, input_type: ParseType, sync_channels: bool = True, threshold_us: int = 0):
        super().__init__(in_ports)
        self.parse_type = input_type
        self.sync_channels = sync_channels
        self.threshold_us = threshold_us

    def process(self, inputs):
        if self.sync_channels:
            if not check_timestamp_sync(inputs, self.get_in_ports(), self.threshold_us):
                raise StageProcessingError("Timestamp sync failed")

        # decode all inputs to numeric values
        values = [decode_sensor_data(s, self.parse_type) for s in inputs]

        product = 1
        if self.parse_type in (ParseType.FLOAT, ParseType.DOUBLE):
            product = 1.0

        for v in values:
            product *= v

        # pack result as bytes depending on type
        if self.parse_type in (ParseType.UINT8, ParseType.INT8):
            data_bytes = struct.pack("<b" if self.parse_type == ParseType.INT8 else "<B", product)
        elif self.parse_type in (ParseType.UINT16, ParseType.INT16):
            data_bytes = struct.pack("<h" if self.parse_type == ParseType.INT16 else "<H", product)
        elif self.parse_type in (ParseType.UINT32, ParseType.INT32):
            data_bytes = struct.pack("<i" if self.parse_type == ParseType.INT32 else "<I", product)
        elif self.parse_type == ParseType.FLOAT:
            data_bytes = struct.pack("<f", product)
        elif self.parse_type == ParseType.DOUBLE:
            data_bytes = struct.pack("<d", product)
        else:
            raise StageProcessingError(f"Unsupported ParseType: {self.parse_type}")

        return SensorData(
            data=data_bytes,
            timestamp=inputs[0].timestamp
        )
