# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the backend application code into the container
COPY . .

# Make port 8080 available to the world outside this container
EXPOSE 8080

# Run uvicorn when the container launches
# The --host 0.0.0.0 is important to make it accessible from outside the container
# The port is set to 8080 to match the docker-compose.yml
CMD ["sh", "-c", "python init_db.py && uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8080}"]
