from sensor_processing_stage import SensorProcessingStage
from processing_utils import decode_sensor_data, check_timestamp_sync, SensorData, ParseType, StageProcessingError


class IfStage(SensorProcessingStage):
    """
        Outputs the second input if the first input (condition) is non-zero.
    """
    def __init__(self, sync_channels: bool = False, threshold_us: int = 0):
        super().__init__(2)
        self.sync_channels = sync_channels
        self.threshold_us = threshold_us

    def process(self, inputs):
        condition_sample, value_sample = inputs

        if condition_sample is None or value_sample is None:
            raise StageProcessingError("One of the inputs is None")

        if self.sync_channels:
            if not check_timestamp_sync(inputs, 2, self.threshold_us):
                raise StageProcessingError("Timestamp sync failed")

        condition = decode_sensor_data(condition_sample, ParseType.UINT8)

        if condition != 0:
            return SensorData(
                data=value_sample.data,
                timestamp=value_sample.timestamp
            )

        return None
