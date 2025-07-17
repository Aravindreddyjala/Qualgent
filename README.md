# Qualgent AppWright Backend Challenge

A scalable backend service and accompanying CLI (`qgjob`) for submitting and monitoring AppWright test jobs.

## Table of Contents

* [Prerequisites](#prerequisites)
* [Setup](#setup)
* [Usage](#usage)

  * [CLI Commands](#cli-commands)
  * [API Endpoints](#api-endpoints)
* [Architecture](#architecture)
* [Docker Setup](#docker-setup)
* [GitHub Actions](#github-actions)
* [Development Workflow](#development-workflow)
* [Contributing](#contributing)
* [License](#license)

## Prerequisites

* **Git** (v2.20+)
* **Docker** & **Docker Compose** (v2+)
* **Language Runtime** (pick one):

  * Python 3.10+
  * Node.js 16+
  * Go 1.18+
* **Redis** or **PostgreSQL** (if not using Docker Compose)

## Setup

1. **Clone the repository**

   ```bash
   git clone git@github.com:Aravindreddyjala/qualgent-appwright.git
   cd qualgent-appwright
   ```

2. **Switch to feature branch** (e.g. `scaffold-project`):

   ```bash
   git checkout scaffold-project
   ```

3. **Install dependencies**

   * **Python**

     ```bash
     python3 -m venv .venv
     source .venv/bin/activate
     pip install -r requirements.txt
     ```
   * **Node.js**

     ```bash
     npm install
     ```
   * **Go**

     ```bash
     go mod download
     ```

## Usage

### CLI Commands

* **Submit a job**

  ```bash
  qgjob submit \
    --org-id YOUR_ORG \
    --app-version-id YOUR_VERSION \
    --test path/to/test.spec.js \
    [--target emulator|device|browserstack] \
    [--priority N]
  ```

* **Check job status**

  ```bash
  qgjob status --job-id YOUR_JOB_ID
  ```

### API Endpoints

* `POST /jobs`
  Enqueue a new test job.
  **Request Body**:

  ```json
  {
    "org_id": "string",
    "app_version_id": "string",
    "test_path": "string",
    "target": "emulator|device|browserstack",
    "priority": 1
  }
  ```

* `GET /jobs/{job_id}`
  Retrieve job status and logs.
  **Response**:

  ```json
  {
    "job_id": "string",
    "status": "pending|running|passed|failed",
    "attempts": 1,
    "logs": []
  }
  ```

## Architecture

```text
+-----------+       +---------+       +---------+
|   qgjob   | <---> |   API   | <---> |  Queue  |
|  (CLI)    |       | Service |       | (Redis) |
+-----------+       +---------+       +---------+
                              |
                              v
                         +---------+
                         | Worker  |
                         +---------+
```

* **CLI**: Submits and polls jobs.
* **API Service**: Exposes REST endpoints and persists job metadata.
* **Queue**: Holds pending jobs.
* **Worker**: Executes AppWright tests, updates job status, retries on failure.

## Docker Setup

1. Build and start services:

   ```bash
   docker-compose up --build
   ```
2. Services available:

   * API: `http://localhost:8000`
   * Redis: `redis://localhost:6379`
   * CLI: run via `docker exec -it app qgjob ...`

## GitHub Actions

Included workflow triggers on `push` to run a sample AppWright test via the CLI:

```yaml
name: AppWright Test
on: [push]
jobs:
  run-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Install & Submit Job
        run: |
          pip install qgjob
          JOB_ID=$(qgjob submit --org-id=qualgent --app-version-id=$GITHUB_SHA --test tests/smoke.spec.js)
      - name: Poll Status
        run: |
          qgjob status --job-id=$JOB_ID
```

## Development Workflow

1. Create a branch for each feature or bugfix.
2. Commit often with clear messages.
3. Push and open a Pull Request against `main`.
4. Run tests locally before merging.


