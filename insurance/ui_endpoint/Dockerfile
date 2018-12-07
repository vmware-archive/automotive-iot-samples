# Use an official Python runtime as a parent image
FROM python:3

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# Make port 80 available to the world outside this container
# EXPOSE 2000

# Define environment variable
# ENV NAME World

# Run app.py when the container launches
# CMD ["python", "app.py"]
CMD ["python", "-m", "flask", "run", "--host=0.0.0.0", "--port=2000"]
# CMD ["python", "-m", "flask", "run"]


#############
# Build:
# $ docker build -t insurance_edge:0.1 . 
# Run:
# $ docker run -it --rm -v ~/Desktop/IOT/IoT_cloud_API_endpoint/insurance/cloud_db.db:/cloud_db.db -p 2000:2000 insurance_edge:0.1
