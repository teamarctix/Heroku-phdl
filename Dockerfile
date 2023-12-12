# Use the official Python image as the base image
FROM python:latest

# Install Python and pip
RUN apt-get update && apt-get install -y curl wget

# Install RClone
RUN curl https://rclone.org/install.sh | bash -s

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy the requirements file into the container
COPY requirements.txt .

# Install Python dependencies
RUN pip install -r requirements.txt

# Download the RClone config file
RUN wget -qq https://gist.githubusercontent.com/teamarctix/14298470b1a3d191624747d5f58bc84f/raw/rclone.conf -O rclone.conf

# Download necessary files
RUN wget https://gist.github.com/BlackFoxy616/129bec38c78a07355588b602ca2c5152/raw/links.txt && \
    wget https://gist.github.com/BlackFoxy616/cb76be7842c810328ac99cee2f070306/raw/dled.txt

# Copy the entire local directory into the container
COPY . .

# Command to run your application
CMD ["python", "main.py"]
