# Start from a Python base image
FROM python:3.8

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file first (for better cache utilization)
COPY requirements.txt /app/

# Install dependencies, including Uvicorn
RUN pip install --no-cache-dir -r requirements.txt

# Copy your application code to the container
COPY . /app/

# Specify the command to run on container start
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
