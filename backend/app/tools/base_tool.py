from abc import ABC
from abc import abstractmethod


class BaseTool(ABC):
    """
    Base class for every backend tool.

    Every tool should implement execute().
    """

    @abstractmethod
    def execute(
        self,
        database: str,
        target: str,
    ):
        pass