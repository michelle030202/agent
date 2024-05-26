"""http request module"""
import aiohttp
from .base import Task, TaskParameters


class HTTPRequestParameters(TaskParameters):
    """Parameters for the HTTPRequestTask.

    Attributes:
        method (str): The HTTP method to use (e.g., GET, POST).
        domain (str): The domain to send the request to.
        port (int): The port to use for the HTTP request.
        path (str): The path to send the request to.
    """
    method: str
    domain: str
    port: int
    path: str


class HTTPRequestTask(Task):
    """Task to perform an HTTP request to a given domain."""

    async def run(self, parameters: HTTPRequestParameters) -> str:
        """Runs the HTTP request task.

        Args:
            parameters (HTTPRequestParameters): The parameters for the HTTP request task.

        Returns:
            str: The response text from the HTTP request.
        """
        url = f"http://{parameters.domain}:{parameters.port}{parameters.path}"
        try:
            async with aiohttp.ClientSession() as session:
                async with session.request(parameters.method, url) as response:
                    response_text = await response.text()
                    return response_text
        except aiohttp.ClientError as e:
            return str(e)
