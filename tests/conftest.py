import pytest
from task_manager import TaskManager
from tasks.dns_query import DNSTask, DNSQueryParameters
from tasks.http_request import HTTPRequestTask, HTTPRequestParameters


@pytest.fixture
def agent1():
    manager = TaskManager()
    manager._tasks["dns_query"] = (DNSTask, DNSQueryParameters)
    return manager


@pytest.fixture
def agent2():
    manager = TaskManager()
    manager._tasks["http_request"] = (HTTPRequestTask, HTTPRequestParameters)
    return manager