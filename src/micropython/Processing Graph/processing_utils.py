import struct

from enum import Enum

class ParseType(Enum):
    UINT8 = 1
    INT8 = 2
    UINT16 = 3
    INT16 = 4
    UINT32 = 5
    INT32 = 6
    FLOAT = 7
    DOUBLE = 8

class SensorData:

    def __init__(self, data: bytes, timestamp: int):
        self.data = data
        self.timestamp = timestamp
        self.size = len(data)


def decode_sensor_data(sample: SensorData, parse_type: ParseType):
    data = sample.data
    if parse_type == ParseType.UINT8:
        return data[0]
    elif parse_type == ParseType.INT8:
        return struct.unpack("<b", data)[0]
    elif parse_type == ParseType.UINT16:
        return struct.unpack("<H", data)[0]
    elif parse_type == ParseType.INT16:
        return struct.unpack("<h", data)[0]
    elif parse_type == ParseType.UINT32:
        return struct.unpack("<I", data)[0]
    elif parse_type == ParseType.INT32:
        return struct.unpack("<i", data)[0]
    elif parse_type == ParseType.FLOAT:
        return struct.unpack("<f", data)[0]
    elif parse_type == ParseType.DOUBLE:
        return struct.unpack("<d", data)[0]
    else:
        raise ValueError("Unsupported parse type")

def decode_as_float(parse_type: ParseType, data: bytes):
    if parse_type == ParseType.UINT8:
        return float(data[0])
    elif parse_type == ParseType.INT8:
        return float(struct.unpack("<b", data)[0])
    elif parse_type == ParseType.UINT16:
        return float(struct.unpack("<H", data)[0])
    elif parse_type == ParseType.INT16:
        return float(struct.unpack("<h", data)[0])
    elif parse_type == ParseType.UINT32:
        return float(struct.unpack("<I", data)[0])
    elif parse_type == ParseType.INT32:
        return float(struct.unpack("<i", data)[0])
    elif parse_type == ParseType.FLOAT:
        return struct.unpack("<f", data)[0]
    elif parse_type == ParseType.DOUBLE:
        return struct.unpack("<d", data)[0]
    else:
        return 0.0

def check_timestamp_sync(inputs, in_ports: int, threshold_us: int):
    ref_ts = inputs[0].timestamp
    for i in range(1, in_ports):
        ts = inputs[i].timestamp
        diff = abs(ts - ref_ts)
        if diff > threshold_us:
            return False
    return True
