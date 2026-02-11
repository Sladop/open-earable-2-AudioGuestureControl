import threading
import queue

from processing_pipeline import ProcessingPipeline

pipelines = {}
message_queue = queue.Queue()

def set_processing_pipeline(name: str, pipeline: ProcessingPipeline):
    pipelines[name] = pipeline

def get_processing_pipeline(name: str):
    return pipelines.get(name)

def remove_processing_pipeline(name: str):
    pipelines.pop(name, None)

def processing_thread():
    while True:
        msg = message_queue.get()
        for pipeline in pipelines.values():
            pipeline.inject(msg)

def sensor_processing_consumer_init():
    t = threading.Thread(target=processing_thread, daemon=True)
    t.start()
