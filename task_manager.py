import asyncio
from typing import Dict, Type, Any, Tuple, List, Union
from tasks import (
    DNSTask, DNSQueryParameters,
    HTTPRequestTask, HTTPRequestParameters,
    PortScanTask, PortScanParameters,
    NetShareTask, NetShareParameters,
    HTTPServerTask, HTTPServerParameters,
    RegistryTask, RegistryParameters,
    ProcessTreeTask, ProcessTreeParameters
)
from tasks.base import Task, TaskParameters


class TaskManager:
    """Manages and executes tasks, either singly or in parallel."""

    def __init__(self):
        """
        Initializes the TaskManager with a dictionary of available tasks.
        """
        self._tasks: Dict[str, Tuple[Type[Task], Type[TaskParameters]]] = {
            "dns_query": (DNSTask, DNSQueryParameters),
            "http_request": (HTTPRequestTask, HTTPRequestParameters),
            "port_scan": (PortScanTask, PortScanParameters),
            "net_share": (NetShareTask, NetShareParameters),
            "http_server": (HTTPServerTask, HTTPServerParameters),
            "registry_task": (RegistryTask, RegistryParameters),
            "process_tree_task": (ProcessTreeTask, ProcessTreeParameters),  # Ensure this class is properly defined
        }

    @property
    def tasks(self) -> Dict[str, Tuple[Type[Task], Type[TaskParameters]]]:
        """
        Returns the dictionary of registered tasks.

        Returns:
            Dict[str, Tuple[Type[Task], Type[TaskParameters]]]: A dictionary mapping task names to their classes and parameter classes.
        """
        return self._tasks

    async def run_task(self, task_type: Union[str, List[Tuple[str, Dict[str, Any]]]], parameters: Dict[str, Any] = None) -> Any:
        """
        Runs a single task or multiple tasks in parallel.

        Args:
            task_type (Union[str, List[Tuple[str, Dict[str, Any]]]]): A single task type or a list of tasks with their parameters.
            parameters (Dict[str, Any], optional): Parameters for a single task. Defaults to None.

        Returns:
            Any: Result(s) of the task(s).
        """
        if isinstance(task_type, list):
            # Run multiple tasks in parallel
            return await self._run_multiple_tasks(task_type)
        else:
            # Run a single task
            return await self._run_single_task(task_type, parameters)

    async def _run_single_task(self, task_type: str, parameters: Dict[str, Any]) -> Any:
        """
        Runs a single task.

        Args:
            task_type (str): The type of task to run.
            parameters (Dict[str, Any]): The parameters for the task.

        Returns:
            Any: Result of the task.

        Raises:
            ValueError: If the task type is not found.
        """
        task_info = self.tasks.get(task_type)
        if not task_info:
            raise ValueError(f"Task '{task_type}' not found")

        task_class, parameter_class = task_info
        task = task_class()
        task_parameters = self.create_parameters(parameter_class, parameters)
        return await task.run(task_parameters)

    async def _run_multiple_tasks(self, tasks: List[Tuple[str, Dict[str, Any]]]) -> Tuple[Any, ...]:
        """
        Runs multiple tasks in parallel.

        Args:
            tasks (List[Tuple[str, Dict[str, Any]]]): A list of tuples with task types and their parameters.

        Returns:
            Tuple[Any, ...]: Results of the tasks.
        """
        coroutines = [self._run_single_task(task_type, params) for task_type, params in tasks]
        return await asyncio.gather(*coroutines)

    @staticmethod
    def create_parameters(parameter_class: Type[TaskParameters], parameters: Dict[str, Any]) -> TaskParameters:
        """
        Creates parameters for a task.

        Args:
            parameter_class (Type[TaskParameters]): The parameter class of the task.
            parameters (Dict[str, Any]): The parameters for the task.

        Returns:
            TaskParameters: An instance of TaskParameters.
        """
        return parameter_class(**parameters)


task_manager = TaskManager()
