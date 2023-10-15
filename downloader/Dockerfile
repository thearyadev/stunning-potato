# Use ubuntu:latest as base image
FROM ubuntu:latest

# Set work directory
WORKDIR /lewdlocale

# Copy current directory contents into the container at /lewdlocale
COPY . .

# Install necessary packages
RUN apt-get update && apt upgrade && apt-get install -y \
    software-properties-common \
    wget \
    build-essential \
    libssl-dev \
    zlib1g-dev \
    libncurses5-dev \
    libncursesw5-dev \
    libreadline-dev \
    libsqlite3-dev \
    libgdbm-dev \
    libdb5.3-dev \
    libbz2-dev \
    libexpat1-dev \
    liblzma-dev \
    tk-dev \
    libffi-dev

# Download and install Python 3.11.3
RUN wget https://www.python.org/ftp/python/3.11.3/Python-3.11.3.tgz && \
    tar -xvf Python-3.11.3.tgz && \
    cd Python-3.11.3 && \
    ./configure --enable-optimizations && \
    make altinstall

# Install pip for Python 3
RUN apt-get install -y python3-pip

# Install poetry
RUN pip install poetry==1.3.2

# Install dependencies using poetry
RUN poetry install

# Install ffmpeg
RUN apt-get install -y ffmpeg

# Clean up APT when done
RUN apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# Set the entrypoint
ENTRYPOINT ["poetry", "run", "python", "launch.py", "--app", "downloader", "--flush", "False", "--log-level", "INFO"]
