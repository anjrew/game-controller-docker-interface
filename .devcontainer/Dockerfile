# Use an official Python runtime as a parent image
FROM python:3.8

WORKDIR /workspace

# Copy the current directory contents into the container at /app
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
