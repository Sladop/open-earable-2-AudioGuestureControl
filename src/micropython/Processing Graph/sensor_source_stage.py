from sensor_processing_stage import SensorProcessingStage

class SensorSourceStage(SensorProcessingStage):
    """Source stage for a sensor."""

    def __init__(self, sensor_id: int):
        super().__init__(0)
        self.sensor_id = sensor_id

    def process(self, inputs):
        raise NotImplementedError("Source stage should not process data.")

    def get_sensor_id(self):
        return self.sensor_id
