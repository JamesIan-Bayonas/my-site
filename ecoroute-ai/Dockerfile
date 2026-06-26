# Use a lightweight, stable official Python runtime environment
FROM python:3.12-slim

# Set system environment optimizations
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Establish our processing container directory
WORKDIR /app

# Install basic system layer dependencies needed for scientific libraries
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy over package configuration metrics
COPY requirements.txt /app/

# Install dependencies globally inside our isolated virtual slice
RUN pip install --no-cache-dir -r requirements.txt

# Copy over the entire rest of our application system directory
COPY . /app/

# Expose our Asynchronous Webhook API port to the host system network
EXPOSE 8000

# By default, run our headless API gateway background daemon
CMD ["python", "api_gateway.py"]