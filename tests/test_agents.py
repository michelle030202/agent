import pytest
import asyncio


@pytest.mark.asyncio
async def test_agents(agent1, agent2):
    """Test running tasks on two agents in parallel."""

    task1 = ("dns_query", {"domain": "example.com"})
    task2 = ("http_request", {"method": "GET", "domain": "google.com", "port": 80, "path": "/"})

    result1 = await agent1.run_task(task1[0], task1[1])
    result2 = await agent2.run_task(task2[0], task2[1])

    assert isinstance(result1, str)
    assert "<title>Google</title>" in result2
