"""
Task Runner

Usage:
  main.py run_single <task_type> <params>
  main.py run_multiple <tasks_params>
  main.py (-h | --help)
  main.py --version

Options:
  -h --help     Show this screen.
  --version     Show version.

Arguments:
  task_type     The type of task to run.
  params        Task parameters in JSON format.
  tasks_params  JSON array of task types and parameters.

Examples:
  main.py run_single dns_query '{"domain": "example.com"}'
  main.py run_single http_request '{"method": "GET", "domain": "example.com", "port": 80, "path": "/"}'
  main.py run_single port_scan '{"domain": "example.com", "from_port": 1, "to_port": 1024}'
  main.py run_single net_share '{"action": "GET", "name": "SharedFolder"}'
  main.py run_single http_server '{"port": 8080, "page_uri": "/test", "data": "Hello, world!"}'
  main.py run_single registry_task '{"action": "GET", "key": "HKEY_LOCAL_MACHINE\\Software\\Example"}'
  main.py run_single process_tree_task '{"param1": "1234"}'
  main.py run_multiple '[{"task_type": "dns_query", "params": {"domain": "example.com"}}, {"task_type": "http_request", "params": {"method": "GET", "domain": "example.com", "port": 80, "path": "/"}}]'

Task Descriptions:
  dns_query           Perform a DNS query for the specified domain.
  http_request        Make an HTTP request with specified method, domain, port, and path.
  port_scan           Scan ports on the specified domain within the given port range.
  net_share           Manage network shares with actions like GET, ADD, and DELETE.
  http_server         Start an HTTP server on the specified port, serving data at the given URI.
  registry_task       Perform registry operations like GET, SET, and DELETE on specified keys.
  process_tree_task   Retrieve the process tree starting from a given PID.
"""

import json
import asyncio
from docopt import docopt
from task_manager import task_manager


async def parse_and_run(task_type: str = None, params: str = None, tasks_params: str = None) -> None:
    """
    Parses JSON parameters and runs tasks.

    Args:
        task_type (str, optional): The type of task to run.
        params (str, optional): JSON string of parameters for a single task.
        tasks_params (str, optional): JSON string of multiple tasks and their parameters.

    Returns:
        None
    """
    if tasks_params:
        tasks = json.loads(tasks_params)
        task_list = [(task['task_type'], task['params']) for task in tasks]
        results = await task_manager.run_task(task_list)
        print("Tasks results:", results)
    else:
        parsed_params = json.loads(params)
        result = await task_manager.run_task(task_type, parsed_params)
        print("Task result:", result)


async def main_async(arguments: dict) -> None:
    """
    Main async function to execute tasks based on command-line arguments.

    Args:
        arguments (dict): Parsed command-line arguments.

    Returns:
        None
    """
    action_map = {
        'run_single': lambda args: parse_and_run(task_type=args['<task_type>'], params=args['<params>']),
        'run_multiple': lambda args: parse_and_run(tasks_params=args['<tasks_params>']),
    }

    for action, func in action_map.items():
        if arguments[action]:
            await func(arguments)


if __name__ == "__main__":
    arguments = docopt(__doc__, version='Task Runner 1.0')
    asyncio.run(main_async(arguments))
