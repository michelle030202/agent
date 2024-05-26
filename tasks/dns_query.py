"""dns_query module"""
import socket
import asyncio
from .base import Task, TaskParameters


class DNSQueryParameters(TaskParameters):
    """Parameters for the DNSTask.

    Attributes:
        domain (str): The domain to perform a DNS query on.
    """
    domain: str


class DNSTask(Task):
    """Task to perform a DNS query on a given domain."""

    async def run(self, parameters: DNSQueryParameters) -> str:
        """Runs the DNS query task.

        Args:
            parameters (DNSQueryParameters): The parameters for the DNS query task.

        Returns:
            str: The IP address of the domain.
        """
        return await self.query_dns(parameters.domain)

    @staticmethod
    async def query_dns(domain: str) -> str:
        """Queries the DNS for the given domain.

        Args:
            domain (str): The domain to query.

        Returns:
            str: The IP address of the domain.
        """
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, socket.gethostbyname, domain)
