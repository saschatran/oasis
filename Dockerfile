# Use an official Python runtime as a parent image
FROM python:3.8

# Set the working directory in the container
WORKDIR /usr/src/

# Install system dependencies required for building TLSH, radare2, and ssdeep
RUN apt-get update && apt-get install -y \
    git \
    build-essential \
    cmake \
    automake \
    libtool \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
# Copy just the requirements.txt first to leverage Docker cache
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Install Jupyter
RUN pip install jupyter

# Copy the rest of your application's code
COPY . .

# Copy the start-up script and give execution permissions
# COPY start.sh .
# RUN chmod +x ./start.sh

# Expose the port Jupyter will run on
EXPOSE 8888

# Set the default command to run the start-up script
#CMD ["./start.sh"]
