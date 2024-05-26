import psutil
from .base import Task, TaskParameters


class ProcessTreeParameters(TaskParameters):
    """Parameters for the ProcessTreeTask.

    Attributes:
        pid (int): The process ID to start the tree from.
    """
    pid: int


class ProcessTreeTask(Task):
    """Task to retrieve the process tree starting from a given PID."""

    async def run(self, parameters: ProcessTreeParameters) -> dict:
        """Runs the process tree task.

        Args:
            parameters (ProcessTreeParameters): The parameters for the process tree task.

        Returns:
            dict: The process tree starting from the given PID.
        """
        pid = parameters.pid
        if not psutil.pid_exists(pid):
            return f"PID {pid} does not exist"

        process = psutil.Process(pid)
        root_process = self._find_root_process(process)
        return self._get_process_tree(root_process)

    @staticmethod
    def _find_root_process(process: psutil.Process) -> psutil.Process:
        """Finds the root process in the ancestry of the given process.

        Args:
            process (psutil.Process): The process to start the search from.

        Returns:
            psutil.Process: The root process.
        """
        current = process
        while current.ppid() != 0:
            try:
                current = psutil.Process(current.ppid())
            except psutil.NoSuchProcess:
                break
        return current

    @staticmethod
    def _get_process_tree(process: psutil.Process) -> dict:
        """Builds the process tree starting from the given process.

        Args:
            process (psutil.Process): The process to start the tree from.

        Returns:
            dict: The process tree structure.
        """
        tree = {
            "pid": process.pid,
            "name": process.name(),
            "cmdline": process.cmdline(),
            "children": []
        }
        try:
            for child in process.children(recursive=False):
                child_tree = ProcessTreeTask._get_process_tree(child)
                if child_tree:
                    tree["children"].append(child_tree)
        except psutil.NoSuchProcess:
            pass
        return tree
