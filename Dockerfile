# For more information, please refer to https://aka.ms/vscode-docker-python
FROM python:3.10.6-slim as requirements

# Keeps Python from generating .pyc files in the container
# ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
# ENV PYTHONUNBUFFERED=1

# Define temp dir
WORKDIR /temp

# Install poetry
RUN pip install poetry

# Copy poetry config files
COPY ./poetry.lock ./pyproject.toml /temp/

# Export dependencies in requirements.txt
RUN poetry export -o requirements.txt --without-hashes


# Second layer: installing libraries for building psycopg2
FROM python:3.10.6-slim as builder

# Install dependencies
RUN apt-get update; \
    apt-get install -y --no-install-recommends \
    libpq-dev \
    libc-dev \
    gcc;


# Third layer (app)
FROM builder

WORKDIR /marketplace

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

# For reference app folder as package
ENV PYTHONPATH=/marketplace

# Copy requirements from requirements layer
COPY --from=requirements /temp/requirements.txt /marketplace/requirements.txt

# Install requirements
RUN python3 -m pip install --no-cache-dir --upgrade -r requirements.txt

WORKDIR /marketplace/app

# Copy project files
COPY ./app .

# Creates a non-root user with an explicit UID and adds permission to access the /marketplace folder
# For more info, please refer to https://aka.ms/vscode-docker-python-configure-containers
RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser /marketplace
USER appuser

EXPOSE 8001

# Single handler for cluster node in future * NOW REDECLARED IN COMPOSE *
CMD ["python3", "main.py"]
