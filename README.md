# Trace Orchestrator Python Flask SQLite App Docker Container

This Docker container sets up a Python Flask application with SQLite as the database. It provides a basic web application for managing user names.

## Requirements

- Docker
- Docker Compose

## Setup Instructions

1. Clone the repository:

   ```bash
   git clone <repository_url>
   cd trace_orchestrator
   ```

2. Build and run the Docker container using Docker Compose:

   ```bash
   docker-compose up -d
   ```

3. Access the application:

   Open a web browser and navigate to `http://localhost:3000` to access the  application.

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


```

{
    "runOrder": [
        "ZuBmU-WNsQAXLYQJ6mVVjjEjvUD3ZC83",
        "ZQMxtishNAAWrGeLXggk2jVbU83oGHCu",
        "Ytbfm470DAAZDKpA6DWtb7176gAiQ7XB"
    ]
}

```