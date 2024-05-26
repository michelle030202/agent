# Task Management System

This project is a task management system that allows for the execution of various tasks asynchronously. 
The system is designed to be extendable and includes tasks such as DNS queries, HTTP requests, port scanning, 
process tree retrieval, registry operations, and network share management.

## Project Set Up

1. Install the dependencies:
    ```sh
   pip install -r requirements.txt

2. To run a single task, use the main.py script:
    ```sh
   python main.py run_single <task_type> <params>
   
3. To run multiple tasks in parallel:
    ```sh
   python main.py run_multiple '[{"task_type": "dns_query", "params": {"domain": "google.com"}}, 
   {"task_type": "http_request", "params": {"method": "GET", "domain": "google.com", "port": 80, "path": "/"}}]'
   
4. To run the tests, use pytest/tests + name of the test

