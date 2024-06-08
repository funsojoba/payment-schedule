FROM python:3.8.0-slim as builder

# Set the working directory
WORKDIR /app

# Environment variable to ensure output is sent directly to terminal (stdout)
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

# Copy the requirements file
COPY ./requirements.txt .

# Update package list and install necessary system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    python-dev \
    libpq-dev \
    postgresql-client \
    postgresql \
    postgresql-contrib \
    postgis \
    wget \
    wkhtmltopdf \
    gdal-bin \
    libgdal-dev \
    libgeos-dev \
    --no-install-recommends && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . .
