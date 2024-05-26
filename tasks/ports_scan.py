import asyncio
from typing import List
from functools import lru_cache
from .base import Task, TaskParameters


class PortScanParameters(TaskParameters):
    """Parameters for the PortScanTask.

    Attributes:
        domain (str): The domain to scan for open ports.
        from_port (int): The starting port number to scan.
        to_port (int): The ending port number to scan.
    """

    domain: str
    from_port: int
    to_port: int


class PortScanTask(Task):
    """Task to perform a port scan on a given domain."""

    async def run(self, parameters: PortScanParameters) -> List[int]:
        """Runs the port scan task.

        Args:
            parameters (PortScanParameters): The parameters for the port scan task.

        Returns:
            List[int]: A list of open ports.
        """
        open_ports = []
        coroutines = [self._scan_port(parameters.domain, port) for port in
                      range(parameters.from_port, parameters.to_port + 1)]
        results = await asyncio.gather(*coroutines)
        for port, is_open in zip(range(parameters.from_port, parameters.to_port + 1), results):
            if is_open:
                open_ports.append(port)
        return open_ports

    @staticmethod
    @lru_cache(maxsize=None)
    async def _scan_port(domain: str, port: int) -> bool:
        """Scans a single port.

        Args:
            domain (str): The domain to scan.
            port (int): The port to scan.

        Returns:
            bool: True if the port is open, False otherwise.
        """
        try:
            conn = asyncio.open_connection(domain, port)
            reader, writer = await asyncio.wait_for(conn, timeout=1)
            writer.close()
            await writer.wait_closed()
            return True
        except (asyncio.TimeoutError, ConnectionRefusedError) as e:
            return False
