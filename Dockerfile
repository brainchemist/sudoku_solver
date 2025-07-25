# Step 1: Use an official Python runtime as a parent image
FROM python:3.10-slim

# Step 2: Install system dependencies for Pillow (like zlib, gcc, and other build dependencies)
RUN apt-get update && apt-get install -y \
    libjpeg-dev \
    libz-dev \
    libfreetype6-dev \
    zlib1g-dev \
    gcc \
    g++ \
    make \
    && rm -rf /var/lib/apt/lists/*

# Step 3: Set the working directory in the container
WORKDIR /app

# Step 4: Copy the current directory contents into the container at /app
COPY . /app

# Step 5: Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Step 6: Expose port 5000 (default Flask port)
EXPOSE 5000

# Step 7: Set environment variable to specify the Flask app entry point
ENV FLASK_APP=app.py

# Step 8: Define the command to run your Flask app in production mode (with Flask's built-in server for development only)
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]
