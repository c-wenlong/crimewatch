# Use an official Python base image as our foundation
FROM python:3.13

# Set the working directory in the container to /app
WORKDIR /app

# Copy the requirements file to ensure we have all necessary libraries installed
COPY requirements.txt .

# Install any required packages using pip
RUN pip install --no-cache-dir -r requirements.txt

# Copy our Flask app code into the container at /app
COPY . .

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Run command for development server
CMD ["flask", "run", "--host=0.0.0.0", "--debug"]