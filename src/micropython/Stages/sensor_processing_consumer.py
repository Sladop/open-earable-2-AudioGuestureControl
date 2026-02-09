class SensorProcessingConsumer:
    def __init__(self):
        self._pipelines: dict[str, "Pipeline"] = {}

    def set_pipeline(self, name: str, pipeline):
        """Pipeline registrieren"""
        self._pipelines[name] = pipeline

    def get_pipeline(self, name: str):
        """Pipeline abrufen"""
        return self._pipelines.get(name)

    def remove_pipeline(self, name: str):
        """Pipeline entfernen"""
        self._pipelines.pop(name, None)

    def inject_message(self, msg):
        """
        msg ist ein Sensor-Datenobjekt oder Dictionary
        Leitet msg an alle registrierten Pipelines weiter.
        """
        for pipeline in self._pipelines.values():
            pipeline.inject(msg)

