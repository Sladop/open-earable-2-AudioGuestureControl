from sensor_processing_stage import SensorProcessingStage
from processing_utils import decode_sensor_data, check_timestamp_sync

class AndStage(SensorProcessingStage):
    def __init__(self, in_ports, sync_timestamps=False, threshold_us=0):
        super().__init__(in_ports)
        self.sync_timestamps = sync_timestamps
        self.threshold_us = threshold_us

    def process(self, inputs, output):
        if self.sync_timestamps:
            if not check_timestamp_sync(inputs, self.get_in_ports(), self.threshold_us):
                return -1

        # AND
        out = 0xFF
        for inp in inputs:
            val = decode_sensor_data(inp, "uint8")  # decode_sensor_data muss uint8 unterstützen
            out &= val

        output.clear()
        output.update(inputs[0])

        output["data"] = out.to_bytes(1, "little", signed=False)
        output["size"] = 1

        return 0
