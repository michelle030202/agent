"""http_server module"""
from aiohttp import web
from .base import Task, TaskParameters


class HTTPServerParameters(TaskParameters):
    """Parameters for the HTTPServerTask.

    Attributes:
        port (int): The port number on which the server will run.
        page_uri (str): The URI path that the server will respond to.
        data (str): The data to be served at the specified URI.
    """
    port: int
    page_uri: str
    data: str


class HTTPServerTask(Task):
    """Task to start an HTTP server on a given port and serve data at a specified URI."""

    async def run(self, parameters: HTTPServerParameters) -> str:
        """Runs the HTTP server task.

        Args:
            parameters (HTTPServerParameters): The parameters for the HTTP server task.

        Returns:
            str: A message indicating that the server has started.
        """
        server = HTTPServerInstance(parameters.port, parameters.page_uri, parameters.data)
        await server.start()
        return f"Server started on port {parameters.port}"


class HTTPServerInstance:
    """Instance of an HTTP server."""

    def __init__(self, port: int, page_uri: str, data: str):
        """Initializes the HTTP server instance.

        Args:
            port (int): The port number on which the server will run.
            page_uri (str): The URI path that the server will respond to.
            data (str): The data to be served at the specified URI.
        """
        self.port = port
        self.page_uri = page_uri
        self.data = data

    async def start(self) -> None:
        """Starts the HTTP server."""
        app = web.Application()
        app.router.add_get(self.page_uri, self.handle_request)
        runner = web.AppRunner(app)
        await runner.setup()
        site = web.TCPSite(runner, '0.0.0.0', self.port)
        await site.start()

    async def handle_request(self, request: web.Request) -> web.Response:
        """Handles incoming HTTP requests.

        Args:
            request (web.Request): The incoming request.

        Returns:
            web.Response: The HTTP response.
        """
        if request.path == self.page_uri:
            return web.Response(text=self.data, content_type='text/html')
