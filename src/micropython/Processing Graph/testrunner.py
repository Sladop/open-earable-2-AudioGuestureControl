import csv
import time
from sensor_processing_consumer import (
    set_processing_pipeline,
    sensor_processing_consumer_init,
    message_queue
)
from processing_pipeline import ProcessingPipeline
from sensor_source_stage import SensorSourceStage

from and_stage import AndStage
from not_stage import NotStage
from if_stage import IfStage
from adding_stage import AddingStage
from multiply_stage import MultiplyStage
from biquad_filter_stage import BiquadFilterStage
from component_extractor_stage import ComponentExtractorStage
from peak_detector_stage import PeakDetectorStage
from switch_stage import SwitchStage
from zero_crossing_detector import ZeroCrossingDetectorStage


def load_csv_as_raw_bytes(file_path):
    messages = []
    with open(file_path, newline="") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            raw_bytes = bytes.fromhex(row["value_bytes_hex"])
            msg = {
                "timestamp": int(row["timestamp"]),
                "id": int(row["sensor_id"]),
                "sensor_type": row["sensor_type"],
                "data": raw_bytes  # Rohbytes, wie vom Sensor
            }
            messages.append(msg)
    return messages


def test_stage(stage_class, messages):
    """Testet eine Stage einzeln mit Rohdaten"""
    stage_name = stage_class.__name__
    print(f"\n=== Testing {stage_name} ===")

    pipeline = ProcessingPipeline()
    stage_instance = stage_class()
    in_ports = stage_instance.get_in_ports()

    sensor_ids = sorted({msg["id"] for msg in messages})[:in_ports]
    for sensor_id in sensor_ids:
        pipeline.add_source(f"source{sensor_id}", SensorSourceStage(sensor_id))

    pipeline.add_stage("test_stage", stage_instance)

    for sensor_id in sensor_ids:
        pipeline.connect_by_name(f"source{sensor_id}", "test_stage")

    set_processing_pipeline(f"pipeline_{stage_name}", pipeline)

    sensor_processing_consumer_init()

    for msg in messages:
        if msg["id"] in sensor_ids:
            message_queue.put({
                "timestamp": msg["timestamp"],
                "id": msg["id"],
                "sensor_type": msg["sensor_type"],
                "data": msg["data"]
            })

    time.sleep(1)

if __name__ == "__main__":
    messages = load_csv_as_raw_bytes("sampleData.csv")

    test_stage(AndStage, messages)
    test_stage(NotStage, messages)
    test_stage(IfStage, messages)
    test_stage(AddingStage, messages)
    test_stage(MultiplyStage, messages)
    test_stage(BiquadFilterStage, messages)
    test_stage(ComponentExtractorStage, messages)
    test_stage(PeakDetectorStage, messages)
    test_stage(SwitchStage, messages)
    test_stage(ZeroCrossingDetectorStage, messages)
