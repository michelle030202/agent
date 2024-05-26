"""Net share module"""

from dataclasses import dataclass
from .base import Task, TaskParameters


@dataclass
class NetShareParameters(TaskParameters):
    """Parameters for the NetShareTask.

    Attributes:
        action (str): The action to perform (GET, ADD, DELETE).
        name (str): The name of the share to manage.
    """
    action: str
    name: str


class NetShareTask(Task):
    """Task to manage network shares with actions like GET, ADD, and DELETE."""

    async def run(self, parameters: NetShareParameters) -> str:
        """Runs the network share management task.

        Args:
            parameters (NetShareParameters): The parameters for the network share task.

        Returns:
            str: The result of the network share action.
        """
        action = parameters.action.upper()
        if not parameters.name:
            return "Invalid parameters: Name is required"

        action_methods = {
            "GET": self.get_share,
            "ADD": self.add_share,
            "DELETE": self.delete_share,
        }

        if action not in action_methods:
            return "Invalid action"

        return action_methods[action](parameters.name)

    @staticmethod
    def get_share(name: str) -> str:
        """Handles the GET action for a network share.

        Args:
            name (str): The name of the share to get.

        Returns:
            str: The result of the GET action.
        """
        # Placeholder for actual get share implementation
        return f"Getting share {name}"

    @staticmethod
    def add_share(name: str) -> str:
        """Handles the ADD action for a network share.

        Args:
            name (str): The name of the share to add.

        Returns:
            str: The result of the ADD action.
        """
        # Placeholder for actual add share implementation
        return f"Adding share {name}"

    @staticmethod
    def delete_share(name: str) -> str:
        """Handles the DELETE action for a network share.

        Args:
            name (str): The name of the share to delete.

        Returns:
            str: The result of the DELETE action.
        """
        # Placeholder for actual delete share implementation
        return f"Deleting share {name}"
