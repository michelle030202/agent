""""Registry module"""
import os
import json
from functools import wraps
from typing import Optional, Any
from dataclasses import dataclass
from .base import Task, TaskParameters

REGISTRY_FILE = "mock_registry.json"


def ensure_registry_file_exists(func):
    """Decorator to ensure the registry file exists before performing operations.

    Args:
        func (Callable): The function to wrap.

    Returns:
        Callable: The wrapped function.
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        if not os.path.exists(REGISTRY_FILE):
            with open(REGISTRY_FILE, 'w') as file:
                json.dump({}, file)
        return func(*args, **kwargs)

    return wrapper


@dataclass
class RegistryParameters(TaskParameters):
    """Parameters for the RegistryTask.

    Attributes:
        action (str): The action to perform (GET, SET, DELETE).
        key (str): The registry key to act on.
        value (Optional[Any]): The value to set for the registry key (for SET action).
    """
    action: str
    key: str
    value: Optional[Any] = None


class RegistryTask(Task):
    """Task to perform registry operations."""

    async def run(self, parameters: RegistryParameters) -> str:
        """Runs the registry task.

        Args:
            parameters (RegistryParameters): The parameters for the registry task.

        Returns:
            str: The result of the registry operation.
        """
        action = parameters.action.upper()
        key = parameters.key
        value = parameters.value

        if not action or not key:
            return "Invalid parameters: Action and Key are required"

        actions = {
            "GET": self.handle_get,
            "SET": self.handle_set,
            "DELETE": self.handle_delete,
        }

        if action in actions:
            return actions[action](key, value)

        return "Invalid action"

    @staticmethod
    @ensure_registry_file_exists
    def read_registry() -> dict:
        """Reads the registry from the file.

        Returns:
            dict: The contents of the registry.
        """
        with open(REGISTRY_FILE, 'r') as file:
            return json.load(file)

    @staticmethod
    @ensure_registry_file_exists
    def write_registry(registry: dict) -> None:
        """Writes the registry to the file.

        Args:
            registry (dict): The registry to write.
        """
        with open(REGISTRY_FILE, 'w') as file:
            json.dump(registry, file, indent=4)

    @classmethod
    def handle_get(cls, key: str) -> str:
        """Handles the GET action for the registry task.

        Args:
            key (str): The registry key to get.
            value (Optional[Any]): Not used for GET action.

        Returns:
            str: The value of the registry key or an error message.
        """
        registry = cls.read_registry()
        return registry.get(key, "Registry key not found")

    @classmethod
    def handle_set(cls, key: str, value: Any) -> str:
        """Handles the SET action for the registry task.

        Args:
            key (str): The registry key to set.
            value (Any): The value to set for the registry key.

        Returns:
            str: "Success" if the operation was successful, or an error message.
        """
        if value is None:
            return "Invalid parameters: Value is required for SET action"
        registry = cls.read_registry()
        registry[key] = value
        cls.write_registry(registry)
        return "Success"

    @classmethod
    def handle_delete(cls, key: str) -> str:
        """Handles the DELETE action for the registry task.

        Args:
            key (str): The registry key to delete.
            value (Optional[Any]): Not used for DELETE action.

        Returns:
            str: "Success" if the operation was successful, or an error message.
        """
        registry = cls.read_registry()
        if key in registry:
            del registry[key]
            cls.write_registry(registry)
            return "Success"
        return "Registry key not found"
