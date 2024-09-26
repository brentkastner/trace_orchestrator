[![Python Tests](https://github.com/brentkastner/trace_orchestrator/actions/workflows/python-app.yml/badge.svg?branch=main)](https://github.com/brentkastner/trace_orchestrator/actions/workflows/python-app.yml)
# Trace Orchestrator Python Flask SQLite App Docker Container

This Docker container sets up a Python Flask application with SQLite as the database. It provides a basic API to orchestrate Usetrace traces and tags (groups of traces). While Usetrace does not advocate for trace ordering and trace dependencies there are times where things need to be run in a specific order. This orchestrator is light-weight and uses local SQLLITE to store the traces and their order and track execution.

The following diagram illustrates the architecture. This can be run anywhere but recommend a containerized approach. It will drop rigth into a hosting service like Render with no changes to code required.

![Trace Orchestration](/orchestration.png)

## Requirements

- Docker
- Docker Compose

## Setup Instructions

1. Clone the repository:

   ```bash
   git clone <repository_url>
   cd trace_orchestrator
   ```
2. Run the tests:

   ```
   python -m pytest
   ```

3. Initialize the database

   ```
   python src/init_db.py
   ```

4. Build and run the Docker container using Docker Compose:

   ```bash
   docker-compose up -d
   ```

5. Access the application:

   Open a web browser and navigate to `http://localhost:3000` to access the  application.

6. Environment Variables

   If you pass an environment variable HOSTNAME to the container the container will automatically use this variable. This is important because the HOSTNAME is used to construct the WEBHOOK url that Usetrace uses to indicate it has finished running one of the traces.

7. Sample CI Integration command

   From your CI create json file in the format below and name it something like test_order.json. Then load the tests into the run using the following sample command which POSTs the json file to the orchestrator. You should receive a hash back which will identify the unique run of all the traces and tags you've listed. You can also watch the status on the /getRuns GET endpoint

   ```
    curl -X POST -H "Content-Type: application/json" -d @test_order.json https://<HOSTNAME>/scheduleRun/wKFv06_08lboHBo7l5NJIA
   ```

## Endpoints

   /scheduleRun/<client_id>

   /getRuns

   /webhook/<run_hash>

## Notes

- The Docker Compose configuration uses version 3.7.
- The Python Flask application is built on top of the Python 3.9 Docker image.
- The SQLite database file is stored in the `src` directory as `database.db`.
- The Flask application code is located in the `src` directory.
- The `requirements.txt` file specifies the required Python packages and their versions:
  - Flask==2.3.2
  - Gunicorn==20.1.0
  - requests
- The application uses Gunicorn as the HTTP server to run the Flask application.
- The Docker container exposes port 3000, which is mapped to port 3000 on the host machine.
- The Docker container performs a health check every 30 seconds to ensure the Flask application is accessible.

## Kicking Off an Ordered Run

Send this basic JSON document to /scheduleRun/<clienthash> as JSON and POST - there is a seed client hash in the database at wKFv06_08lboHBo7l5NJIA

```
/scheduleRun/wKFv06_08lboHBo7l5NJIA/
```
insert secret key if required by the project /scheduleRun/wKFv06_08lboHBo7l5NJIA?key= 

```

{
    "projectID": "YXlFJTqD6gAZF_7K9TE7VmYiYVazGMc6",
    "requiredCapabilities": [
        {"browserName": "chrome"},
        {"browserName": "firefox"}
    ],
    "runOrder": [
        "tag:goon",
        "ZuBmU-WNsQAXLYQJ6mVVjjEjvUD3ZC83",
        "ZQMxtishNAAWrGeLXggk2jVbU83oGHCu",
        "Ytbfm470DAAZDKpA6DWtb7176gAiQ7XB"
    ]
}

```