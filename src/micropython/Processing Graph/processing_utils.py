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
    """
   SensorValue Struct

    Attributes:
        data (bytes): Rohdaten
        timestamp (int): Zeitstempel
    """
    def __init__(self, data: bytes, timestamp: int):
        self.data = data
        self.timestamp = timestamp


def decode_sensor_data(sample: SensorData, parse_type: ParseType):
    """
        Decodes raw sensor data into the  numerical val.

        Interprets the bytes from `SensorData.data` according to the given
        `parse_type` and returns the value as int or float.

        Args:
            sample (SensorData): The sensor data object containing the raw bytes (`data`) and timestamp.
            parse_type (ParseType): The data type of the raw bytes. Supported types:
                - ParseType.UINT8
                - ParseType.INT8
                - ParseType.UINT16
                - ParseType.INT16
                - ParseType.UINT32
                - ParseType.INT32
                - ParseType.FLOAT
                - ParseType.DOUBLE

        Returns:
            int, float: Decoded numerical value of the sensor.

        Raises:
            ValueError: If an unsupported `parse_type` is entered.
    """
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
        raise ValueError(f"Unsupported parse_type {parse_type}")

def check_timestamp_sync(inputs, in_ports: int, threshold_us: int):
    """
        Check if multiple sensor samples are synchronized within a given threshold.

        Compares the timestamps of multiple sensor inputs and returns True
        if all timestamps are within `threshold_us` of the first sample's timestamp.

        Args:
            inputs (list of SensorData): List of sensor data objects
            in_ports (int): Number of inputs.
            threshold_us (int): Maximum allowed difference in time.

        Returns:
            bool: True if all timestamps are within the threshold, False otherwise.
        """
    ref_ts = inputs[0].timestamp
    for i in range(1, in_ports):
        ts = inputs[i].timestamp
        diff = abs(ts - ref_ts)
        if diff > threshold_us:
            return False
    return True
