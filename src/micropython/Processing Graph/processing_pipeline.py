from collections import deque
from sensor_processing_stage import SensorProcessingStage
from sensor_source_stage import SensorSourceStage

class Edge:
    def __init__(self, src, dst, dst_port):
        self.src = src
        self.dst = dst
        self.dst_port = dst_port

class PipelineNode:
    def __init__(self, name: str, stage: SensorProcessingStage):
        self.name = name
        self.stage = stage
        self.inputs = []
        self.outputs = []
        self.output = None
        self.has_output = False

class ProcessingPipeline:
    def __init__(self):
        self.stages = []
        self.source_map = {}  # sensorID - list of node indces

    def add_source(self, name: str, source: SensorSourceStage):
        idx = len(self.stages)
        self.stages.append(PipelineNode(name, source))
        self.source_map.setdefault(source.get_sensor_id(), []).append(idx)

    def add_stage(self, name: str, stage: SensorProcessingStage):
        self.stages.append(PipelineNode(name, stage))

    def connect(self, src, dst, dst_port=0):
        self.stages[dst].inputs.append(Edge(src, dst, dst_port))
        self.stages[src].outputs.append(Edge(src, dst, dst_port))

    def connect_by_name(self, src_name, dst_name, dst_port=0):
        src_idx = dst_idx = None
        for i, node in enumerate(self.stages):
            if node.name == src_name:
                src_idx = i
            if node.name == dst_name:
                dst_idx = i
        if src_idx is None or dst_idx is None:
            raise ValueError("Source or Destination node not found")
        self.connect(src_idx, dst_idx, dst_port)

    def inject(self, sample):
        sensor_id = sample['id']
        if sensor_id not in self.source_map:
            return -1

        for src_idx in self.source_map[sensor_id]:
            node = self.stages[src_idx]
            node.output = sample
            node.has_output = True
            self.run_from(src_idx)

    def run_from(self, start_idx):
        queue = deque()
        queue.extend(e.dst for e in self.stages[start_idx].outputs)

        while queue:
            i = queue.popleft()
            node = self.stages[i]
            in_count = node.stage.get_in_ports()

            if in_count == 0:
                if node.has_output:
                    queue.extend(e.dst for e in node.outputs)
                continue

            if len(node.inputs) != in_count:
                continue

            inputs_ready = True
            input_data = [None] * in_count
            for p, e in enumerate(node.inputs):
                if not self.stages[e.src].has_output:
                    inputs_ready = False
                    break
                input_data[p] = self.stages[e.src].output

            if not inputs_ready:
                continue

            out = node.stage.process(input_data)
            node.output = out
            node.has_output = True

            queue.extend(e.dst for e in node.outputs)

    def get_output(self, node_index):
        return self.stages[node_index].output
