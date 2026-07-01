from spark.session import SparkManager


class SparkManagerService:

    def __init__(self):
        self.manager = SparkManager()

    def get_spark(self):
        return self.manager.get_spark()

    def stop(self):
        self.manager.stop()