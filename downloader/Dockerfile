# Use ubuntu:latest as base image
FROM ubuntu:latest

# Set work directory
WORKDIR /lewdlocale

# Copy current directory contents into the container at /lewdlocale
COPY . .

# Install pip for Python 3
RUN apt-get install -y python3.11

# Install poetry
RUN pip install poetry==1.3.2

# Install dependencies using poetry
RUN poetry install

# Install ffmpeg
RUN apt-get install -y ffmpeg

# Set the entrypoint
ENTRYPOINT ["poetry", "run", "python", "launch.py", "--app", "downloader", "--flush", "False", "--log-level", "INFO"]
