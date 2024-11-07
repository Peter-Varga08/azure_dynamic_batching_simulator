# Azure Dynamic Batching Simulator

BERT model endpoint simulator for testing dynamic batching during inference time with Azure ML Studio endpoint-like syntactics.

## Requirements

- Python 3.10
- Poetry

## Development
###  Installation

1. Clone the repository:

    ```sh
    git clone git@github.com:Peter-Varga08/azure_dynamic_batching_simulator.git
    cd azure_dynamic_batching_simulator
    ```

2. Option 1: Install the dependencies in local virtual environment
    ```sh
   poetry install
   ```

   Option 2: Build docker image and install dependencies in docker container (recommended)
    ```sh
    make build
    ```

### Running the Application
1. Option 1: in local environment

    ```sh
   poetry shell # spawn a shell within the virtual environment
   make server  # start the FastAPI application
   ```

   Option 2: in docker container (recommended)

   <u>NOTE</u>: This will also start the `locust` service for load-testing.
    ```sh
    make up
    ```

2. The application will be available at `http://0.0.0.0:8000`.

## Endpoints

- `GET /` - Returns a "Hello World" message.
- `POST /score` - Accepts a JSON payload and returns a model prediction.


## Load-testing
The application can be load-tested against various batching configurations using `locust` by running the following command:
1. Option 1: Local environment

    ```sh
    make load-test
    ```
   Option 2: in docker container (recommended)

    ```sh
    # nothing to do, running the application with `make up` spins up the locust service automatically
    ```
2. The locust web interface will be available at `http://0.0.0.0:8089`
3. Enter the URL of the FastAPI application (`http://0.0.0.0:8000`) and the number of users to simulate.

## Pre-commit Hooks

This project uses pre-commit hooks to ensure code quality. To set up the hooks, run:

```sh
poetry run pre-commit install
