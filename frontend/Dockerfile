# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy requirements.txt if you have one
COPY requirements.txt requirements.txt

# Install dependencies
RUN pip3 install -r requirements.txt --verbose

# Copy the rest of the application code
COPY . .

# Command to run your app (update as needed)
CMD ["streamlit", "run", "app.py"]