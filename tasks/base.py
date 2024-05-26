"""Base module for all tasks."""
from pydantic import BaseModel
from typing import Optional, Any
from abc import ABC, abstractmethod


class TaskParameters(BaseModel):
    """General TaskParameters class for generic tasks.

    This class serves as a base for defining parameters for various tasks, leveraging Pydantic for
    validation and serialization.

    Attributes:
        param1 (Optional[Any]): An optional generic parameter.
        param2 (Optional[Any]): Another optional generic parameter.
    """
    param1: Optional[Any] = None
    param2: Optional[Any] = None


class Task(ABC):
    """Base Task class.

    This class serves as an abstract base class for all tasks, enforcing a consistent interface.
    """

    @abstractmethod
    async def run(self, parameters: TaskParameters) -> Any:
        """Abstract method to run the task.

        Args:
            parameters (TaskParameters): The parameters required to run the task.

        Returns:
            Any: The result of the task.
        """
        pass
