# Use a specific Python version
FROM python:3.9

# Set the working directory
WORKDIR /app

# Install necessary packages
RUN apt-get update && \
    apt-get install -y netcat-openbsd gcc libpq-dev && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Copy requirements.txt and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Set the environment variable for Django settings
ENV PYTHONUNBUFFERED 1

# Command to run the application
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
