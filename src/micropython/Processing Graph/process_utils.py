def decode_as_float(parse_type, data_bytes):
    import struct
    if parse_type == 'uint8':
        return float(data_bytes[0])
    elif parse_type == 'int8':
        return float(int.from_bytes(data_bytes, 'little', signed=True))
    elif parse_type == 'uint16':
        return float(int.from_bytes(data_bytes, 'little'))
    elif parse_type == 'int16':
        return float(int.from_bytes(data_bytes, 'little', signed=True))
    elif parse_type == 'uint32':
        return float(int.from_bytes(data_bytes, 'little'))
    elif parse_type == 'int32':
        return float(int.from_bytes(data_bytes, 'little', signed=True))
    elif parse_type == 'float':
        return struct.unpack('<f', data_bytes)[0]
    elif parse_type == 'double':
        return float(struct.unpack('<d', data_bytes)[0])
    return 0.0

def check_timestamp_sync(inputs, threshold_us):
    if not inputs:
        return False
    ref_ts = inputs[0]['time']
    for inp in inputs[1:]:
        diff = abs(inp['time'] - ref_ts)
        if diff > threshold_us:
            return False
    return True