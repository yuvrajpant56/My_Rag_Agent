# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Add the current directory to Python's path
ENV PYTHONPATH=/app

# Copy the requirements file into the container at /app
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the 'src' directory from your host to /app in the container
COPY ./src .

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Run main.py when the container launches
# This command assumes you are running a web server like FastAPI with Uvicorn.
# If you run your app differently, you may need to adjust this line.
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]