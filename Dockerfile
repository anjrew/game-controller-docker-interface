# Start from a Python base image
FROM python:3.8

# Install pygame and gym (or any other dependencies)
RUN pip install pygame gym

# Copy your application code to the container (assuming your application is in the app/ directory)
COPY main.py /app/

# Set the working directory
WORKDIR /app

# Run your application
CMD ["python", "main.py"]
