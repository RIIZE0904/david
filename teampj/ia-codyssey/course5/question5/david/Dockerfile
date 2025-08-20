FROM ubuntu:20.04
# Set the working directory
WORKDIR /app

# Copy the requirements file into the container
COPY . .

# Install the required packages
RUN apt-get update && apt-get install -y python3-pip && rm -rf /var/lib/apt/lists/*
RUN pip3 install --no-cache-dir -r requirements.txt

# Expose the port the app runs on
EXPOSE 80

# Command to run the application
CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:80"]
