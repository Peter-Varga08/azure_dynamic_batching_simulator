# Variables
IMAGE_NAME = dynamic_batching
CONTAINER_NAME = dynamic_batching
DOCKERFILE = Dockerfile
REQUIREMENTS_FILE = requirements.txt

# Default target
.PHONY: all
all: help

# Build the Docker image
.PHONY: build
build:
	docker compose build --no-cache

# Run the Docker container
.PHONY: run
run:
	docker run --name $(CONTAINER_NAME) -p 8000:8000 $(IMAGE_NAME)

.PHONY: up
up:
	docker compose up

.PHONY: server
server:
	export PYTHONPATH="src" && uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload

# Stop the Docker container
.PHONY: stop
stop:
	docker stop $(CONTAINER_NAME)

# Remove the Docker container
.PHONY: rm
rm:
	docker rm $(CONTAINER_NAME)

# Run pre-commit hooks
.PHONY: pre-commit
pre-commit:
	pre-commit run --all-files

# Create requirements file from the current environment
.PHONY: requirements
requirements:
	poetry export -f $(REQUIREMENTS_FILE) --output $(REQUIREMENTS_FILE) --without-hashes

# Clean up Docker images and containers
.PHONY: cleanup
cleanup:
	docker rm -f $(CONTAINER_NAME) || true
	docker rmi $(IMAGE_NAME) || true

.PHONY: load-test
load-test:
	locust -f tests/locustfile.py

# Display help
.PHONY: help
help:
	@echo "Makefile commands:"
	@echo "  build       - Build the Docker image"
	@echo "  run         - Run the Docker container"
	@echo "  stop        - Stop the Docker container"
	@echo "  rm          - Remove the Docker container"
	@echo "  pre-commit  - Run pre-commit hooks"
	@echo "  requirements - Create a requirements.txt file from the current environment"
	@echo "  cleanup     - Remove the Docker container and image"
	@echo "  help        - Display this help message"
