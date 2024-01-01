# Use an official Python runtime as a parent image
FROM mcr.microsoft.com/devcontainers/python:3.10-buster

WORKDIR /workspace

# Install necessary packages including Git and DKMS
RUN apt-get update \
    && apt-get install -y git dkms usbutils \
    && rm -rf /var/lib/apt/lists/*



# Copy the current directory contents into the container at /app
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

RUN git clone https://github.com/medusalix/xone

WORKDIR /workspace/xone

RUN .install.sh --release
