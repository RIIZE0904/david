FROM python:3.10-slim

# Set the working directory
WORKDIR /app

# Copy the requirements file into the container
COPY . .

# Install the required packages
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port the app runs on
EXPOSE 80

# Command to run the application
CMD ["gunicorn", "main:app", "--bind", "0.0.0.0:80"]
