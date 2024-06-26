# syntax=docker/dockerfile:1

# Comments are provided throughout this file to help you get started.
# If you need more help, visit the Dockerfile reference guide at
# https://docs.docker.com/go/dockerfile-reference/

# Want to help us make this template better? Share your feedback here: https://forms.gle/ybq9Krt8jtBL3iCk7

ARG PYTHON_VERSION=3.9.6
FROM python:${PYTHON_VERSION}-slim as base

# Prevents Python from writing pyc files.
ENV PYTHONDONTWRITEBYTECODE=1

# Keeps Python from buffering stdout and stderr to avoid situations where
# the application crashes without emitting any logs due to buffering.
ENV PYTHONUNBUFFERED=1

# Set environment variables
ENV MPLCONFIGDIR=/tmp/matplotlib

# Create a directory for the images and set permissions
RUN mkdir -p /app/images && chmod 777 /app/images

# Create a directory for the uploads and set permissions
RUN mkdir -p /app/uploads && chmod 777 /app/uploads

WORKDIR /app

# Create a non-privileged user that the app will run under.
# See https://docs.docker.com/go/dockerfile-user-best-practices/
ARG UID=10001
RUN adduser \
    --disabled-password \
    --gecos "" \
    --home "/nonexistent" \
    --shell "/sbin/nologin" \
    --no-create-home \
    --uid "${UID}" \
    appuser

# Download dependencies as a separate step to take advantage of Docker's caching.
# Leverage a cache mount to /root/.cache/pip to speed up subsequent builds.
# Leverage a bind mount to requirements.txt to avoid having to copy them into
# into this layer.
RUN --mount=type=cache,target=/root/.cache/pip \
    --mount=type=bind,source=requirements.txt,target=requirements.txt \
    python -m pip install -r requirements.txt

# Install SQLite
RUN apt-get update && apt-get install -y sqlite3

# Switch to the non-privileged user to run the application.
USER appuser

# Check if the data.db file exists, and if not, create it
# RUN test -f data.db || sqlite3 data.db ""

# Copy the pre-created SQLite database file into the container.
COPY data.db /app/data.db

# Create a directory for the uploads and set permissions
COPY uploads /app/uploads

# Copy the source code into the container.
COPY . .

# Ensure that the directory has the necessary permissions for the appuser
USER root
RUN chown -R appuser:appuser /app
USER appuser

# Expose the port that the application listens on.
EXPOSE 5000

# Define environment variable
ENV FLASK_APP=app.py

# Run app.py when the container launches
CMD ["gunicorn", "-b", "0.0.0.0:5001", "app:app"]
# CMD ["flask", "run", "--help", "--host", "0.0.0.0", "--port", "5001"]
