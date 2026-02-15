from sensor_processing_stage import SensorProcessingStage
from processing_utils import decode_sensor_data, check_timestamp_sync, ParseType

import struct

class AddingStage(SensorProcessingStage):
    def __init__(self, in_ports, input_type: ParseType, sync_channels=False, threshold_us=0):
        super().__init__(in_ports)
        self.parse_type = input_type
        self.sync_channels = sync_channels
        self.threshold_us = threshold_us

    def process(self, inputs, output):
        # timestamp sync prüfen
        if self.sync_channels:
            if not check_timestamp_sync(inputs, self.get_in_ports(), self.threshold_us):
                return -1


        output.clear()
        output.update(inputs[0])

        # summe inpus
        total = sum(decode_sensor_data(inp, self.parse_type) for inp in inputs)

        if self.parse_type == ParseType.PARSE_TYPE_UINT8:
            output["data"] = total.to_bytes(1, "little", signed=False)
            output["size"] = 1
        elif self.parse_type == ParseType.PARSE_TYPE_INT8:
            output["data"] = total.to_bytes(1, "little", signed=True)
            output["size"] = 1
        elif self.parse_type == ParseType.PARSE_TYPE_UINT16:
            output["data"] = total.to_bytes(2, "little", signed=False)
            output["size"] = 2
        elif self.parse_type == ParseType.INT16:
            output["data"] = total.to_bytes(2, "little", signed=True)
            output["size"] = 2
        elif self.parse_type == ParseType.PARSE_TYPE_UINT32:
            output["data"] = total.to_bytes(4, "little", signed=False)
            output["size"] = 4
        elif self.parse_type == ParseType.INT32:
            output["data"] = total.to_bytes(4, "little", signed=True)
            output["size"] = 4
        elif self.parse_type == ParseType.PARSE_TYPE_FLOAT:
            output["data"] = struct.pack("<f", float(total))
            output["size"] = 4
        elif self.parse_type == ParseType.PARSE_TYPE_DOUBLE:
            output["data"] = struct.pack("<d", float(total))
            output["size"] = 8
        else:
            return -2  # unsupported type

        return 0
